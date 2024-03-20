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
        tx_hash = contract.functions.withdraw(100).transact({
                    'from': accounts[0],  # 替换为你的账户地址
                    'gas': 100000  # 适当设置gas限额
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        tx_hash = contract.functions.deposit().transact({
            'from': accounts[0],  # 替换为你的账户地址
            'value': 2000,  # 替换为你想要存款的金额，以wei为单位
            'gas': 100000  # 适当设置gas限额
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        # 转账金额（单位：wei）
        amount = web3.to_wei(0.01, 'ether')
        # 构建交易
        nonce = web3.eth.get_transaction_count(accounts[0])
        transaction = contract.functions.transfer(accounts[1], amount).build_transaction({
            'chainId': 10,  # 确保这里的chainId匹配你的网络
            'gas': 100000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
        # 签名交易
        signed_txn = web3.eth.account.sign_transaction(transaction, '0x90eee9fcf6901b0814d1753a864a2c49fe6fa92d891960bd8ca5ed7d15309f79')
        # 发送交易
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # 获取交易哈希
        print("Transaction hash:", web3.to_hex(tx_hash))

        # 调用 getTotalBalance 函数获取存款总额
        total_balance = contract.functions.getTotalBalance().call()

        print("Total balance in contract:", total_balance)

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

ct = Contract()
ct.getContract()

