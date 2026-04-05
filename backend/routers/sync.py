from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db, Wallet, SyncStatus
from schemas import SyncResponse
from etl_service import fetch_and_save_transactions

router = APIRouter(
    prefix="/sync",
    tags=["Sync"]
)


# ─── POST trigger sync for a wallet ───────────────────
@router.post("/{wallet_address}", response_model=SyncResponse)
def sync_wallet(
    wallet_address      : str,
    background_tasks    : BackgroundTasks,
    db                  : Session = Depends(get_db)
):
    """
    Trigger a sync for a wallet.
    Fetches latest transactions from Covalent
    and saves to database.
    """
    # Check wallet exists
    wallet = db.query(Wallet).filter_by(
        address=wallet_address.lower()
    ).first()
    
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {wallet_address} not found. Add it first via POST /wallets"
        )
    
    # Run sync
    result = fetch_and_save_transactions(wallet_address, db)
    
    return SyncResponse(
        wallet_address  = wallet_address,
        saved           = result["saved"],
        skipped         = result["skipped"],
        status          = "completed"
    )


# ─── GET sync status for a wallet ─────────────────────
@router.get("/{wallet_address}/status")
def get_sync_status(wallet_address: str, db: Session = Depends(get_db)):
    """Get last sync status for a wallet"""
    
    sync = db.query(SyncStatus).filter_by(
        wallet_address=wallet_address.lower()
    ).first()
    
    if not sync:
        return {
            "wallet_address"    : wallet_address,
            "status"            : "never_synced",
            "last_synced_at"    : None,
            "total_tx_fetched"  : 0
        }
    
    return {
        "wallet_address"    : wallet_address,
        "status"            : sync.status,
        "last_synced_at"    : sync.last_synced_at,
        "total_tx_fetched"  : sync.total_tx_fetched,
        "error_message"     : sync.error_message
    }