from web3 import Web3
import requests, json, time, secrets
from decimal import Decimal

# web3 = Web3(Web3.HTTPProvider("https://carrot.megaeth.com/rpc"))
web3 = Web3(Web3.HTTPProvider("https://carrot.megaeth.com/rpc"))
chainId = web3.eth.chain_id
# Ensure the connection is made
if not web3.is_connected():
    print("Failed to connect to network")
    exit()

# Log to a text file
def log(txt):
    with open('datamegaethwallet.txt', "a") as f:
        f.write(txt + '\n')
            
# Send all ether from one address to another
def send_all_ether(sender_address, sender_private_key, recipient_address):
    try:
        # Get sender's balance
        balance = web3.eth.get_balance(sender_address)
        print(f"Sender balance: {web3.from_wei(balance, 'ether')} ETH")
        
        # Use the sender's full balance, excluding the gas cost
        # Get current gas fee using EIP-1559 parameters
        gas_data = int(web3.eth.gas_price*Decimal(2.0))  # For EIP-1559: web3.eth.gas_price returns maxFeePerGas
        max_fee_per_gas = gas_data  # You can adjust this if you want to include more logic
        
        # Standard gas limit for ETH transfer
        gas_limit = 22000
        
        # Calculate the gas cost
        gas_cost = gas_limit * max_fee_per_gas
        
        # Subtract the gas cost from the balance to ensure the sender has enough ETH
        amount_to_send = balance - gas_cost
        
        if amount_to_send <= 0:
            print(f"Not enough balance to cover gas cost. Balance: {web3.from_wei(balance, 'ether')} ETH")
            return
        
        # Build the transaction with EIP-1559 parameters
        transaction = {
            'to': recipient_address,
            'value': amount_to_send,  # Send all Ether after gas cost
            'gas': 21000,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_fee_per_gas,
            'nonce': web3.eth.get_transaction_count(sender_address),
            'chainId': web3.eth.chain_id  # Automatically use the current chain ID
        }
        
        # Send the transaction
        print(f"Processing send {web3.from_wei(amount_to_send, 'ether')} ETH To {recipient_address}")
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(transaction, sender_private_key).rawTransaction)
        
        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction sent! Tx Hash: {web3.to_hex(tx_hash)}")
    
    except Exception as e:
        print(f"Error while sending eth: {e}")

def req_faucet(token, addr, proxy=None):
    try:
        url = f"https://carrot.megaeth.com/claim"
        headers = {
            "content-type": "application/json",
            "origin": "https://testnet.megaeth.com",
            "referer": "https://testnet.megaeth.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        
        # Prepare the proxy settings if provided
        proxies = {
            "http": proxy,
            "https": proxy
        } if proxy else None

        # Data for the API request
        data = {
            "addr": addr,
            "token": token
        }

        # Send POST request with the optional proxy
        response = requests.post(url, headers=headers, json=data, proxies=proxies)

        # Return the JSON response
        return response.json()
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
        
def get_token(apikey, idreq, proxy=None):
    try:
        url = f"https://api.sctg.xyz/res.php?key={apikey}&id={idreq}&action=get"

        response = requests.get(url)
        
        # Return the JSON response
        return response.text
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
        
def get_id(apikey, proxy=None):
    try:
        url = "https://api.sctg.xyz/in.php"

        payload = {
            "key": apikey,
            "method": "turnstile",
            "pageurl": "https://testnet.megaeth.com/",
            "sitekey": "0x4AAAAAABA4JXCaw9E2Py-9"
        }
        headers = {"content-type": "application/x-www-form-urlencoded"}

        response = requests.post(url, data=payload, headers=headers)
        return response.text
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

recipient = input('input address evm recipient megaeth testnet : ')
proxy = input('input http rotate proxy [ http://user:pass@ip:port : ')
apikey = input('input apikey https://sctg.xyz/ : ')
while True:
    try:
        sender = web3.eth.account.from_key(secrets.token_hex(32))
        print(f'Processing get id solve turnstile...')
        getid = get_id(apikey)
        
        if getid[:2] == "OK":
            print(f'id : {getid[3:]}')
            print(f'Processing get token solve turnstile...')
            
            # Loop to retry getting the token until it's ready
            gettoken = ""
            while gettoken != "OK":
                gettoken = get_token(apikey, getid[3:])
                if gettoken == "CAPCHA_NOT_READY":
                    print(f'Captcha not ready, retrying...')
                    time.sleep(2)  # Wait for a while before retrying (adjust as needed)
                elif gettoken[:2] == "OK":
                    print(f'token : {gettoken[3:]}')
                    time.sleep(1)
                    reqfaucet = req_faucet(gettoken[3:], sender.address, proxy)
                    txhash = reqfaucet["txhash"]
                    
                    if not txhash or txhash == "None" or txhash == "":
                        print(f'Get faucet failed for address {sender.address}')
                        print(f'{reqfaucet}')
                    else:
                        print(f'Get faucet success for address {sender.address}')
                        print(f'txhash : {txhash}')
                        log(f'{sender.address}|{web3.to_hex(sender.key)}')
                        time.sleep(1)
                        send_all_ether(sender.address, sender.key, web3.to_checksum_address(recipient))
                else:
                    print(f'Get token solve turnstile failed!')
        else:
            print(f'Get id solve turnstile failed!')
    except Exception as e:
        print(str(e))