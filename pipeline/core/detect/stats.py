import json
from collections import defaultdict
from pathlib import Path
from typing import Dict


def compute_detection_stats(coco_path: Path) -> Dict:
    """
    Compute detection statistics from a COCO-format annotations file.

    Args:
        coco_path (Path): Path to the COCO JSON file.

    Returns:
        A dictionary containing:
            - image_count
            - annotation_count
            - class_distribution: Dict[label, count]
    """
    if not coco_path.exists():
        raise FileNotFoundError(f"COCO file not found at {coco_path}")

    with coco_path.open("r") as f:
        data = json.load(f)

    image_count = len(data.get("images", []))
    annotation_count = len(data.get("annotations", []))

    category_map = {cat["id"]: cat["name"] for cat in data.get("categories", [])}
    class_distribution: Dict = defaultdict(int)

    for ann in data.get("annotations", []):
        cat_id = ann["category_id"]
        label = category_map.get(cat_id, f"class_{cat_id}")
        class_distribution[label] += 1

    return {
        "image_count": image_count,
        "annotation_count": annotation_count,
        "class_distribution": dict(class_distribution),
    }


def print_stats_summary(stats: Dict):
    """
    Pretty print stats returned by `compute_detection_stats`.

    Args:
        stats (dict): Dictionary returned by compute_detection_stats.
    """
    print("📊 Detection Summary")
    print(f"- Images Tagged: {stats['image_count']}")
    print(f"- Total Detections: {stats['annotation_count']}")
    print("- Class Distribution:")
    for label, count in stats["class_distribution"].items():
        print(f"  - {label}: {count}")
