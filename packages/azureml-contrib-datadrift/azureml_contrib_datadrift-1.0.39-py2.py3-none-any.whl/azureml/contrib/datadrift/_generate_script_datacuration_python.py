# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import argparse
import pandas as pd
import time
import os
import uuid

from datetime import datetime, timedelta
from pathlib import Path
from azureml.core.run import Run
from azureml.contrib.datadrift import datadrift
from azureml.contrib.datadrift._logging._metric_logger import _MetricLogger
from azureml.contrib.datadrift._logging._telemetry_logger import _TelemetryLogger, INSTRUMENTATION_KEY
from azureml.contrib.datadrift._logging._telemetry_logger_context_filter import _TelemetryLoggerContextFilter
from azureml.contrib.datadrift._utils.constants import LOG_FLUSH_LATENCY, RUN_TYPE_SCHEDULE, RUN_TYPE_ADHOC
from azureml.contrib.datadrift._datadiff import Metric

module_logger = _TelemetryLogger.get_telemetry_logger('_generate_script_datacuration_python')


def merge(row):
    result = {}
    for idx in row.index:
        if not idx.startswith('$'):
            result[idx] = row[idx]
    return result


def main():
    parser = argparse.ArgumentParser("script")

    parser.add_argument("--scoring_data", type=str, help="Training Data Reference Object")
    parser.add_argument("--predictions_data", type=str, help="Scoring Data Reference Object")
    parser.add_argument("--model_serving_output_path_root", type=str, help="Model serving output path root")
    parser.add_argument("--model_serving_output_path", type=str, help="Model serving output path")
    parser.add_argument("--workspace_name", type=str, help="Workspace name")
    parser.add_argument("--model_name", type=str, help="Model name")
    parser.add_argument("--model_version", type=str, help="Model version")
    parser.add_argument("--service", type=str, help="Deployed service name")
    parser.add_argument("--pipeline_name", type=str, help="Deployed pipeline name")
    parser.add_argument("--root_correlation_id", type=str, help="Caller correlation Id")
    parser.add_argument("--instrumentation_key", type=str, help="Application insight instrumentation key")
    parser.add_argument("--version", type=str, help="Pipeline version")
    parser.add_argument("--subscription_id", type=str, help="Subscription Id")
    parser.add_argument("--resource_group", type=str, help="Resource Group")
    parser.add_argument("--enable_metric_logger", type=bool, default=False, help="Enable metrics logger")
    parser.add_argument("--latency_in_days", type=int, default=1, help="latency in days")
    parser.add_argument("--target_date", type=str, help="Target date of the data. The format should be YYYY-MM-DD")
    parser.add_argument("--adhoc_run", type=str, default=RUN_TYPE_SCHEDULE, help="adhoc run")
    parser.add_argument("--datadrift_id", type=str, help="Datadrift object id")

    args = parser.parse_args()
    run = Run.get_context()
    adhoc_run = (args.adhoc_run == RUN_TYPE_ADHOC)

    try:
        runid = run.get_details()["runId"]
    except AttributeError:
        runid = "{}".format(uuid.uuid4())

    log_context = {'workspace_name': args.workspace_name, 'model_name': args.model_name,
                   'model_version': args.model_version, 'service': args.service, 'pipeline_name': args.pipeline_name,
                   'pipeline_version': args.version, 'root_correlation_id': args.root_correlation_id, 'run_id': runid,
                   'subscription_id': args.subscription_id, 'resource_group': args.resource_group,
                   'datadrift_id': args.datadrift_id,
                   'run_type': RUN_TYPE_ADHOC if adhoc_run else RUN_TYPE_SCHEDULE}

    module_logger.addFilter(_TelemetryLoggerContextFilter(log_context))
    curation_time = datetime.utcnow()

    try:
        with _TelemetryLogger.log_activity(module_logger,
                                           activity_name="_generate_script_datacuration_python") as logger:
            logger.info("In script.py, runid:{}".format(runid))

            for arg in vars(args):
                logger.debug("{}: {}".format(arg, getattr(args, arg)))

            # if target_date is specified, use it as target date. Otherwise, switch to use (utcnow - latency_in_days)
            if args.target_date:
                target_date = datetime.strptime(args.target_date, '%Y-%m-%d')
            else:
                target_date = curation_time - timedelta(days=args.latency_in_days)

            # read and process inputs(scoring) data
            if adhoc_run:
                scoring_data_path = args.scoring_data
            else:
                scoring_data_path = os.path.join("{}{}".format(args.scoring_data, target_date.strftime('%Y')),
                                                 target_date.strftime('%m'), target_date.strftime('%d'),
                                                 "data.csv")
            inputs = pd.read_csv(scoring_data_path, index_col='$CorrelationId')

            rowcount_scoring = len(inputs.index)
            logger.debug("Scoring data row count:{}".format(rowcount_scoring))
            logger.debug("Scoring data schema:{}".format(inputs.dtypes))

            inputs.rename(columns={'$Timestamp': '$Timestamp_Inputs', '$RequestId': '$RequestId_Inputs'}, inplace=True)
            inputs['$Features'] = inputs.filter(regex=r'^(?!\$)').to_dict('records')
            inputs = inputs[['$RequestId_Inputs', '$Timestamp_Inputs', '$Features']]

            # read and process predictions data
            if adhoc_run:
                predictions_data_path = args.predictions_data
            else:
                predictions_data_path = os.path.join("{}{}".format(args.predictions_data, target_date.strftime('%Y')),
                                                     target_date.strftime('%m'), target_date.strftime('%d'),
                                                     "data.csv")
            predictions = pd.read_csv(predictions_data_path, index_col='$CorrelationId')

            rowcount_predictions = len(predictions.index)
            logger.debug("Prediction data row count:{}".format(rowcount_predictions))
            logger.debug("Prediction data schema:{}".format(predictions.dtypes))

            # filter out rows with null correlation id
            predictions = predictions.loc[predictions.index.notnull()]
            # do de-duplication on correlation id
            predictions = predictions[~predictions.index.duplicated(keep='first')]
            rowcount_predictions_filtered = len(predictions.index)
            logger.debug("Prediction data after flitering and dedup row count:{}"
                         .format(rowcount_predictions_filtered))

            predictions.rename(columns={'$Timestamp': '$Timestamp_Predictions',
                                        '$RequestId': '$RequestId_Predictions'}, inplace=True)
            predictions['$Prediction_Result'] = predictions.filter(regex=r'^(?!\$)').to_dict('records')
            predictions = predictions[['$RequestId_Predictions', '$Timestamp_Predictions', '$Prediction_Result']]

            # join inputs and predictions to get model serving data
            serving_data = inputs.join(predictions, on='$CorrelationId', how='left')
            serving_data['$Timestamp_Curation'] = curation_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
            serving_data['$ModelName'] = args.model_name
            serving_data['$ModelVersion'] = args.model_version
            serving_data['$ServiceName'] = args.service

            # added columns that indicate the availability of label data and signal data
            serving_data['$LabelDataIsAvailable'] = False
            serving_data['$SignalDataIsAvailable'] = False

            rowcount_serving = len(serving_data.index)
            logger.debug("Model serving data row count:{}".format(rowcount_serving))
            logger.debug("Modle serving data schema:{}".format(serving_data.dtypes))

            # Remove GUID generated by azureml pipelinedata.
            model_serving_output_path_root = str(Path(args.model_serving_output_path_root).parents[1])
            if adhoc_run:
                model_serving_output_path = args.model_serving_output_path
            else:
                model_serving_output_path = datadrift.DataDrift._get_model_serving_path(args.model_name,
                                                                                        args.model_version,
                                                                                        args.service,
                                                                                        target_date)
            model_serving_output = os.path.join(model_serving_output_path_root,
                                                model_serving_output_path,
                                                "data.parquet")

            logger.debug("Model serving data output path is:{}".format(model_serving_output))
            logger.debug("Creating output metrics directory if not exist: {}"
                         .format(os.path.dirname(model_serving_output)))
            os.makedirs(os.path.dirname(model_serving_output), exist_ok=True)

            # using fastparquet as the parquet engine because pyarrow is not able to handle dict.
            # using gzip as compression option instead of default snappy.
            # compared to snappy, gzip is better in saving storage cost but has more CPU cost.
            # gzip is always available and no additional package is required.
            serving_data.to_parquet(fname=model_serving_output, engine='fastparquet', index=True, compression='gzip')

            # log metrics
            if args.enable_metric_logger:
                metric_logger = _MetricLogger(INSTRUMENTATION_KEY)

                extended_properties = {'target_date': target_date.strftime("%Y-%m-%d"),
                                       'model_name': args.model_name,
                                       'model_version': args.model_version,
                                       'service': args.service,
                                       'pipeline_name': args.pipeline_name,
                                       'runid': runid,
                                       'datadrift_id': args.datadrift_id,
                                       'run_type': RUN_TYPE_ADHOC if adhoc_run else RUN_TYPE_SCHEDULE}
                metric_logger.log_metric(Metric(name='rowcount_scoring',
                                                value=rowcount_scoring,
                                                extended_properties=extended_properties))
                metric_logger.log_metric(Metric(name='rowcount_predictions',
                                                value=rowcount_predictions,
                                                extended_properties=extended_properties))
                metric_logger.log_metric(Metric(name='rowcount_predictions_filtered',
                                                value=rowcount_predictions_filtered,
                                                extended_properties=extended_properties))
                metric_logger.log_metric(Metric(name='rowcount_serving',
                                                value=rowcount_serving,
                                                extended_properties=extended_properties))

                logger.info('metrics logged')
    except FileNotFoundError as e:
        # scoring or predictions data is missing.
        # exit rather than fail to let the other curation and drift steps run.
        logger.error(e, exc_info=True)
        return 0
    except KeyError as e:
        # scoring data or predictions data is malformed.
        # exit rather than fail to let the other curation and drift steps run.
        logger.error(e, exc_info=True)
        return 0
    except Exception as e:
        # failed due to unexpected exception. raise the exception.
        logger.error(e, exc_info=True)
        raise
    finally:
        # allow time for async channel to send the service log entities to application insights
        if module_logger.handlers:
            for handler in module_logger.handlers:
                handler.flush()
                if type(handler).__name__ == 'AppInsightsLoggingHandler':
                    print('Wait some time for application insights async channel to flush')
                    time.sleep(LOG_FLUSH_LATENCY)


if __name__ == '__main__':
    main()
