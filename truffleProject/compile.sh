#!/bin/bash
truffle compile
truffle migrate --network live > contractAddr.txt
# find contract address
str2="address:"

if grep -q $str2 contractAddr.txt; then
  while read line; do 
	if [[ $line == *$str2* ]]; then
		# Left to right, after colon string
		echo ${line##*:} > contractAddr.txt
	fi
  done < contractAddr.txt
else
	echo "migrate failure"
fi

