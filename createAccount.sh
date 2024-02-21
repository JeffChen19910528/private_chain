#!/bin/bash
#create account
read -p "password: " pwd
geth --datadir "data" account new --password <(echo $pwd) 
 
printf "$pwd\n" >> password.txt