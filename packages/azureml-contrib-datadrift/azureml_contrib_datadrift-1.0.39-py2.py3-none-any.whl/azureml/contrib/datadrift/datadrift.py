# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Defines the data drift logic between two datasets, relies on the DataSets API."""

import glob
import json
import os
import shutil
import tempfile
import uuid
import warnings
from collections import OrderedDict
from datetime import datetime, timezone

import jsonpickle
import matplotlib.pyplot as plt
import pkg_resources
import requests
from azureml._base_sdk_common import __version__
from azureml._base_sdk_common import __version__ as VERSION
from azureml._model_management._constants import WORKSPACE_RP_API_VERSION
from azureml.contrib.datadrift import (
    _generate_script, _generate_script_datacuration_python, _generate_script_datacuration_pyspark, alert_configuration
)
from azureml.contrib.datadrift._logging._telemetry_logger import _TelemetryLogger
from azureml.contrib.datadrift._logging._telemetry_logger_context_adapter import _TelemetryLoggerContextAdapter
from azureml.contrib.datadrift._restclient import DataDriftClient
from azureml.contrib.datadrift._restclient.models import AlertConfiguration
from azureml.contrib.datadrift._restclient.models import DataDriftDto, DataDriftRunDto
from azureml.contrib.datadrift._utils.constants import MODEL_NAME, MODEL_VERSION, \
    DRIFT_THRESHOLD, DATETIME, SERVICE_NAME, \
    METRIC_COLUMN_METRICS, METRIC_DATASET_METRICS, METRIC_TYPE, HAS_DRIFT, RUN_ID, SCORING_DATE, \
    METRIC_DATASHIFT_MCC_TEST, PIPELINE_PARAMETER_ADHOC_RUN, RUN_TYPE_ADHOC, RUN_TYPE_SCHEDULE, \
    METRIC_STATISTICAL_DISTANCE_ENERGY, METRIC_STATISTICAL_DISTANCE_WASSERSTEIN, METRIC_DATASHIFT_FEATURE_IMPORTANCE, \
    FIGURE_FEATURE_IMPORTANCE_TITLE, FIGURE_FEATURE_IMPORTANCE_Y_LABEL
from azureml.contrib.datadrift._utils.constants import SERVICE, COLUMN_NAME
from azureml.core import Datastore
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
from azureml.core.runconfig import RunConfiguration
from azureml.data.data_reference import DataReference
from azureml.exceptions import WebserviceException, ComputeTargetException
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule
from azureml.pipeline.steps import PythonScriptStep
from msrest.exceptions import HttpOperationError

from ._utils.parameter_validator import ParameterValidator

module_logger = _TelemetryLogger.get_telemetry_logger(__name__)

DEFAULT_COMPUTE_TARGET_NAME = "datadrift-server"
DEFAULT_VM_SIZE = "STANDARD_D2_V2"
DEFAULT_VM_MAX_NODES = 4
DEFAULT_DRIFT_THRESHOLD = 0.2


