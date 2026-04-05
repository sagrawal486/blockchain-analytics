import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("COVALENT_API_KEY")

# This is a well-known Polygon wallet for testing
TEST_WALLET = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
CHAIN_ID = "matic-mainnet"  # Polygon

def get_wallet_transactions(wallet_address: str):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v3/"
    
    response = requests.get(
        url,
        auth=(API_KEY, ""),  # Covalent uses API key as username
        params={
            "page-size": 10  # Get last 10 transactions
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        transactions = data["data"]["items"]
        
        print(f"\n✅ Found {len(transactions)} transactions for wallet:")
        print(f"   {wallet_address}\n")
        
        for i, tx in enumerate(transactions[:5], 1):  # Show first 5
            print(f"Transaction {i}:")
            print(f"  Hash     : {tx['tx_hash']}")
            print(f"  Date     : {tx['block_signed_at']}")
            print(f"  From     : {tx['from_address']}")
            print(f"  To       : {tx['to_address']}")
            print(f"  Value    : {int(tx['value']) / 1e18:.6f} MATIC")
            print(f"  Success  : {tx['successful']}")
            print("-" * 60)
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    get_wallet_transactions(TEST_WALLET)
    