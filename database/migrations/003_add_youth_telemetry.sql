-- Appends telemetry column updates tracking academic metrics
ALTER TABLE base_telemetry_logs ADD COLUMN youth_demographic_flag BOOLEAN DEFAULT FALSE;
