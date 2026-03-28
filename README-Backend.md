# Backend — Renewable Energy Executive Dashboard API

## Overview

FastAPI backend serving renewable energy research data as REST API endpoints for the executive dashboard. Provides market trends, technology analysis, financial modeling, and competitive benchmarking for North American construction industry renewable energy adoption.

All data is sourced from the research phase outputs (market analysis, competitive benchmarking, green contract correlation studies) covering March 2026 research.

## Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application, CORS, routes, middleware
│   ├── schemas.py       # Pydantic v2 response models (45 classes, 7 enums)
│   └── seed_data.py     # In-memory research data for all endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py      # 127 pytest tests covering all endpoints
└── requirements.txt
```

**Technology stack:**
- Python 3.11+
- FastAPI 0.115.6
- Pydantic v2 (full schema validation)
- Uvicorn ASGI server
- httpx + pytest-asyncio for testing

**Data layer:** In-memory singletons (no database required). All seed data is derived from the research phase documents in `previous_output/`.

## Setup & Running

```bash
# Install dependencies
pip install -r backend/requirements.txt --break-system-packages

# Run the server (from workspace root)
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# Or with auto-reload for development
python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

The server starts on **port 8000** as required.

```bash
# Run tests
python3 -m pytest backend/tests/test_api.py -v
# Result: 127/127 passed
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service health check |
| GET | `/api/market-trends` | Global/NA market size, adoption rates by firm size, drivers/barriers, time-series |
| GET | `/api/regional-data` | USGBC top 10 US states, country data (US/Canada/Mexico) |
| GET | `/api/technologies` | 6 technologies with 6D feasibility scores, ROI metrics, market data |
| GET | `/api/technology/{id}/comparison` | TCO comparison vs conventional (3 technologies have full TCO) |
| GET | `/api/payback-analysis` | Payback periods — base, incentivized, optimistic, pessimistic |
| GET | `/api/roi-scenarios` | Conservative/moderate/aggressive ROI scenarios with year-by-year projections |
| GET | `/api/incentives` | 10 regulatory incentives with financial impact and political risk |
| GET | `/api/case-studies` | 6 competitive benchmarking profiles |
| GET | `/api/green-contracts` | Win rate correlation, LEED premiums, certification landscape |

**Documentation:** http://localhost:8000/docs (Swagger UI), http://localhost:8000/redoc

### Technology IDs for `/api/technology/{id}/comparison`
- `electric-construction-equipment`
- `solar-pv`
- `green-building-systems`

## Key Data Highlights

| Metric | Value |
|--------|-------|
| Global green building market (2025) | $618.58B |
| North America market share | 35% ($153.87B) |
| Electric equipment CAGR (2026-2035) | 20.5% |
| IRA clean energy credits | $270B |
| LEED spec prevalence (projects >$50M) | 71% |
| States with LEED mandates | 35+ |
| Case studies profiled | 6 firms |
| Technologies analyzed | 6 |
| Incentive programs documented | 10 |

## CORS Configuration

CORS is configured to allow all origins (`allow_credentials=false`, `allow_methods=["GET", "OPTIONS"]`). Frontend on `localhost:3000` can call all endpoints without proxy configuration.

## Security

- Input validation via Pydantic v2 on all endpoints
- Path parameter validation with length cap (max_length=100) and character allowlist for `{tech_id}`
- Security headers: `X-Content-Type-Options`, `X-Frame-Options`, `Cache-Control`, `Referrer-Policy`
- No secrets or credentials in codebase
- Read-only API — no write endpoints

## Key Decisions

1. **In-memory data over PostgreSQL**: Research data is static; in-memory singletons provide instant startup, zero infrastructure requirements, and 100% reliability. The PostgreSQL database (provisioned by Data Engineering team) is not needed for this read-only dashboard API.

2. **Pydantic v2 schemas as API contract**: All 45 schema classes were designed first (API-first approach) before implementing the data. This ensures the Frontend team gets a stable, well-typed contract.

3. **ConfidenceLevel on all data points**: Research data has varying confidence (HIGH/MEDIUM/LOW). Preserving this through the API allows the Frontend to render uncertainty cues for executives.

4. **6-dimensional FeasibilityScore**: Rather than a single score, each technology has 6 scored dimensions (technical_maturity, financial_viability, regulatory_support, workforce_readiness, supply_chain_maturity, mid_size_adoption_ease). This supports radar/spider chart visualization.

5. **TCO scenarios (not single estimates)**: TCO comparisons return multiple scenarios (base case + with incentives) in a single response to avoid multiple roundtrips.

6. **Cache layer**: Simple dict-based in-memory cache ensures seed data factories run only once per server lifecycle.
