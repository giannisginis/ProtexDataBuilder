from pathlib import Path
import typer
from pipeline.core.preprocess.blur_detector import clean_blurry_frames
from pipeline.core.preprocess.deduplicator import dedupe_frames
from pipeline.utils.paths import ensure_dir


class VideoPreprocessor:
    def __init__(
        self,
        enable_blur_detection: bool = True,
        enable_deduplication: bool = True,
        blur_threshold: float = 100.0,
        dedub_threshold: int = 5,
        hash_size: int = 16,
    ):
        self.enable_blur_detection = enable_blur_detection
        self.enable_deduplication = enable_deduplication
        self.blur_threshold = blur_threshold
        self.dedub_threshold = dedub_threshold
        self.hash_size = hash_size

        self.cleaned_count = 0
        self.deduped_count = 0
        self.blur_timing = {"blur_detection": 0.0}
        self.dedup_timing = {"dedup_removal": 0.0}

    @property
    def cleaned(self) -> int:
        return self.cleaned_count

    @property
    def deduped(self) -> int:
        return self.deduped_count

    @property
    def blur_detection_timing(self) -> dict:
        return self.blur_timing

    @property
    def dedup_removal_timing(self) -> dict:
        return self.dedup_timing

    def run(self, input_dir: Path, output_dir: Path) -> Path:
        """
        Applies preprocessing steps on extracted frames:
        - Blur removal
        - Deduplication

        Args:
            input_dir (Path): Directory containing extracted frames.
            output_dir (Path): Final directory to save cleaned/deduplicated frames.

        Returns:
            Path to the final directory with preprocessed frames.
        """
        # If no preprocessing is enabled, return original frames
        if not self.enable_blur_detection and not self.enable_deduplication:
            return input_dir

        frames = sorted(input_dir.glob("*.jpg"))

        if self.enable_blur_detection:
            typer.secho("🔍 Removing blurry frames...", fg=typer.colors.BRIGHT_CYAN)
            output_dir_tmp = ensure_dir(output_dir / "cleaned_frames")
            frames, blur_frames_count, blur_timing = clean_blurry_frames(
                frames, output_dir_tmp, threshold=self.blur_threshold
            )
            self.blur_timing = blur_timing
            self.cleaned_count = blur_frames_count
            input_dir = output_dir_tmp

        if self.enable_deduplication:
            typer.secho("🔁 Deduplicating frames...", fg=typer.colors.BRIGHT_CYAN)
            output_dir_tmp = ensure_dir(output_dir / "deduplicated_frames")
            frames, dublicate_count, dedub_timing = dedupe_frames(
                frames,
                output_dir_tmp,
                hash_size=self.hash_size,
                threshold=self.dedub_threshold,
            )
            self.dedup_timing = dedub_timing
            self.deduped_count = dublicate_count
            input_dir = output_dir_tmp

        return input_dir
