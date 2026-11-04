-- Migration 034: Advanced Monetization, Reseller Mesh, and Yield Ledger Tables
BEGIN;

-- 1. Create a registry for White-Label Resellers and Managed Service Providers (MSPs)
CREATE TABLE IF NOT EXISTS white_label_resellers (
    reseller_id VARCHAR(64) PRIMARY KEY,
    company_name VARCHAR(128) NOT NULL,
    custom_domain VARCHAR(255) UNIQUE,
    wholesale_rate_per_minute NUMERIC(6, 4) DEFAULT 0.1200,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Extend billing_vault to track specific wallet classifications and pre-funded balances
ALTER TABLE billing_vault ADD COLUMN IF NOT EXISTS wallet_type VARCHAR(32) DEFAULT 'retail_client'; -- 'retail_client', 'developer_api', 'white_label_msp', 'system_treasury'
ALTER TABLE billing_vault ADD COLUMN IF NOT EXISTS total_compute_minutes_used NUMERIC(12, 2) DEFAULT 0.00;

-- 3. Create a verification log for Institutional Insurance Certificates
CREATE TABLE IF NOT EXISTS insurance_compliance_registry (
    certificate_id VARCHAR(32) PRIMARY KEY,
    client_id VARCHAR(64) NOT NULL,
    underwriter_id VARCHAR(64) NOT NULL,
    composure_score_percentage NUMERIC(5, 2) NOT NULL,
    is_active_policy BOOLEAN DEFAULT TRUE,
    issued_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create an audit table for High-Frequency Yield Farming and Compute Arbitrage
CREATE TABLE IF NOT EXISTS high_frequency_yield_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_id VARCHAR(32) NOT NULL,
    yield_source VARCHAR(32) NOT NULL, -- 'api_bandwidth_resell', 'idle_render_farming'
    amount_earned_usd NUMERIC(12, 6) NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optimize telemetry lookup loops across all multi-angle transactional paths
CREATE INDEX IF NOT EXISTS idx_resellers_domain ON white_label_resellers(custom_domain);
CREATE INDEX IF NOT EXISTS idx_insurance_client ON insurance_compliance_registry(client_id);
CREATE INDEX IF NOT EXISTS idx_yield_timestamp ON high_frequency_yield_log(recorded_at);

-- Seed the central System Treasury wallet so the High-Frequency Yield loops can deposit cash immediately
INSERT INTO billing_vault (client_id, wallet_type, ledger_balance, active)
VALUES ('mrg_system_treasury', 'system_treasury', 0.00, TRUE)
ON CONFLICT (client_id) DO NOTHING;COMMIT;
