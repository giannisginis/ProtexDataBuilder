from pipeline.utils.paths import list_images, ensure_dir, ensure_parent_dir


def test_list_images(tmp_path):
    img1 = tmp_path / "image1.jpg"
    img2 = tmp_path / "image2.png"
    txt = tmp_path / "notes.txt"
    img1.write_text("fake")
    img2.write_text("fake")
    txt.write_text("not an image")

    results = list_images(tmp_path)
    assert img1 in results
    assert img2 in results
    assert txt not in results
    assert len(results) == 2


def test_list_images_with_custom_extensions(tmp_path):
    webp = tmp_path / "pic.webp"
    jpg = tmp_path / "pic.jpg"
    webp.write_text("x")
    jpg.write_text("x")

    results = list_images(tmp_path, extensions=[".webp"])
    assert webp in results
    assert jpg not in results
    assert len(results) == 1


def test_ensure_dir(tmp_path):
    target = tmp_path / "nested" / "folder"
    assert not target.exists()
    result = ensure_dir(target)
    assert target.exists()
    assert result == target


def test_ensure_parent_dir(tmp_path):
    file_path = tmp_path / "some" / "dir" / "file.txt"
    assert not file_path.parent.exists()
    result = ensure_parent_dir(file_path)
    assert file_path.parent.exists()
    assert result == file_path
