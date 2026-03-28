# Data Engineering

## Overview

This team set up the PostgreSQL database schema and seed data for the **Renewable Energy Executive Dashboard** — an interactive tool helping mid-size construction firms ($50M–$500M revenue) evaluate renewable energy adoption strategies.

The database is built on research from:
- **Market Analysis**: North American green building market ($618.58B globally, 2025)
- **Competitive Benchmarking**: 6 case studies (Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie)
- **Green Contract Correlation**: LEED/WELL certification win rate and value premiums (CBRE 2022 data)
- **Regulatory Research**: IRA, GSA mandates, and state-level green building policies

## Architecture

```
db/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── models.py          # SQLAlchemy ORM models (6 tables)
├── queries/
│   └── queries.py         # Data access layer — all query functions
├── seeds/
│   └── seed_all.py        # Research-backed seed data
├── migrations/
│   └── 001_initial_schema.sql  # Standalone SQL DDL (alternative to Alembic)
├── db_utils.py            # Connection utilities (session_scope, get_db)
└── entrypoint.py          # Startup script (wait for DB → migrate → seed)

alembic/
├── env.py                 # Alembic configuration
└── versions/
    └── 001_initial_schema.py   # Alembic migration
alembic.ini                # Alembic settings
```

## Schema: 6 Tables

### `market_trends`
Year/region green building market data.
- `year` — e.g., 2025, 2030, 2034
- `region` — e.g., "Global", "North America", "United States - California"
- `adoption_rate` — NUMERIC(5,1) — percentage of firms adopting
- `market_size` — NUMERIC(15,2) — billions USD

**Seed data**: 20 records covering Global, North America, US by firm size, Canada, Mexico, and Electric Construction Equipment market.

### `technologies`
Renewable technologies with cost and feasibility data.
- `name` — technology name
- `category` — "Solar Energy" | "Electric Construction Equipment" | "Sustainable Building Materials" | "Building Systems & AI"
- `feasibility_score` — NUMERIC(4,1) — 0–100 scale
- `tco` / `conventional_tco` — NUMERIC(15,2) — total cost of ownership USD
- `maturity_level` — "Emerging" | "Growing" | "Established" | "Mainstream"
- `cagr` — NUMERIC(5,1) — compound annual growth rate %

**Seed data**: 12 technologies across 4 categories.

### `roi_scenarios`
ROI analysis with 3 scenarios per technology.
- `technology_id` — UUID FK → technologies.id
- `scenario_type` — "conservative" | "moderate" | "optimistic"
- `payback_years` — NUMERIC(5,1)
- `roi_percentage` — NUMERIC(6,1)
- `assumptions` — full narrative of scenario drivers
- `npv` / `irr` — financial metrics

**Seed data**: 36 scenarios (3 per technology × 12 technologies).

### `case_studies`
6 firm case studies (Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie).
- `firm_name` / `size` / `headquarters`
- `technologies_adopted` — TEXT[] — array of technology names
- `annual_revenue_m` — NUMERIC(10,2) — annual revenue in millions USD
- `investment` — NUMERIC(15,2) — sustainability investment in millions USD
- `outcomes` — measurable results with data citations
- `timeline` — e.g., "1995-present"
- `net_zero_year` — commitment year (nullable)

### `regulatory_incentives`
13 federal and state incentives/mandates.
- `policy_name` / `jurisdiction` / `type`
- `financial_impact` — narrative description
- `financial_impact_b` — NUMERIC(15,2) — quantified impact in billions USD
- `expiration` — DATE (nullable for permanent mandates)
- `is_active` — "yes" | "no"

**Seed data**: IRA ITC/PTC, GSA LEED Gold mandate, Exec Order 14057, California CALGreen + Buy Clean + Net Zero, NY All-Electric Buildings Act + Local Law 97, Canada CGBS, Colorado roadmap, IRA EV credits.

### `green_contracts`
10 certification types with bid win rate and contract premium data.
- `certification_type` — e.g., "LEED Gold", "WELL Building Standard"
- `win_rate_premium` — NUMERIC(5,1) — percentage points above non-certified
- `contract_value_premium` — NUMERIC(5,1) — % higher contract value
- `construction_cost_premium` — NUMERIC(5,1) — % over conventional
- `operating_cost_savings` — NUMERIC(5,1) — % savings over 5 years
- `asset_value_increase` — NUMERIC(5,1) — % asset value uplift

**Seed data**: Baseline, LEED Certified/Silver/Gold/Platinum, WELL, Living Building Challenge, ENERGY STAR, Green Globes, B Corp.

## Setup & Running

### Prerequisites
```bash
pip install psycopg2-binary sqlalchemy alembic --break-system-packages
```

### Run migrations + seed
```bash
# Full setup (waits for DB, migrates, seeds)
DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb python3 db/entrypoint.py

# Or step by step:
export PATH="$PATH:/home/agent/.local/bin"
DATABASE_URL=postgresql://agent:agent_dev@postgres:5432/appdb alembic upgrade head
python3 db/seeds/seed_all.py

# Or use the SQL file directly:
psql $DATABASE_URL -f db/migrations/001_initial_schema.sql
```

## API / Interfaces

### Backend team import guide

```python
# Connection
from db.db_utils import session_scope, get_db, get_engine

# Models
from db.models import (
    Base, MarketTrend, Technology, ROIScenario,
    CaseStudy, RegulatoryIncentive, GreenContract,
)

# Query functions (all return JSON-serializable dicts)
from db.queries.queries import (
    get_market_trends,            # List with region/year filters
    get_market_trend_summary,     # KPI cards summary
    get_technologies,             # List with category/maturity filters
    get_technology_categories,    # Category aggregates
    get_technology_with_roi,      # Single tech + all 3 ROI scenarios
    get_roi_scenarios,            # ROI scenarios with tech/type filters
    get_payback_analysis,         # Cross-tech payback comparison
    get_case_studies,             # 6 firm case studies
    get_regulatory_incentives,    # Policy data with jurisdiction filter
    get_green_contracts,          # Certification premium data
    get_green_contract_comparison, # Certification comparison table
    get_dashboard_summary,        # All-in-one dashboard data
)

# FastAPI dependency injection
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/api/market-trends")
def market_trends(db: Session = Depends(get_db)):
    return get_market_trends(db)

@app.get("/api/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    return get_dashboard_summary(db)
```

### Suggested API endpoint mapping
| Endpoint | Query Function |
|----------|---------------|
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

## Key Decisions

1. **UUID primary keys** — All tables use `gen_random_uuid()` UUIDs, distributed-system-friendly.
2. **Alembic migrations** — Every schema change is a versioned migration with upgrade/downgrade. Both `001_initial_schema.py` (Alembic) and `001_initial_schema.sql` (raw SQL) are provided for flexibility.
3. **NUMERIC precision** — Monetary values use `NUMERIC(15,2)` (2 decimal places), percentages use `NUMERIC(5,1)` (1 decimal place), matching task requirements exactly.
4. **Research-backed data** — All seed data is sourced from actual research reports (CBRE, Precedence Research, ENR, USGBC, GBCI, World Green Building Council). Sources are cited in the `notes`/`assumptions` columns.
5. **DAL design** — `queries.py` functions accept an SQLAlchemy Session (injected by FastAPI's `Depends(get_db)`) and return plain Python dicts that are JSON-serializable — no ORM leakage to the API layer.
6. **Idempotent seeding** — `seed_all.py` clears and re-inserts data on every run, safe for re-execution.
7. **ARRAY support** — `technologies_adopted` in `case_studies` uses PostgreSQL's native `TEXT[]` array type for efficient storage of multi-technology adoption lists.
