#!/bin/bash

declare -a addr arr objaddr
counter=0
DIR="$PWD"/data/keystore

for FILE in "$DIR"/*
do
    arr[$counter]="$FILE"
    counter=$((counter + 1))
done
# get address
count=0
for i in "${arr[@]}"
do
   addr[$count]=$(jq -r '.address' $i)
   addr[$count]="0x"${addr[$count]}
   echo ${addr[$count]}
   count=$((count + 1))
done
# write address
rm address.txt
count=0
for i in "${addr[@]}"
do
   printf "$i\n" >> address.txt
done

# create new json object 
count=0
len=${#addr[@]}
len=$((len - 1))
echo "$len"
for i in "${addr[@]}"
do 
    jsonobj+='"'$i'": {"balance":"200000000000000000000"}'
    if [ "$count" -lt $len ]; then
        jsonobj+=','
    else
         jsonobj+='}'
    fi
    count=$((count + 1))
done
echo $jsonobj
data= jq -r '.alloc={}' genesis.json

data= jq --arg val "$jsonobj" '.alloc= $val' genesis.json > file.json
# delete backslash and  Quotes 
sed --in-place 's/\\//g' file.json
replace='"alloc": {'
search='"alloc": "'
result= sed -i "s/$search/$replace/" file.json
replace='}'
search='}"'
result= sed -i "s/$search/$replace/" file.json

echo $result
# update geth data
rm genesis.json
mv file.json genesis.json
# geth init
geth --datadir data init genesis.json