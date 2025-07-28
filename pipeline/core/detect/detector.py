import json
import logging
from typing import Tuple, Dict
from pathlib import Path
from tqdm import tqdm
from pipeline.models.base import BaseModelRunner
from pipeline.utils.timing import timed_step


@timed_step("run_detection_to_coco", flat=True)
def run_detection_to_coco(
    model: BaseModelRunner,
    image_dir: Path,
    output_path: str,
    conf_threshold: float = 0.25,
) -> Tuple[int, int]:
    """
    Run YOLO pre-tagging on images and output COCO-format JSON.

    Args:
        model: YOLO model.
        image_dir: Path to image directory.
        output_path: Path to write COCO-format JSON.
        conf_threshold: Confidence threshold.

    Returns:
        Tuple of (image count, annotation count).
    """
    image_files = sorted([f for f in image_dir.glob("*.jpg")])

    coco_output: Dict = {"images": [], "annotations": [], "categories": []}
    category_map = {}
    next_image_id = 1
    next_ann_id = 1
    next_category_id = 1

    for image_file in tqdm(image_files, desc="Pretagging"):
        result = model.predict(image_file)

        coco_output["images"].append(
            {
                "id": next_image_id,
                "file_name": image_file.name,
                "height": result.height,
                "width": result.width,
            }
        )

        for box in result.boxes:
            if box["conf"] < conf_threshold:
                continue

            label = box["label"]

            if label not in category_map:
                category_map[label] = next_category_id
                coco_output["categories"].append(
                    {"id": next_category_id, "name": label}
                )
                next_category_id += 1

            coco_output["annotations"].append(
                {
                    "id": next_ann_id,
                    "image_id": next_image_id,
                    "category_id": category_map[label],
                    "bbox": [
                        box["x1"],
                        box["y1"],
                        box["x2"] - box["x1"],
                        box["y2"] - box["y1"],
                    ],
                    "area": (box["x2"] - box["x1"]) * (box["y2"] - box["y1"]),
                    "iscrowd": 0,
                }
            )
            next_ann_id += 1

        next_image_id += 1

    with open(output_path, "w") as f:
        json.dump(coco_output, f, indent=2)

    logging.info(f"Saved COCO annotations to {output_path}")
    return next_image_id - 1, next_ann_id - 1
