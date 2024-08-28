pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT 
contract ERC20Token {
    // 帳戶結構
    struct Account {
        address owner;
        uint balance;
    }

    // 狀態變數
    Account[] public accounts;
    mapping(address => uint) public accountIndex; // 透過地址快速找到帳戶索引

    // 事件
    event AccountCreated(address indexed owner, uint indexed accountIndex);
    event BalanceChecked(address indexed owner, uint balance);
    event TransferCompleted(address indexed from, address indexed to, uint amount);

    // 建立帳戶
    function createAccount(uint initialDeposit) public payable {
        // 驗證：確保該地址尚未擁有帳戶
        require(accountIndex[msg.sender] == 0, "You already have an account"); 

        // 驗證：確保存入的 Ether 數量與 initialDeposit 相符
        require(msg.value == initialDeposit, "Incorrect deposit amount");

        // 建立新帳戶，初始餘額為 initialDeposit
        uint newAccountIndex = accounts.length;
        accounts.push(Account({
            owner: msg.sender,
            balance: initialDeposit
        }));
        accountIndex[msg.sender] = newAccountIndex + 1; // 索引從 1 開始，0 表示未找到

        // 觸發事件
        emit AccountCreated(msg.sender, newAccountIndex);
    }

    // 檢查餘額
     function checkBalance() public returns (uint) {
        // Validation: Ensure the address has an account
        uint _accountIndex = accountIndex[msg.sender];
        require(_accountIndex > 0, "You don't have an account yet");

        return accounts[_accountIndex - 1].balance;
    }

    // 轉帳
    function transfer(address _to, uint _amount) public {
        // 驗證
        uint _fromIndex = accountIndex[msg.sender];
        uint _toIndex = accountIndex[_to];
        require(_fromIndex > 0, "You don't have an account yet");
        require(_toIndex > 0, "Recipient does not have an account yet");
        require(accounts[_fromIndex - 1].balance >= _amount, "Insufficient balance");

        // 並行控制 (透過餘額檢查防止重複扣款)
        require(accounts[_fromIndex - 1].balance == checkBalance(), "Account balance has changed, please retry");

        // 執行轉帳
        accounts[_fromIndex - 1].balance -= _amount;
        accounts[_toIndex - 1].balance += _amount;

        // 觸發事件
        emit TransferCompleted(msg.sender, _to, _amount);
    }
}