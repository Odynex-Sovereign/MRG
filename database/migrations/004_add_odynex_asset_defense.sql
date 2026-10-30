-- Extend the session_metrics table to account for institutional asset defense
ALTER TABLE session_metrics 
    ADD COLUMN tutsa_preemption_compliance INT CHECK (tutsa_preemption_compliance BETWEEN 0 AND 100),
    ADD COLUMN wto_tariff_resilience INT CHECK (wto_tariff_resilience BETWEEN 0 AND 100),
    ADD COLUMN prior_art_validation_score INT CHECK (prior_art_validation_score BETWEEN 0 AND 100),
    ADD COLUMN generational_continuity_index INT CHECK (generational_continuity_index BETWEEN 0 AND 100);

-- Establish an explicit registry tracking corporate prior art structures
CREATE TABLE odynex_prior_art_registry (
    art_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    framework_name VARCHAR(150) NOT NULL DEFAULT 'Project Koridor: Adaptive Futures',
    principal_architect VARCHAR(100) NOT NULL DEFAULT 'David Fabian Cadelinia',
    assignee_entity VARCHAR(150) NOT NULL DEFAULT 'Odynex Axis Logistics LLC',
    tutsa_classification_status VARCHAR(50) NOT NULL DEFAULT 'Protected',
    wto_tariff_exemption_code VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Seed the initial defensive record to secure structural prior art boundaries
INSERT INTO odynex_prior_art_registry (framework_name, principal_architect, assignee_entity, tutsa_classification_status)
VALUES (
    'Project Koridor: Adaptive Futures (Transpacific Wealth Registry)',
    'David Fabian Cadelinia',
    'Odynex Axis Logistics LLC',
    'Trade Secret Exempt');