class DataDrift:
    """Class for AzureML DataDrift.

    DataDrift class provides set of convenient APIs to identify any drifting between given training
    and/or scoring datasets for a model. A DataDrift object is created with a workspace, a model name
    and a version, list of services, and optional tuning parameters. A DataDrift task can be scheduled
    using enable_schedule() API and/or a one time task can be submitted using run(target_date) API.
    """

    def __init__(self, workspace, model_name, model_version):
        """Datadrift constructor.

        The Datadrift constructor is used to retrieve a cloud representation of a Datadrift object associated with the
        provided workspace. Must provide model_name and model_version.

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDrift on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :return: A datadrift object
        :rtype: DataDrift
        """
        if workspace is ... or model_name is ... or model_version is ...:
            # Instantiate an empty DataDrift object. Will be initialized by DataDrift.get()
            return

        log_context = {'workspace_name': workspace.name, 'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id}

        self._logger = _TelemetryLoggerContextAdapter(module_logger, log_context)

        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)

        with _TelemetryLogger.log_activity(self._logger, activity_name="constructor") as logger:

            try:
                dd_list = DataDrift._get_datadrift_list(workspace, model_name, model_version, logger=logger)
                if len(dd_list) > 1:
                    error_msg = "Multiple DataDrift objects for: {} {} {}".format(workspace, model_name, model_version)
                    logger.error(error_msg)
                    raise LookupError(error_msg)
                elif len(dd_list) == 1:
                    dto = dd_list[0]
                    self._initialize(workspace, dto.model_name, dto.model_version, dto.services,
                                     compute_target_name=dto.compute_target_name, frequency=dto.frequency,
                                     interval=dto.interval, feature_list=dto.features,
                                     drift_threshold=dto.drift_threshold, alert_config=dto.alert_configuration,
                                     schedule_start=dto.schedule_start_time if dto.schedule_start_time else None,
                                     enabled=dto.enabled, schedule_id=dto.schedule_id, dd_id=dto.id)
                else:
                    error_msg = "Could not find DataDrift object for: {} {} {}".format(workspace, model_name,
                                                                                       model_version)
                    logger.error(error_msg)
                    raise KeyError(error_msg)
            except HttpOperationError or KeyError:
                # DataDrift object doesn't exist for model_name and model_version, create one instead
                logger.error("DataDrift object for model_name: {}, model_version: {} doesn't exist. Create with "
                             "Datadrift.create()".format(model_name, model_version))
                raise

    def _initialize(self, workspace, model_name, model_version, services, compute_target_name=None, frequency=None,
                    interval=None, feature_list=None, schedule_start=None, alert_config=None, schedule_id=None,
                    enabled=False, dd_id=None, drift_threshold=None):
        r"""Class DataDrift Constructor helper.

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDrift on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :param services: Optional, list of webservices to test for data drifting
        :type services: :class:list(str)
        :param compute_target_name: Optional, AzureML ComputeTarget name, may create one if needed and required
        :type compute_target_name: str
        :param frequency: Optional, how often the pipeline is run. i.e. "Day", "Week", "Month", default is "Day"
        :type frequency: str
        :param interval: Optional, how often the pipeline runs based on frequency. i.e. If frequency = "Day" and \
                         interval = 2, the pipeline will run every other day
        :type interval: int
        :param feature_list: Optional, whitelisted features to run the datadrift detection on
        :type feature_list: :class:list(str)
        :param schedule_start: Optional, start time of data drift schedule in UTC
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, alert configuration parameters
        :type alert_config: azureml.contrib.datadrift._restclient.models.AlertConfiguration
        :param schedule_id: Optional, pipeline schedule ID
        :type schedule_id: int
        :param enabled: Optional, whether the schedule is enabled or not
        :type enabled: bool
        :param dd_id: Optional, internal ID, only retrieved from service
        :type dd_id: int
        :param drift_threshold: Optional, threshold to enable DataDrift alerts on
        :type drift_threshold: float
        :return: A datadrift object
        :rtype: DataDrift
        """
        self._workspace = workspace
        self._model_name = model_name
        self._model_version = model_version
        self._services = services
        self._compute_target_name = compute_target_name
        self._frequency = frequency
        self._interval = interval
        self._feature_list = feature_list
        # TODO: Below values are defaulted in private preview. Enable for public preview.
        self._drift_threshold = drift_threshold
        self._baseline_dataset = None
        self._baseline_dataset_start_time = None
        self._baseline_dataset_end_time = None

        self._schedule_start = schedule_start
        self._schedule_id = schedule_id
        self._enabled = enabled
        self._id = dd_id

        # Set alert configuration
        self._alert_config = alert_configuration.AlertConfiguration(
            alert_config.email_addresses) if alert_config else None

        # Instantiate service client
        self._client = DataDriftClient(self.workspace.service_context)

        if not hasattr(self, '_logger'):
            log_context = {'workspace_name': workspace.name, 'model_name': model_name, 'model_version': model_version,
                           'subscription_id': workspace.subscription_id}

            self._logger = _TelemetryLoggerContextAdapter(module_logger, log_context)

    def __repr__(self):
        """Return the string representation of a DataDrift object.

        :return: DataDrift object string
        :rtype: str
        """
        return str(self.__dict__)

    @property
    def workspace(self):
        """Get the workspace of the DataDrift object.

        :return: Workspace object
        :rtype: azureml.core.workspace.Workspace
        """
        return self._workspace

    @property
    def model_name(self):
        """Get the model name associated with the DataDrift object.

        :return: Model name
        :rtype: str
        """
        return self._model_name

    @property
    def model_version(self):
        """Get the model version associated with the DataDrift object.

        :return: Model version
        :rtype: int
        """
        return self._model_version

    @property
    def services(self):
        """Get the list of services attached to the DataDrift object.

        :return: List of service names
        :rtype: :class:list(str)
        """
        return self._services

    @property
    def compute_target_name(self):
        """Get the Compute Target name attached to the DataDrift object.

        :return: Compute Target name
        :rtype: str
        """
        return self._compute_target_name

    @property
    def frequency(self):
        """Get the frequency of the DataDrift schedule.

        :return: String of either "Day", "Week" or "Month"
        :rtype: str
        """
        return self._frequency

    @property
    def interval(self):
        """Get the interval of the DataDrift schedule.

        :return: Integer value of time unit
        :rtype: int
        """
        return self._interval

    @property
    def feature_list(self):
        """Get the list of whitelisted features for the DataDrift object.

        :return: List of feature names
        :rtype: :class:list(str)
        """
        return self._feature_list

    @property
    def drift_threshold(self):
        """Get the drift threshold for the DataDrift object.

        :return: Drift threshold
        :rtype: float
        """
        return self._drift_threshold

    @property
    def baseline_dataset(self):
        """Get the baseline dataset.

        :return: Dataset type of the baseline dataset
        :rtype: azureml.core.dataset.Dataset
        """
        return self._baseline_dataset

    @property
    def baseline_dataset_start_time(self):
        """Get the start time of the baseline dataset.

        :return: start_time of baseline dataset
        :rtype: datetime.datetime
        """
        return self._baseline_dataset_start_time

    @property
    def baseline_dataset_end_time(self):
        """Get the end time of the baseline dataset.

        :return: Tuple of datetime objects (start_time, end_time)
        :rtype: datetime.datetime
        """
        return self._baseline_dataset_end_time

    @property
    def schedule_start(self):
        """Get the start time of the schedule.

        :return: Datetime object of schedule start time in UTC
        :rtype: datetime.datetime
        """
        return self._schedule_start

    @property
    def alert_config(self):
        """Get the alert configuration for the DataDrift object.

        :return: AlertConfiguration object.
        :rtype: azureml.contrib.datadrift.AlertConfiguration
        """
        return self._alert_config

    @property
    def enabled(self):
        """Get the boolean value for whether the DataDrift is enabled or not.

        :return: Boolean value; true for enabled
        :rtype: bool
        """
        return self._enabled

    @staticmethod
    def create(workspace, model_name, model_version, services, compute_target_name=None,
               frequency=None, interval=None, feature_list=None, schedule_start=None, alert_config=None,
               drift_threshold=None):
        r"""Create a new DataDrift object in the Azure Machine Learning Workspace.

        Throws an exception if a DataDrift for the same model_name and model_version already exists in the workspace.

        :param workspace: Object that points to workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDrift on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :param services: Optional, list of webservices to test for data drifting
        :type services: :class:list(str)
        :param compute_target_name: Optional, AzureML ComputeTarget name
        :type compute_target_name: str
        :param frequency: Optional, how often the pipeline is run. i.e. "Day", "Week", "Month", default is "Day"
        :type frequency: str
        :param interval: Optional, how often the pipeline runs based on frequency. i.e. If frequency = "Day" and \
                         interval = 2, the pipeline will run every other day
        :type interval: int
        :param feature_list: Optional, whitelisted features to run the datadrift detection on
        :type feature_list: :class:list(str)
        :param schedule_start: Optional, start time of data drift schedule in UTC
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, configuration object for DataDrift alerts
        :type alert_config: azureml.contrib.datadrift.AlertConfiguration
        :param drift_threshold: Optional, threshold to enable DataDrift alerts on
        :type drift_threshold: float
        :return: A datadrift object
        :rtype: azureml.datadrift.DataDrift
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)
        services = ParameterValidator.validate_services(services)
        compute_target_name = ParameterValidator.validate_compute_target_name(compute_target_name, workspace)
        frequency = ParameterValidator.validate_frequency(frequency)
        interval = ParameterValidator.validate_interval(interval)
        feature_list = ParameterValidator.validate_features(feature_list)
        schedule_start = ParameterValidator.validate_datetime(schedule_start)
        alert_config = ParameterValidator.validate_alert_configuration(alert_config)
        drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)

        logger = _TelemetryLogger.get_telemetry_logger('datadrift.create')
        log_context = {'workspace_name': workspace.name, 'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id}

        logger = _TelemetryLoggerContextAdapter(logger, log_context)
        with _TelemetryLogger.log_activity(logger, activity_name="datadrift.create") as logger:

            dd_client = DataDriftClient(workspace.service_context)

            try:
                if list(dd_client.list(model_name, model_version, logger=logger)):
                    error_msg = "DataDrift already exists for model_name: {}, model_version: {}. Please use " \
                                "DataDrift.get() to retrieve the DataDrift object".format(model_name, model_version)
                    logger.error(error_msg)
                    raise KeyError(error_msg)
            except HttpOperationError:
                # DataDrift object doesn't exist for model_name and model_version, create one instead
                logger.error("Error checking DataDrift object for model_name: {}, model_version: {}"
                             .format(model_name, model_version))
                raise

            if not compute_target_name:
                compute_target_name = DEFAULT_COMPUTE_TARGET_NAME

            if not drift_threshold:
                drift_threshold = DEFAULT_DRIFT_THRESHOLD

            # Write object to service
            dto = DataDriftDto(frequency=frequency,
                               schedule_start_time=schedule_start.replace(tzinfo=timezone.utc).isoformat()
                               if schedule_start else None,
                               schedule_id=None,
                               interval=interval,
                               alert_configuration=AlertConfiguration(alert_config.email_addresses)
                               if alert_config else None,
                               id=None,
                               model_name=model_name,
                               model_version=model_version,
                               services=services,
                               compute_target_name=compute_target_name,
                               drift_threshold=drift_threshold,
                               base_line_dataset=None,
                               base_line_dataset_start_time=None,
                               base_line_dataset_end_time=None,
                               features=feature_list,
                               enabled=False)
            client_dto = dd_client.create(dto, logger)

            dd = DataDrift(..., ..., ...)
            dd._initialize(workspace, client_dto.model_name, client_dto.model_version, client_dto.services,
                           compute_target_name=compute_target_name, frequency=client_dto.frequency,
                           interval=client_dto.interval, feature_list=client_dto.features,
                           schedule_start=client_dto.schedule_start_time if client_dto.schedule_start_time else None,
                           alert_config=client_dto.alert_configuration, schedule_id=client_dto.schedule_id,
                           enabled=client_dto.enabled, dd_id=client_dto.id,
                           drift_threshold=client_dto.drift_threshold)
            return dd

    @staticmethod
    def get(workspace, model_name, model_version):
        """Retrieve a unique DataDrift object for a given workspace, model_name, model_version and list of services.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Name of model to run DataDrift on
        :type model_name: str
        :param model_version: Version of model
        :type model_version: int
        :return: DataDrift object
        :rtype: azureml.datadrift.DataDrift
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        model_name = ParameterValidator.validate_model_name(model_name)
        model_version = ParameterValidator.validate_model_version(model_version)

        logger = _TelemetryLogger.get_telemetry_logger('datadrift.get')
        log_context = {'workspace_name': workspace.name, 'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id}
        logger = _TelemetryLoggerContextAdapter(logger, log_context)

        with _TelemetryLogger.log_activity(logger, activity_name="get") as logger:
            logger.info("Getting DataDrift object for: {} {} {}".format(workspace, model_name, model_version))
            return DataDrift(workspace, model_name, model_version)

    @staticmethod
    def list(workspace, model_name=None, model_version=None, services=None):
        """Get a list of DataDrift objects given a workspace. Model and services are optional input parameters.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Optional, name of model to run DataDrift on
        :type model_name: str
        :param model_version: Optional, version of model
        :type model_version: int
        :param services: Optional, names of webservices
        :type services: :class:list(str)
        :return: List of DataDrift objects
        :rtype: :class:list(azureml.datadrift.DataDrift)
        """
        workspace = ParameterValidator.validate_workspace(workspace)
        if model_name is not None:
            model_name = ParameterValidator.validate_model_name(model_name)
        if model_version is not None:
            model_version = ParameterValidator.validate_model_version(model_version)
        if services is not None:
            services = ParameterValidator.validate_services(services)

        logger = _TelemetryLogger.get_telemetry_logger('datadrift.list')
        log_context = {'workspace_name': workspace.name, 'model_name': model_name, 'model_version': model_version,
                       'subscription_id': workspace.subscription_id}
        logger = _TelemetryLoggerContextAdapter(logger, log_context)

        with _TelemetryLogger.log_activity(logger, activity_name="list") as logger:
            dto_list = DataDrift._get_datadrift_list(workspace, model_name, model_version, services, logger)
            dd_list = []
            for dto in dto_list:
                dd = DataDrift(..., ..., ...)
                dd._initialize(workspace, dto.model_name, dto.model_version, dto.services,
                               compute_target_name=dto.compute_target_name, frequency=dto.frequency,
                               interval=dto.interval,
                               feature_list=dto.features, drift_threshold=dto.drift_threshold,
                               alert_config=dto.alert_configuration,
                               schedule_start=dto.schedule_start_time if dto.schedule_start_time else None,
                               enabled=dto.enabled, schedule_id=dto.schedule_id, dd_id=dto.id)
                # TODO: Add baseline and drift threshold info after private preview
                dd_list.append(dd)
            return dd_list

    @staticmethod
    def _get_datadrift_list(workspace, model_name, model_version, services=None, logger=None, client=None):
        """Get list of DataDrift objects from service.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param model_name: Optional, name of model to run DataDrift on
        :type model_name: str
        :param model_version: Optional, version of model
        :type model_version: int
        :param services: Optional, names of webservices
        :type services: :class:list(str)
        :param logger: Activity logger for service call
        :type logger: datetime.datetime
        :param client: DataDrift service client
        :type client: azureml.contrib.datadrift._restclient.DataDriftClient
        :return: List of DataDrift objects
        :rtype: list(azureml.contrib.datadrift._restclient.models.DataDriftDto)
        """
        dd_client = client if client else DataDriftClient(workspace.service_context)

        return list(dd_client.list(model_name=model_name, model_version=model_version, services=services,
                                   logger=logger))

    @staticmethod
    def _get_or_create_aml_compute(workspace, name, should_create=False):
        """Retrieve or create an aml compute using name.

        Try to retrieve then create a new one if it doesn't exist and the flag should_create is True.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :param name: the name of aml compute target
        :type name: str
        :return: Azure ML Compute target
        :rtype: azureml.core.compute.compute.ComputeTarget
        """
        log_context = {'workspace_name': workspace.name, 'subscription_id': workspace.subscription_id}
        # TODO: De-provision compute if it's not run
        aml_compute = None
        try:
            aml_compute = AmlCompute(workspace, name)
            module_logger.info("found existing compute target.", extra={'properties': log_context})
        except ComputeTargetException as e:
            if should_create:
                module_logger.info("creating new compute target", extra={'properties': log_context})

                provisioning_config = AmlCompute.provisioning_configuration(
                    vm_size=DEFAULT_VM_SIZE,
                    max_nodes=DEFAULT_VM_MAX_NODES
                )

                aml_compute = ComputeTarget.create(workspace, name, provisioning_config)

                aml_compute.wait_for_completion(show_output=True)
            else:
                error_message = "compute target {} is not available." \
                                "Use create_compute_target=True to allow creation of a new compute target." \
                    .format(name)
                module_logger.error(error_message, extra={'properties': log_context})
                raise ComputeTargetException(error_message) from e
        return aml_compute

    @staticmethod
    def _generate_script():
        """Generate the data drift script.

        :return: Tuple of output directory, script name
        :rtype: tuple(str, str)
        """
        script_string = pkg_resources.resource_string(__package__,
                                                      os.path.basename(_generate_script.__file__)).decode('utf-8')
        curr_time = datetime.utcnow()
        date_components = curr_time.strftime('%Y/%m/%d').split("/")
        # Create a unique hash for the script name
        output_dir = os.path.join("scripts", *date_components)
        script_name = "drift-{}.py".format(curr_time.strftime('%H-%M-%S-%f'))

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, script_name), 'w+', newline="") as f:
            f.write(script_string)

        return output_dir, script_name

    @staticmethod
    def _generate_script_datacuration_python():
        """Generate the data curation python script.

        :return: Tuple of output directory, script name
        :rtype: tuple(str, str)
        """
        script_string = pkg_resources.resource_string(__package__,
                                                      os.path.basename(_generate_script_datacuration_python
                                                                       .__file__)).decode('utf-8')
        curr_time = datetime.utcnow()
        date_components = curr_time.strftime('%Y/%m/%d').split("/")
        # Create a unique hash for the script name
        output_dir = os.path.join("scripts", *date_components)
        script_name = "curation-{}.py".format(curr_time.strftime('%H-%M-%S-%f'))

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, script_name), 'w+', newline="") as f:
            f.write(script_string)

        return output_dir, script_name

    @staticmethod
    def _generate_script_datacuration_pyspark():
        """Generate the data curation pyspark script.

        :return: Tuple of output directory, script name
        :rtype: tuple(str, str)
        """
        script_string = pkg_resources.resource_string(__package__,
                                                      os.path.basename(_generate_script_datacuration_pyspark
                                                                       .__file__)).decode('utf-8')
        curr_time = datetime.utcnow()
        date_components = curr_time.strftime('%Y/%m/%d').split("/")
        # Create a unique hash for the script name
        output_dir = os.path.join("scripts", *date_components)
        script_name = "curation-pyspark-{}.py".format(curr_time.strftime('%H-%M-%S-%f'))

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(os.path.join(output_dir, script_name), 'w+', newline="") as f:
            f.write(script_string)

        return output_dir, script_name

    def run(self, target_date, create_compute_target=False):
        """Run an ad-hoc data drift detection run on a model for a specified time window.

        :param target_date:  Target date of scoring data in UTC
        :type target_date: datetime.datetime
        :param create_compute_target: Whether the DataDrift API should automatically create an AML compute target
        :type create_compute_target: bool
        :return: Pipeline run
        :rtype: azureml.pipeline.core.run.PipelineRun
        """
        target_date = ParameterValidator.validate_datetime(target_date)

        cid = str(uuid.uuid4())

        with _TelemetryLogger.log_activity(self._logger, activity_name="run",
                                           custom_dimensions={'correlation_id': cid}) as logger:
            # get the aml compute target or create if it is not available and create_compute_target is True
            self._get_or_create_aml_compute(self._workspace, self._compute_target_name, create_compute_target)

            output_dir_drift, script_name_drift = self._generate_script()
            output_dir_curation, script_name_curation = self._generate_script_datacuration_python()
            pipeline = self._create_validate_pipeline(output_dir_drift, script_name_drift,
                                                      output_dir_curation, script_name_curation,
                                                      cid,
                                                      target_date)
            run_name = "drift-run-{}".format(datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S"))
            pipeline_run = pipeline.submit(run_name,
                                           pipeline_parameters={PIPELINE_PARAMETER_ADHOC_RUN: RUN_TYPE_ADHOC},
                                           continue_on_step_failure=True)
            logger.info("Submitted pipeline for execution, run name: {}".format(run_name))

            dto = DataDriftRunDto(data_drift_id=self._id,
                                  execution_run_id=pipeline_run.id,
                                  id=None,
                                  model_name=self.model_name,
                                  model_version=self.model_version,
                                  services=self.services,
                                  compute_target_name=self.compute_target_name,
                                  start_time=target_date.replace(tzinfo=timezone.utc).isoformat(),
                                  base_line_dataset=self.baseline_dataset,
                                  base_line_dataset_start_time=self.baseline_dataset_start_time,
                                  base_line_dataset_end_time=self.baseline_dataset_end_time,
                                  features=self.feature_list,
                                  drift_threshold=self.drift_threshold)
            self._client.run(self._id, dto, logger)

            return pipeline_run

    def enable_schedule(self, create_compute_target=False):
        """Create a schedule to run  a datadrift job for a specified model and webservice."""
        with _TelemetryLogger.log_activity(self._logger, activity_name="enable_schedule") as logger:
            if not self.enabled:
                # TODO: Add check for baseline dataset property being set

                # get the aml compute target or create if it is not available and create_compute_target is True
                self._get_or_create_aml_compute(self._workspace, self._compute_target_name, create_compute_target)

                output_dir_drift, script_name_drift = self._generate_script()
                output_dir_curation, script_name_curation = self._generate_script_datacuration_python()

                try:
                    pipeline_name = "drift-{}-pipeline".format(datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S"))
                    pipeline = self._create_validate_pipeline(output_dir_drift, script_name_drift,
                                                              output_dir_curation, script_name_curation,
                                                              pipeline_name)
                except HttpOperationError or SystemError:
                    logger.exception("Could not create pipeline: {}".format(pipeline_name))
                    raise

                try:
                    published_pipeline = pipeline.publish(name=pipeline_name,
                                                          description=pipeline_name,
                                                          continue_on_step_failure=True)
                except HttpOperationError or SystemError:
                    logger.exception("Unable to publish pipeline: {}".format(pipeline_name))
                    raise
                try:
                    schedule = self._create_schedule(published_pipeline)
                    logger.info('Created schedule with id: {}, pipeline_name: {}'.format(schedule.id, pipeline_name))
                    warnings.warn("Pipeline {} is created and scheduled successfully."
                                  "Please don't delete this pipeline."
                                  "Otherwise, data drift service will not work.".format(pipeline_name))
                    self._schedule_id = schedule.id
                    self._schedule_start = datetime.utcnow()
                    self._enabled = True
                    self._update_remote(logger)
                except HttpOperationError or SystemError:
                    logger.exception("Unable to enable schedule with ID: {} in workspace: {}"
                                     .format(self._schedule_id, self.workspace))
                    raise

    def disable_schedule(self):
        """Disable a schedule for a specified model and web service."""
        with _TelemetryLogger.log_activity(self._logger, activity_name="disable_schedule") as logger:
            if self._schedule_id is None:
                logger.info("There is no schedule for this DataDrfit object.")
                return

            try:
                schedule = Schedule.get(self.workspace, self._schedule_id)
            except HttpOperationError or SystemError:
                logger.exception("Unable to retrieve schedule with ID: {} in workspace: {}"
                                 .format(self._schedule_id, self.workspace))
                raise
            try:
                schedule.disable(wait_for_provisioning=True)
                self._schedule_id = None
                self._schedule_start = None
                self._enabled = False
                self._update_remote(logger)
            except HttpOperationError or SystemError:
                logger.exception("Unable to disable schedule with ID: {} in workspace: {}"
                                 .format(self._schedule_id, self.workspace))
                raise

    def get_output(self, start_time, end_time, run_id=None):
        """Get a tuple of the drift results and metrics for a specific DataDrift object over a given time window.

        :param start_time: Start time of results window in UTC
        :type start_time: datetime.datetime
        :param end_time: End time of results window in UTC
        :type end_time: datetime.datetime
        :param run_id: Optional, adhoc run id
        :type run_id: int
        :return: Tuple of a list of drift results, and a list of individual dataset and columnar metrics
        :rtype: tuple(:class:list(), :class:list())
        """
        # example of outputs:
        # results : [{'service_name': 'service1', 'result':
        #                                         [{'has_drift': True, 'datetime': '2019-04-03', 'model_name':
        #                                           'modelName', 'model_version': 2, 'drift_threshold': 0.3}]}]
        #
        # metrics : [{'service_name': 'service1',
        #             'metrics': [{'datetime': '2019-04-03', 'model_name': 'modelName', 'model_version': 2,
        #                          'dataset_metrics': [{'name': 'ds_mcc_train', 'value': 0.345345345345559},
        #                                              {'name': 'ds_mcc_test', 'value': 0.4567346534613245},
        #                                              {'name': 'ds_mcc_all', 'value': 0.9801960588196069}],
        #                          'column_metrics': [{'feature1': [{'name': 'ds_feature_importance', 'value': 288.0},
        #                                                           {'name': 'wasserstein_distance',
        #                                                            'value': 4.858040000000001},
        #                                                           {'name': 'energy_distance',
        #                                                           'value': 2.7204799576545313}]}]}]}]
        #

        start_time = ParameterValidator.validate_datetime(start_time)
        end_time = ParameterValidator.validate_datetime(end_time)
        if run_id is not None:
            run_id = ParameterValidator.validate_run_id(run_id)

        results = []
        metrics = []

        get_metrics = self._get_metrics()

        # Check if metrics exist
        if not get_metrics or len(get_metrics) == 0:
            error_msg = "Metrics do not exist for model: {} with version: {}".format(self.model_name,
                                                                                     self.model_version)
            self._logger.error(error_msg)
            raise NameError(error_msg)

        # Filter based on input params
        if run_id:
            get_metrics = [m for m in get_metrics if m.extended_properties[RUN_ID] == run_id]
        get_metrics = [m for m in get_metrics if
                       start_time < m.extended_properties[SCORING_DATE] < end_time]

        for metric in get_metrics:
            if metric.name == METRIC_DATASHIFT_MCC_TEST:
                # Overall drift coefficient; add to results return object
                service_exists = False
                for r in results:
                    if r[SERVICE_NAME] == metric.extended_properties['service']:
                        # Service already in dict; add metric to result list
                        service_exists = True
                        res = r['result']
                        res.append({HAS_DRIFT: metric.value > metric.extended_properties[DRIFT_THRESHOLD],
                                    DATETIME: metric.extended_properties[SCORING_DATE],
                                    MODEL_NAME: metric.extended_properties[MODEL_NAME],
                                    MODEL_VERSION: metric.extended_properties[MODEL_VERSION],
                                    DRIFT_THRESHOLD: metric.extended_properties[DRIFT_THRESHOLD]})
                if not service_exists:
                    # Add new service to results list
                    result = [{
                        HAS_DRIFT: metric.value > metric.extended_properties[DRIFT_THRESHOLD],
                        DATETIME: metric.extended_properties[SCORING_DATE],
                        MODEL_NAME: metric.extended_properties[MODEL_NAME],
                        MODEL_VERSION: metric.extended_properties[MODEL_VERSION],
                        DRIFT_THRESHOLD: metric.extended_properties[DRIFT_THRESHOLD]
                    }]
                    res = {SERVICE_NAME: metric.extended_properties['service'], "result": result}
                    results.append(res)
            # Add to metrics return object
            metric_service_exists = False
            for m in metrics:
                if m[SERVICE_NAME] == metric.extended_properties['service']:
                    metric_service_exists = True
                    met_metric_exists = False
                    for met in m['metrics']:
                        datetime_check = met[DATETIME] == metric.extended_properties[SCORING_DATE]
                        model_name_check = met[MODEL_NAME] == metric.extended_properties[MODEL_NAME]
                        model_version_check = met[MODEL_VERSION] == metric.extended_properties[MODEL_VERSION]
                        if datetime_check and model_name_check and model_version_check:
                            _metric = {'name': metric.name, 'value': metric.value}
                            met_metric_exists = True
                            # Add to already existing metric dictionary
                            if metric.extended_properties[METRIC_TYPE] == 'dataset':
                                if METRIC_DATASET_METRICS not in met:
                                    met[METRIC_DATASET_METRICS] = []
                                met[METRIC_DATASET_METRICS].append(_metric)

                            elif metric.extended_properties[METRIC_TYPE] == 'column':
                                column_in_metrics = False
                                if METRIC_COLUMN_METRICS not in met:
                                    met[METRIC_COLUMN_METRICS] = []
                                for c_metric in met[METRIC_COLUMN_METRICS]:
                                    if metric.extended_properties['column_name'] in c_metric:
                                        column_in_metrics = True
                                        column = c_metric[metric.extended_properties['column_name']]
                                        column.append(_metric)
                                if not column_in_metrics:
                                    # Create column dict in column_metrics
                                    column_dict = {metric.extended_properties['column_name']: [_metric]}
                                    met[METRIC_COLUMN_METRICS].append(column_dict)
                    if not met_metric_exists:
                        # Add new metric in metrics list
                        _metric = {'name': metric.name, 'value': metric.value}

                        metric_dict = DataDrift._create_metric_dict(metric)
                        m['metrics'].append(metric_dict)

            if not metric_service_exists:
                # Add metrics service dict
                _metric = {'name': metric.name, 'value': metric.value}

                metrics_list = []
                metric_dict = DataDrift._create_metric_dict(metric)
                metrics_list.append(metric_dict)
                service_metric = {SERVICE_NAME: metric.extended_properties['service'], 'metrics': metrics_list}
                metrics.append(service_metric)

        return results, metrics

    @staticmethod
    def _create_metric_dict(metric):
        """Create metrics dictionary.

        :param metric: Metric object
        :type metric: azureml.contrib.datadrift._datadiff.Metric
        :return: Dictionary of metrics delineated by service
        :rtype: dict()
        """
        _metric = {'name': metric.name, 'value': metric.value}
        metric_dict = {DATETIME: metric.extended_properties[SCORING_DATE],
                       MODEL_NAME: metric.extended_properties[MODEL_NAME],
                       MODEL_VERSION: metric.extended_properties[MODEL_VERSION]}
        if metric.extended_properties[METRIC_TYPE] == 'dataset':
            if METRIC_DATASET_METRICS not in metric_dict:
                metric_dict[METRIC_DATASET_METRICS] = []
            metric_dict[METRIC_DATASET_METRICS].append(_metric)

        elif metric.extended_properties[METRIC_TYPE] == 'column':
            column_dict = {metric.extended_properties['column_name']: [_metric]}
            metric_dict[METRIC_COLUMN_METRICS].append(column_dict)

        return metric_dict

    def update(self, services=..., compute_target_name=..., frequency=..., interval=..., feature_list=...,
               schedule_start=..., alert_config=..., create_compute_target=False, drift_threshold=...):
        r"""Update the schedule associated with the DataDrift object.

        :param services: Optional, list of services to update
        :type services: :class:list(str)
        :param compute_target_name: Optional, AzureML ComputeTarget name, creates one if none is specified
        :type compute_target_name: str
        :param frequency: How often the pipeline is run. i.e. "Day", "Week", "Month", default is "Day"
        :type frequency: str
        :param interval: Optional, how often the pipeline runs based on frequency. i.e. If frequency = "Day" and \
                         interval = 2, the pipeline will run every other day
        :type interval: int
        :param feature_list: Whitelisted features to run the datadrift detection on
        :type feature_list: :class:list(str)
        :param schedule_start: Start time of data drift schedule in UTC
        :type schedule_start: datetime.datetime
        :param alert_config: Optional, configuration object for DataDrift alerts
        :type alert_config: azureml.contrib.datadrift.AlertConfiguration
        :param create_compute_target: Whether the DataDrift API should automatically create an AML compute target
                                      Will be ignored if the schedule is disabled.
        :type create_compute_target: bool
        :param drift_threshold: Threshold to enable DataDrift alerts on
        :type drift_threshold: float
        :return: self
        :rtype: azureml.contrib.datadrift.DataDrift
        """
        with _TelemetryLogger.log_activity(self._logger, activity_name="update") as logger:
            if services is not ...:
                services = ParameterValidator.validate_services(services)
                self._services = services
            if compute_target_name is not ...:
                self._compute_target_name = ParameterValidator.validate_compute_target_name(compute_target_name,
                                                                                            self.workspace)
                if not self._compute_target_name:
                    self._compute_target_name = DEFAULT_COMPUTE_TARGET_NAME
            if frequency is not ...:
                self._frequency = ParameterValidator.validate_frequency(frequency, instance_logger=self._logger)
            if interval is not ...:
                self._interval = ParameterValidator.validate_interval(interval, instance_logger=self._logger)
            if feature_list is not ...:
                self._feature_list = ParameterValidator.validate_features(feature_list)
            if schedule_start is not ...:
                self._schedule_start = ParameterValidator.validate_datetime(schedule_start)
            if alert_config is not ...:
                self._alert_config = ParameterValidator.validate_alert_configuration(alert_config)
            if drift_threshold is not ...:
                self._drift_threshold = ParameterValidator.validate_drift_threshold(drift_threshold)
                if not self._drift_threshold:
                    self._drift_threshold = DEFAULT_DRIFT_THRESHOLD
            # TODO: Re-enable below values after private preview
            # if baseline_dataset is not ...:
            #     self._baseline_dataset = baseline_dataset
            # if baseline_dataset_start_time is not ...:
            #     self._baseline_dataset_start_time = baseline_dataset_start_time
            # if baseline_dataset_end_time is not ...:
            #     self._baseline_dataset_end_time = baseline_dataset_end_time

            # Disable and remove reference to previous schedule, and create a new schedule with updated params
            if self.enabled:
                self.disable_schedule()
                self.enable_schedule(create_compute_target=create_compute_target)

            self._update_remote(logger)
            return self

    def _update_remote(self, logger):
        """Update the DataDrift entry in the service database.

        :param logger: Activity logger for service call
        :type logger: datetime.datetime
        :return: DataDrift data transfer object
        :rtype: logging.Logger
        """
        dto = DataDriftDto(frequency=self._frequency,
                           schedule_start_time=self._schedule_start.replace(tzinfo=timezone.utc).isoformat()
                           if self._schedule_start else None,
                           schedule_id=self._schedule_id,
                           interval=self._interval,
                           alert_configuration=AlertConfiguration(self.alert_config.email_addresses)
                           if self.alert_config else None,
                           id=self._id,
                           model_name=self._model_name,
                           model_version=self._model_version,
                           services=self._services,
                           compute_target_name=self._compute_target_name,
                           base_line_dataset=self._baseline_dataset,
                           base_line_dataset_start_time=self._baseline_dataset_start_time,
                           base_line_dataset_end_time=self._baseline_dataset_end_time,
                           features=self._feature_list,
                           enabled=self._enabled,
                           drift_threshold=self._drift_threshold)
        return self._client.update(self._id, dto, logger)

    def _get_predictions_data(self, service, start_time=None, end_time=None):
        """Retrieve predictions data for given model and webservice.

        :param service: Service name
        :type model_name: str
        :param start_time:  Start of predictions data time window in UTC
        :type start_time: datetime.datetime
        :param end_time: End of scoring data time window in UTC
        :type end_time: datetime.datetime
        :return: DataReference object pointing to Azure Blob Storage location of predictions data
        :rtype: azureml.data.data_reference.DataReference
        """
        # TODO: Need re-visit this code when pipeline/schedule team supports dynamic paramters.
        if start_time is None:
            predictions_data_path = "{}/{}/{}/{}/{}/{}/predictions/" \
                .format(self.workspace.subscription_id,
                        self.workspace.resource_group,
                        self.workspace.name, service,
                        self.model_name, self.model_version)
        else:
            # pass the parent folder of the predictions data and the data driff scprit will use UTC (Today-1)
            # as target date.
            predictions_data_path = "{}/{}/{}/{}/{}/{}/predictions/{}/data.csv" \
                .format(self.workspace.subscription_id,
                        self.workspace.resource_group,
                        self.workspace.name, service,
                        self.model_name, self.model_version,
                        start_time.strftime('%Y/%m/%d'))

        blob_datastore = self.workspace.get_default_datastore()

        # Switch to model data blob container
        try:
            ds = Datastore.get(self.workspace, datastore_name='modeldata')
        except Exception:
            ds = Datastore.register_azure_blob_container(workspace=self.workspace,
                                                         datastore_name='modeldata',
                                                         container_name='modeldata',
                                                         account_name=blob_datastore.account_name,
                                                         account_key=blob_datastore.account_key,
                                                         create_if_not_exists=True)

        predictions_data_blob_ref = DataReference(datastore=ds, data_reference_name="predictions_data",
                                                  path_on_datastore=predictions_data_path)
        return predictions_data_blob_ref

    def _get_scoring_data(self, service, start_time=None, end_time=None):
        """Retrieve scoring data for given model and webservice.

        :param service: Service name
        :type model_name: str
        :param start_time:  Start of scoring data time window in UTC
        :type start_time: datetime.datetime
        :param end_time: End of scoring data time window in UTC
        :type end_time: datetime.datetime
        :return: DataReference object pointing to Azure Blob Storage location of scoring data
        :rtype: azureml.data.data_reference.DataReference
        """
        # TODO: Need re-visit this code when pipeline/schedule team supports dynamic paramters.
        if start_time is None:
            scoring_data_path = "{}/{}/{}/{}/{}/{}/inputs/".format(self.workspace.subscription_id,
                                                                   self.workspace.resource_group,
                                                                   self.workspace.name, service,
                                                                   self.model_name, self.model_version)
        else:
            # pass the parent folder of the scoring data and the data driff scprit will use UTC (Today-1)
            # as target date.
            scoring_data_path = "{}/{}/{}/{}/{}/{}/inputs/{}/data.csv".format(self.workspace.subscription_id,
                                                                              self.workspace.resource_group,
                                                                              self.workspace.name, service,
                                                                              self.model_name, self.model_version,
                                                                              start_time.strftime('%Y/%m/%d'))

        blob_datastore = self.workspace.get_default_datastore()

        # Switch to model data blob container
        try:
            ds = Datastore.get(self.workspace, datastore_name='modeldata')
        except Exception:
            ds = Datastore.register_azure_blob_container(workspace=self.workspace,
                                                         datastore_name='modeldata',
                                                         container_name='modeldata',
                                                         account_name=blob_datastore.account_name,
                                                         account_key=blob_datastore.account_key,
                                                         create_if_not_exists=True)

        scoring_data_blob_ref = DataReference(datastore=ds, data_reference_name="scoring_data",
                                              path_on_datastore=scoring_data_path)
        return scoring_data_blob_ref

    def _create_schedule(self, published_pipeline):
        """Create a schedule in the user's workspace from the pipeline and input frequency and interval.

        :param published_pipeline: Pipeline to be scheduled
        :type published_pipeline: azureml.pipeline.core.PublishedPipeline
        :return: Schedule based on the pipeline and specified frequency and interval
        :rtype: azureml.pipeline.core.schedule
        """
        # TODO: Implement hours and minutes
        # TODO: Restore schedule_start to datetime object once Pipeline team fixes bug
        recurrence = ScheduleRecurrence(frequency=self.frequency, interval=self.interval,
                                        start_time=None if self.schedule_start is None
                                        else self.schedule_start.strftime("%Y-%m-%dT%H:%M:%S"))

        schedule = Schedule.create(workspace=self.workspace, name=published_pipeline.name,
                                   pipeline_id=published_pipeline.id,
                                   experiment_name='Schedule_Run',
                                   recurrence=recurrence,
                                   pipeline_parameters={PIPELINE_PARAMETER_ADHOC_RUN: RUN_TYPE_SCHEDULE},
                                   wait_for_provisioning=True,
                                   description="Schedule Run")
        # Set the schedule_start to the schedule's start time
        return schedule

    def _create_validate_pipeline(self, script_dir_drift, script_name_drift, script_dir_curation, script_name_curation,
                                  correlation_id, target_date=None):
        """Create the data drift pipeline and validate it.

        :param script_dir_drift: Directory where data drift script is located
        :type script_dir_drift: str
        :param script_name_drift: Data drift script name
        :type script_name_drift: str
        :param script_dir_curation: Directory where data curation script is located
        :type script_dir_curation: str
        :param script_name_curation: Data curation script name
        :type script_name_curation: str
        :param correlation_id: caller correlation id
        :type correlation_id: str
        :param target_date: the target date for adhoc run. Leave it as None if it is for schedule run.
        :type target_date: datetime.datetime
        :return: Pipeline
        :rtype: azureml.pipeline.core.Pipeline
        """
        instrumentation_key = self._get_app_insights_instrumentation_key()
        # Create a new runconfig object
        run_amlcompute = RunConfiguration()

        # Use the cpu_cluster you created above.
        run_amlcompute.target = self.compute_target_name

        # Enable Docker
        run_amlcompute.environment.docker.enabled = True

        # Set Docker base image to the default CPU-based image
        run_amlcompute.environment.docker.base_image = DEFAULT_CPU_IMAGE

        # Use conda_dependencies.yml to create a conda environment in the Docker image for execution
        run_amlcompute.environment.python.user_managed_dependencies = False

        # Specify CondaDependencies obj, add necessary packages
        run_amlcompute.environment.python.conda_dependencies = CondaDependencies.create()

        # TODO: Pin minimal version of each dependency as documented in setup.py
        conda_packages = ['scikit-learn', 'scipy>=1.0.0', 'numpy', 'lightgbm', 'pandas', 'jsonpickle']
        for conda_package in conda_packages:
            run_amlcompute.environment.python.conda_dependencies.add_conda_package(conda_package)

        if VERSION.split('.')[0] == '0':
            # dev SDK
            # Pin the version of all AML packages except dataprep in a dev range if it is a dev SDK
            # TODO: Remove this and add to pip_packages above once azureml-contrib-datadrift is checked in
            azureml_build_index_base_url = "https://azuremlsdktestpypi.azureedge.net/"
            dev_url = "{}{}/{}/".format(azureml_build_index_base_url,
                                        'sdk-release/master',
                                        '588E708E0DF342C4A80BD954289657CF')
            simple_url = "https://pypi.python.org/simple"
            run_amlcompute.environment.python.conda_dependencies.set_pip_option(
                "--index-url {}".format(dev_url))
            run_amlcompute.environment.python.conda_dependencies.set_pip_option(
                "--extra-index-url {}".format(simple_url))

            dev_sdk_version_upper_bound = '0.1.1'
            pip_packages = ["{}>={},<{}".format('azureml-defaults', VERSION, dev_sdk_version_upper_bound),
                            "{}>={},<{}".format('azureml-pipeline', VERSION, dev_sdk_version_upper_bound),
                            "{}>={},<{}".format('azureml-widgets', VERSION, dev_sdk_version_upper_bound),
                            "{}>={},<{}".format('azureml-telemetry', VERSION, dev_sdk_version_upper_bound),
                            'azureml-dataprep',
                            "{}>={},<{}".format('azureml-core', VERSION, dev_sdk_version_upper_bound),
                            "{}>={},<{}".format('azureml-contrib-datadrift', VERSION, dev_sdk_version_upper_bound)]
        else:
            # prod SDK
            # TODO: need pin the version of AML packages in prod as well
            pip_packages = ['azureml-defaults',
                            'azureml-pipeline',
                            'azureml-widgets',
                            'azureml-telemetry',
                            'azureml-dataprep',
                            'azureml-core',
                            'azureml-contrib-datadrift']

        for pip_package in pip_packages:
            run_amlcompute.environment.python.conda_dependencies.add_pip_package(pip_package)

        curr_time = datetime.utcnow()
        pipeline_name = "drift-{}-pipeline".format(curr_time.strftime("%Y-%m-%d-%H-%M-%S"))

        pipeline_param_adhoc_run = PipelineParameter(name=PIPELINE_PARAMETER_ADHOC_RUN,
                                                     default_value=RUN_TYPE_SCHEDULE)

        steps = list()
        for service in self.services:
            scoring_data = self._get_scoring_data(service, target_date)
            predictions_data = self._get_predictions_data(service, target_date)
            model_serving_output_path_root, model_serving_output_path = \
                self._get_model_serving_output_reference(service, target_date)
            metrics_output_path_root, metrics_output_path = self._get_metric_output_reference(service, target_date)
            target_date_str = None if target_date is None else target_date.strftime("%Y-%m-%d")

            arguments_curation = ["--scoring_data", scoring_data,
                                  "--predictions_data", predictions_data,
                                  "--model_serving_output_path_root", model_serving_output_path_root,
                                  "--model_serving_output_path", model_serving_output_path,
                                  "--instrumentation_key", instrumentation_key,
                                  "--workspace_name", self.workspace.name,
                                  "--model_name", self.model_name,
                                  "--model_version", self.model_version,
                                  "--service", service,
                                  "--pipeline_name", pipeline_name,
                                  "--root_correlation_id", correlation_id,
                                  "--latency_in_days", 1,
                                  "--version", __version__,
                                  "--subscription_id", self._workspace.subscription_id,
                                  "--datadrift_id", self._id,
                                  "--enable_metric_logger", True,
                                  "--adhoc_run", pipeline_param_adhoc_run]

            if target_date_str:
                arguments_curation.append("--target_date")
                arguments_curation.append(target_date_str)

            step_curation_name = "{}-{}".format(script_name_curation, service)
            step_curation = PythonScriptStep(

                script_name=script_name_curation,
                name=step_curation_name,

                arguments=arguments_curation,
                inputs=[scoring_data, predictions_data],
                outputs=[model_serving_output_path_root],
                compute_target=self.compute_target_name,
                source_directory=script_dir_curation,
                runconfig=run_amlcompute)

            steps.append(step_curation)
            self._logger.debug("Curation step {} created".format(step_curation_name))

            arguments_drift = ["--scoring_data", scoring_data,
                               "--metrics_output_path_root", metrics_output_path_root,
                               "--metrics_output_path", metrics_output_path,
                               "--instrumentation_key", instrumentation_key,
                               "--workspace_name", self.workspace.name,
                               "--model_name", self.model_name,
                               "--model_version", self.model_version,
                               "--service", service,
                               "--pipeline_name", pipeline_name,
                               "--root_correlation_id", correlation_id,
                               "--version", __version__,
                               "--subscription_id", self._workspace.subscription_id,
                               "--datadrift_id", self._id,
                               "--enable_metric_logger", True,
                               "--drift_threshold", self.drift_threshold,
                               "--adhoc_run", pipeline_param_adhoc_run]

            if target_date_str:
                arguments_drift.append("--target_date")
                arguments_drift.append(target_date_str)
            if self.feature_list is not None and len(self.feature_list) > 0:
                arguments_drift.append("--features_whitelist")
                arguments_drift.extend(self.feature_list)

            step_drift_name = "{}-{}".format(script_name_drift, service)
            step_drift = PythonScriptStep(

                script_name=script_name_drift,
                name=step_drift_name,

                arguments=arguments_drift,
                inputs=[scoring_data, model_serving_output_path_root],
                outputs=[metrics_output_path_root],
                compute_target=self.compute_target_name,
                source_directory=script_dir_drift,
                runconfig=run_amlcompute)

            steps.append(step_drift)
            self._logger.debug("Drift step {} created".format(step_drift_name))

        pipeline1 = Pipeline(workspace=self.workspace, steps=steps)
        self._logger.debug("Pipeline is built")

        pipeline1.validate()
        self._logger.debug("Simple validation complete")

        return pipeline1

    def _get_app_insights_instrumentation_key(self):
        """Get the instrumentation key of the Application Insights instance associated with the current workspace.

        :param workspace: Object that points to the workspace
        :type workspace: azureml.core.workspace.Workspace
        :raises azureml.exceptions.WebserviceException
        :return: the instrumentation key of the Application Insights instance
        :rtype: str
        """
        keys_endpoint = 'https://management.azure.com/subscriptions/{}/resourceGroups/{}/providers/' \
                        'Microsoft.MachineLearningServices/workspaces/' \
                        '{}/listKeys'.format(self.workspace.subscription_id,
                                             self.workspace.resource_group,
                                             self.workspace.name)
        headers = self.workspace._auth.get_authentication_header()
        params = {'api-version': WORKSPACE_RP_API_VERSION}

        try:
            keys_resp = requests.post(
                keys_endpoint, headers=headers, params=params)
            keys_resp.raise_for_status()
        except requests.exceptions.HTTPError:
            raise WebserviceException('Unable to retrieve workspace keys to run image:\n'
                                      'Response Code: {}\n'
                                      'Headers: {}\n'
                                      'Content: {}'.format(keys_resp.status_code, keys_resp.headers,
                                                           keys_resp.content))
        content = keys_resp.content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        keys_dict = json.loads(content)

        return keys_dict['appInsightsInstrumentationKey']

    def _get_model_serving_output_reference(self, service, target_date):
        """Get the pipelinedata reference to model serving output root and relative path on datastore.

        :param service: Service name
        :type service: str
        :param target_date: target date of model serving data
        :rtype: datetime.datetime
        :return: Pipelinedata reference to model serving output root
        :rtype: str
        :return: Relative path to model serving on datastore
        :rtype: str
        """
        blob_datastore = self.workspace.get_default_datastore()

        try:
            ds = Datastore.get(self.workspace, datastore_name='modelservingdata')
        except Exception:
            ds = Datastore.register_azure_blob_container(workspace=self.workspace,
                                                         datastore_name='modelservingdata',
                                                         container_name='modelservingdata',
                                                         account_name=blob_datastore.account_name,
                                                         account_key=blob_datastore.account_key,
                                                         create_if_not_exists=True)

        model_serving_output_path_root = PipelineData(name="ModelServing", datastore=ds, is_directory=True)

        model_serving_output_relative_path = DataDrift._get_model_serving_path(
            self.model_name, self.model_version, service, target_date)

        return model_serving_output_path_root, model_serving_output_relative_path

    @staticmethod
    def _get_model_serving_path(model_name, model_version, service, target_date=None):
        """Get the metric path for a given model version, instance start_time and frequency of diff.

        :param model_name: Model name
        :type model_name: str
        :param model_version: Model version
        :type model_version: str
        :param service: Service name
        :type service: str
        :param target_date: Diff instance target date. If none datetime portion is ommitted.
        :type target_date: datetime.datetime
        :return: Relative path to metric on datastore
        :rtype: str
        """
        metrics_output_path = "ModelServing/{}/{}/{}/".format(
            model_name, model_version, service)

        if target_date is not None:
            metrics_output_path += "{}/".format(target_date.strftime('%Y/%m/%d'))

        return metrics_output_path

    def _get_metric_output_reference(self, service, target_date):
        """Get the pipelinedata reference to metric output root and relative path on datastore.

        :param service: Service name
        :type service: str
        :param target_date: target date of metrics
        :type target_date: datetime.datetime
        :return: Pipelinedata reference to metric output root
        :rtype: str
        :return: Relative path to metric on datastore
        :rtype: str
        """
        ds = Datastore(self.workspace, "workspaceblobstore")

        metric_output_path_root = PipelineData(name="DataDrift", datastore=ds,
                                               is_directory=True)

        metric_output_relative_path = DataDrift._get_metrics_path(self.model_name, self.model_version,
                                                                  service, target_date)

        return metric_output_path_root, metric_output_relative_path

    @staticmethod
    def _get_metrics_path(model_name, model_version, service, target_date=None):
        """Get the metric path for a given model version, instance target date and frequency of diff.

        :param model_name: Model name
        :type model_name: str
        :param model_version: Model version
        :type model_version: int
        :param service: Service name
        :type service: str
        :param target_date: Diff instance start time. If none datetime portion is ommitted.
        :type target_date: datetime.datetime
        :return: Relative path to metric on datastore
        :rtype: str
        """
        metrics_output_path = "DataDrift/Metrics/{}/{}/{}/".format(
            model_name, model_version, service)

        if target_date is not None:
            metrics_output_path += "{}/".format(target_date.strftime('%Y/%m/%d'))

        return metrics_output_path

    def _get_metrics(self):
        """Get all metrics for current datadrift instance."""
        ds = Datastore(self.workspace, "workspaceblobstore")
        local_temp_root = os.path.join(tempfile.gettempdir(), self.workspace.get_details()["workspaceid"])
        os.makedirs(local_temp_root, exist_ok=True)

        metrics = []

        for s in self.services:
            metrics_rel_path = DataDrift._get_metrics_path(self.model_name, self.model_version, s)

            ds.download(target_path=local_temp_root, prefix=metrics_rel_path, show_progress=False)

            metrics_list = glob.glob(os.path.join(
                local_temp_root, *"{}/**/*.json".format(metrics_rel_path).split("/")), recursive=True)

            for f in metrics_list:
                with open(f, 'r') as metrics_json:
                    data = metrics_json.read()
                    metrics = metrics + jsonpickle.decode(data)

        # tempfile.gettempdir() always points to same folder with same guid
        # thus empty temp folder to ensure new contents will be downloaded in each running.
        shutil.rmtree(local_temp_root, ignore_errors=True)

        return metrics

    def _get_valid_dates(self, input_start, input_end, available_dates):
        """Return valid dates by cross checking API input start/end dates and available dates.

        :param input_start:  start of presenting data time window in UTC
        :type input_start: datetime.datetime
        :param input_end: end of presenting data time window in UTC
        :type input_end: datetime.datetime
        :param available_dates: a set of all dates for which data drift results are available
        :type available_dates: set(datetime.datetime)
        :return: start date of valid range
        :rtype: datetime.datetime
        :return: end date of valid range
        :rtype: datetime.datetime
        """
        if input_start is not None and input_end is not None and input_start > input_end:
            self._logger.error("Invalid Time Range from {} to {}".format(input_start, input_end))
            raise ValueError("Invalid Time Range from {} to {}".format(input_start, input_end))

        dates = list(available_dates)
        dates.sort()

        range_st = input_start if input_start is not None else dates[0]
        range_ed = input_end if input_end is not None else dates[-1]
        range_st_locked = True if input_start is None else False
        range_ed_locked = True if input_end is None else False

        if range_ed < dates[0] or range_st > dates[-1]:
            self._logger.error("No available data from {} to {}".format(range_st, range_ed))
            raise ValueError("No available data from {} to {}".format(range_st, range_ed))

        for dt in dates:
            if not range_st_locked and range_st <= dt:
                range_st = dt
                range_st_locked = True
            if not range_ed_locked and (range_ed <= dt or dt == dates[-1]):
                range_ed = dt
                range_ed_locked = True

        self._logger.debug("Valid Time Range is from {} to {}".format(range_st, range_ed))

        return range_st, range_ed

    @staticmethod
    def _generate_plot_figure(environment, ordered_content, with_details):
        """Show trends for a metrics.

        :param environment: information of workspace, model, model version and service
        :type ordered_content: str
        :param ordered_content: all contents to present presorted by date
        :type ordered_content: nested dict
        :param with_details: flag of show all or not
        :type with_details: bool
        :return: matplotlib.figure.Figure
        """
        dates = list(ordered_content.keys())
        drifts_train = []
        feature_importance = {}
        distance_energy = {}
        distnace_wasserstein = {}
        columns_importance = []
        columns_distance_e = []
        columns_distance_w = []

        for d in dates:
            drifts_train.append(ordered_content[d][METRIC_DATASHIFT_MCC_TEST])
            if with_details is True:
                if len(columns_importance) == 0:
                    columns_importance = list(ordered_content[d][METRIC_DATASHIFT_FEATURE_IMPORTANCE].keys())
                for c in columns_importance:
                    if c not in feature_importance:
                        feature_importance[c] = {}
                    feature_importance[c][d] = ordered_content[d][METRIC_DATASHIFT_FEATURE_IMPORTANCE][c]
                    # distance is available only for numeric columns.
                    if c in ordered_content[d][METRIC_STATISTICAL_DISTANCE_ENERGY]:
                        if c not in distance_energy:
                            distance_energy[c] = {}
                        distance_energy[c][d] = ordered_content[d][METRIC_STATISTICAL_DISTANCE_ENERGY][c]
                        if c not in columns_distance_e:
                            columns_distance_e.append(c)
                    # distance is available only for numeric columns.
                    if c in ordered_content[d][METRIC_STATISTICAL_DISTANCE_WASSERSTEIN]:
                        if c not in distnace_wasserstein:
                            distnace_wasserstein[c] = {}
                        distnace_wasserstein[c][d] = ordered_content[d][METRIC_STATISTICAL_DISTANCE_WASSERSTEIN][c]
                        if c not in columns_distance_w:
                            columns_distance_w.append(c)

        # show data drift
        width = 10
        height = 8
        ratio = 2 if with_details is True else 1
        figure = plt.figure(figsize=(width * ratio, height * ratio))
        plt.suptitle(environment, fontsize=14)
        plt.subplots_adjust(bottom=0.1, top=0.85 if with_details is True else 0.75, hspace=0.5)
        plt.tight_layout()
        ax1 = plt.subplot(ratio, ratio, 1)

        plt.sca(ax1)
        plt.plot(dates, drifts_train, '-g', marker='x', linewidth=2.0, markersize=10)
        plt.xlabel("Date", fontsize=16)
        plt.ylabel("Drift", fontsize=16)
        plt.xticks(rotation=15)
        plt.title("Data Drift\n", fontsize=20)

        if with_details is True:
            ax2 = plt.subplot(ratio, ratio, 2)
            ax3 = plt.subplot(ratio, ratio, 3)
            ax4 = plt.subplot(ratio, ratio, 4)
            colors = plt.cm.get_cmap('hsv', len(columns_importance))

            plt.sca(ax2)
            plt.yscale('log')
            for c in columns_importance:
                plt.plot(dates, feature_importance[c].values(),
                         c=colors(columns_importance.index(c)), marker='x',
                         linewidth=2.0, markersize=10)
            plt.xlabel("Date", fontsize=16)
            plt.ylabel(FIGURE_FEATURE_IMPORTANCE_Y_LABEL, fontsize=16)
            plt.xticks(rotation=15)
            plt.title(FIGURE_FEATURE_IMPORTANCE_TITLE, fontsize=20)
            plt.legend(columns_importance)

            plt.sca(ax3)
            plt.yscale('log')
            for c in columns_distance_e:
                # keep the column color aligned with feature importance↘
                plt.plot(dates, distance_energy[c].values(),
                         c=colors(columns_importance.index(c)), marker='x',
                         linewidth=2.0, markersize=10)
            plt.xlabel("Date", fontsize=16)
            plt.ylabel("Distance", fontsize=16)
            plt.xticks(rotation=15)
            plt.title("Energy Distance\n", fontsize=20)
            plt.legend(columns_distance_e)

            plt.sca(ax4)
            plt.yscale('log')
            for c in columns_distance_w:
                # keep the column color aligned with feature importance↘
                plt.plot(dates, distnace_wasserstein[c].values(),
                         c=colors(columns_importance.index(c)), marker='x',
                         linewidth=2.0, markersize=10)
            plt.xlabel("Date", fontsize=16)
            plt.ylabel("Distance", fontsize=16)
            plt.xticks(rotation=15)
            plt.title("Wasserstein Distance\n", fontsize=20)
            plt.legend(columns_distance_w)

        return figure

    def show(self, start_time=None, end_time=None, with_details=False):
        """Show data drift trend in given time range for a given model, version and service.

        :param start_time:  Optional, start of presenting data time window in UTC
        :type start_time: datetime.datetime
        :param end_time: Optional, end of presenting data time window in UTC
        :type end_time: datetime.datetime
        :param with_details: Show additional graphs of feature importance and energy/wasserstein distance if it's True
        :type with_details: bool
        :return: diction of all figures. Key is service_name
        :rtype: dict()
        """
        if start_time is not None:
            start_time = ParameterValidator.validate_datetime(start_time)
        if end_time is not None:
            end_time = ParameterValidator.validate_datetime(end_time)

        metrics = self._get_metrics()

        if len(metrics) == 0:
            raise FileNotFoundError("DataDrift results are unavailable.")

        metrics_dates = set()
        metrics_services = set()
        for m in metrics:
            metrics_dates.add(m.extended_properties[SCORING_DATE])
            metrics_services.add(m.extended_properties["service"])

        # get min/max date in metrics and cross check with input start/end time to determine output range
        range_st, range_ed = self._get_valid_dates(start_time, end_time, metrics_dates)

        # build metrics for graph showing of each service in valid date range
        # the graph is per service; In side each graph, there might be sub plots for different measurements.
        # considering the order in dict is not guaranteed, organize all contents with date key and sort by date
        # general data drift will be stored per day
        # detailed measurement will be sorted per measurement per column per day
        contents = {}
        for s in metrics_services:
            if s not in contents:
                contents[s] = {}
            for m in metrics:
                date = m.extended_properties[SCORING_DATE]
                if range_st <= date and range_ed >= date:
                    if date not in contents[s]:
                        contents[s][date] = {}
                    if m.extended_properties[METRIC_TYPE] == "dataset":
                        contents[s][date][m.name] = m.value
                        contents[s][date][SERVICE] = m.extended_properties[SERVICE]
                    if with_details is True and m.extended_properties[METRIC_TYPE] == "column":
                        if m.name not in contents[s][date]:
                            contents[s][date][m.name] = {}
                        contents[s][date][m.name][m.extended_properties[COLUMN_NAME]] = m.value

        # produce figures
        figures = {}
        for c in contents:
            # sort by date to ensure correct order in graph
            ordered_content = OrderedDict(sorted(contents[c].items(), key=lambda t: t[0]))

            # environment information (alignment refined with extra spaces
            environment = "Workspace Name : {}           \n" \
                          "Model Name : {}\n" \
                          "Model Version : {}                            \n" \
                          "Service Name : {}  ". \
                format(self.workspace.name, self.model_name, self.model_version, c)

            figure = DataDrift._generate_plot_figure(environment, ordered_content, with_details)

            figures[c] = figure

        return figures
