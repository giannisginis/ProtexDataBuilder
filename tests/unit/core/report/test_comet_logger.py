from unittest.mock import patch
from pipeline.core.report.comet_logger import CometLogger


@patch("pipeline.core.report.comet_logger.Experiment")
def test_logger_initialization(mock_experiment):
    logger = CometLogger(
        project_name="test-project",
        api_key="fake-key",
        disabled=False,
        experiment_name="test-run",
        tags=["unit", "test"],
    )
    mock_experiment.assert_called_once()
    logger.experiment.set_name.assert_called_once_with("test-run")
    logger.experiment.add_tags.assert_called_once_with(["unit", "test"])


@patch("pipeline.core.report.comet_logger.Experiment")
def test_log_metrics(mock_experiment):
    logger = CometLogger("project", api_key="fake-key", disabled=False)
    logger.log_metrics({"accuracy": 0.9, "loss": 0.1})
    assert logger.experiment.log_metric.call_count == 2


@patch("pipeline.core.report.comet_logger.Experiment")
def test_log_params(mock_experiment):
    logger = CometLogger("project", api_key="fake-key", disabled=False)
    logger.log_params({"model": "YOLOv8", "skip": 2})
    assert logger.experiment.log_parameter.call_count == 2


@patch("pipeline.core.report.comet_logger.Experiment")
def test_logger_end(mock_experiment):
    logger = CometLogger("project", api_key="fake-key", disabled=False)
    logger.end()
    logger.experiment.end.assert_called_once()
