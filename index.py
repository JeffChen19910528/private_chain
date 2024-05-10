from web3 import Web3
import json

class Contract:
    def __init__(self):
        pass

    def getContract(self):
        path = 'truffleProject/contractAddr.txt'
        f = open(path, 'r')
        deployed_contract_address = f.read().strip()
        print(deployed_contract_address)
        f.close()
        abi = 'truffleProject/build/contracts/Test.json'
        with open(abi) as file:
            contract_json = json.load(file)  # load contract info as JSON
            contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
        #print('abi: ' + str(contract_abi))
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        
        # 發送代幣
        tx = contract.functions.transfer(accounts[2], 100).transact({'from': accounts[1]})
        web3.eth.wait_for_transaction_receipt(tx)
        # 查詢餘額
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
        file1 = open(path, 'r')
        pwd = file1.readlines()
        return pwd

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

pw = Password()
pwd = pw.getPassword()

count = 0
for account in accounts:
    web3.geth.personal.unlock_account(str(account), pwd[count].strip())
    count += 1

ct = Contract()
ct.getContract()

