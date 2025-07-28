import shutil
import logging
from typing import List, Tuple
from pathlib import Path
import cv2
from pipeline.utils.timing import timed_step


def variance_of_laplacian(image):
    """Compute the Laplacian variance (blurriness metric)."""
    return cv2.Laplacian(image, cv2.CV_64F).var()


@timed_step("blur_detection", flat=True)
def clean_blurry_frames(
    frames: List[Path], output_dir: Path, threshold: float = 100.0
) -> Tuple[List[Path], int]:
    """
    Filter out blurry frames and copy non-blurry frames to output_dir.

    Args:
        frames: List of input image file paths.
        output_dir: Directory where non-blurry images will be saved.
        threshold: Laplacian variance threshold below which images are considered blurry.

    Returns:
        List of non-blurry image paths in output_dir.
    """
    logging.info(f"Starting Blur detection on {len(frames)} frames")

    cleaned = []
    blur_frames_count = 0

    for image_path in frames:
        img = cv2.imread(str(image_path))
        if img is None:
            logging.warning(f"Unreadable image: {image_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        var = variance_of_laplacian(gray)

        if var >= threshold:
            dest = output_dir / image_path.name
            shutil.copy2(image_path, dest)
            cleaned.append(dest)
        else:
            logging.info(f"Skipping blurry frame: {image_path.name} (score={var:.2f})")
            blur_frames_count += 1
    logging.info(f"Blur detection complete: {len(cleaned)} non-blurry frames saved")
    return cleaned, blur_frames_count
