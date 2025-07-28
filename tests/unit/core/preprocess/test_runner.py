from pipeline.core.preprocess.runner import VideoPreprocessor


def test_video_preprocessor_end_to_end(create_test_images, tmp_path):
    input_dir = tmp_path / " input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    create_test_images(input_dir)

    pre = VideoPreprocessor(
        enable_blur_detection=True,
        enable_deduplication=True,
        blur_threshold=100,  # high to remove blurry image
        dedub_threshold=0,  # strict for exact duplicates
        hash_size=8,
    )

    final_dir = pre.run(input_dir=input_dir, output_dir=output_dir)

    final_files = list(final_dir.glob("*.jpg"))
    print(pre.cleaned, pre.deduped, final_files, final_dir)

    # Expect only 1 image left after blur + dedup
    assert len(final_files) == 1
    assert pre.cleaned == 1  # 1 blurry image removed
    assert pre.deduped == 1  # 1 duplicate image removed
    assert final_dir.exists()
