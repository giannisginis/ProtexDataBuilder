import os
import yaml
from pathlib import Path
from deepmerge import always_merger
from typing import Optional


def load_config_from_file(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def load_config_from_env(env: Optional[str] = None) -> dict:
    base_config_path = Path("pipeline/config/base.yaml")
    env = env or os.getenv("APP_ENV", "dev")
    env_config_path = Path(f"pipeline/config/{env}.yaml")

    with open(base_config_path) as f:
        base = yaml.safe_load(f)

    if env_config_path.exists():
        with open(env_config_path) as f:
            override = yaml.safe_load(f)
        return always_merger.merge(base, override)
    else:
        return base


def load_config(config_path: Optional[str] = None, env: Optional[str] = None) -> dict:
    """
    Load configuration either from a specific file or from environment-based configs.

    Args:
        config_path: Path to YAML config file (optional).
        env: Environment name for config override (e.g., dev, prod) (optional).

    Returns:
        Merged config dict.
    """
    if config_path:
        return load_config_from_file(config_path)
    else:
        return load_config_from_env(env)
