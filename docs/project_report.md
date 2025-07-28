## Cloud-Readiness Evaluation

This pipeline was designed with cloud deployment across multiple client sites in mind. Here's how it aligns with key requirements:

### ✅ Reliability

- All components are modular and tested in isolation (frame extraction, deduplication, detection).
- Logging and validation are included at every stage (e.g., unreadable frames, blur detection).
- Dockerized for reproducibility and consistent behavior across environments.

### ✅ Modularity

- Each stage is implemented as a standalone module and callable via a unified CLI.
- Configuration is handled via YAML, allowing dynamic control over detection models and thresholds.
- The `Preprocessor` class encapsulates cleaning and deduplication logic, enabling future extension.

### ✅ Cost Awareness

- Blurry and duplicate frames are filtered early to reduce unnecessary inference.
- Frame skipping is configurable via `--skip`, saving both compute and storage.
- Time metrics for each stage are logged and reported, allowing cost/performance tradeoffs.

This design enables efficient scaling of dataset generation jobs across multiple sites while keeping costs and operational risks under control.
