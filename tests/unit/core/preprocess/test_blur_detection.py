from pipeline.core.preprocess.blur_detector import clean_blurry_frames


def test_clean_blurry_frames(create_blurry_test_images, tmp_path):
    input_images = create_blurry_test_images()
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    cleaned, blurred_count, _ = clean_blurry_frames(
        input_images, output_dir, threshold=50.0
    )

    assert len(cleaned) == 1
    assert cleaned[0].name == "clear.jpg"
    assert blurred_count == 1
    assert (output_dir / "clear.jpg").exists()
    assert not (output_dir / "blurry.jpg").exists()
