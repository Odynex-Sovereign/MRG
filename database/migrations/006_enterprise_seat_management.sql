-- database/migrations/006_enterprise_seat_management.sql

-- Create an explicit registry tracking organization/corporate boundaries
CREATE TABLE IF NOT EXISTS enterprise_organizations (
    org_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_name VARCHAR(255) NOT NULL UNIQUE,
    subscription_tier VARCHAR(50) NOT NULL DEFAULT 'enterprise_crucible',
    max_seat_allocation INT NOT NULL DEFAULT 50,
    stripe_customer_id VARCHAR(255) UNIQUE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    is_subscription_active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Establish link mappings between user records and corporate seats
CREATE TABLE IF NOT EXISTS organization_seat_assignments (
    assignment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES enterprise_organizations(org_id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE UNIQUE,
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexing layers to optimize cluster seat lookup validation routines
CREATE INDEX idx_seat_assignments_org ON organization_seat_assignments(org_id);
