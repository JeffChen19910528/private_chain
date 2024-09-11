pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
// SPDX-License-Identifier: MIT
contract ERC20Token is ERC20{
   constructor() ERC20("Vulnerable Token", "VTK") {
        _mint(msg.sender, 100 * 10 ** decimals()); // 初始分配 100 個代幣給部署者
    }

    function transfer(address _to, uint256 _amount) public override returns (bool) {
        // 模擬雙花攻擊：在餘額扣除前發送兩次交易
        _transfer(msg.sender, _to, _amount);

        // 故意不檢查餘額是否足夠，允許第二次轉帳成功
        _transfer(msg.sender, _to, _amount); 

        return true; // 雖然第二次轉帳可能失敗，但仍返回 true
    }
}