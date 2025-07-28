from unittest.mock import MagicMock, patch
from pipeline.models.yolo import YOLOv8Runner


def test_yolov8runner_predict_mock(tmp_path):
    image_path = tmp_path / "test.jpg"
    image_path.write_text("fake-image-content")  # Placeholder content

    mock_result = MagicMock()
    mock_result.boxes.data.tolist.return_value = [
        [10, 20, 50, 60, 0.9, 0],  # x1, y1, x2, y2, conf, cls_id
    ]
    mock_result.orig_shape = (240, 320)

    with patch("pipeline.models.yolo.YOLO") as MockYOLO:
        mock_model_instance = MagicMock()
        mock_model_instance.names = {0: "person"}

        # model(image)[0] ⇒ mock_result
        mock_model_instance.return_value = [mock_result]
        MockYOLO.return_value = mock_model_instance

        runner = YOLOv8Runner("fake_model.pt")
        result = runner.predict(image_path)

        assert result.width == 320
        assert result.height == 240
        assert len(result.boxes) == 1
        assert result.boxes[0]["label"] == "person"
        assert result.boxes[0]["conf"] == 0.9


def test_class_names_property():
    with patch("pipeline.models.yolo.YOLO") as MockYOLO:
        mock_model = MockYOLO.return_value
        mock_model.names = {0: "person", 1: "car"}

        runner = YOLOv8Runner("fake-path.pt")
        assert runner.class_names == {0: "person", 1: "car"}
