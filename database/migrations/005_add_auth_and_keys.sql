-- database/migrations/005_add_auth_and_keys.sql

-- Enable cryptographic extensions for password hashing validation inside PostgreSQL if needed
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Extend users table to securely support decentralized authentication & platform authorization roles
ALTER TABLE users 
    ADD COLUMN password_hash VARCHAR(255) NOT NULL DEFAULT '$2b$12$DummyHashForExistingMigrationSafety.PlaceholderValue',
    ADD COLUMN account_role VARCHAR(50) NOT NULL DEFAULT 'operator' CHECK (account_role IN ('super_admin', 'architect', 'enterprise_supervisor', 'operator')),
    ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE,
    ADD COLUMN last_login_at TIMESTAMP WITH TIME ZONE;

-- Establish a high-frequency API Key Registry to clear automated edge nodes (such as standalone WebRTC boxes)
CREATE TABLE developer_api_keys (
    key_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    key_prefix VARCHAR(12) NOT NULL,
    hashed_secret_token VARCHAR(255) NOT NULL UNIQUE,
    assigned_label VARCHAR(100) NOT NULL DEFAULT 'Default Edge Deployment Node',
    rate_limit_per_minute INT NOT NULL DEFAULT 120,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexing layers to guarantee sub-millisecond lookups during high-frequency real-time authorization checks
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_api_keys_hash ON developer_api_keys(hashed_secret_token);

-- Comment metadata for operational clarity across distributed database clusters
COMMENT ON COLUMN users.account_role IS 'super_admin = Full Grid control, architect = David Fabian Cadelinia / Custom Persona tier, operator = Standard student/employee simulator';
