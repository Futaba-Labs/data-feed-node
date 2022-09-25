from web3 import Web3
import asyncio
import pandas as pd

web3 = Web3(Web3.HTTPProvider("https://proportionate-multi-bridge.ethereum-goerli.discover.quiknode.pro/<>"))



#Goerli 
PoolDataProvider_Aave  = "0x9BE876c6DC42215B00d7efe892E2691C3bc35d10"
DataProvider_Aave = web3.toChecksumAddress(PoolDataProvider_Aave)
dataProvider = web3.eth.contract(address = DataProvider_Aave)


def get_balance():
    # print(web3.clientVersion)
    balance = web3.eth.get_balance(PoolDataProvider_Aave)

    
def get_function(input: str, event) :
    pass
    
def handle_event(event):
    # print(Web3.toJSON(event))
    try: 
        getTrans = Web3.toJSON(event).strip('"')
        # print(getTrans)
        trans = web3.eth.get_transaction(getTrans) #Look up txs 
        # receipt = web3.eth.get_transaction_receipt(getTrans) #Look up tx receipts 
        # print(receipt)
        # to = trans['to']
        data = trans
        # print(data)
        df = pd.DataFrame(data=data, columns = ['from'])
        print(df)
    except Exception as e:
        print(f'error occured {e}')
    

# #Specify by specific contract 
# event_filter = web3.eth.filter({"address": })

async def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)

def main():
    # block_filter = w3.eth.filter('latest')
    tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                # log_loop(block_filter, 2),
                log_loop(tx_filter, 2)))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
    # get_balance()