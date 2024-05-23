from web3 import Web3
import json

class Contract:
    def __init__(self):
        pass

    def getContract(self):
        # Read contract address from JSON file
        path = 'truffleProject/contractAddr.json'
        with open(path, 'r') as f:
            contract_data = json.load(f)
            # Assuming the key is the ABI file name without the .json extension
            abi_key = list(contract_data.keys())[0]
            deployed_contract_address = contract_data[abi_key]

        print(deployed_contract_address)

        # Load contract ABI
        abi_path = f'truffleProject/build/contracts/{abi_key}.json'
        with open(abi_path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']

        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        # Send tokens
        tx = contract.functions.transfer(accounts[1], 100).transact({'from': accounts[0]})
        web3.eth.wait_for_transaction_receipt(tx)
        print("transfer confirmed.")

        # Query balance
        balance = contract.functions.balanceOf(accounts[2]).call()
        print(f'Balance2: {balance}')
        balance = contract.functions.balanceOf(accounts[1]).call()
        print(f'Balance1: {balance}')
        balance = contract.functions.balanceOf(accounts[0]).call()
        print(f'Balance0: {balance}')

        # Approve tokens
        approval_tx = contract.functions.approve(accounts[1], 100).transact({'from': accounts[0]})
        web3.eth.wait_for_transaction_receipt(approval_tx)
        print("Approval confirmed.")

        tx_hash = contract.functions.transferFrom(accounts[0], accounts[2], 100).transact({'from': accounts[1]})
        # 等待交易確認
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print("transferFrom confirmed.")

        balance = contract.functions.balanceOf(accounts[2]).call()
        print(f'Balance2: {balance}')
        balance = contract.functions.balanceOf(accounts[1]).call()
        print(f'Balance1: {balance}')
        balance = contract.functions.balanceOf(accounts[0]).call()
        print(f'Balance0: {balance}')

class Password:
    def __init__(self):
        pass

    def getPassword(self):
        path = 'password.txt'
        with open(path, 'r') as file:
            pwd = file.readlines()
        return pwd

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
ct.getContract()
