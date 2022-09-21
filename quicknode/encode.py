from web3 import Web3
from eth_account.messages import encode_defunct
import asyncio
import json
from getABI import convert_abi_from_api
from eth_utils.curried import to_hex, to_bytes
from typing import List


web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/"))


from eth_account import Account


def setup_variables():
    array = []
    

def create_account() -> list():
    Account.enable_unaudited_hdwallet_features()
    acct, mnemonic = Account.create_with_mnemonic()
    account = acct.address
    acct == Account.from_mnemonic(mnemonic)
    key = acct.key
    pair = [account, key]
    print(pair)
    return pair

def encode_message(message: str):
   encoded = encode_defunct(text = message)
   return encoded

def sign_message(message: str):    
    pair = create_account()
    encoded = encode_message(message)
    signed_message = web3_optimism.eth.account.sign_message(encoded, private_key=pair[1])
    print(signed_message)
    return signed_message
    
if __name__ == '__main__':
    sign_message("tosign")
   
 
