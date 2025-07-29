# 📦 Protex DataBuilder

**Protex DataBuilder** is a modular, containerized dataset generation pipeline that converts timelapse videos into clean, annotated image datasets using computer vision and MLOps best practices. It supports reproducible frame extraction, preprocessing (blur and deduplication), YOLOv8-based pre-tagging, and Markdown reporting.

## 🚀 Features

- 🎥 Extract frames from input timelapse videos
- 🧹 Clean frames by removing blurry or duplicate images
- 🏷️ Pre-tag images using YOLOv8 object detection
- 📊 Generate COCO-format annotations
- 📝 Produce dataset statistics and Markdown reports
- 🐳 Dockerized CLI interface via [Typer](https://typer.tiangolo.com/)
- ✅ CI-verified with linting and test coverage checks
- 📈 Metrics logging with [Comet-ML](https://www.comet.com/)
- ☁️ Terraform modules for deploying ECR, EC2, and Batch jobs on AWS

## 📚 Full Usage Guide

For detailed instructions on running the pipeline locally, via Docker, or with Comet-ML tracking, see:

👉 [USAGE.md](docs/USAGE.md)

## 📁 Project Structure

```
├── pipeline/             # Core modules
│   ├── config/           # Custom model config YAML files
│   ├── core/             # Stages: extract, preprocess, detect, report
│   ├── models/           # Detection wrappers (YOLOv8)
│   ├── utils/            # Config, helpers, paths
│   ├── validation/       # Video input checks
│   └── cli.py            # Typer CLI entrypoint
│   └── constants.py      # Codebase constants
├── tests/                # Unit & integration tests
├── Dockerfile
├── Makefile
├── .github/workflows/   # GitHub Actions CI
└── infra/aws            # Terraform AWS Handling
```
