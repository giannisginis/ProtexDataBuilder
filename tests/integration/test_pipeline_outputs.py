from typer.testing import CliRunner
from pipeline.cli import app
from pathlib import Path
import json

runner = CliRunner()


def test_pipeline_outputs(tmp_path: Path, create_test_video):
    video_path = tmp_path / "sample.mp4"
    create_test_video(video_path, num_frames=5, width=64, height=64)

    frames_dir = tmp_path / "frames"
    coco_path = tmp_path / "annotations.coco.json"
    reports_dir = tmp_path / "reports"

    result = runner.invoke(
        app,
        [
            "--video",
            str(video_path),
            "--output",
            str(frames_dir),
            "--coco_output",
            str(coco_path),
            "--reports_output",
            str(reports_dir),
            "--pretag",
        ],
    )

    # Check it ran correctly
    assert result.exit_code == 0, (
        f"CLI failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}\n"
        f"exception: {result.exception}"
    )

    # Check frames exist
    frames = list(frames_dir.glob("*.jpg"))
    assert frames, "No frames generated in frames_output."

    # Check COCO file exists
    assert coco_path.exists(), "COCO output file not found."

    # Validate COCO JSON structure
    with open(coco_path) as f:
        data = json.load(f)
    assert "images" in data and isinstance(
        data["images"], list
    ), "Missing 'images' in COCO file."
    assert "annotations" in data and isinstance(
        data["annotations"], list
    ), "Missing 'annotations' in COCO file."
