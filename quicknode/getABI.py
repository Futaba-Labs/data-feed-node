from web3 import Web3 
import urllib.request, json 

api_optimism = "https://api-optimistic.etherscan.io/api?module=contract&action=getabi&address=0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654&format=raw"

def convert_abi_from_api(api_link: str):
    
    etherscan_api = api_link
    with urllib.request.urlopen(etherscan_api) as url:
        data = json.load(url)
    return data
        
        
if __name__ == '__main__':
    convert_abi_from_api(api_optimism)