from getABI import convert_abi_from_api
from web3 import Web3 
import asyncio
import json 
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
from eth_account import Account



web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/<token>"))
web3_optimism.middleware_onion.inject(geth_poa_middleware, layer=0)



OPTIMISM_REGISTRY_CONTRACT = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
api_pool = "http://api-optimistic.etherscan.io/api?module=contract&action=getabi&address=0x270d4c1b6f0bb172a9fd628e29530ca484190013&format=raw"
abi = convert_abi_from_api(api_pool)

# data = '[{"inputs":[{"internalType":"address","name":"admin","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_logic","type":"address"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"initialize","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]'
# abi = json.loads(data)

contract_aave = web3_optimism.eth.contract(
        address=OPTIMISM_REGISTRY_CONTRACT,
        abi=abi
    )

def data_functions():
    totalsupply = contract_aave.functions.FLASHLOAN_PREMIUM_TO_PROTOCOL().call()
    #convert supply to Wei which is 18 decimal places
    # print('Total Supply: ', totalsupply/1000000)
    print('Contract Name: ', contract_aave.functions.FLASHLOAN_PREMIUM_TO_PROTOCOL().call())
    print('MAX_NUMBER_RESERVES ', contract_aave.functions.MAX_NUMBER_RESERVES().call())
    


def handle_event(event):
    print(Web3.toJSON(event))

def get_last_block_number():
    last_block_number = web3_optimism.eth.block_number
    return last_block_number

#Coroutine
async def log_loop(event_filter, poll_interval):
    last_block_number = get_last_block_number()
    block = web3_optimism.eth.get_block(last_block_number)
    number = block['number']
    event_filter = contract_aave.events.ReserveDataUpdated.createFilter(fromBlock= number )
    while True:
        for ReserveDataUpdated in event_filter.get_new_entries():
            timestamp = block['timestamp']
            liquidityRate = ReserveDataUpdated['args']['liquidityRate']
            liquidity = int(web3_optimism.fromWei(liquidityRate, 'ether'))
            # print (f"LiquidityRate : {web3_optimism.fromWei(liquidityRate, 'ether') }")
            # print(f"Timestamp : {timestamp}")
            
            return liquidity, timestamp

            
            # data_acquired = web3_optimism.fromWei(liquidityRate, 'ether')
            # return data_acquired

        
async def get_data():
    last_block_number = get_last_block_number()
    block = web3_optimism.eth.get_block(last_block_number)
    number = block['number']
    event_filter = contract_aave.events.ReserveDataUpdated.createFilter(fromBlock= number )
    #opens loop
    data_acquisition = await asyncio.gather(log_loop(event_filter, 2))
    print(data_acquisition)
    
    
# ------------------ ENCODING --------------------- 

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

    
if __name__ == "__main__":
    # event_filter = contract_aave.events.ReserveDataUpdated.createFilter(fromBlock='pending')
    # asyncio.run(log_loop(event_filter, 2))
    asyncio.run(get_data())

 


        