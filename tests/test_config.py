import importlib

from chain_tools import config as config_module


def test_defaults_when_env_unset(monkeypatch):
    monkeypatch.delenv("CHAIN_RPC_URL", raising=False)
    importlib.reload(config_module)
    assert config_module.SETTINGS.rpc_url == "http://127.0.0.1:8545"
    assert config_module.SETTINGS.password_file == "password.txt"


def test_env_override(monkeypatch):
    monkeypatch.setenv("CHAIN_RPC_URL", "http://example.com:1234")
    importlib.reload(config_module)
    try:
        assert config_module.SETTINGS.rpc_url == "http://example.com:1234"
    finally:
        monkeypatch.delenv("CHAIN_RPC_URL", raising=False)
        importlib.reload(config_module)


def test_double_spend_private_key_requires_env(monkeypatch):
    monkeypatch.delenv("DOUBLE_SPEND_PRIVATE_KEY", raising=False)
    importlib.reload(config_module)
    try:
        config_module.SETTINGS.double_spend_private_key()
        assert False, "expected RuntimeError"
    except RuntimeError:
        pass


def test_double_spend_private_key_reads_env(monkeypatch):
    monkeypatch.setenv("DOUBLE_SPEND_PRIVATE_KEY", "0xabc123")
    importlib.reload(config_module)
    try:
        assert config_module.SETTINGS.double_spend_private_key() == "0xabc123"
    finally:
        monkeypatch.delenv("DOUBLE_SPEND_PRIVATE_KEY", raising=False)
        importlib.reload(config_module)
