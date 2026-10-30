-- Creates default analytical data loggers for baseline metrics
CREATE TABLE IF NOT EXISTS base_telemetry_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_packet_size INT NOT NULL,
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
