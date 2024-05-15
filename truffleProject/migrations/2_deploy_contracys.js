var Test = artifacts.require("./Test.sol");
var ERC20Token = artifacts.require("./ERC20Token.sol");
module.exports = function(deployer) {
   deployer.deploy(Test);
   deployer.deploy(ERC20Token);
};
