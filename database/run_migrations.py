import os
import asyncio
import glob
import asyncpg

async def run_ordered_migrations():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("DATABASE_URL missing. Skipping migration automation.")
        return

    print("Connecting to target database cluster...")
    conn = await asyncpg.connect(db_url)
    
    try:
        # Collect and run all migration scripts sequentially
        migration_files = sorted(glob.glob("database/migrations/*.sql"))
        for file_path in migration_files:
            print(f"Applying migration sequence: {file_path}")
            with open(file_path, "r") as f:
                sql_script = f.read()
            await conn.execute(sql_script)
        print("Successfully synced all database schemas.")
    except Exception as e:
        print(f"Migration script error encountered: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(run_ordered_migrations())
