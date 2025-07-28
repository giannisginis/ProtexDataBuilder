from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, List, Dict


class DetectionResult:
    def __init__(self, boxes: List[Dict[str, Any]], width: int, height: int):
        self.boxes = boxes  # List of dicts with x1, y1, x2, y2, conf, label
        self.width = width
        self.height = height


class BaseModelRunner(ABC):
    @abstractmethod
    def predict(self, image_path: Path) -> DetectionResult:
        """Run inference and return parsed results."""
        pass

    @property
    @abstractmethod
    def class_names(self) -> Dict[int, str]:
        """Mapping of class ID to name."""
        pass
