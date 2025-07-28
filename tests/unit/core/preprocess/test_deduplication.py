from pipeline.core.preprocess.deduplicator import dedupe_frames


def test_dedupe_frames(create_duplicate_test_images, tmp_path):
    input_images = create_duplicate_test_images()
    output_dir = tmp_path / "deduped"
    output_dir.mkdir()

    deduped, dup_count, _ = dedupe_frames(
        input_images,
        output_dir=output_dir,
        hash_size=8,
        threshold=0,  # Zero tolerance for exact match
    )

    assert len(deduped) == 2  # 2 unique images: white and black
    assert dup_count == 1  # One duplicate
    deduped_names = sorted(p.name for p in deduped)
    assert "img_1.jpg" in deduped_names
    assert "img_3.jpg" in deduped_names
    assert not (output_dir / "img_2.jpg").exists()
