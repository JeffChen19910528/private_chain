"""Centralized, environment-overridable settings for chain_tools."""

import os
from dataclasses import dataclass


def _load_dotenv(path: str = ".env") -> None:
    """Populate os.environ from a simple KEY=VALUE .env file, if present."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()


@dataclass(frozen=True)
class Settings:
    rpc_url: str = os.environ.get("CHAIN_RPC_URL", "http://127.0.0.1:8545")
    truffle_dir: str = os.environ.get("TRUFFLE_PROJECT_DIR", "truffleProject")
    contract_addr_file: str = os.environ.get("CONTRACT_ADDR_FILE", "contractAddr.json")
    password_file: str = os.environ.get("PASSWORD_FILE", "password.txt")
    keystore_dir: str = os.environ.get("KEYSTORE_DIR", "data/keystore")
    private_key_env_var: str = "DOUBLE_SPEND_PRIVATE_KEY"

    def double_spend_private_key(self) -> str:
        key = os.environ.get(self.private_key_env_var)
        if not key:
            raise RuntimeError(
                f"Set the {self.private_key_env_var} environment variable "
                "(see .env.example) before running a double-spend demo."
            )
        return key


SETTINGS = Settings()
