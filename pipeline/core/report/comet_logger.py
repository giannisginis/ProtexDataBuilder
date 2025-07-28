import os
from typing import Dict, Optional, List
from comet_ml import Experiment


class CometLogger:
    def __init__(
        self,
        project_name: str,
        workspace: Optional[str] = None,
        api_key: Optional[str] = None,
        experiment_name: Optional[str] = None,
        experiment_key: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        disabled: bool = False,
    ):
        self.api_key = api_key or os.getenv("COMET_API_KEY")

        if not self.api_key and not disabled:
            raise ValueError(
                "Comet-ML API key not provided. "
                "Set COMET_API_KEY environment variable or pass api_key explicitly."
            )

        self.experiment = Experiment(
            api_key=self.api_key,
            project_name=project_name,
            workspace=workspace,
            experiment_key=experiment_key,
            auto_output_logging=False,
            disabled=disabled,
        )

        if experiment_name:
            self.experiment.set_name(experiment_name)
        if tags:
            self.experiment.add_tags(tags)
        if notes:
            self.experiment.log_other("notes", notes)

    def log_metrics(self, metrics: Dict[str, float]):
        for key, value in metrics.items():
            self.experiment.log_metric(key, value)

    def log_params(self, params: Dict[str, str]):
        for key, value in params.items():
            self.experiment.log_parameter(key, value)

    def log_assets(self, assets: Dict[str, str]):
        for key, value in assets.items():
            self.experiment.log_asset(value, file_name=key)

    def end(self):
        self.experiment.end()
