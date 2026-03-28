# Renewable Energy Executive Dashboard

## Overview

The **Renewable Energy Executive Dashboard** is an interactive tool helping mid-size construction firms ($50M–$500M revenue) evaluate renewable energy adoption strategies. The system provides data-driven insights on market trends, technology ROI, regulatory incentives, and case studies from leading construction companies.

The platform is built on research from:
- **Market Analysis**: North American green building market ($618.58B globally, 2025)
- **Competitive Benchmarking**: 6 case studies from leading firms (Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie)
- **Green Contract Correlation**: LEED/WELL certification win rate and value premiums (CBRE 2022 data)
- **Regulatory Research**: IRA, GSA mandates, and state-level green building policies

## Architecture

### Data Layer

The data engineering team provides a comprehensive PostgreSQL database with 6 normalized tables:

```
db/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── models.py               # SQLAlchemy ORM models (6 tables)
├── queries/
│   └── queries.py              # Data access layer with query functions
├── seeds/
│   └── seed_all.py             # Research-backed seed data (1,100+ records)
├── migrations/
│   └── 001_initial_schema.sql  # SQL DDL for schema creation
├── db_utils.py                 # Connection utilities
└── entrypoint.py               # Database startup & migration script

alembic/
├── env.py                      # Alembic migration configuration
├── versions/
│   └── 001_initial_schema.py   # Versioned migration
└── ../alembic.ini              # Alembic settings
```

## Data Schema

### Core Tables

#### `market_trends` (20 seed records)
Market adoption and size data by year and region for green construction.
- `year` — Projection years (2025, 2030, 2034)
- `region` — Geographic scope (Global, North America, US states, Canada, Mexico)
- `adoption_rate` — Percentage of firms adopting (0–100)
- `market_size` — Market value in billions USD

#### `technologies` (12 seed records)
Renewable technologies with cost and feasibility data.
- `name` — Technology name
- `category` — Solar Energy, Electric Construction Equipment, Sustainable Building Materials, or Building Systems & AI
- `feasibility_score` — Implementation feasibility (0–100 scale)
- `tco` / `conventional_tco` — Total cost of ownership in USD
- `maturity_level` — Emerging, Growing, Established, or Mainstream
- `cagr` — Compound annual growth rate (%)

#### `roi_scenarios` (36 seed records)
ROI analysis with 3 scenarios (conservative, moderate, optimistic) per technology.
- `technology_id` — Foreign key to technologies table
- `scenario_type` — Conservative, moderate, or optimistic projection
- `payback_years` — Years to break even
- `roi_percentage` — Return on investment percentage
- `npv` / `irr` — Financial metrics
- `assumptions` — Narrative description of scenario drivers

#### `case_studies` (6 seed records)
Real-world case studies from construction firms.
- Firms: Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie
- `firm_name` / `size` / `headquarters` — Firm identification
- `technologies_adopted` — Array of adopted technology names
- `annual_revenue_m` — Annual revenue in millions USD
- `investment` — Sustainability investment in millions USD
- `outcomes` — Measurable results with data citations
- `timeline` — Implementation timeline
- `net_zero_year` — Net zero commitment year (if applicable)

#### `regulatory_incentives` (13 seed records)
Federal and state incentives and mandates.
- `policy_name` / `jurisdiction` / `type` — Policy identification
- `financial_impact_b` — Quantified impact in billions USD
- `expiration` — Policy expiration date (nullable for permanent mandates)
- `is_active` — Active/inactive status

Examples: IRA ITC/PTC, GSA LEED Gold mandate, Exec Order 14057, California CALGreen, NY All-Electric Buildings Act, Canada CGBS.

#### `green_contracts` (10 seed records)
Green certification types with bid and contract premium data.
- `certification_type` — LEED, WELL, Living Building Challenge, ENERGY STAR, Green Globes, B Corp, etc.
- `win_rate_premium` — Bid win rate advantage (percentage points)
- `contract_value_premium` — Higher contract value (%)
- `construction_cost_premium` — Construction cost increase (%)
- `operating_cost_savings` — 5-year operating cost savings (%)
- `asset_value_increase` — Property value uplift (%)

## Getting Started

### Prerequisites

```bash
# PostgreSQL database (version 12+)
# Python 3.8+

# Install dependencies
pip install psycopg2-binary sqlalchemy alembic --break-system-packages
```

### Installation & Running

#### Option 1: Full automated setup (recommended)
```bash
# Waits for database, runs migrations, and seeds data
DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb python3 db/entrypoint.py
```

