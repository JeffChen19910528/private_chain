mkdir data

初始化
geth  --datadir data init genesis.json 
啟動私有網路,預設8545
geth --datadir "data" --networkid 10 --http --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" --http.corsdomain "*" --snapshot=false --allow-insecure-unlock console 2> 1.log --dev --dev.period 1

truffle mignate --network live
