
from web3 import Web3
import asyncio
import json

# Params 
web3_goerli = Web3(Web3.HTTPProvider("https://eth-goerli.g.alchemy.com/v2/iF_FH5ImUM5oCWOKpzv1nHha0Q2iD8Ss"), request_kwargs={'timeout': 60})
web3_polygon = Web3(Web3.HTTPProvider('https://polygon-mumbai.g.alchemy.com/v2/NGauPEJAYB84xVdGHaT_mRVTDE-enCr7'))

#1. Catch specific events via node provider of polygon testnet
PoolDataProvider_Aave  = "0x9BE876c6DC42215B00d7efe892E2691C3bc35d10"
DataProvider_Aave = web3_goerli.toChecksumAddress(PoolDataProvider_Aave)
dataProvider = web3_goerli.eth.contract(address = DataProvider_Aave)

data = '[{}]'
abi = json.loads(data)

    
def handle_event(event):
    # print(Web3.toJSON(event))
    try: 
        getTrans = Web3.toJSON(event).strip('"')
        trans = web3_goerli.eth.get_transaction(getTrans) #Look up txs 
        to_decode = trans.input
        # print(to_decode)
        dataProvider.decode_function_input(to_decode)
        # print(x)
        data = trans["gasPrice"]
        # print(data)
    except Exception as e:
        print(f'error occured {e}')
    
#2. At that timing, access a specific variable of a specific contract (e.g., a variable related to APY of AAVE)
event_filter = web3_goerli.eth.filter({"address": PoolDataProvider_Aave})
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
   
    tx_filter = web3_goerli.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(block_filter, 2),
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    
    # check_provider(web3_goerli)
    # check_provider(web3_polygon)
    
    main()


#3. Encode the data


#4. Switch to goerli's node provider
#5. Sign the contract based on the encoded data
#6. Sends a transaction with the encoded data and timestamp as arguments


