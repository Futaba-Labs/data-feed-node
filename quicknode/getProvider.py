import urllib.request, json
import os
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware


load_dotenv()

OPTIMISIM_PROVIDER = os.getenv('OPTIMISIM_PROVIDER')
POLYGON_PROVIDER = os.getenv('POLYGON_PROVIDER')
AURORA_PROVIDER = os.getenv('AURORA_PROVIDER')
CRONOS_PROVIDER = os.getenv('CRONOS_PROVIDER')
OASIS_PROVIDER = os.getenv('OASIS_PROVIDER')

POLYGON_TESTNET_PROVIDER = os.getenv('POLYGON_TESTNET_PROVIDER')

def get_provider_from_chain_id(chainId):
    web3_provider = Web3(Web3.HTTPProvider(POLYGON_TESTNET_PROVIDER))
    if chainId == 10:
        web3_provider = Web3(Web3.HTTPProvider(OPTIMISIM_PROVIDER))
    elif chainId == 1313161554:
        web3_provider = Web3(Web3.HTTPProvider(AURORA_PROVIDER))
    elif chainId == 25:
        web3_provider = Web3(Web3.HTTPProvider(CRONOS_PROVIDER))
    elif chainId == 42262:
        web3_provider = Web3(Web3.HTTPProvider(OASIS_PROVIDER))
    elif chainId == 137:
        web3_provider = Web3(Web3.HTTPProvider(POLYGON_PROVIDER))

    web3_provider.middleware_onion.inject(geth_poa_middleware, layer=0)

    return web3_provider

if __name__ == '__main__':
    # optimism provider
    provider = get_provider_from_chain_id(10)
    print(provider.eth.account)
