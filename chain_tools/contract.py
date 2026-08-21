"""Loading deployed contract addresses/ABIs produced by truffleProject/compile.sh."""

import json
from pathlib import Path
from typing import Optional, Tuple

from .config import SETTINGS


class ContractRepository:
    def __init__(self, truffle_dir: Optional[str] = None, addr_file: Optional[str] = None):
        self.truffle_dir = Path(truffle_dir or SETTINGS.truffle_dir)
        self.addr_file = Path(addr_file or SETTINGS.contract_addr_file)

    def _addr_path(self) -> Path:
        if self.addr_file.is_absolute() or self.addr_file.exists():
            return self.addr_file
        return self.truffle_dir / self.addr_file.name

    def load_deployment(self, contract_name: Optional[str] = None) -> Tuple[str, str]:
        """Return (contract_name, address), accepting either
        {"Name": "0xaddr"} or {"Name": {"address": "0xaddr"}}."""
        with self._addr_path().open(encoding="utf-8") as f:
            data = json.load(f)

        name = contract_name or next(iter(data))
        entry = data[name]
        address = entry["address"] if isinstance(entry, dict) else entry
        return name, address

    def load_abi(self, contract_name: str) -> list:
        abi_path = self.truffle_dir / "build" / "contracts" / f"{contract_name}.json"
        with abi_path.open(encoding="utf-8") as f:
            return json.load(f)["abi"]

    def get_contract(self, web3, contract_name: Optional[str] = None):
        name, address = self.load_deployment(contract_name)
        abi = self.load_abi(name)
        return web3.eth.contract(address=address, abi=abi)
