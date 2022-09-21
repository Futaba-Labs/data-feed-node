from web3 import Web3
import asyncio
import json
from getABI import convert_abi_from_api

# Params 
web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/"))
web3_polygon = Web3(Web3.HTTPProvider('https://polygon-mumbai.g.alchemy.com/v2/<>'))

#api etherscan
api_optimism = "https://api-optimistic.etherscan.io/api?module=contract&action=getabi&address=0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654&format=raw"

#Variables
PoolDataProvider_Aave = "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654"
abi = convert_abi_from_api(api_optimism)
dataProvider = web3_optimism.eth.contract(address = PoolDataProvider_Aave, abi=abi)


#Optimism 
def contract_transaction():
    # DataProvider_Aave = web3_optimism.toChecksumAddress(PoolDataProvider_Aave)
    usdc_address = "0x7F5c764cBc14f9669B88837ca1490cCa17c31607"
    tx = dataProvider.functions.getReserveEModeCategory(usdc_address)
    print(tx)

data = '[{}]'
abi = json.loads(data)

    
def handle_event(event):
    # print(Web3.toJSON(event))
    try: 
        getTrans = Web3.toJSON(event).strip('"')
        trans = web3_optimism.eth.get_transaction(getTrans) #Look up txs 
        to_decode = trans.input
        # print(to_decode)
        dataProvider.decode_function_input(to_decode)
        # print(x)
        data = trans["gasPrice"]
        # print(data)
    except Exception as e:
        print(f'error occured {e}')
    
#2. At that timing, access a specific variable of a specific contract (e.g., a variable related to APY of AAVE)
event_filter = web3_optimism.eth.filter({"address": PoolDataProvider_Aave})
async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)
        
def check_provider(HTTPProvider: str):
    res = HTTPProvider.isConnected()
    print(res)

def main():
    # block_filter = w3.eth.filter('latest')
   
    tx_filter = web3_optimism.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(block_filter, 2),
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    contract_transaction()
    
    # check_provider(web3_goerli)
    # check_provider(web3_polygon)
    
    


#3. Encode the data


#4. Switch to goerli's node provider
#5. Sign the contract based on the encoded data
#6. Sends a transaction with the encoded data and timestamp as arguments

