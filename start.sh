#!/bin/bash

declare -a addr 
count=0
while IFS= read -r line
do
  addr[$count]=$line
  #echo "$line"
  count=$((count + 1))
done < "address.txt"

#echo "${addr[@]}"

#get password.txt lines
mapfile -t lines < password.txt
count=0
for line in "${lines[@]}"; do
   count=$((count + 1))
done

counts=0
count=$((count - 1))

for line in "${lines[@]}"; do
   accounts+=$counts
   if [ $counts -lt $count ] ;then
      accounts+=','
   fi
   counts=$((counts + 1))
done

# start ethereum
geth --datadir "data" --networkid 10 --http --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" --http.corsdomain "*" --snapshot=false --allow-insecure-unlock --unlock ${accounts} --password "password.txt" console 2> 1.log