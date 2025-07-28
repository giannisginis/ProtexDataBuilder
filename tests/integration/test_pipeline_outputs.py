import subprocess
import json
from pathlib import Path


def test_pipeline_outputs(tmp_path: Path):
    # Paths
    video_path = "tests/assets/sample.mp4"
    frames_dir = tmp_path / "frames"
    coco_path = tmp_path / "annotations.coco.json"

    # Run CLI pipeline
    result = subprocess.run(
        [
            "poetry",
            "run",
            "python",
            "-m",
            "pipeline.cli",
            "--video",
            video_path,
            "--output",
            str(frames_dir),
            "--coco_output",
            str(coco_path),
            "--reports_output",
            "reports",
            "--pretag",
        ],
        capture_output=True,
        text=True,
    )

    # Ensure pipeline ran successfully
    assert result.returncode == 0, f"Pipeline failed:\n{result.stderr}"

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
