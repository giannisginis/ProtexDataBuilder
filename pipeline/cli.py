import typer
import logging
from pathlib import Path

from pipeline.validation.validator import validate_video, ValidationError
from pipeline.core.extract.extractor import extract_frames
from pipeline.core.detect.detector import run_detection_to_coco
from pipeline.core.report.reporter import generate_report
from pipeline.core.preprocess.runner import VideoPreprocessor as Preprocessor
from pipeline.models.yolo import YOLOv8Runner
from pipeline.utils.helpers import load_config
from pipeline.utils.paths import ensure_dir
from pipeline.utils.paths import ensure_parent_dir

app = typer.Typer(help="MLOps Dataset Generation CLI")


@app.command()
def run(
    video: str = typer.Option(..., "--video", "-v", help="Path to input video file."),
    output_dir: str = typer.Option(
        ..., "--output", "-o", help="Output directory for extracted frames."
    ),
    coco_output: str = typer.Option(
        ...,
        "--coco_output",
        "-co",
        help="Path to save COCO-format annotation file.",
    ),
    pretag: bool = typer.Option(
        False, help="Run YOLOv8 pre-tagging and save COCO output."
    ),
    skip: int = typer.Option(1, help="Save every nth frame."),
    blur_detection: bool = typer.Option(
        False, help="Remove blurry frames before deduplication."
    ),
    clean_threshold: float = typer.Option(
        100.0, help="Blurriness threshold for frame cleaning."
    ),
    dedup_detection: bool = typer.Option(False, help="Remove duplicate frames."),
    hash_size: int = typer.Option(8, help="Hash size for deduplication."),
    dedub_threshold: int = typer.Option(
        5, help="Hamming distance threshold for duplicates."
    ),
    report_dir: str = typer.Option(
        ..., "--reports_output", "-ro", help="Path to save Markdown report."
    ),
    config: str = typer.Option(None, help="Path to detection model config YAML file."),
    env: str = typer.Option("dev", help="Environment to use (dev/test/prod)"),
):
    """
    Run full pipeline: validate → extract → clean/dedup → detect → report.
    """
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s", level=logging.INFO
    )
    output_dir_path = ensure_dir(Path(output_dir))

    preprocessed_dir = output_dir_path / "proprocessed_frames"
    preprocessed_dir = ensure_dir(Path(preprocessed_dir))
    coco_output_path = ensure_parent_dir(Path(coco_output))
    report_path = ensure_dir(Path(report_dir))

    try:
        cap, metadata = validate_video(video)
    except ValidationError as e:
        typer.secho(f"Validation failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.echo("Video validated successfully.")
    for k, v in metadata.items():
        typer.echo(f"{k}: {v}")

    timings = {}

    # Frame extraction
    typer.secho("\nExtracting frames...", fg=typer.colors.BRIGHT_CYAN)
    extracted_count, extraction_time = extract_frames(cap, output_dir_path, skip)
    cap.release()
    typer.secho(
        f"Saved {extracted_count} frames to {output_dir_path}", fg=typer.colors.GREEN
    )
    timings.update(extraction_time)

    # Preprocessing
    pre = Preprocessor(
        enable_blur_detection=blur_detection,
        enable_deduplication=dedup_detection,
        blur_threshold=clean_threshold,
        dedub_threshold=dedub_threshold,
        hash_size=hash_size,
    )
    tag_input_dir = pre.run(input_dir=output_dir_path, output_dir=preprocessed_dir)
    timings.update(pre.blur_detection_timing)
    timings.update(pre.dedup_removal_timing)
    typer.secho(
        f"Preprocessing complete: {pre.cleaned} blurry frames removed, "
        f"{pre.deduped} duplicate frames removed.",
        fg=typer.colors.GREEN,
    )
    # Load config
    if config:
        typer.secho(
            f"Loading config from file: {config} (overrides environment '{env}')"
        )
    else:
        typer.secho(
            f"No config file provided. Using environment: '{env}' (from config/{env}.yaml)",
            fg=typer.colors.BRIGHT_YELLOW,
        )

    cfg = load_config(config_path=config, env=env)
    model_path = cfg.get("model", {}).get("path", "yolov8n.pt")
    conf_threshold = cfg.get("model", {}).get("confidence_threshold", 0.25)

    # Pre-tagging (optional)
    if pretag:
        typer.secho("\nRunning YOLOv8 pre-tagging...", fg=typer.colors.BRIGHT_CYAN)
        model = YOLOv8Runner(model_path)
        img_count, ann_count, detection_time = run_detection_to_coco(
            model, tag_input_dir, coco_output_path, conf_threshold
        )
        timings.update(detection_time)
        typer.secho(
            f"Tagged {img_count} images with {ann_count} annotations → {coco_output_path}",
            fg=typer.colors.GREEN,
        )

    # Generate report
    typer.secho("\nGenerating report...", fg=typer.colors.BRIGHT_CYAN)
    generate_report(
        video_path=video,
        extracted_frame_count=extracted_count,
        total_frames=metadata["frame_count"],
        coco_path=coco_output_path,
        out_path=f"{report_path}/report_sample.md",
        timings=timings,
        cleaned_frames=pre.cleaned,
        deduped_frames=pre.deduped,
    )
    typer.secho(f"✅ Report saved to {report_path}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
