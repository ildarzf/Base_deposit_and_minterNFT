# Base_deposit_and_minterNFT

ETH Mainnet to Base Mainnet L2  and Mint NFT BASEBUILDERS

Выводит ETH через официальный контракт в Base Mainnet L2. Сумму указывается в ETH.



wallets.txt вводим приватники 1 приватник одна строчка.

Кошельки перемешиваются.

Можно использовать только в режиме депозита. Для этого поставте mint_nft = False

Если на счету в сети Басе есть средства то пробудет сминтить NFT BASEBUILDERS

###################  ИЗМЕНЯЕМЫЕ ПАРАМЕТРЫ  #################

DEP_FROM = 0.0011 # от в ETH

DEP_TO = 0.0015 # до в ETH

wal_sleep_min = 100    # минимальная задержка между кошелька

wal_sleep_max = 140    # максимальная задержка между кошелька

wal_action_sleep = 10   # время ожидания между действиями

time_to_conf = 260 #  Время ожидания подтверждения транзакции в секундках (уменьшить до 120 когда перестанет лагать BSC)

Gwei = 18  # если газ выше уходим в ожидание

rpc_base = "https://developer-access-mainnet.base.org/"   # Нода Майннет Басе

rpc_eth = "https://rpc.ankr.com/eth"    # Нода Эфира

shuffle = True # False / True Перемешивать кошельки или нет

mint_nft = True # False / True Минтить НФТ Билдера или нет. Ставим False если нужен только депозит 

###########################################################


DONATE на тесты скриптов и благодарность сюда (evm сети) : 0xe7b5cb9f137C663D07EF2539678392650c8e3645

Telegram channel https://t.me/ildar_scripts

Telegram https://t.me/ildarzf

Telegram chat https://t.me/ildarscriptschat
