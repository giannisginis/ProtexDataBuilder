import cv2
from pathlib import Path
from pipeline.core.extract.extractor import extract_frames


def test_extract_frames(create_test_video, tmp_path: Path):
    video_path = tmp_path / "test_video.mp4"
    output_dir = tmp_path / "frames"
    create_test_video(video_path, num_frames=5)

    cap = cv2.VideoCapture(str(video_path))
    assert cap.isOpened()

    extracted_count, _ = extract_frames(cap, str(output_dir), skip_frequency=1)

    output_files = list(output_dir.glob("*.jpg"))
    assert extracted_count == 5
    assert len(output_files) == 5
    for f in output_files:
        assert f.suffix == ".jpg"
        assert f.exists()
