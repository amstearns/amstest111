"""
Renewable Energy Executive Dashboard — FastAPI Backend
Serves research data as REST API endpoints for the executive dashboard.
"""

import time
from datetime import datetime, timezone
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from .schemas import (
    HealthResponse,
    TechnologiesResponse,
    TechnologyComparisonResponse,
    MarketTrendsResponse,
    RegionalDataResponse,
    PaybackAnalysisResponse,
    ROIScenariosResponse,
    IncentivesResponse,
    CaseStudiesResponse,
    GreenContractsResponse,
)
from .seed_data import (
    get_market_trends,
    get_regional_data,
    get_technologies,
    get_technology_comparison,
    get_payback_analysis,
    get_roi_scenarios,
    get_incentives,
    get_case_studies,
    get_green_contracts,
    TECHNOLOGIES_DATA,
)

# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------

START_TIME = time.monotonic()

app = FastAPI(
    title="Renewable Energy Executive Dashboard API",
    description=(
        "REST API serving renewable energy research data for the executive dashboard. "
        "Covers market trends, technologies, financial analysis, and competitive benchmarking "
        "for North American construction industry renewable energy adoption."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# ---------------------------------------------------------------------------
# CORS — allow frontend on localhost:3000; wildcard for development
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Public read-only API; credentials not used
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)


# ---------------------------------------------------------------------------
# Security headers middleware
# ---------------------------------------------------------------------------


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "public, max-age=300"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# ---------------------------------------------------------------------------
# Cache layer (simple in-memory singleton)
# ---------------------------------------------------------------------------

_cache: dict = {}


def _cached(key: str, factory):
    if key not in _cache:
        _cache[key] = factory()
    return _cache[key]


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns service health status, version, and uptime.",
    tags=["Health"],
)
async def health_check() -> HealthResponse:
    uptime = time.monotonic() - START_TIME
    return HealthResponse(
        status="ok",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        database="in-memory",
        uptime_seconds=round(uptime, 2),
    )


# ---------------------------------------------------------------------------
# Market Data Endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/api/market-trends",
    response_model=MarketTrendsResponse,
    summary="Market Trends",
    description=(
        "Returns adoption rates by firm size, market size data for green building "
        "and electric construction equipment markets, key market drivers and barriers, "
        "and time-series projections through 2034."
    ),
    tags=["Market Data"],
)
async def market_trends() -> MarketTrendsResponse:
    return _cached("market_trends", get_market_trends)


@app.get(
    "/api/regional-data",
    response_model=RegionalDataResponse,
    summary="Regional Data",
    description=(
        "Returns North American regional breakdowns: USGBC top 10 US states for LEED (2025), "
        "state-level policy drivers, and country-level data for US, Canada, and Mexico."
    ),
    tags=["Market Data"],
)
async def regional_data() -> RegionalDataResponse:
    return _cached("regional_data", get_regional_data)


# ---------------------------------------------------------------------------
# Technology Endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/api/technologies",
    response_model=TechnologiesResponse,
    summary="Technologies",
    description=(
        "Returns all renewable energy and green building technologies with feasibility scores "
        "(6-dimensional), ROI metrics, market size data, and adoption rates. "
        "Covers electric equipment, solar PV, green building systems, battery storage, "
        "mass timber, and green hydrogen."
    ),
    tags=["Technologies"],
)
async def technologies() -> TechnologiesResponse:
    return _cached("technologies", get_technologies)


@app.get(
    "/api/technology/{tech_id}/comparison",
    response_model=TechnologyComparisonResponse,
    summary="Technology TCO Comparison",
    description=(
        "Returns Total Cost of Ownership (TCO) comparison between a green technology "
        "and its conventional equivalent. Includes base case and incentivized scenarios "
        "with component-level cost breakdowns. "
        "Valid IDs: electric-construction-equipment, solar-pv, green-building-systems"
    ),
    tags=["Technologies"],
)
async def technology_comparison(
    tech_id: Annotated[str, Path(max_length=100, pattern=r"^[a-z0-9\-]+$")]
) -> TechnologyComparisonResponse:
    result = get_technology_comparison(tech_id)
    if result is None:
        valid_ids = [t.id for t in TECHNOLOGIES_DATA if t.id in ("electric-construction-equipment", "solar-pv", "green-building-systems")]
        raise HTTPException(
            status_code=404,
            detail={
                "detail": f"Technology '{tech_id}' not found or TCO comparison not available",
                "code": "TECHNOLOGY_NOT_FOUND",
                "valid_ids": valid_ids,
            },
        )
    return result


# ---------------------------------------------------------------------------
# Financial Endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/api/payback-analysis",
    response_model=PaybackAnalysisResponse,
    summary="Payback Analysis",
    description=(
        "Returns payback period analysis for all technologies — base case, "
        "with incentives, optimistic, and pessimistic scenarios. "
        "Modeled for a representative mid-size construction firm ($100-200M revenue)."
    ),
    tags=["Financial"],
)
async def payback_analysis() -> PaybackAnalysisResponse:
    return _cached("payback_analysis", get_payback_analysis)


@app.get(
    "/api/roi-scenarios",
    response_model=ROIScenariosResponse,
    summary="ROI Scenarios",
    description=(
        "Returns conservative, moderate, and aggressive ROI projection scenarios "
        "with year-by-year financial projections. Each scenario includes initial investment, "
        "10-year ROI, NPV, IRR, and breakeven year."
    ),
    tags=["Financial"],
)
async def roi_scenarios() -> ROIScenariosResponse:
    return _cached("roi_scenarios", get_roi_scenarios)


@app.get(
    "/api/incentives",
    response_model=IncentivesResponse,
    summary="Regulatory Incentives",
    description=(
        "Returns all major regulatory incentives including IRA tax credits, "
        "Section 179D deduction, state mandates, and Canadian programs — "
        "with financial impact modeling and political risk assessment."
    ),
    tags=["Financial"],
)
async def incentives() -> IncentivesResponse:
    return _cached("incentives", get_incentives)


# ---------------------------------------------------------------------------
# Competitive Endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/api/case-studies",
    response_model=CaseStudiesResponse,
    summary="Case Studies",
    description=(
        "Returns competitive benchmarking profiles for 6 construction firms "
        "(Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie) "
        "with technology adoption details, ROI metrics, and lessons for mid-size firms."
    ),
    tags=["Competitive"],
)
async def case_studies() -> CaseStudiesResponse:
    return _cached("case_studies", get_case_studies)


@app.get(
    "/api/green-contracts",
    response_model=GreenContractsResponse,
    summary="Green Contract Win Rate Correlation",
    description=(
        "Returns data on how green credentials correlate with contract win rates: "
        "bid win rate multipliers by credential level, contract premiums for LEED buildings, "
        "certification landscape, and client preference breakdown."
    ),
    tags=["Competitive"],
)
async def green_contracts() -> GreenContractsResponse:
    return _cached("green_contracts", get_green_contracts)
