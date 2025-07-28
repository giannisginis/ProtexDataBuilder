import json
from pathlib import Path
from pipeline.core.report.reporter import generate_report


def test_generate_report(tmp_path: Path):
    coco_data = {
        "images": [{"id": 1, "file_name": "img1.jpg", "height": 100, "width": 100}],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "bbox": [0, 0, 10, 10],
                "area": 100,
                "iscrowd": 0,
            }
        ],
        "categories": [{"id": 1, "name": "cat"}],
    }
    coco_path = tmp_path / "detections.coco.json"
    with coco_path.open("w") as f:
        json.dump(coco_data, f)

    report_path = tmp_path / "report.md"

    generate_report(
        video_path="tests/assets/sample.mp4",
        extracted_frame_count=10,
        total_frames=20,
        coco_path=coco_path,
        out_path=str(report_path),
        timings={"frame_extraction": 0.05, "preprocessing": 0.1},
        cleaned_frames=3,
        deduped_frames=2,
    )

    assert report_path.exists()
    content = report_path.read_text()
    assert "# Dataset Generation Report" in content
    assert "**Input Video:** `tests/assets/sample.mp4`" in content
    assert "**Total Video Frames:** 20" in content
    assert "**Frames Extracted:** 10" in content
    assert "**Frame Drop Ratio:** 50.00%" in content
    assert "**Blury Frames Removed:** 3" in content
    assert "**Dublicate Frames Removed:** 2" in content
    assert "**Images Tagged:** 1" in content
    assert "**Total Detections:** 1" in content
    assert "- cat: 1" in content
    assert "- frame_extraction: 0.05 sec" in content
    assert "- preprocessing: 0.10 sec" in content
