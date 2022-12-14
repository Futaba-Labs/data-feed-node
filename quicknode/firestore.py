from web3 import Web3
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from getABI import convert_abi_from_api
from getProvider import get_provider_from_chain_id
from eth_abi import encode
from eth_account import Account
from eth_account.messages import encode_defunct
from dotenv import load_dotenv
import asyncio
import json
import os

# Use a service account.
cred = credentials.Certificate('futaba-node-dashboard-test-private-key.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

load_dotenv()
PRIVATE_KEY = os.getenv('PRIVATE_KEY')


def get_last_block_number(web3_provider):
    last_block_number = web3_provider.eth.block_number
    return last_block_number

def get_compound_data(event_data, web3_provider, timestamp, src_chain_id):
    src_contract = event_data['src_contract'].address
    abi = convert_abi_from_api(src_contract, src_chain_id)
    contract_address = web3_provider.toChecksumAddress(src_contract)
    contract = web3_provider.eth.contract(address=contract_address, abi=abi)
    supply_rate = 0
    if src_chain_id == 1284:
        supply_rate = contract.functions.supplyRatePerTimestamp().call()
    else:
        supply_rate = contract.functions.supplyRatePerBlock().call()

    price = contract.functions.exchangeRateStored().call()

    print("chain_id: " + str(web3_provider.eth.chain_id))
    print('contract address: ' + src_contract)
    print('price: ' + str(price))
    print ("supply_rate: " + str(supply_rate))

    # encode data
    encoded_price = encode(['uint256'], [price])
    encoded_supply_rate = encode(['uint256'], [supply_rate])
    feeds = [{
        "name": "price",
        "timestamp": timestamp,
        "value": encoded_price
    }, {
        "name": "supplyRate",
        "timestamp": timestamp,
        "value": encoded_supply_rate
    }]

    return feeds

def get_aave_data(event_data, web3_provider, timestamp, event):
    value = event['args'][event_data['valuable_name']]

    print("chain_id: " + str(web3_provider.eth.chain_id))
    print('contract address: ' + event_data['src_contract'].address)
    print(f'name: ' + event_data['valuable_name'])
    print ("value: " + str(value))

    # encode data
    encoded_data = encode(['uint256'], [value])
    feeds = [{
        "name": event_data['valuable_name'],
        "timestamp": timestamp,
        "value": encoded_data
    }]
    return feeds

#Coroutine
async def log_loop(event_data, poll_interval):
    while True:
        for event in event_data['event_filter'].get_new_entries():
            web3_provider = event_data['web3_provider']
            last_block_number = get_last_block_number(web3_provider)
            block = web3_provider.eth.get_block(last_block_number)
            timestamp = block['timestamp']
            src_contract = event_data['src_contract'].address
            print(src_contract)
            feeds = []
            if src_contract == "0x39AA39c021dfbaE8faC545936693aC917d5E7563" or src_contract == "0x02e9081DfadD37A852F9a73C4d7d69e615E61334":
                feeds = get_compound_data(event_data, web3_provider, timestamp, event_data['src_chain_id'])
            elif src_contract == "0x794a61358D6845594F94dc1DB02A252b5b4814aD":
                feeds = get_aave_data(event_data, web3_provider, timestamp, event)

            f = open('Database.json')

            # returns JSON object as
            # a dictionary
            data = json.load(f)
            web3_provider = get_provider_from_chain_id(event_data['dst_chain_id'])
            contract_address = web3_provider.toChecksumAddress("0xd737408b3ce7c6559496ea0cade16a951945356b")
            contract = web3_provider.eth.contract(address=contract_address, abi=data["abi"])

            # encode array of feed data
            result = contract.functions.encode(feeds).call()

            # hash encoded data
            hash = web3_provider.solidityKeccak(['bytes'], [result])
            message = encode_defunct(hexstr=Web3.toHex(hash))

            # create signature
            signed_message = web3_provider.eth.account.sign_message(message, private_key=PRIVATE_KEY)
            signature = signed_message.signature

            # send transaction
            transaction = contract.functions.storeData(result, signature, timestamp, event_data['src_chain_id'], event_data['src_contract'].address).build_transaction({'from': "0x330C4fBDa3b1a47088934289CF6039b5bAB20e45"})
            transaction.update({ 'nonce' : web3_provider.eth.get_transaction_count('0x330C4fBDa3b1a47088934289CF6039b5bAB20e45') })
            signed_tx = web3_provider.eth.account.sign_transaction(transaction, PRIVATE_KEY)
            txn_hash = web3_provider.eth.send_raw_transaction(signed_tx.rawTransaction)
            txn_receipt = web3_provider.eth.wait_for_transaction_receipt(txn_hash)
            print(txn_receipt)
        await asyncio.sleep(poll_interval)

async def get_data():
    # get evebt_list
    event_data_list = await create_event_filters()
    # opens loop
    await asyncio.gather(*[log_loop(event_data, 1) for event_data in event_data_list])

async def create_event_filters():
    # get all document
    docs = db.collection(u'jobs').stream()
    event_filters = []
    for doc in docs:
        data = doc.to_dict()

        address = data['eventContractAddress']
        src_chain_id = data['srcChainId']

        web3_provider = get_provider_from_chain_id(src_chain_id)

        last_block_number = get_last_block_number(web3_provider)
        block = web3_provider.eth.get_block(last_block_number)
        number = block['number']

        abi = convert_abi_from_api(address, src_chain_id)
        contract_address = web3_provider.toChecksumAddress(data['srcContractAddress'])

        contract = web3_provider.eth.contract(
            address = contract_address,
            abi = abi
        )

        # get event_filter
        event_filter = event_filter = web3_provider.eth.filter('latest')
        if(src_chain_id == 137):
            event_filter = eval('contract.events.'+data['eventName']+'.createFilter(fromBlock='+ str(number)+ ')')

        # add other information
        event_filters.append({'event_filter': event_filter, 'src_contract': contract, 'valuable_name': data['valuableName'], 'dst_chain_id': data['dstChainId'], 'web3_provider': web3_provider, 'src_chain_id': src_chain_id})
    return event_filters


if __name__ == "__main__":
    asyncio.run(get_data())