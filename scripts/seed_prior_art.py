# scripts/seed_prior_art.py
import os
import asyncio
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

async def seed_defensive_prior_art():
    if not DATABASE_URL:
        print("CRITICAL ERROR: DATABASE_URL variable is not set in runtime environment.")
        return

    print("Opening secure connection to Fly.io cluster relational database...")
    conn = await asyncpg.connect(DATABASE_URL)
    
    try:
        print("Injecting foundational architecture prior art blueprints into registry...")
        
        # Seed foundational system elements
        await conn.execute("""
            INSERT INTO odynex_prior_art_registry 
                (framework_name, principal_architect, assignee_entity, tutsa_classification_status, wto_tariff_exemption_code)
            VALUES 
                ($1, $2, $3, $4, $5),
                ($6, $7, $8, $9, $10)
            ON CONFLICT DO NOTHING;
        """, 
        "Project Koridor: Adaptive Futures (Transpacific Wealth Registry Grid)", 
        "David Fabian Cadelinia", 
        "Odynex Axis Logistics LLC", 
        "Trade Secret Exempt", 
        "WTO-EX-2026-ALPHA",
        
        "Multi-Agent Real-Time Cognitive Pipeline (Sub-100ms Telemetry Sync Framework)", 
        "David Fabian Cadelinia", 
        "Odynex Axis Logistics LLC", 
        "Proprietary Preemptive Art", 
        "WTO-EX-2026-BETA")

        print("Checking active database records to confirm insertion integrity...")
        rows = await conn.fetch("SELECT art_id, framework_name FROM odynex_prior_art_registry;")
        for r in rows:
            print(f"  • Registered Protected Asset ID: {r['art_id']} -> Name: {r['framework_name']}")
            
        print("\n✅ [SUCCESS] Odynex Axis Logistics LLC corporate prior art successfully seeded.")
        
    except Exception as err:
        print(f"Database insertion exception encountered: {err}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(seed_defensive_prior_art())
