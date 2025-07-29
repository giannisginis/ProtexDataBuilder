## Protex DataBuilder — Pipeline Report

## 🧩 Pipeline Summary

This pipeline processes timelapse videos into high-quality, pre-tagged image datasets suitable for training computer vision models. The CLI tool performs the following steps:

- **Validation:** Checks video integrity and metadata.
- **Frame Extraction:** Extracts frames at user-defined intervals.
- **Preprocessing:**

  - Blur detection using Laplacian variance.
  - Deduplication using perceptual hashing.

- **Detection (Optional):** Uses YOLOv8 to tag objects in frames.
- **Annotation:** Generates COCO-format JSON with image metadata and bounding boxes.
- **Reporting:** Produces a Markdown summary with stats and timing breakdowns.
- **Metrics:** Logs observability metrics (frame counts, detection stats, timing) to Comet-ML.

## 📊 Dataset Statistics & Observability Metrics

- **Input video:** `data/videos/timelapse_test.mp4`
- **Total frames in video:** 4077
- **Frames extracted:** 4077
- **Frame drop ratio:** 0.00%
- **Blurry frames removed:** 0
- **Duplicate frames removed:** 3793
- **Final images pre-tagged:** 284
- **Total detections:** 122

### Class Distribution:

| Class      | Count |
| ---------- | ----- |
| car        | 80    |
| bus        | 10    |
| truck      | 10    |
| person     | 9     |
| tv         | 5     |
| boat       | 3     |
| laptop     | 2     |
| train      | 2     |
| cell phone | 1     |

### Time Breakdown:

| Stage            | Time (sec) |
| ---------------- | ---------- |
| Frame extraction | 14.20      |
| Blur detection   | 22.61      |
| Deduplication    | 15.22      |
| YOLOv8 detection | 15.33      |

## 🚀 Improvements for Production

📁 See [Production Readiness Plan](./PRODUCTION_SPEC.md) for infrastructure and scaling strategy.
