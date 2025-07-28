import json
from pathlib import Path
from pipeline.core.detect.stats import compute_detection_stats


def test_compute_detection_stats(tmp_path: Path):
    # Create a dummy COCO JSON file
    coco_data = {
        "images": [
            {"id": 1, "file_name": "img1.jpg", "height": 100, "width": 100},
            {"id": 2, "file_name": "img2.jpg", "height": 100, "width": 100},
        ],
        "annotations": [
            {
                "id": 1,
                "image_id": 1,
                "category_id": 1,
                "bbox": [0, 0, 10, 10],
                "area": 100,
                "iscrowd": 0,
            },
            {
                "id": 2,
                "image_id": 1,
                "category_id": 1,
                "bbox": [0, 0, 20, 20],
                "area": 400,
                "iscrowd": 0,
            },
            {
                "id": 3,
                "image_id": 2,
                "category_id": 2,
                "bbox": [0, 0, 30, 30],
                "area": 900,
                "iscrowd": 0,
            },
        ],
        "categories": [
            {"id": 1, "name": "person"},
            {"id": 2, "name": "car"},
        ],
    }

    coco_path = tmp_path / "annotations.coco.json"
    with open(coco_path, "w") as f:
        json.dump(coco_data, f)

    stats = compute_detection_stats(coco_path)

    assert stats["image_count"] == 2
    assert stats["annotation_count"] == 3
    assert stats["class_distribution"] == {"person": 2, "car": 1}
