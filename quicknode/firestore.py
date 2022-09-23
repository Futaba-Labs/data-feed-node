
from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from getABI import convert_abi_from_api
from web3.middleware import geth_poa_middleware
import asyncio

# Use a service account.
cred = credentials.Certificate('futaba-node-dashboard-test-private-key.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# Params
web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/<>"))
web3_optimism.middleware_onion.inject(geth_poa_middleware, layer=0)
web3_polygon = Web3(Web3.HTTPProvider('https://polygon-mainnet.g.alchemy.com/v2/<>'))

OPTIMISM_REGISTRY_CONTRACT = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
api_pool = "http://api-optimistic.etherscan.io/api?module=contract&action=getabi&address=0x270d4c1b6f0bb172a9fd628e29530ca484190013&format=raw"
abi = convert_abi_from_api(api_pool)

contract_aave = web3_optimism.eth.contract(
        address=OPTIMISM_REGISTRY_CONTRACT,
        abi=abi
    )

def get_last_block_number():
    last_block_number = web3_optimism.eth.block_number
    return last_block_number

#Coroutine
async def log_loop(event_data, poll_interval):
    while True:
        for event in event_data['event_filter'].get_new_entries():
            last_block_number = get_last_block_number()
            block = web3_optimism.eth.get_block(last_block_number)
            timestamp = block['timestamp']
            value = event['args'][event_data['valuable_name']]
            print(f'name: ' + event_data['valuable_name'])
            print ("value: " + str(value))
        await asyncio.sleep(poll_interval)

async def get_data():
    last_block_number = get_last_block_number()
    block = web3_optimism.eth.get_block(last_block_number)
    number = block['number']
    # get evebt_list
    event_data_list = create_event_filters(number)
    # opens loop
    await asyncio.gather(*[log_loop(event_data, 1) for event_data in event_data_list])

def create_event_filters(number):
    # get all document
    docs = db.collection(u'jobs').stream()
    event_filters = []
    for doc in docs:
        data = doc.to_dict()
        contract = web3_optimism.eth.contract(
            address=data['srcContractAddress'],
            abi=abi
        )
        # get event_filter
        event_filter = eval('contract.events.'+data['eventName']+'.createFilter(fromBlock='+str(number)+')')

        # add other information
        event_filters.append({'event_filter': event_filter, 'src_contract': contract, 'valuable_name': data['valuableName'], 'dst_chain_id': data['dstChainId']})
    return event_filters


if __name__ == "__main__":
    asyncio.run(get_data())
