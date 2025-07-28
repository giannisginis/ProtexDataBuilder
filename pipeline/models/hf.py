from pathlib import Path
from typing import List, Dict, Any
from pipeline.models.base import BaseModelRunner, DetectionResult


class HuggingFaceRunner(BaseModelRunner):
    """
    Model runner using a HuggingFace object detection pipeline.
    Defaults to DETR (facebook/detr-resnet-50).
    """

    _coco_classes = [
        "__background__",
        "person",
        "bicycle",
        "car",
        "motorcycle",
        "airplane",
        "bus",
        "train",
        "truck",
        "boat",
        "traffic light",
        "fire hydrant",
        "stop sign",
        "parking meter",
        "bench",
        "bird",
        "cat",
        "dog",
        "horse",
        "sheep",
        "cow",
        "elephant",
        "bear",
        "zebra",
        "giraffe",
        "backpack",
        "umbrella",
        "handbag",
        "tie",
        "suitcase",
        "frisbee",
        "skis",
        "snowboard",
        "sports ball",
        "kite",
        "baseball bat",
        "baseball glove",
        "skateboard",
        "surfboard",
        "tennis racket",
        "bottle",
        "wine glass",
        "cup",
        "fork",
        "knife",
        "spoon",
        "bowl",
        "banana",
        "apple",
        "sandwich",
        "orange",
        "broccoli",
        "carrot",
        "hot dog",
        "pizza",
        "donut",
        "cake",
        "chair",
        "couch",
        "potted plant",
        "bed",
        "dining table",
        "toilet",
        "tv",
        "laptop",
        "mouse",
        "remote",
        "keyboard",
        "cell phone",
        "microwave",
        "oven",
        "toaster",
        "sink",
        "refrigerator",
        "book",
        "clock",
        "vase",
        "scissors",
        "teddy bear",
        "hair drier",
        "toothbrush",
    ]

    def __init__(self, model_name: str = "facebook/detr-resnet-50") -> None:
        """
        Initialize the HuggingFace detection pipeline.

        Args:
            model_name: HuggingFace model identifier for object detection.
        """
        from transformers import pipeline

        try:
            self.detector = pipeline("object-detection", model=model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load HuggingFace model: {e}") from e

    def predict(self, image_path: Path) -> DetectionResult:
        """
        Run object detection on an image and return DetectionResult.

        Args:
            image_path: Path to the input image.

        Returns:
            DetectionResult: structured result with bounding boxes, class names, and image size.
        """
        from PIL import Image, UnidentifiedImageError

        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        try:
            img = Image.open(image_path)
        except UnidentifiedImageError as e:
            raise ValueError(f"Unable to open image: {image_path}") from e

        try:
            results = self.detector(str(image_path))
        except Exception as e:
            raise RuntimeError(f"Model prediction failed on {image_path}") from e

        boxes: List[Dict[str, Any]] = []

        for r in results:
            box = r["box"]
            x1 = box["xmin"]
            y1 = box["ymin"]
            x2 = box["xmax"]
            y2 = box["ymax"]
            boxes.append(
                {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "conf": r["score"],
                    "label": r["label"],
                    "class_id": r["label"],  # Consider mapping label to ID
                }
            )

        return DetectionResult(boxes, width=img.width, height=img.height)

    @property
    def class_names(self) -> Dict[int, str]:
        """
        Return COCO class index → name mapping.

        Returns:
            Dictionary of class indices to labels.
        """
        return {i: name for i, name in enumerate(self._coco_classes)}
