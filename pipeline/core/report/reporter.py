import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional
from pipeline.core.report.comet_logger import CometLogger


def generate_report(
    video_path: str,
    extracted_frame_count: int,
    total_frames: int,
    coco_path: Path,
    comet_logger: Optional[CometLogger] = None,
    out_path: str = "report.md",
    timings: Optional[Dict] = None,
    cleaned_frames: Optional[int] = None,
    deduped_frames: Optional[int] = None,
):
    """
    Generate a Markdown report of dataset generation metrics.

    Args:
        video_path: Original input video.
        extracted_frame_count: Number of frames extracted.
        total_frames: Total frames in video (from metadata).
        coco_path: Path to COCO detection output.
        out_path: File to write the report.
        timings: Optional dict of step durations (in seconds).
    """
    report_lines = []
    report_lines.append("# Dataset Generation Report\n")
    report_lines.append(f"**Input Video:** `{video_path}`")
    report_lines.append(f"**Total Video Frames:** {total_frames}")
    report_lines.append(f"**Frames Extracted:** {extracted_frame_count}")
    report_lines.append(
        f"**Frame Drop Ratio:** {1 - extracted_frame_count / total_frames:.2%}\n"
    )
    report_lines.append(f"**Blury Frames Removed:** {cleaned_frames}")
    report_lines.append(f"**Dublicate Frames Removed:** {deduped_frames}")

    # Parse COCO detections
    if Path(coco_path).exists():
        with open(coco_path) as f:
            data = json.load(f)
        image_count = len(data.get("images", []))
        annotation_count = len(data.get("annotations", []))
        categories: Dict = defaultdict(int)
        for ann in data.get("annotations", []):
            cat_id = ann["category_id"]
            categories[cat_id] += 1
        category_map = {cat["id"]: cat["name"] for cat in data.get("categories", [])}

        report_lines.append(f"**Images Tagged:** {image_count}")
        report_lines.append(f"**Total Detections:** {annotation_count}\n")
        report_lines.append("## Class Distribution:")
        for cid, count in categories.items():
            label = category_map.get(cid, f"class_{cid}")
            report_lines.append(f"- {label}: {count}")
    else:
        report_lines.append(f"COCO detection file not found: `{coco_path}`")

    # Time breakdown
    if timings:
        report_lines.append("\n## Time Breakdown:")
        for step, duration in timings.items():
            report_lines.append(f"- {step}: {duration:.2f} sec")

    # Save report
    Path(out_path).write_text("\n".join(report_lines))

    # Log to Comet if available
    if comet_logger:
        comet_logger.log_assets(
            {
                "pipeline_summary.md": out_path,
            }
        )
