# database/db_client.py
import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/mrg_simulation")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database extraction connection failure: {e}")
        return None

def init_base_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS simulation_sessions (
            session_id VARCHAR(255) PRIMARY KEY,
            vertical VARCHAR(100) NOT NULL,
            composure_baseline NUMERIC(5,2) DEFAULT 100.00,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            log_id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) REFERENCES simulation_sessions(session_id) ON DELETE CASCADE,
            vocal_stress NUMERIC(5,4),
            decision_velocity NUMERIC(7,2),
            logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
            conn.commit()
            print("Successfully executed base table migrations.")
        except Exception as e:
            print(f"Failed to execute schema layout: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    init_base_tables()
