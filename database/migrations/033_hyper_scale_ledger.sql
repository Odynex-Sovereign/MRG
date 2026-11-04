-- Migration 033: Hyper-Scale Ledger & Unified Registry Topology
BEGIN;

-- Generate table structure for independent developer token tracking
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(64) NOT NULL,
    token_hash VARCHAR(64) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optimize telemetry lookup indexing for high-frequency token verification cycles
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(token_hash);

-- Create transactional ledger history table to maintain auditable audit records
CREATE TABLE IF NOT EXISTS structural_ledger_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id VARCHAR(64) NOT NULL,
    delta_amount NUMERIC(12, 4) NOT NULL,
    transaction_type VARCHAR(32) NOT NULL, -- 'api_consumption', 'marketplace_split', 'crypto_settle'
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMIT;
