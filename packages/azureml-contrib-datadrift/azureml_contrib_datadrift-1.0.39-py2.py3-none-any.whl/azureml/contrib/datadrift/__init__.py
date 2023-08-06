# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Enable DataDrift detection on Azure ML."""

from .datadrift import DataDrift
from .alert_configuration import AlertConfiguration
from ._datadiff import Metric, MetricType
from azureml._base_sdk_common import __version__ as VERSION

__all__ = ["DataDrift", "Metric", "MetricType", "AlertConfiguration"]
__version__ = VERSION
