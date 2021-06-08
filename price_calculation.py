from decouple import config
from web3 import Web3
import json

erc20_abi = json.loads('[{"constant": true,"inputs": [],"name": "name","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_spender","type": "address"},{"name": "_value","type": "uint256"}],"name": "approve","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [],"name": "totalSupply","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_from","type": "address"},{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transferFrom","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [],"name": "decimals","outputs": [{"name": "","type": "uint8"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [{"name": "_owner","type": "address"}],"name": "balanceOf","outputs": [{"name": "balance","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": true,"inputs": [],"name": "symbol","outputs": [{"name": "","type": "string"}],"payable": false,"stateMutability": "view","type": "function"},{"constant": false,"inputs": [{"name": "_to","type": "address"},{"name": "_value","type": "uint256"}],"name": "transfer","outputs": [{"name": "","type": "bool"}],"payable": false,"stateMutability": "nonpayable","type": "function"},{"constant": true,"inputs": [{"name": "_owner","type": "address"},{"name": "_spender","type": "address"}],"name": "allowance","outputs": [{"name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"},{"payable": true,"stateMutability": "payable","type": "fallback"},{"anonymous": false,"inputs": [{"indexed": true,"name": "owner","type": "address"},{"indexed": true,"name": "spender","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Approval","type": "event"},{"anonymous": false,"inputs": [{"indexed": true,"name": "from","type": "address"},{"indexed": true,"name": "to","type": "address"},{"indexed": false,"name": "value","type": "uint256"}],"name": "Transfer","type": "event"}]')
web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))

bnb = web3.eth.contract((Web3.toChecksumAddress("0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c")), abi=erc20_abi)
busd = web3.eth.contract((Web3.toChecksumAddress("0xe9e7cea3dedca5984780bafc599bd69add087d56")), abi=erc20_abi)
myToken = web3.eth.contract((Web3.toChecksumAddress(config('my_bep20_token_address'))), abi=erc20_abi)

def getPrice():
    # Get bnb price in usd
    bnb_balance = bnb.functions.balanceOf(Web3.toChecksumAddress("0x1b96b92314c44b159149f7e0303511fb2fc4774f")).call()
    busd_balance = busd.functions.balanceOf(Web3.toChecksumAddress("0x1b96b92314c44b159149f7e0303511fb2fc4774f")).call()
    bnb_price = busd_balance / bnb_balance

    # Get the price of the token in bnb
    bnb_balance = bnb.functions.balanceOf(Web3.toChecksumAddress(config('my_bep20_wbnb_pair_address'))).call()
    myToken_balance = myToken.functions.balanceOf(Web3.toChecksumAddress(config('my_bep20_wbnb_pair_address'))).call()
    token_price_in_bnb = (bnb_balance / 10**18) / (myToken_balance / 10**int(config('my_token_decimals')))

    # Token price in usd
    my_token_price = token_price_in_bnb * bnb_price

    return f"{my_token_price:.10f}"  # 10 to display 10 decimals in the price
