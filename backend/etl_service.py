import requests
import os
from datetime import datetime
from sqlalchemy.orm import Session
from database import Transaction, TokenTransfer, SyncStatus, Wallet
from dotenv import load_dotenv

load_dotenv()

API_KEY     = os.getenv("COVALENT_API_KEY")
CHAIN_ID    = "matic-mainnet"
NATIVE_TOKEN = "MATIC"

def fetch_and_save_transactions(wallet_address: str, db: Session, page_size: int = 25):
    """
    Fetch transactions from Covalent API
    and save them to PostgreSQL database
    """
    print(f"\n🔄 Syncing wallet: {wallet_address}")
    
    # Update sync status to running
    sync = db.query(SyncStatus).filter_by(wallet_address=wallet_address).first()
    if not sync:
        sync = SyncStatus(wallet_address=wallet_address, chain=CHAIN_ID)
        db.add(sync)
    
    sync.status = "running"
    db.commit()
    
    try:
        # Fetch from Covalent
        url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v3/"
        response = requests.get(
            url,
            auth=(API_KEY, ""),
            params={"page-size": page_size}
        )
        
        data = response.json()
        transactions = data["data"]["items"]
        
        saved_count = 0
        skipped_count = 0
        
        for tx in transactions:
            # Check if transaction already exists
            existing = db.query(Transaction).filter_by(
                tx_hash=tx["tx_hash"]
            ).first()
            
            if existing:
                skipped_count += 1
                continue
            
            # Parse and save transaction
            new_tx = Transaction(
                tx_hash         = tx["tx_hash"],
                wallet_address  = wallet_address.lower(),
                chain           = CHAIN_ID,
                block_height    = tx.get("block_height"),
                block_signed_at = datetime.fromisoformat(
                    tx["block_signed_at"].replace("Z", "+00:00")
                ),
                from_address    = tx.get("from_address"),
                to_address      = tx.get("to_address"),
                value_raw       = tx.get("value"),
                value_native    = int(tx.get("value", 0)) / 1e18,
                native_token    = NATIVE_TOKEN,
                gas_used        = tx.get("gas_spent"),
                fees_paid       = int(tx.get("fees_paid", 0)) / 1e18,
                successful      = tx.get("successful"),
                raw_data        = tx
            )
            db.add(new_tx)
            saved_count += 1
        
        db.commit()
        
        # Update sync status to completed
        sync.status             = "completed"
        sync.last_synced_at     = datetime.now()
        sync.total_tx_fetched   += saved_count
        db.commit()
        
        print(f"✅ Sync complete!")
        print(f"   Saved  : {saved_count} new transactions")
        print(f"   Skipped: {skipped_count} already existing")
        
        return {"saved": saved_count, "skipped": skipped_count}
        
    except Exception as e:
        sync.status = "failed"
        sync.error_message = str(e)
        db.commit()
        print(f"❌ Error: {e}")
        raise e


def get_wallet_summary(wallet_address: str, db: Session):
    """Get summary stats for a wallet from DB"""
    
    transactions = db.query(Transaction).filter_by(
        wallet_address=wallet_address.lower()
    ).all()
    
    if not transactions:
        return {"message": "No transactions found"}
    
    total_in  = sum(
        float(tx.value_native) 
        for tx in transactions 
        if tx.to_address and tx.to_address.lower() == wallet_address.lower()
    )
    total_out = sum(
        float(tx.value_native) 
        for tx in transactions 
        if tx.from_address and tx.from_address.lower() == wallet_address.lower()
    )
    
    return {
        "wallet"            : wallet_address,
        "total_transactions": len(transactions),
        "total_in_matic"    : round(total_in, 6),
        "total_out_matic"   : round(total_out, 6),
        "successful_txs"    : sum(1 for tx in transactions if tx.successful),
        "failed_txs"        : sum(1 for tx in transactions if not tx.successful)
    }