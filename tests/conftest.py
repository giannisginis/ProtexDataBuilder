import pytest
import numpy as np
import cv2
from pathlib import Path
from typing import Callable, Any


@pytest.fixture
def create_test_images() -> Callable[[Path], Any]:
    """Create 2 duplicate and 1 blurry image."""

    def _create(tmp_path: Path):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.putText(
            img, "Test", (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3
        )
        blurred_img = cv2.GaussianBlur(img, (15, 15), 0)
        images = [img, img.copy(), blurred_img]
        paths = []
        for i, im in enumerate(images):
            path = tmp_path / f"img_{i+1}.jpg"
            cv2.imwrite(str(path), im)
            paths.append(path)
        return paths

    return _create


@pytest.fixture
def create_blurry_test_images(tmp_path: Path) -> Callable[[], Any]:
    """Creates one sharp and one blurry image."""

    def _create():
        clear_path = tmp_path / "clear.jpg"
        blurry_path = tmp_path / "blurry.jpg"

        # Sharp image (checkerboard pattern)
        sharp = np.zeros((100, 100), dtype=np.uint8)
        sharp[::2, ::2] = 255
        sharp[1::2, 1::2] = 255
        cv2.imwrite(str(clear_path), sharp)

        # Blurry image (Gaussian blur of sharp)
        blur = cv2.GaussianBlur(sharp, (11, 11), 0)
        cv2.imwrite(str(blurry_path), blur)

        return [clear_path, blurry_path]

    return _create


@pytest.fixture
def create_duplicate_test_images(tmp_path: Path) -> Callable[[], Any]:
    """Creates 2 identical and 1 different image."""

    def _create():
        img1 = np.full((100, 100, 3), 255, dtype=np.uint8)  # White
        img2 = img1.copy()  # Duplicate of img1
        img3 = np.full((100, 100, 3), 0, dtype=np.uint8)  # Black (unique)

        paths = []
        for i, img in enumerate([img1, img2, img3], start=1):
            path = tmp_path / f"img_{i}.jpg"
            cv2.imwrite(str(path), img)
            paths.append(path)

        return paths

    return _create


@pytest.fixture
def create_test_video() -> Callable[[Path, int, int, int], None]:
    """Create a dummy video file for testing."""

    def _create(
        video_path: Path, num_frames: int = 5, width: int = 320, height: int = 240
    ):
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(video_path), fourcc, 1.0, (width, height))

        for _ in range(num_frames):
            frame = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            out.write(frame)
        out.release()

    return _create
