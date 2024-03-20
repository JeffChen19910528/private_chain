pragma solidity ^0.8.0;

contract Test {
    mapping(address => uint256) private balances;
    address public owner;
    event Deposit(address indexed depositor, uint256 amount);
    event Withdrawal(address indexed withdrawer, uint256 amount);
    event Transfer(address indexed to, uint amount);

     constructor() {
        owner = msg.sender;
    }

    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than 0");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 amount) public {
        require(amount > 0, "Withdrawal amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        balances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);
        emit Withdrawal(msg.sender, amount);
    }

    function transfer(address payable _to, uint _amount) public {
        require(msg.sender == owner, "Only the owner can perform this action");
        require(address(this).balance >= _amount, "Insufficient balance in contract");
        _to.transfer(_amount);
        emit Transfer(_to, _amount);
    }

    function getBalance() public view returns (uint256) {
        return msg.sender.balance;
    }

    function getTotalBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
