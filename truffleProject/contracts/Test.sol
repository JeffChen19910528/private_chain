pragma solidity ^0.5.0;

contract Test {
    uint favoriteNumber;

    function saveNumber(uint _Number) public {
        favoriteNumber = _Number;
    }


    function deleteNumber() public {
        favoriteNumber = 0;
    }


    function getNumber() public view returns(uint) {
        return favoriteNumber;
    }
}
