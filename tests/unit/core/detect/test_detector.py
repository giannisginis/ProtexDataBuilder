import json
import numpy as np
import cv2
from pathlib import Path
from pipeline.core.detect.detector import run_detection_to_coco
from pipeline.models.base import DetectionResult


class MockModel:
    def predict(self, image_path: Path) -> DetectionResult:
        return DetectionResult(
            boxes=[
                {
                    "x1": 10,
                    "y1": 20,
                    "x2": 50,
                    "y2": 80,
                    "conf": 0.9,
                    "label": "person",
                    "class_id": "person",
                }
            ],
            width=100,
            height=200,
        )


def create_dummy_images(dir: Path, count: int = 2):
    for i in range(count):
        img = np.zeros((200, 100, 3), dtype=np.uint8)
        cv2.imwrite(str(dir / f"img_{i+1}.jpg"), img)


def test_run_detection_to_coco(tmp_path: Path):
    image_dir = tmp_path / "images"
    output_path = tmp_path / "annotations.coco.json"
    image_dir.mkdir()

    create_dummy_images(image_dir)

    model = MockModel()
    image_count, ann_count, func_exc_time = run_detection_to_coco(
        model, image_dir, str(output_path)
    )

    assert image_count == 2
    assert ann_count == 2
    assert output_path.exists()

    with open(output_path) as f:
        data = json.load(f)

    assert "images" in data
    assert "annotations" in data
    assert "categories" in data
    assert len(data["images"]) == 2
    assert len(data["annotations"]) == 2
    assert data["categories"][0]["name"] == "person"
