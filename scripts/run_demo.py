"""Create two funded contract accounts and race a same-nonce double-spend."""

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from web3 import Web3

from chain_tools.attacks import simulate_same_nonce_double_spend
from chain_tools.chain import get_web3, unlock_all_accounts
from chain_tools.config import SETTINGS
from chain_tools.contract import ContractRepository
from chain_tools.wallet import PasswordStore


async def main():
    web3 = get_web3()
    print("Connection Successful")
    print(f"block_number: {web3.eth.block_number}")

    accounts = web3.eth.accounts
    for idx, account in enumerate(accounts):
        print(f"account balance{idx}: {web3.eth.get_balance(account)}")

    unlock_all_accounts(web3, PasswordStore().load())

    contract = ContractRepository().get_contract(web3)

    account1, account2 = accounts[0], accounts[1]

    balance1 = web3.eth.get_balance(account1)
    print(f"Account 1 initial balance: {Web3.from_wei(balance1, 'ether')} ether")
    if balance1 < web3.to_wei("1.0", "ether"):
        print("Account 1 has insufficient balance. Please fund it first.")

    initial_deposit = web3.to_wei("5.0", "ether")
    for label, account in (("Account 1", account1), ("Account 2", account2)):
        tx_hash = contract.functions.createAccount(initial_deposit).transact(
            {"from": account, "value": initial_deposit}
        )
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        status = "successful" if receipt["status"] == 1 else "failed"
        print(f"{label} creation transaction {status}: {receipt}")

    time.sleep(5)

    private_key = SETTINGS.double_spend_private_key()
    await simulate_same_nonce_double_spend(web3, contract, account1, account2, private_key)


if __name__ == "__main__":
    asyncio.run(main())
