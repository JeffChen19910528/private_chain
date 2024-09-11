from web3 import Web3
import json
import os

class Password:
    def __init__(self, path):
        self.path = path

    def get_passwords(self):
        try:
            with open(self.path, 'r') as file:
                passwords = file.readlines()
                return [pwd.strip() for pwd in passwords]
        except IOError:
            print("Error: File does not appear to exist.")
            return []

web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

if web3.is_connected():
    print("Connection Successful")
else:
    print("Connection Failed")

print('block_number: ' + str(web3.eth.block_number))
accounts = web3.eth.accounts


password_handler = Password('password.txt')
passwords = password_handler.get_passwords()

for account, password in zip(accounts, passwords):
    try:
        web3.geth.personal.unlock_account(account, password, 15000)
    except Exception as e:
        print(f"Error unlocking account {account}: {str(e)}")

# 指定Truffle项目路径
truffle_project_path = "truffleProject"

# 读取合约地址
with open(os.path.join(truffle_project_path, 'contractAddr.json')) as f:
    contract_addresses = json.load(f)

# 读取合约ABI
with open(os.path.join(truffle_project_path, 'build/contracts/ERC20Token.json')) as f:
    token_json = json.load(f)
    token_abi = token_json['abi']

# 获取合约地址
contract_address = contract_addresses['ERC20Token']['address']

# 創建合約對象
contract = web3.eth.contract(address=contract_address, abi=token_abi)

balance = contract.functions.balanceOf(accounts[0]).call()
print(f'Initial balance: {balance}')

# 嘗試進行雙花攻擊
try:
    print('transfer 99999999999999998000...')
    # 發送兩次相同的轉帳交易
    tx_hash1 = contract.functions.transfer(accounts[1], 99999999999999998000).transact({'from': accounts[0]}) 

    # 等待交易完成
    web3.eth.wait_for_transaction_receipt(tx_hash1)

    # 再次獲取帳戶餘額
    balance = contract.functions.balanceOf(accounts[0]).call()
    print(f'Balance after double spend attempt: {balance}')

except Exception as e:
    print(f'Error: {e}')