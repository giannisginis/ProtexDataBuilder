from pathlib import Path
from ultralytics import YOLO

from pipeline.models.base import BaseModelRunner, DetectionResult


class YOLOv8Runner(BaseModelRunner):
    def __init__(self, model_path: str = "yolov8n.pt"):
        self.model = YOLO(model_path)

    def predict(self, image_path: Path, verbose: bool = False) -> DetectionResult:
        result = self.model(str(image_path), verbose=verbose)[0]
        boxes = []
        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls_id = box
            boxes.append(
                {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "conf": conf,
                    "label": self.model.names[int(cls_id)],
                    "class_id": int(cls_id),
                }
            )

        return DetectionResult(
            boxes=boxes, width=result.orig_shape[1], height=result.orig_shape[0]
        )

    @property
    def class_names(self):
        return self.model.names
