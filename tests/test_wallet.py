import pytest

from chain_tools.wallet import PasswordStore, list_keystore_files


def test_password_store_strips_blank_lines(tmp_path):
    pw_file = tmp_path / "password.txt"
    pw_file.write_text("123456\n\n123456\n", encoding="utf-8")

    store = PasswordStore(str(pw_file))
    assert store.load() == ["123456", "123456"]


def test_password_store_missing_file(tmp_path):
    store = PasswordStore(str(tmp_path / "missing.txt"))
    with pytest.raises(FileNotFoundError):
        store.load()


def test_list_keystore_files(tmp_path):
    keystore_dir = tmp_path / "keystore"
    keystore_dir.mkdir()
    (keystore_dir / "b.json").write_text("{}", encoding="utf-8")
    (keystore_dir / "a.json").write_text("{}", encoding="utf-8")

    files = list_keystore_files(str(keystore_dir))
    assert [p.name for p in files] == ["a.json", "b.json"]


def test_list_keystore_files_missing_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        list_keystore_files(str(tmp_path / "missing"))
