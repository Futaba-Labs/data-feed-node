from getABI import convert_abi_from_api
from web3 import Web3 
import asyncio
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
from eth_account import Account
from eth_abi import encode


web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/bjsw4mIncmXszy3-UoYdPnvlQb6b6Wep"))
web3_mumbai = Web3(Web3.HTTPProvider("https://polygon-mumbai.g.alchemy.com/v2/eXWIi7Ku5cbVWKDb6IcY9bIyJfMkxv9R"))
web3_optimism.middleware_onion.inject(geth_poa_middleware, layer=0)
web3_mumbai.middleware_onion.inject(geth_poa_middleware, layer=0)

DB_MUMBAI = "0xd737408b3CE7c6559496ea0cAde16A951945356b"

PRIV="5034f6fc81f0fb42429875413da341faf69888122913159b2aa15d3e98f37bb9"



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


## ------ ONLY FOR TESTING  -------

# def encoding():
    
#     liquidity_encoded = encode(['uint256'], [2302323])
#     liquidity_name = encode(['string'], ['liquidityRate'])
#     timestamp = 20000
#     feeds = (liquidity_name , liquidity_encoded, timestamp)
#     # print(feeds)
    
#     e = encode(['(bytes,bytes,uint256)'], [feeds])
#     hash = str(web3_optimism.solidityKeccak(['bytes'], ['0x' + e.hex()])) 
#     #Sign message
#     pair = create_account()
#     encoded = encode_defunct(text = hash)
#     signed_message = web3_optimism.eth.account.sign_message(encoded, private_key=pair[1])
#     signature = signed_message.signature.hex()
#     # data = encode(['string'], [signature])
#     priv = "5034f6fc81f0fb42429875413da341faf69888122913159b2aa15d3e98f37bb9"
#     # pair = create_account()
#     nonce = web3_mumbai.eth.getTransactionCount("0xA071F1BC494507aeF4bc5038B8922641c320d486")
#     print(nonce)
#     tx = {
#         'from' : "0xA071F1BC494507aeF4bc5038B8922641c320d486",
#         'nonce' : nonce,
#         'maxFeePerGas' : 2000000000,
#         'maxPriorityFeePerGas' : 1000000000,
#         'gas' : 100000,
#         'to' : DB_MUMBAI,
#         'value' : 2000000000,
#         'data': signature,
#         'chainId' : 80001
#     }                   
                                        
#     signed_tx = web3_mumbai.eth.account.sign_transaction(tx, priv)
#     print(signed_tx)
#     tx_hash = web3_mumbai.eth.sendRawTransaction(signed_tx.rawTransaction)
#     print(tx_hash)
    
#     #get transaction hash
#     print(web3_mumbai.toHex(tx_hash))

    

#Coroutine
async def log_loop(event_data, poll_interval):
    last_block_number = get_last_block_number()
    block = web3_optimism.eth.get_block(last_block_number)
    number = block['number']
    event_filter = contract_aave.events.ReserveDataUpdated.createFilter(fromBlock= number )
    while True:
        for event in event_data.get_new_entries():
            timestamp = block['timestamp']
            value = event['args'][event_data['valuable_name']]
            print(f'name: ' + event_data['valuable_name'])
            print ("value: " + str(value))
            
            #encode data
            encoded_data = encode(['uint256'], [value])
            feeds = [{
                "name": event_data['valuable_name'],
                "timestamp": timestamp,
                "value": encoded_data
            }]
            contract_address = web3_mumbai.toChecksumAddress("0xd737408b3ce7c6559496ea0cade16a951945356b")
            abi = convert_abi_from_api(api_pool)
            contract = web3_mumbai.eth.contract(address = contract_address, abi=abi)

            # encode array of feed data
            result = contract.functions.encode(feeds).call()
            print(result)
            
            # hash encoded data
            hash = web3_optimism.solidityKeccak(['bytes'], [result])
            message = encode_defunct(hexstr=Web3.toHex(hash))
            
            #create signature
            signed_message = web3_mumbai.eth.account.sign_message(message, private_key=PRIV)
            signature = signed_message.signature
            
            #send transaction
            transaction = contract.functions.storeData(result, signature, timestamp, )
            
            
            
            



            
            



            
            
            
            liquidityRate = ReserveDataUpdated['args']['liquidityRate']
            liquidity = int(web3_optimism.fromWei(liquidityRate, 'ether'))
            liquidity_encoded = encode(['uint256'], [liquidity])
            # liquidity_name = encode(['string'], ['liquidityRate'])
            liquidity_name = 'liquidityRate'
            
            #Encode array 
            feeds = [(liquidity_name ,timestamp, liquidity_encoded)]
            e = encode(['(string,uint256,bytes)[]'], [feeds])
            
            #Hash
            hash = str(web3_optimism.solidityKeccak(['bytes'], ['0x' + e.hex()]))
            
            #Sign message
            pair = create_account()
            encoded = encode_defunct(text = hash)
            signed_message = web3_optimism.eth.account.sign_message(encoded, private_key=pair[1])
            print(signed_message)
            print( "--------------------------------------------------" )
            signature = signed_message.signature.hex()
            print(f"Signaure is signature is : {signature}")
            return {"signature" : signature, "data_encoded" : e}
        

            
        
async def get_data():
    last_block_number = get_last_block_number()
    block = web3_optimism.eth.get_block(last_block_number)
    number = block['number']
    timestamp = block['timestamp']
    event_filter = contract_aave.events.ReserveDataUpdated.createFilter(fromBlock= number )
    data_acquisition = await asyncio.gather(log_loop(event_filter, 2))
    data = data_acquisition[0]
    array_encoded = data["data_encoded"]
    signature = data["signature"]
    
    priv = "5034f6fc81f0fb42429875413da341faf69888122913159b2aa15d3e98f37bb9"
    pair = create_account()
    nonce = web3_mumbai.eth.getTransactionCount("0xA071F1BC494507aeF4bc5038B8922641c320d486")
    print(nonce)
    tx = {
        'from' : "0xA071F1BC494507aeF4bc5038B8922641c320d486",
        'nonce' : nonce,
        'maxFeePerGas' : 3815333396 ,
        'maxPriorityFeePerGas' : 3815333382,
        'gas' : 100000,
        'to' : DB_MUMBAI,
        'value' : 6000000000000000,
        # 'signature': signature,
        # 'timestamp': timestamp,
        'data': array_encoded,
        'chainId' : 80001
    }                   
                                        
    signed_tx = web3_mumbai.eth.account.sign_transaction(tx, priv)
    print(signed_tx)
    tx_hash = web3_mumbai.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(tx_hash)
    
    # get transaction hash
    print(web3_mumbai.toHex(tx_hash))



        
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
    # encoding()


 


        