from pathlib import Path
from typing import List


def list_images(
    directory: Path, extensions: List[str] = [".jpg", ".png"]
) -> List[Path]:
    """
    List image files in a directory.

    Args:
        directory (Path): The directory to search.
        extensions (list): Allowed image file extensions.

    Returns:
        List of Path objects pointing to image files.
    """
    return sorted(
        [
            f
            for f in directory.iterdir()
            if f.suffix.lower() in extensions and f.is_file()
        ]
    )


def ensure_dir(path: Path) -> Path:
    """
    Ensure a directory exists, create if not.

    Args:
        path (Path): Directory path.

    Returns:
        Path object.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_parent_dir(path: Path) -> Path:
    """
    Ensure the parent directory of a file path exists.

    Args:
        path (Path): File path.

    Returns:
        The original path.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
