# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""This package contains the core functionality for Azure Machine Learning service pipelines.

Azure Machine Learning service pipelines represent a collections of
:class:`azureml.pipeline.core.PipelineStep` which can be executed as a workflow.
For more details about pipeline and its advantages, you may refer to,
https://docs.microsoft.com/en-us/azure/machine-learning/service/concept-ml-pipelines.
"""
from .builder import PipelineStep, PipelineData, StepSequence
from .pipeline import Pipeline
from .graph import PublishedPipeline, PortDataReference, OutputPortBinding, InputPortBinding, TrainingOutput
from .graph import PipelineParameter, PipelineDataset
from .schedule import Schedule, ScheduleRecurrence, TimeZone
from .pipeline_endpoint import PipelineEndpoint
from .run import PipelineRun, StepRun, StepRunOutput
from azureml.core import Run

__all__ = ["PipelineRun",
           "StepRun",
           "StepRunOutput",
           "PipelineStep",
           "PipelineData",
           "Pipeline",
           "PublishedPipeline",
           "PipelineParameter",
           "PortDataReference",
           "OutputPortBinding",
           "InputPortBinding",
           "TrainingOutput",
           "StepSequence",
           "Schedule",
           "ScheduleRecurrence",
           "TimeZone",
           "PipelineEndpoint",
           "PipelineDataset"
           ]


Run.add_type_provider('azureml.PipelineRun', PipelineRun._from_dto)
Run.add_type_provider('azureml.StepRun', StepRun._from_dto)
Run.add_type_provider('azureml.ReusedStepRun', StepRun._from_reused_dto)
