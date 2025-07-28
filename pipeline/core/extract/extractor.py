import os
import logging
from datetime import datetime
import cv2
from pipeline.utils.timing import timed_step


@timed_step("frame_extraction", flat=True)
def extract_frames(
    cap: cv2.VideoCapture, output_dir: str, skip_frequency: int = 1
) -> int:
    """
    Extract frames from the given open VideoCapture and save as JPEG images.

    Args:
        cap: OpenCV VideoCapture instance (already opened).
        output_dir: Directory where extracted frames will be saved.
        skip_frequency: Save every nth frame. Default is 1 (every frame).

    Returns:
        total_frames_saved: Number of frames written.
    """
    logging.info("Starting frame extraction")
    os.makedirs(output_dir, exist_ok=True)

    frame_idx = 0
    saved_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_idx % skip_frequency == 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"frame_{frame_idx:06d}_{timestamp}.jpg"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, frame)
            saved_count += 1
        frame_idx += 1

    logging.info(f"Extracted {saved_count} frames to {output_dir}")
    return saved_count
