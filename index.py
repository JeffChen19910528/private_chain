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
        print('abi: ' + str(contract_abi))
        contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
        messagge = contract.functions.getNumber().call() 
        print(messagge)

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
print('account balance: ' + str(web3.eth.get_balance(accounts[0])))

pw = Password()
pwd = pw.getPassword()

count = 0
for account in accounts:
    web3.geth.personal.unlock_account(str(account), pwd[count].strip())
    count += 1

tx_hash = web3.eth.send_transaction({
    "from": accounts[0],
    "to": accounts[1],
    "value": 123
})

tx = web3.eth.get_transaction(tx_hash)
print('tx hash: ' + str(tx))
ct = Contract()
ct.getContract()
