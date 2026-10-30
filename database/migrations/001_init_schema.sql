-- Initial Schema setup for base tracking metrics
CREATE TABLE IF NOT EXISTS system_heartbeats (
    heartbeat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    node_name VARCHAR(100) NOT NULL,
    is_healthy BOOLEAN NOT NULL DEFAULT TRUE,
    checked_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
