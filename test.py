from web3 import Web3
import json
import requests, urllib3, chardet


web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

if web3.is_connected():
    print("Connection Successful")
else:
    print("Connection Failed")

print('block_number: ' + str(web3.eth.block_number))
accounts = web3.eth.accounts
print('accounts: ' + str(accounts))
print('account balance: ' + str(web3.eth.get_balance(accounts[0])))

try:
    tx_hash = web3.eth.send_transaction({
        'from': accounts[0], 
        'to': accounts[1], 
        'value': web3.to_wei('1', 'ether')
    })
    print(f"Transaction hash: {tx_hash.hex()}") 
except ValueError as e:
    if "authentication needed" in str(e):
        print("Account is locked. Please unlock it.")
    else:
        print(f"An error occurred: {e}")



print(f"requests version: {requests.__version__}")
print(f"urllib3 version: {urllib3.__version__}")
print(f"chardet version: {chardet.__version__}")