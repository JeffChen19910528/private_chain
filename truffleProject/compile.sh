#!/bin/bash

# Compile contracts using Truffle
echo "Compiling contracts..."
truffle compile

# Migrate contracts and output to file
echo "Migrating contracts..."
truffle migrate --network live > contractAddr.txt

# Define string to search for
str2="address:"

# Check if migration was successful and the address was found
if grep -q "$str2" contractAddr.txt; then
    # Extract the address and overwrite the file with just the address
    grep "$str2" contractAddr.txt | cut -d ':' -f 2 | head -n 1 > contractAddr.txt
    echo "Contract address extracted successfully."
else
    echo "Migration failure or contract address not found."
fi
