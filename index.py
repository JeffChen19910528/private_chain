from web3 import Web3
import json
import asyncio
import time

class Contract:
    def __init__(self):
        pass

    async def getContract(self, web3):
        # Read contract address from JSON file
        path = 'truffleProject/contractAddr.json'  # 請替換為您的實際路徑
        with open(path, 'r') as f:
            contract_data = json.load(f)
            abi_key = list(contract_data.keys())[0]
            deployed_contract_address = contract_data[abi_key]

        print(deployed_contract_address)

        # Load contract ABI
        abi_path = f'truffleProject/build/contracts/{abi_key}.json'  # 請替換為您的實際路徑
        with open(abi_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']

        return web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

class Password:
    def __init__(self):
        pass

    def getPassword(self):
        path = 'password.txt'
        with open(path, 'r') as file:
            pwd = file.readlines()
        return pwd

async def simulate_double_spending(web3, contract, account1, account2):
    contract_balance = contract.functions.checkBalance().call({"from": account1}) 

    if contract_balance < web3.to_wei("1.0", "ether"):
        print("account1 在合約中的餘額不足，無法轉帳。")
        return  # 如果餘額不足，則退出函數

    # 建立兩筆轉帳交易，都從 account1 轉帳到 account2
    gas_price = web3.to_wei('2300', 'gwei') 
    gas_price1 = web3.to_wei('4300', 'gwei')

    # 獲取 nonce，使用 await 等待異步操作完成
    nonce = web3.eth.get_transaction_count(account1)

    tx1 = contract.functions.transfer(account2, web3.to_wei("3.0", "ether")).build_transaction({
        "from": account1,
        "nonce": nonce,
        "gasPrice": gas_price,
    })

    tx2 = contract.functions.transfer(account2, web3.to_wei("4.0", "ether")).build_transaction({
        "from": account1,
        "nonce": nonce, 
        "gasPrice": gas_price1,
    })

    # 簽署交易
    PRIVATE_KEY1 = "0xfef23bca7ca9d717684779f752cf2d248425c3f475894b319bac98ffd0e87325"
    signed_tx1 = web3.eth.account.sign_transaction(tx1, private_key=PRIVATE_KEY1)
    signed_tx2 = web3.eth.account.sign_transaction(tx2, private_key=PRIVATE_KEY1)

    # 同時發送這兩筆交易
    try:
        tx1_hash = web3.eth.send_raw_transaction(signed_tx1.rawTransaction)
        tx2_hash = web3.eth.send_raw_transaction(signed_tx2.rawTransaction)

        receipt1, receipt2 = await asyncio.gather(
            web3.eth.wait_for_transaction_receipt(tx1_hash), 
            web3.eth.wait_for_transaction_receipt(tx2_hash)
        )

        receipt1 = await asyncio.gather(
            web3.eth.wait_for_transaction_receipt(tx1_hash)
        )

        print(f"Transaction 1 receipt: {receipt1[0]}")
        print(f"Transaction 2 receipt: {receipt2[0]}")

    except Exception as e:
        print("發生錯誤:", e)  # 其中一筆交易應該會失敗

    # 檢查 account1 的餘額
    balance = contract.functions.checkBalance().call({"from": account1})
    print("account1 餘額:", Web3.from_wei(balance, "ether"))

async def main():
    # Connect to local Ethereum node
    web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545')) 
    if web3.is_connected():
        print("Connection Successful")
    else:
        print("Connection Failed")

    print('block_number: ' + str(web3.eth.block_number))
    print('accounts: ' + str(web3.eth.accounts))
    accounts = web3.eth.accounts
    count = 0
    for account in accounts:
        print('account balance'+ str(count) +': ' + str(web3.eth.get_balance(account)))
        count += 1

    # Unlock accounts
    pw = Password()
    pwd = pw.getPassword()

    count = 0
    for account in accounts:
        web3.geth.personal.unlock_account(str(account), pwd[count].strip())
        count += 1

    # Interact with the contract
    ct = Contract()
    contract = await ct.getContract(web3)

    # 為 account1 和 account2 建立帳戶 (在 main 函數中執行一次)
    accounts = web3.eth.accounts
    account1 = accounts[0]
    account2 = accounts[1]

    # 檢查 account1 的初始餘額
    balance1 = web3.eth.get_balance(account1)
    print(f"Account 1 initial balance: {Web3.from_wei(balance1, 'ether')} ether")

    # 如果 account1 餘額不足，請在此處增加餘額
    if balance1 < web3.to_wei("1.0", "ether"):
        print("Account 1 has insufficient balance. Please add more ether.")
        # 在這裡添加增加 account1 餘額的程式碼，例如挖礦或其他方式

    initial_deposit = web3.to_wei("5.0", "ether")  # 設定初始存款金額

    tx_hash1 = contract.functions.createAccount(initial_deposit).transact({"from": account1, "value": initial_deposit})
    receipt1 = web3.eth.wait_for_transaction_receipt(tx_hash1) 
    if receipt1['status'] == 1:
        print(f"Account 1 creation transaction successful: {receipt1}")
    else:
        print(f"Account 1 creation transaction failed: {receipt1}")

    tx_hash2 = contract.functions.createAccount(initial_deposit).transact({"from": account2, "value": initial_deposit})
    receipt2 = web3.eth.wait_for_transaction_receipt(tx_hash2) 
    if receipt2['status'] == 1:
        print(f"Account 2 creation transaction successful: {receipt2}")
    else:
        print(f"Account 2 creation transaction failed: {receipt2}")

    # 等待一段時間，確保帳戶狀態已經更新
    time.sleep(5)

     # 等待帳戶建立交易完成後，再調用 simulate_double_spending
    await simulate_double_spending(web3, contract, account1, account2)

   
if __name__ == "__main__":
    asyncio.run(main()) 
