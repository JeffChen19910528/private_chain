from web3 import Web3

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # 使用默认的本地节点地址
# 读取 keystore 文件
keystore_file_path = '/home/jeff/private_chain/data/keystore/UTC--2023-12-27T08-34-33.613585625Z--8ae9625821e1bb233432522da632a8f9f2e7a243'
with open(keystore_file_path, 'r') as f:
    keystore = f.read()

# 输入 keystore 的密码
password = input("Enter your keystore password: ")

# 使用 Web3.eth.accounts.decrypt 方法解密私钥
try:
    private_key = w3.eth.account.decrypt(keystore, password)
    print("Decryption successful.")
    print("Your private key is:", private_key.hex())
except ValueError as e:
    print("Error:", e)