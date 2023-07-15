import json
from web3.auto import Web3
import decimal
import random
import time
from tqdm import tqdm
from hexbytes import HexBytes
from eth_account.messages import encode_defunct




############################################  ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ  #######################################
DEP_FROM = 0.0011 # от в ETH
DEP_TO = 0.0015 # до в ETH

wal_sleep_min = 110    # минимальная задержка между кошелька
wal_sleep_max = 140    # максимальная задержка между кошелька
wal_action_sleep = 15   # время ожидания между действиями
time_to_conf = 260 #  Время ожидания подтверждения транзакции в секундках (уменьшить до 120 когда перестанет лагать BSC)
Gwei = 18  # если газ выше уходим в ожидание
rpc_base = "https://developer-access-mainnet.base.org/"   # Нода Майннет Басе
rpc_eth = "https://rpc.ankr.com/eth"    # Нода Эфира
shuffle = True # False / True Перемешивать кошельки или нет
###########################################################################################################

def sleeping(from_sleep, to_sleep):
    x = random.randint(from_sleep, to_sleep)
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))

def deposit(privat_key):
    web3 = Web3(Web3.HTTPProvider(rpc_eth))
    to_address = '0x49048044D57e1C92A77f79988d21Fa8fAF74E97e'
    account = web3.eth.account.from_key(privat_key)
    chain_id = 1 #Ethereum
    address = account.address
    nonce = web3.eth.get_transaction_count(address)
    amount_to_transfer = round(random.uniform(DEP_FROM, DEP_TO), 5)
    amount = intToDecimal(amount_to_transfer, 18)
    gasLimit = web3.eth.estimate_gas({'to': Web3.to_checksum_address(to_address), 'from': Web3.to_checksum_address(address),
                                      'value': web3.to_wei(0.0001, 'ether')}) + random.randint(10000, 30000)

    tx_built = {
        'chainId': chain_id,
        'gas': gasLimit,
        'gasPrice': web3.eth.gas_price,
        'nonce': nonce,
        'to': Web3.to_checksum_address(to_address),
        'value': int(amount)
    }

    tx_signed = web3.eth.account.sign_transaction(tx_built, privat_key)
    tx_hash = web3.eth.send_raw_transaction(tx_signed.rawTransaction)

    print(f'Deposit to Base: Transaction hash: https://etherscan.io/tx/{tx_hash.hex()}')
    print('Waiting for receipt...')
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=time_to_conf)
    print('Отправил')

def wait_dep(private_key):
    rpc_base = "https://developer-access-mainnet.base.org/"
    web3 = Web3(Web3.HTTPProvider(rpc_base))
    account = web3.eth.account.from_key(private_key).address
    while True:
        balance_gas = web3.eth.get_balance(account)
        if web3.from_wei(balance_gas, "ether") > 0:
            print('Депозит поступил', web3.from_wei(balance_gas, "ether"))
            break
        else:
            print('Ждем поступления средств')
            sleeping(10, 20)
    return balance_gas

def send_msg(private_key):
    web3 = Web3(Web3.HTTPProvider(rpc_base))
    msg = "all your base are belong to you."
    message = encode_defunct(text=msg)
    signed_message = web3.eth.account.sign_message(message, private_key=private_key)
    res = web3.eth.account.signHash(message.body, private_key)
    msg = signed_message.signature.hex()
    return msg

def mintnft(private_key, msg):
    rpc_base = "https://developer-access-mainnet.base.org/"
    web3 = Web3(Web3.HTTPProvider(rpc_base))
    mint_abi ='[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes","name":"signature","type":"bytes"}],"name":"mint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    minter = web3.to_checksum_address('0x1fc10ef15e041c5d3c54042e52eb0c54cb9b710c') # контракт base mint NFT
    minting = web3.eth.contract(address=minter, abi=mint_abi)
    address = web3.eth.account.from_key(private_key).address
    gasLimit = 100000 #web3.eth.estimate_gas({'to': web3.to_checksum_address(to_address), 'from': web3.to_checksum_address(address), 'value': web3.to_wei(0.0001, 'ether')}) + random.randint(10000, 30000)
    _signature = msg
    try:
        tx = minting.functions.mint(_signature
        ).build_transaction({
          'from': address,
          'gas': gasLimit,
          'gasPrice':  web3.eth.gas_price,
          'nonce': web3.eth.get_transaction_count(address)
          })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(address)
        print(f'Mint NFT: Transaction hash: https://basescan.org/tx/{tx_hash.hex()}')
        print('Waiting for receipt...')
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=time_to_conf)
        print('Отправил')
    except Exception as err:
        print(address, '  Ошибка.  ', err)

def minter():
    with open('wallets.txt', 'r') as f:
        wallets = f.read().splitlines()
    if shuffle:
        random.shuffle(wallets)
    for wallet in wallets:
        try:
            web3 = Web3(Web3.HTTPProvider(rpc_base))
            account = web3.eth.account.from_key(wallet).address
            print(account)
            balance_gas = web3.eth.get_balance(account)
            if web3.from_wei(balance_gas, "ether") == 0:
                while True:
                    web3 = Web3(Web3.HTTPProvider(rpc_eth))
                    current_gas_price = web3.eth.gas_price
                    current_gas_price_gwei = web3.from_wei(current_gas_price, 'gwei')
                    if round(current_gas_price_gwei, 1) <= Gwei:
                        deposit(wallet)  # Депозит в майннет Басе
                        wait_dep(wallet)  # Ждем поступления
                        break
                    else:
                        print('GWEI', round(current_gas_price_gwei, 1))
                        print('Ждем нормальный газ')
                        sleeping(20, 30)
            else:
                print('На счету ', web3.from_wei(balance_gas, "ether"))
            sleeping(wal_action_sleep, wal_action_sleep+5)
            msg = send_msg(wallet)  # Генерируем сообщение
            sleeping(2, 5)
            mintnft(wallet, msg)  # Минт
            sleeping(wal_sleep_min, wal_sleep_max)
        except Exception as err:
            print(err)


if __name__ == '__main__':
        minter()



