from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Wallet
from schemas import WalletCreate, WalletResponse, MessageResponse

router = APIRouter(
    prefix="/wallets",
    tags=["Wallets"]
)


# ─── GET all wallets ───────────────────────────────────
@router.get("/", response_model=List[WalletResponse])
def get_all_wallets(db: Session = Depends(get_db)):
    """Get all monitored wallets"""
    wallets = db.query(Wallet).filter_by(is_active=True).all()
    return wallets


# ─── POST add new wallet ───────────────────────────────
@router.post("/", response_model=WalletResponse)
def add_wallet(wallet: WalletCreate, db: Session = Depends(get_db)):
    """Add a new wallet to monitor"""
    
    # Check if wallet already exists
    existing = db.query(Wallet).filter_by(
        address=wallet.address.lower()
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet {wallet.address} already exists"
        )
    
    new_wallet = Wallet(
        address = wallet.address.lower(),
        label   = wallet.label,
        chain   = wallet.chain
    )
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)
    
    return new_wallet


# ─── GET single wallet ─────────────────────────────────
@router.get("/{address}", response_model=WalletResponse)
def get_wallet(address: str, db: Session = Depends(get_db)):
    """Get a specific wallet by address"""
    
    wallet = db.query(Wallet).filter_by(
        address=address.lower()
    ).first()
    
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {address} not found"
        )
    return wallet


# ─── DELETE wallet ─────────────────────────────────────
@router.delete("/{address}", response_model=MessageResponse)
def delete_wallet(address: str, db: Session = Depends(get_db)):
    """Deactivate a wallet (soft delete)"""
    
    wallet = db.query(Wallet).filter_by(
        address=address.lower()
    ).first()
    
    if not wallet:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet {address} not found"
        )
    
    wallet.is_active = False
    db.commit()
    
    return {"message": f"Wallet {address} deactivated", "success": True}