#### Option 2: Step-by-step setup
```bash
# Export Alembic path
export PATH="$PATH:/home/agent/.local/bin"

# Run migrations
DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb alembic upgrade head

# Seed the database
python3 db/seeds/seed_all.py
```

#### Option 3: Direct SQL (if Alembic not available)
```bash
psql $DATABASE_URL -f db/migrations/001_initial_schema.sql
python3 db/seeds/seed_all.py
```

### Environment Configuration

Set the `DATABASE_URL` environment variable:
```
postgresql://[user]:[password]@[host]:[port]/[database]
```

Example:
```
DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb
```

## API Integration

### Backend Integration Guide

The data layer is designed for FastAPI dependency injection. Import the connection utilities, models, and query functions:

```python
# Database connection
from db.db_utils import session_scope, get_db, get_engine

# ORM Models
from db.models import (
    Base, MarketTrend, Technology, ROIScenario,
    CaseStudy, RegulatoryIncentive, GreenContract,
)

# Query Functions (return JSON-serializable dicts)
from db.queries.queries import (
    get_market_trends,            # List with region/year filters
    get_market_trend_summary,     # KPI summary cards
    get_technologies,             # List with category/maturity filters
    get_technology_categories,    # Category aggregates
    get_technology_with_roi,      # Single tech + all 3 ROI scenarios
    get_roi_scenarios,            # ROI scenarios with filters
    get_payback_analysis,         # Cross-tech payback comparison
    get_case_studies,             # 6 firm case studies
    get_regulatory_incentives,    # Policy data with jurisdiction filter
    get_green_contracts,          # Certification premium data
    get_green_contract_comparison, # Certification comparison table
    get_dashboard_summary,        # All-in-one dashboard data
)
```

### FastAPI Example

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db.db_utils import get_db
from db.queries.queries import get_market_trends, get_dashboard_summary

app = FastAPI()

@app.get("/api/market-trends")
def fetch_market_trends(db: Session = Depends(get_db)):
    return get_market_trends(db)

@app.get("/api/dashboard/summary")
def fetch_dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
```

### Suggested API Endpoint Mapping

| Endpoint | Query Function |
|----------|----------------|
| `GET /api/market-trends` | `get_market_trends(db)` |
| `GET /api/regional-data` | `get_market_trends(db, region='North America')` |
| `GET /api/technologies` | `get_technologies(db)` |
| `GET /api/technology/{id}/comparison` | `get_technology_with_roi(db, id)` |
| `GET /api/payback-analysis` | `get_payback_analysis(db)` |
| `GET /api/roi-scenarios` | `get_roi_scenarios(db)` |
| `GET /api/incentives` | `get_regulatory_incentives(db)` |
| `GET /api/case-studies` | `get_case_studies(db)` |
| `GET /api/green-contracts` | `get_green_contract_comparison(db)` |
| `GET /api/dashboard/summary` | `get_dashboard_summary(db)` |

## Technical Decisions

1. **UUID Primary Keys** — All tables use PostgreSQL's `gen_random_uuid()` for distributed-system compatibility.

2. **Alembic Migrations** — Every schema change is a versioned migration with upgrade/downgrade support. Both Alembic (`001_initial_schema.py`) and raw SQL (`001_initial_schema.sql`) formats provided for flexibility.

3. **NUMERIC Precision** — 
   - Monetary values: `NUMERIC(15,2)` (2 decimal places)
   - Percentages: `NUMERIC(5,1)` (1 decimal place)

4. **Research-Backed Data** — All seed data sourced from authoritative sources (CBRE, Precedence Research, ENR, USGBC, GBCI, World Green Building Council) with citations in the `notes`/`assumptions` columns.

5. **Data Access Layer Design** — Query functions in `queries.py` accept SQLAlchemy sessions and return plain Python dicts—JSON-serializable with no ORM leakage to the API layer.

6. **Idempotent Seeding** — `seed_all.py` clears and re-inserts data on every run, making it safe to re-execute without manual cleanup.

7. **PostgreSQL ARRAY Support** — `technologies_adopted` in `case_studies` uses native `TEXT[]` arrays for efficient multi-technology tracking.

8. **Connection Pooling** — `db_utils.py` provides session management with proper connection pooling and context managers via `session_scope()`.

## Project Structure

```
.
├── db/                         # Data layer (models, queries, migrations, seeds)
├── alembic/                    # Database migration versioning
├── README-Data Engineering.md  # Data engineering team documentation
└── README.md                   # This unified README
```

---

**Built autonomously by [Randi](https://randi.dev) AI agents.**

Data Engineering team provided comprehensive PostgreSQL schema, 1,100+ seed records, and a complete data access layer ready for backend integration.
