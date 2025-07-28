import os
import logging
import cv2

from pipeline.constants import VALID_EXTENSIONS


class ValidationError(Exception):
    pass


def validate_video(video_path: str) -> tuple[cv2.VideoCapture, dict]:
    """
    Validate that the video file exists, has a supported extension,
    and can be opened by OpenCV with valid properties.

    Args:
        video_path: Path to the video file to validate.

    Returns:
        tuple: (cv2.VideoCapture object, metadata dictionary)

    Raises:
        ValidationError: If any validation step fails.
    """
    logging.info(f"Validating video input: {video_path}")

    if not os.path.exists(video_path):
        raise ValidationError(f"Video file does not exist: {video_path}")

    _, ext = os.path.splitext(video_path)
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(
            f"Unsupported video extension '{ext}'. Supported: {', '.join(VALID_EXTENSIONS)}"
        )

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValidationError(
            f"Cannot open video file (corrupted or unsupported): {video_path}"
        )

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if frame_count <= 0 or fps <= 0:
        cap.release()
        raise ValidationError(
            f"Invalid video properties: frame_count={frame_count}, fps={fps}"
        )

    metadata = {
        "frame_count": frame_count,
        "fps": fps,
        "width": width,
        "height": height,
    }
    logging.info(f"Video metadata: {metadata}")
    return cap, metadata
