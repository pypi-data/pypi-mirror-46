# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Accelerate deep neural networks on FPGAs with the Azure ML Hardware Accelerated Models Service."""
from azureml.accel._accel_container_image import AccelImageConfiguration, AccelContainerImage
from azureml.accel._accel_onnx_converter import AccelOnnxConverter
from azureml.accel._client import PredictionClient, client_from_service
from azureml.accel._version import VERSION

__version__ = VERSION

__all__ = [
    "AccelImageConfiguration",
    "AccelContainerImage",
    "AccelOnnxConverter",
    "PredictionClient",
    "client_from_service"
]
