## 🚀 Production Readiness Plan for Protex DataBuilder Pipeline

This document outlines improvements and infrastructure design recommendations to make the video-to-dataset generation pipeline production-ready, scalable, and observable.

### 🔄 Cloud Scalability & Cost Optimization

- **AWS Batch for scalable job processing:**
  Configure AWS Batch with managed compute environments to run multiple pipeline jobs in parallel. Use EC2 Spot Instances to minimize costs for long-running batch workloads.

- **S3-based input/output storage:**
  Store incoming timelapse videos in S3. Output directories for extracted frames, COCO annotations, and reports should also be saved in S3 to ensure durability, availability, and interoperability with downstream systems.

- **Pipeline containerization via AWS ECR:**
  Build and version the pipeline as a Docker container on AWS Elastic Container Registry (ECR). This enables reproducible, version-controlled job execution.

### 🧩 Event-Driven Automation

- **Trigger on upload using S3 + EventBridge:**
  Use S3 event notifications to publish events when new videos are uploaded. Connect to EventBridge to route events to Lambda or Step Functions, which submit jobs to AWS Batch.

- **Monitoring via CloudWatch Events and Logs:**
  Track job lifecycle events and log outputs in CloudWatch to allow real-time failure alerts and dashboard visualization.

### 📊 Observability & Experiment Tracking

- **Optional Prometheus + Grafana integration:**
  Expose metrics such as processing duration, failed jobs, or average detection count using Prometheus exporters. Visualize trends over time in Grafana.

- **Structured logging:**
  Replace plain-text logs with structured JSON logging using `structlog` or `loguru`. This enables better parsing and filtering when sending logs to Datadog, CloudWatch Logs Insights, or ELK stacks.

### 🧠 Smart Model & Config Management

- **Model versioning support:**
  Introduce a `--model-version` CLI flag to dynamically pull YOLO model files from Hugging Face, MLflow, or an internal registry.

- **Secure configuration with AWS SSM/Secrets Manager:**
  Move sensitive configs (e.g., thresholds, API keys) to secure AWS services. Fetch them at runtime based on environment (`dev`, `staging`, `prod`).

### 🛡️ Reliability & CI/CD

- **CI/CD enhancements:**

  - Build Docker images on merge and push to ECR.
  - Run multiple video scenarios in CI: Include short videos, non-standard resolutions, and corrupted inputs to ensure robust error handling and compatibility.
  - Detect dependency drift: Use a bot or scheduled CI job to check for outdated Poetry dependencies. Automatically open pull requests for major or minor bumps with changelogs and assign them to engineers for review and testing.

- **Runtime validation and retries:**
  Use retry logic for transient failures (e.g., model timeouts, S3 write failures).

Great idea! Proposing improvements to the CLI structure shows maturity in both usability and maintainability. Here's what we can mention under **CLI Enhancements** or as part of the **Production Improvements** section of your report:

### 🧵 CLI Modularization & Packaging (Proposed Improvement)

- **Make pipeline stages into subcommands as well:**
  Break down the `run` command into separate Typer subcommands:

  ```bash
  pipeline validate --video input.mp4
  pipeline extract --video input.mp4 --output frames/
  pipeline preprocess --input frames/ --output clean_frames/
  pipeline detect --input clean_frames/ --output detections.coco.json
  pipeline report --coco detections.coco.json --output report.md
  ```

  This enables users to debug or run individual stages independently and improves maintainability.

- **Convert CLI into an installable Python package:**
  Package the CLI (`pipeline.cli`) as a PyPI-distributable tool (`protex-pipeline`) so it can be installed via:

  ```bash
  pip install protex-pipeline
  protex-pipeline run --video ...
  ```

- **Interactive or dry-run mode:**
  Add a `--dry-run` or `--interactive` flag to preview what the CLI will do without executing the steps (e.g., showing file counts, previewing model config).
