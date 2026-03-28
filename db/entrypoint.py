#!/usr/bin/env python3
"""
Database entrypoint for Renewable Energy Executive Dashboard.

This script is called at container startup to:
1. Run Alembic migrations
2. Seed the database with research-backed data

It includes retry logic for when PostgreSQL is not immediately available.
"""
import os
import sys
import time
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agent:agent_dev@postgres:5432/appdb")


def wait_for_db(max_attempts=30, delay=2):
    """Wait until PostgreSQL is accessible."""
    import psycopg2
    for attempt in range(1, max_attempts + 1):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            conn.close()
            print(f"PostgreSQL ready after {attempt} attempt(s)")
            return True
        except Exception as e:
            print(f"Attempt {attempt}/{max_attempts}: {e}")
            if attempt < max_attempts:
                time.sleep(delay)
    return False


def run_migrations():
    """Run alembic upgrade head."""
    workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result = subprocess.run(
        ["python3", "-m", "alembic", "upgrade", "head"],
        cwd=workspace,
        env={**os.environ, "DATABASE_URL": DATABASE_URL},
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        # Try with PATH including local bins
        result = subprocess.run(
            [os.path.expanduser("~/.local/bin/alembic"), "upgrade", "head"],
            cwd=workspace,
            env={**os.environ, "DATABASE_URL": DATABASE_URL, "PATH": os.environ.get("PATH", "") + ":/home/agent/.local/bin"},
            capture_output=True,
            text=True,
        )
    print(result.stdout)
    if result.returncode != 0:
        print("Migration error:", result.stderr, file=sys.stderr)
        return False
    return True


def run_seed():
    """Run the seed script."""
    from db.seeds.seed_all import main
    main()
    return True


if __name__ == "__main__":
    print("=== Renewable Energy Dashboard — DB Initialization ===")
    print(f"DATABASE_URL: {DATABASE_URL}")
    
    if not wait_for_db():
        print("ERROR: Could not connect to PostgreSQL", file=sys.stderr)
        sys.exit(1)
    
    if not run_migrations():
        print("ERROR: Migrations failed", file=sys.stderr)
        sys.exit(1)
    
    if not run_seed():
        print("ERROR: Seeding failed", file=sys.stderr)
        sys.exit(1)
    
    print("=== DB Initialization Complete ===")
