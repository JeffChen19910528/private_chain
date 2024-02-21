初始話
geth  --datadir data init genesis.json 
啟動私有網路,預設8545
geth --datadir "data" --networkid 10 --http --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" --http.corsdomain "*" --snapshot=false --allow-insecure-unlock console 2> 1.log --dev --dev.period 1

password 
123456
000000

personal.unlockAccount(eth.accounts[0], '123456')
personal.unlockAccount(eth.accounts[1], '000000')


truffle mignate --network live
