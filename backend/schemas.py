from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# =============================================
# WALLET SCHEMAS
# =============================================

class WalletCreate(BaseModel):
    address : str
    label   : Optional[str] = None
    chain   : str = "matic-mainnet"

class WalletResponse(BaseModel):
    id          : int
    address     : str
    label       : Optional[str]
    chain       : str
    is_active   : bool
    created_at  : datetime

    class Config:
        from_attributes = True


# =============================================
# TRANSACTION SCHEMAS
# =============================================

class TransactionResponse(BaseModel):
    id              : int
    tx_hash         : str
    wallet_address  : str
    chain           : str
    block_signed_at : Optional[datetime]
    from_address    : Optional[str]
    to_address      : Optional[str]
    value_native    : Optional[float]
    native_token    : Optional[str]
    fees_paid       : Optional[float]
    successful      : Optional[bool]
    is_reconciled   : bool

    class Config:
        from_attributes = True


# =============================================
# SUMMARY SCHEMAS
# =============================================

class WalletSummary(BaseModel):
    wallet              : str
    total_transactions  : int
    total_in_matic      : float
    total_out_matic     : float
    successful_txs      : int
    failed_txs          : int


# =============================================
# SYNC SCHEMAS
# =============================================

class SyncResponse(BaseModel):
    wallet_address  : str
    saved           : int
    skipped         : int
    status          : str


# =============================================
# GENERIC SCHEMAS
# =============================================

class MessageResponse(BaseModel):
    message : str
    success : bool = True
    