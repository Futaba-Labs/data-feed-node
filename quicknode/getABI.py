import urllib.request, json

def convert_abi_from_api(address, chainId):
    scan_api = ""
    data = ""
    if chainId == 10:
        scan_api = "https://api-optimistic.etherscan.io/api?module=contract&action=getabi&address={address}&apikey=K15I7CGDEG5T64ER36WVG24S9Q233AUZBM&format=raw".format(address=address)
    elif chainId == 1:
        scan_api = "https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey=X24HUKIK8QWZ9GA5RURI99XJXF7KAVCP7C".format(address=address)
    elif chainId == 1313161554:
        scan_api = "https://api.aurorascan.dev/api?module=contract&action=getabi&address={address}&apikey=GWZB6NSGDZQS8W1IB3RNDWUAYZS3N71TEU".format(address=address)
    elif chainId == 25:
        scan_api = "https://api.cronoscan.com/api?module=contract&action=getabi&address={address}&apikey=NAWI1MPCSJA2QNMGYE5GDAIYEVNH8NJUJI".format(address=address)
    elif chainId == 42262:
        scan_api = "https://explorer.emerald.oasis.doorgod.io/api?module=contract&action=getabi&address={address}".format(address=address)
    elif chainId == 137:
        scan_api = "https://api.polygonscan.com/api?module=contract&action=getabi&address={address}&apikey=Q9P7I3IHB6JFD8WE3378JST95NY61NGEGW".format(address=address)
    elif chainId == 1284:
        scan_api = "https://api-moonbeam.moonscan.io/api?module=contract&action=getabi&address={address}&apikey=T5DM6VE4H2WP1BKFI5THMQB5G9KSADY7T3".format(address=address)
    
    print(scan_api)
    with urllib.request.urlopen(scan_api) as url:
        data = json.load(url)
        if(chainId != 10):
            data = data['result']

    return data

if __name__ == '__main__':
    # optimism aave contract
    abi = convert_abi_from_api("0x73c46FBd11759fd4Be5b6f0EaBC6308782d157fF", 1313161554)
    print(abi)
