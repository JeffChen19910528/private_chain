#!/bin/bash

# Compile contracts using Truffle
echo "Compiling contracts..."
truffle compile

# Migrate contracts and capture output
echo "Migrating contracts..."
migration_output=$(truffle migrate --network live)

# Define string to search for
str2="contract address:"

# Check if migration was successful and the address was found
if echo "$migration_output" | grep -q "$str2"; then
    # Extract the contract address
    contract_address=$(echo "$migration_output" | grep "$str2" | awk '{print $4}')
    
    # Get the ABI file name (assuming there's only one ABI file for simplicity)
    abi_file=$(ls build/contracts/*.json | head -n 1 | xargs -n 1 basename)
    
    # Remove the .json extension from the ABI file name to use it as the key
    abi_key="${abi_file%.json}"
    
    # Create a JSON object with the ABI file name as the key and the contract address as the value
    json_content="{\"$abi_key\": \"$contract_address\"}"
    
    # Write the JSON content to a file
    echo "$json_content" > contractAddr.json
    echo "Contract address extracted and saved to JSON file successfully."
else
    echo "Migration failure or contract address not found."
fi
