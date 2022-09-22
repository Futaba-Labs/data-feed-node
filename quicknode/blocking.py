import logging
import datetime
from requests import ReadTimeout
from web3.exceptions import BlockNotFound
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv


#Variables 
web3_optimism = Web3(Web3.HTTPProvider("https://opt-mainnet.g.alchemy.com/v2/"))
web3_optimism.middleware_onion.inject(geth_poa_middleware, layer=0)

'''
Timestamping blocks 
'''

def get_last_block_number():
    last_block_number = web3_optimism.eth.block_number
    return last_block_number

def block_per_timestamp(timestamp: int):
    print(web3_optimism.clientVersion)
    
    block_found = False
    last_block_number = get_last_block_number()
    # print(last_block_number)
    timestamp = 1630454400
    close_in_seconds = 600
    
    block = web3_optimism.eth.get_block(last_block_number)
    print(block['number'])
        # difference_in_seconds = int((timestamp - block['timestamp'])/1000)
        # print(difference_in_seconds)
        # block_found = abs(difference_in_seconds) < close_in_seconds
        # print(block_found)
        
        # if block_found:
        #     print(last_block_number)
        #     return last_block_number
            
        
    #     if difference_in_seconds < 0:
    #         last_block_number //= 2
            
    #     else:
    #         last_block_number = int(last_block_number * 1.5) + 1
            
            
if __name__ == '__main__': 
   block_per_timestamp(1630454400)

    
    
   



        
    

