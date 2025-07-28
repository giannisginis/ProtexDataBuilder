from unittest.mock import patch, MagicMock
from pipeline.models.hf import HuggingFaceRunner
from pipeline.models.base import DetectionResult


@patch("pipeline.models.hf.pipeline")
@patch("PIL.Image.open")
def test_huggingface_runner_predict(mock_open, mock_pipeline, tmp_path):
    image_path = tmp_path / "test.jpg"
    image_path.write_text("fake")  # dummy file to pass existence check

    mock_img = MagicMock()
    mock_img.width = 640
    mock_img.height = 480
    mock_open.return_value = mock_img

    mock_prediction = [
        {
            "box": {"xmin": 10, "ymin": 20, "xmax": 110, "ymax": 120},
            "score": 0.9,
            "label": "dog",
        }
    ]
    mock_detector = MagicMock(return_value=mock_prediction)
    mock_pipeline.return_value = mock_detector

    runner = HuggingFaceRunner("mock-model")
    result = runner.predict(image_path)

    assert isinstance(result, DetectionResult)
    assert result.width == 640
    assert result.height == 480
    assert len(result.boxes) == 1
    assert result.boxes[0]["label"] == "dog"
    assert result.boxes[0]["x1"] == 10
