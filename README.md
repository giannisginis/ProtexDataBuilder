# Protex AI: CV Dataset Generation Pipeline

This repository contains a containerized, reproducible, and observable pipeline to generate pre-tagged image datasets from timelapse video. It includes optional enhancements for frame deduplication, input validation, IaC, and off-the-shelf object detection.

## Features

- **Containerized** with Docker: accepts `--video`, `--output-dir`, and `--config` inputs.
- **CI/CD** via GitHub Actions: automatic build, tests, and end-to-end pipeline validation.
- **Observability**: logs metrics (# images, detections/frame, frame-drop ratio) and auto-generates a report.
- **Optional Enhancements**:
  - Frame deduplication (perceptual hashing)
  - Video input validation
  - Terraform scripts to provision minimal cloud infra
  - Off-the-shelf object detection (YOLOv8 via Hugging Face)

## Getting Started

### Prerequisites

- Docker
- Make
- (Optional) Terraform & AWS CLI

### Build & Run

```bash
# Build the Docker image
make build
# Run on a sample video
docker run --rm -t\
		-v $(PWD)/data/videos:/videos \
		-v $(PWD)/outputs:/outputs \
		-v $(PWD)/reports:/reports \
		dataset-pipeline \
		--video /videos/sample.mp4 \
		--output /outputs/frames \
		--coco_output /outputs/detections/detections.coco.json \
		--pretag \
		--blur-detection \
  		--dedup-detection
```
