"""Password file and keystore handling."""

from pathlib import Path
from typing import List, Optional

from .config import SETTINGS


class PasswordStore:
    def __init__(self, path: Optional[str] = None):
        self.path = Path(path or SETTINGS.password_file)

    def load(self) -> List[str]:
        if not self.path.exists():
            raise FileNotFoundError(f"Password file not found: {self.path}")
        with self.path.open(encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]


def list_keystore_files(keystore_dir: Optional[str] = None) -> List[Path]:
    directory = Path(keystore_dir or SETTINGS.keystore_dir)
    if not directory.exists():
        raise FileNotFoundError(f"Keystore directory not found: {directory}")
    return sorted(p for p in directory.iterdir() if p.is_file())


def decrypt_keystore(web3, keystore_path: Path, password: str):
    with open(keystore_path, "r", encoding="utf-8") as f:
        keystore_json = f.read()
    return web3.eth.account.decrypt(keystore_json, password)
