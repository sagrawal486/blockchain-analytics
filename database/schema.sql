-- =============================================
-- BLOCKCHAIN ANALYTICS DATABASE SCHEMA
-- =============================================

-- 1. Wallets Table (wallets we are monitoring)
CREATE TABLE IF NOT EXISTS wallets (
    id              SERIAL PRIMARY KEY,
    address         VARCHAR(42) UNIQUE NOT NULL,
    label           VARCHAR(100),          -- e.g. "Company Treasury Wallet"
    chain           VARCHAR(50) NOT NULL,  -- e.g. "matic-mainnet"
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- 2. Transactions Table (all fetched transactions)
CREATE TABLE IF NOT EXISTS transactions (
    id                  SERIAL PRIMARY KEY,
    tx_hash             VARCHAR(66) UNIQUE NOT NULL,
    wallet_address      VARCHAR(42) NOT NULL,
    chain               VARCHAR(50) NOT NULL,
    block_height        BIGINT,
    block_signed_at     TIMESTAMP,
    from_address        VARCHAR(42),
    to_address          VARCHAR(42),
    value_raw           NUMERIC(78, 0),    -- Raw blockchain value
    value_native        NUMERIC(36, 18),   -- Human readable (e.g. 1.5 MATIC)
    native_token        VARCHAR(20),       -- e.g. MATIC, ETH
    gas_used            BIGINT,
    gas_price           NUMERIC(36, 0),
    fees_paid           NUMERIC(36, 18),
    successful          BOOLEAN,
    is_reconciled       BOOLEAN DEFAULT FALSE,  -- For ERP reconciliation later
    raw_data            JSONB,             -- Store full response for future use
    created_at          TIMESTAMP DEFAULT NOW()
);

-- 3. Token Transfers Table (ERC20 token movements)
CREATE TABLE IF NOT EXISTS token_transfers (
    id                  SERIAL PRIMARY KEY,
    tx_hash             VARCHAR(66) NOT NULL,
    wallet_address      VARCHAR(42) NOT NULL,
    contract_address    VARCHAR(42),
    token_name          VARCHAR(100),
    token_symbol        VARCHAR(20),
    token_decimals      INTEGER,
    from_address        VARCHAR(42),
    to_address          VARCHAR(42),
    amount_raw          NUMERIC(78, 0),
    amount_formatted    NUMERIC(36, 6),
    transfer_type       VARCHAR(10),       -- 'IN' or 'OUT'
    block_signed_at     TIMESTAMP,
    created_at          TIMESTAMP DEFAULT NOW()
);

-- 4. Sync Status Table (track last sync per wallet)
CREATE TABLE IF NOT EXISTS sync_status (
    id                  SERIAL PRIMARY KEY,
    wallet_address      VARCHAR(42) NOT NULL,
    chain               VARCHAR(50) NOT NULL,
    last_synced_at      TIMESTAMP,
    last_block_synced   BIGINT,
    total_tx_fetched    INTEGER DEFAULT 0,
    status              VARCHAR(20) DEFAULT 'pending',  -- pending/running/completed/failed
    error_message       TEXT,
    UNIQUE(wallet_address, chain)
);

-- =============================================
-- INDEXES (for fast queries)
-- =============================================
CREATE INDEX idx_transactions_wallet    ON transactions(wallet_address);
CREATE INDEX idx_transactions_date      ON transactions(block_signed_at);
CREATE INDEX idx_transactions_hash      ON transactions(tx_hash);
CREATE INDEX idx_token_transfers_wallet ON token_transfers(wallet_address);
CREATE INDEX idx_sync_wallet            ON sync_status(wallet_address);