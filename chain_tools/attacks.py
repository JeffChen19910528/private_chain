"""Double-spend attack simulations against the demo chain/contract."""

import asyncio
from typing import Tuple

from web3 import Web3


async def simulate_same_nonce_double_spend(
    web3: Web3,
    contract,
    sender: str,
    receiver: str,
    private_key: str,
    amounts_ether: Tuple[str, str] = ("3.0", "4.0"),
    gas_prices_gwei: Tuple[str, str] = ("2300", "4300"),
    min_balance_ether: str = "1.0",
):
    """Race two competing transfer transactions sharing the same nonce."""
    contract_balance = contract.functions.checkBalance().call({"from": sender})
    if contract_balance < web3.to_wei(min_balance_ether, "ether"):
        print("sender has insufficient contract balance to transfer.")
        return None

    nonce = web3.eth.get_transaction_count(sender)
    gas_price_a = web3.to_wei(gas_prices_gwei[0], "gwei")
    gas_price_b = web3.to_wei(gas_prices_gwei[1], "gwei")

    tx_a = contract.functions.transfer(receiver, web3.to_wei(amounts_ether[0], "ether")).build_transaction(
        {"from": sender, "nonce": nonce, "gasPrice": gas_price_a}
    )
    tx_b = contract.functions.transfer(receiver, web3.to_wei(amounts_ether[1], "ether")).build_transaction(
        {"from": sender, "nonce": nonce, "gasPrice": gas_price_b}
    )

    signed_a = web3.eth.account.sign_transaction(tx_a, private_key=private_key)
    signed_b = web3.eth.account.sign_transaction(tx_b, private_key=private_key)

    try:
        hash_a = web3.eth.send_raw_transaction(signed_a.rawTransaction)
        hash_b = web3.eth.send_raw_transaction(signed_b.rawTransaction)

        receipt_a, receipt_b = await asyncio.gather(
            web3.eth.wait_for_transaction_receipt(hash_a),
            web3.eth.wait_for_transaction_receipt(hash_b),
        )
        print(f"Transaction A receipt: {receipt_a}")
        print(f"Transaction B receipt: {receipt_b}")
    except Exception as exc:
        print("Error (expected - one transaction should fail):", exc)

    balance = contract.functions.checkBalance().call({"from": sender})
    print("sender balance:", Web3.from_wei(balance, "ether"))
    return balance


def exploit_vulnerable_transfer(web3: Web3, token_contract, sender: str, receiver: str, amount: int):
    """Exercise a token contract whose transfer() double-executes _transfer."""
    balance_before = token_contract.functions.balanceOf(sender).call()
    print(f"Balance before: {balance_before}")

    tx_hash = token_contract.functions.transfer(receiver, amount).transact({"from": sender})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    balance_after = token_contract.functions.balanceOf(sender).call()
    print(f"Balance after: {balance_after}")
    return balance_before, balance_after
