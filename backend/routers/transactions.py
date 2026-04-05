from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional

from database import get_db, Transaction
from schemas import TransactionResponse, WalletSummary
from etl_service import get_wallet_summary

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


# ─── GET transactions for a wallet ────────────────────
@router.get("/{wallet_address}", response_model=List[TransactionResponse])
def get_transactions(
    wallet_address  : str,
    limit           : int = Query(default=25, le=100),
    offset          : int = Query(default=0),
    successful_only : bool = Query(default=False),
    db              : Session = Depends(get_db)
):
    """
    Get transactions for a wallet.
    Supports pagination with limit/offset.
    """
    query = db.query(Transaction).filter_by(
        wallet_address=wallet_address.lower()
    )
    
    if successful_only:
        query = query.filter_by(successful=True)
    
    transactions = query\
        .order_by(desc(Transaction.block_signed_at))\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail=f"No transactions found for {wallet_address}"
        )
    
    return transactions


# ─── GET summary for a wallet ─────────────────────────
@router.get("/{wallet_address}/summary", response_model=WalletSummary)
def get_summary(wallet_address: str, db: Session = Depends(get_db)):
    """Get analytics summary for a wallet"""
    
    summary = get_wallet_summary(wallet_address, db)
    
    if "message" in summary:
        raise HTTPException(
            status_code=404,
            detail=summary["message"]
        )
    return summary


# ─── GET single transaction by hash ───────────────────
@router.get("/tx/{tx_hash}", response_model=TransactionResponse)
def get_transaction_by_hash(tx_hash: str, db: Session = Depends(get_db)):
    """Get a specific transaction by hash"""
    
    tx = db.query(Transaction).filter_by(tx_hash=tx_hash).first()
    
    if not tx:
        raise HTTPException(
            status_code=404,
            detail=f"Transaction {tx_hash} not found"
        )
    return tx
