import yaml
from pipeline.utils.helpers import (
    load_config_from_file,
    load_config_from_env,
    load_config,
)


def test_load_config_from_file(tmp_path):
    config_path = tmp_path / "test_config.yaml"
    config_data = {"param1": "value1", "param2": 42}
    config_path.write_text(yaml.dump(config_data))

    loaded = load_config_from_file(str(config_path))
    assert loaded == config_data


def test_load_config_from_env(tmp_path, monkeypatch):
    config_dir = tmp_path / "pipeline" / "config"
    config_dir.mkdir(parents=True)

    base_config = {"param1": "base", "param2": 1}
    dev_override = {"param2": 999, "param3": "new"}

    (config_dir / "base.yaml").write_text(yaml.dump(base_config))
    (config_dir / "dev.yaml").write_text(yaml.dump(dev_override))

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APP_ENV", "dev")

    result = load_config_from_env()

    assert result["param1"] == "base"
    assert result["param2"] == 999
    assert result["param3"] == "new"


def test_load_config_from_env_without_override(tmp_path, monkeypatch):
    config_dir = tmp_path / "pipeline" / "config"
    config_dir.mkdir(parents=True)

    base_config = {"a": 1}
    (config_dir / "base.yaml").write_text(yaml.dump(base_config))

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APP_ENV", "nonexistent")

    result = load_config_from_env()
    assert result == base_config


def test_load_config_with_explicit_path(tmp_path):
    config_path = tmp_path / "manual.yaml"
    config_content = {"key": "value"}
    config_path.write_text(yaml.dump(config_content))

    loaded = load_config(str(config_path))
    assert loaded["key"] == "value"


def test_load_config_with_env(monkeypatch, tmp_path):
    config_dir = tmp_path / "pipeline" / "config"
    config_dir.mkdir(parents=True)
    (config_dir / "base.yaml").write_text(yaml.dump({"x": 1}))
    (config_dir / "prod.yaml").write_text(yaml.dump({"x": 2}))

    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APP_ENV", "prod")

    result = load_config()
    assert result["x"] == 2
