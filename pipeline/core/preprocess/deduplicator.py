import shutil
import logging
from pathlib import Path
from typing import List, Tuple, Any
from PIL import Image
import imagehash

from pipeline.utils.timing import timed_step


@timed_step("dedublication", flat=True)
def dedupe_frames(
    frames: List[Path],
    output_dir: Path,
    hash_size: int = 8,
    threshold: int = 5,
) -> Tuple[List[Any], Any]:
    """
    Deduplicate a list of image paths, copying unique ones to output_dir.

    Args:
        frames: List of image file paths to deduplicate.
        output_dir: Directory where unique frames will be saved.
        hash_size: Size of perceptual hash.
        threshold: Hamming distance threshold for duplicates.

    Returns:
        List of paths to the unique frames in output_dir.
    """
    logging.info(f"Starting deduplication on {len(frames)} frames")

    seen_hashes: List = []
    unique_paths: List = []
    dublicate_count: int = 0

    for img_file in sorted(frames):
        try:
            img = Image.open(img_file)
            phash = imagehash.phash(img, hash_size=hash_size)
        except Exception as e:
            logging.warning(f"Skipping {img_file.name}: cannot compute hash ({e})")
            continue

        is_duplicate = any(phash - h <= threshold for h in seen_hashes)

        if not is_duplicate:
            seen_hashes.append(phash)
            dest = output_dir / img_file.name
            if not dest.exists():
                shutil.copy2(img_file, dest)
            unique_paths.append(dest)
        else:
            logging.debug(f"Duplicate frame detected: {img_file.name}")
            dublicate_count += 1

    logging.info(f"Deduplication complete: {len(unique_paths)} unique frames")
    return unique_paths, dublicate_count
