from sqlalchemy import create_engine, Column, String, Boolean, BigInteger
from sqlalchemy import Numeric, Integer, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Railway Postgres uses *.rlwy.net; public URLs often omit the substring "railway".
_use_pg_ssl = bool(
    os.getenv("RAILWAY_ENVIRONMENT")
    or (DATABASE_URL and "rlwy.net" in DATABASE_URL)
    or (DATABASE_URL and "railway" in DATABASE_URL.lower())
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"} if _use_pg_ssl else {},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# =============================================
# ORM Models (Python classes = DB tables)
# =============================================

class Wallet(Base):
    __tablename__ = "wallets"
    
    id          = Column(Integer, primary_key=True, index=True)
    address     = Column(String(42), unique=True, nullable=False)
    label       = Column(String(100))
    chain       = Column(String(50), nullable=False)
    is_active   = Column(Boolean, default=True)
    created_at  = Column(TIMESTAMP, server_default=func.now())


class Transaction(Base):
    __tablename__ = "transactions"
    
    id              = Column(Integer, primary_key=True, index=True)
    tx_hash         = Column(String(66), unique=True, nullable=False)
    wallet_address  = Column(String(42), nullable=False)
    chain           = Column(String(50), nullable=False)
    block_height    = Column(BigInteger)
    block_signed_at = Column(TIMESTAMP)
    from_address    = Column(String(42))
    to_address      = Column(String(42))
    value_raw       = Column(Numeric(78, 0))
    value_native    = Column(Numeric(36, 18))
    native_token    = Column(String(20))
    gas_used        = Column(BigInteger)
    fees_paid       = Column(Numeric(36, 18))
    successful      = Column(Boolean)
    is_reconciled   = Column(Boolean, default=False)
    raw_data        = Column(JSONB)
    created_at      = Column(TIMESTAMP, server_default=func.now())


class TokenTransfer(Base):
    __tablename__ = "token_transfers"
    
    id                  = Column(Integer, primary_key=True)
    tx_hash             = Column(String(66), nullable=False)
    wallet_address      = Column(String(42), nullable=False)
    token_name          = Column(String(100))
    token_symbol        = Column(String(20))
    from_address        = Column(String(42))
    to_address          = Column(String(42))
    amount_formatted    = Column(Numeric(36, 6))
    transfer_type       = Column(String(10))
    block_signed_at     = Column(TIMESTAMP)
    created_at          = Column(TIMESTAMP, server_default=func.now())


class SyncStatus(Base):
    __tablename__ = "sync_status"
    
    id                  = Column(Integer, primary_key=True)
    wallet_address      = Column(String(42), nullable=False)
    chain               = Column(String(50), nullable=False)
    last_synced_at      = Column(TIMESTAMP)
    total_tx_fetched    = Column(Integer, default=0)
    status              = Column(String(20), default="pending")
    error_message       = Column(Text)


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()