"""Web3 connection and account-unlock helpers."""

from typing import Iterable, Optional

from web3 import Web3

from .config import SETTINGS


def get_web3(rpc_url: Optional[str] = None) -> Web3:
    url = rpc_url or SETTINGS.rpc_url
    web3 = Web3(Web3.HTTPProvider(url))
    if not web3.is_connected():
        raise ConnectionError(f"Unable to connect to chain node at {url}")
    return web3


def unlock_all_accounts(web3: Web3, passwords: Iterable[str], unlock_seconds: int = 15000) -> None:
    for account, password in zip(web3.eth.accounts, passwords):
        try:
            web3.geth.personal.unlock_account(account, password, unlock_seconds)
        except Exception as exc:
            print(f"Error unlocking account {account}: {exc}")
