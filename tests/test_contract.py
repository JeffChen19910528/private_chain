import json

from chain_tools.contract import ContractRepository


def _make_truffle_project(base, address_shape):
    truffle_dir = base / "truffleProject"
    (truffle_dir / "build" / "contracts").mkdir(parents=True)

    if address_shape == "flat":
        addr_data = {"ERC20Token": "0xdeadbeef"}
    else:
        addr_data = {"ERC20Token": {"address": "0xdeadbeef"}}

    (truffle_dir / "contractAddr.json").write_text(json.dumps(addr_data), encoding="utf-8")
    (truffle_dir / "build" / "contracts" / "ERC20Token.json").write_text(
        json.dumps({"abi": [{"type": "function", "name": "transfer"}]}), encoding="utf-8"
    )
    return truffle_dir


def test_load_deployment_flat_shape(tmp_path):
    truffle_dir = _make_truffle_project(tmp_path, "flat")
    repo = ContractRepository(truffle_dir=str(truffle_dir), addr_file=str(truffle_dir / "contractAddr.json"))
    name, address = repo.load_deployment()
    assert name == "ERC20Token"
    assert address == "0xdeadbeef"


def test_load_deployment_nested_shape(tmp_path):
    truffle_dir = _make_truffle_project(tmp_path, "nested")
    repo = ContractRepository(truffle_dir=str(truffle_dir), addr_file=str(truffle_dir / "contractAddr.json"))
    name, address = repo.load_deployment()
    assert name == "ERC20Token"
    assert address == "0xdeadbeef"


def test_load_abi(tmp_path):
    truffle_dir = _make_truffle_project(tmp_path, "nested")
    repo = ContractRepository(truffle_dir=str(truffle_dir), addr_file=str(truffle_dir / "contractAddr.json"))
    abi = repo.load_abi("ERC20Token")
    assert abi == [{"type": "function", "name": "transfer"}]
