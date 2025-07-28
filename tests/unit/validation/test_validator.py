import pytest
from pipeline.validation.validator import validate_video, ValidationError


def test_validate_video_success(create_test_video, tmp_path):
    video_file = tmp_path / "valid_video.mp4"
    create_test_video(video_file, num_frames=5)

    cap, metadata = validate_video(str(video_file))

    assert cap.isOpened()
    assert metadata["frame_count"] > 0
    assert metadata["fps"] > 0
    cap.release()


def test_validate_video_file_not_found(tmp_path):
    fake_path = tmp_path / "missing.mp4"
    with pytest.raises(ValidationError, match="does not exist"):
        validate_video(str(fake_path))


def test_validate_video_unsupported_extension(tmp_path):
    fake_txt = tmp_path / "video.txt"
    fake_txt.write_text("not a video")

    with pytest.raises(ValidationError, match="Unsupported video extension"):
        validate_video(str(fake_txt))


def test_validate_video_corrupt_file(tmp_path):
    corrupt_file = tmp_path / "corrupt.mp4"
    corrupt_file.write_text("garbage")

    with pytest.raises(ValidationError, match="Cannot open video file"):
        validate_video(str(corrupt_file))
