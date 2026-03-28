#!/bin/bash
# =============================================================================
# Run Alembic migrations and seed the database.
#
# Usage:
#   DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb ./run_migrations_and_seed.sh
#
# This script:
#   1. Waits for PostgreSQL to be ready (up to 60 seconds)
#   2. Runs Alembic migrations
#   3. Seeds the database with research-backed data
# =============================================================================

set -e

DB_URL="${DATABASE_URL:-postgresql://agent:agent_dev@postgres:5432/appdb}"
export DATABASE_URL="$DB_URL"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Renewable Energy Dashboard — DB Setup ==="
echo "DATABASE_URL: $DATABASE_URL"

# ---------------------------------------------------------------------------
# Wait for PostgreSQL
# ---------------------------------------------------------------------------
echo "Waiting for PostgreSQL..."
MAX_ATTEMPTS=30
ATTEMPT=0
until python3 -c "
import psycopg2, os, sys
try:
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    conn.close()
    print('PostgreSQL ready')
    sys.exit(0)
except Exception as e:
    print(f'Not ready: {e}', file=sys.stderr)
    sys.exit(1)
"; do
    ATTEMPT=$((ATTEMPT + 1))
    if [ $ATTEMPT -ge $MAX_ATTEMPTS ]; then
        echo "ERROR: PostgreSQL not available after $MAX_ATTEMPTS attempts"
        exit 1
    fi
    echo "  Attempt $ATTEMPT/$MAX_ATTEMPTS — waiting 2s..."
    sleep 2
done

# ---------------------------------------------------------------------------
# Run migrations
# ---------------------------------------------------------------------------
echo ""
echo "Running Alembic migrations..."
cd "$WORKSPACE_DIR"
export PATH="$PATH:/home/agent/.local/bin"
alembic upgrade head

echo "Migrations complete."

# ---------------------------------------------------------------------------
# Seed database
# ---------------------------------------------------------------------------
echo ""
echo "Seeding database..."
python3 "$SCRIPT_DIR/seeds/seed_all.py"

echo ""
echo "=== Setup Complete ==="
