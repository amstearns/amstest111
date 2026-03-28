"""
Data access layer (DAL) for the Renewable Energy Executive Dashboard.

This module provides the Backend team with all query functions needed
to serve the API endpoints. Import as:

    from db.queries.queries import (
        get_market_trends,
        get_technologies,
        get_technology_with_roi,
        get_case_studies,
        get_regulatory_incentives,
        get_green_contracts,
        get_dashboard_summary,
    )

All functions accept an SQLAlchemy Session and return typed dicts
or lists of dicts — JSON-serializable for direct use in FastAPI responses.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional
from uuid import UUID

from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session

from db.models.models import (
    MarketTrend,
    Technology,
    ROIScenario,
    CaseStudy,
    RegulatoryIncentive,
    GreenContract,
)


def _to_float(val) -> Optional[float]:
    """Convert Decimal/None to float for JSON serialization."""
    if val is None:
        return None
    return float(val)


def _model_to_dict(obj: Any, exclude: Optional[set] = None) -> dict:
    """Convert an SQLAlchemy model instance to a JSON-serializable dict."""
    exclude = exclude or set()
    result = {}
    for col in obj.__table__.columns:
        if col.name in exclude:
            continue
        val = getattr(obj, col.name)
        if isinstance(val, Decimal):
            val = float(val)
        elif isinstance(val, UUID):
            val = str(val)
        result[col.name] = val
    return result


# =============================================================================
# MARKET TRENDS
# =============================================================================

def get_market_trends(
    session: Session,
    region: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
) -> list[dict]:
    """
    Fetch market trend records with optional filtering.

    Args:
        session: SQLAlchemy session
        region: Filter by region name (partial match, case-insensitive)
        year_from: Minimum year (inclusive)
        year_to: Maximum year (inclusive)

    Returns:
        List of market trend dicts with all fields
    """
    query = session.query(MarketTrend)

    if region:
        query = query.filter(MarketTrend.region.ilike(f"%{region}%"))
    if year_from:
        query = query.filter(MarketTrend.year >= year_from)
    if year_to:
        query = query.filter(MarketTrend.year <= year_to)

    query = query.order_by(MarketTrend.year, MarketTrend.region)
    return [_model_to_dict(t) for t in query.all()]


def get_market_trend_summary(session: Session) -> dict:
    """
    High-level market summary stats for dashboard KPI cards.

    Returns:
        Dict with global_market_size_2025, na_market_size_2025,
        electric_equipment_market_2025, global_cagr, na_adoption_rate
    """
    global_2025 = session.query(MarketTrend).filter(
        MarketTrend.year == 2025,
        MarketTrend.region == "Global",
    ).first()

    na_2025 = session.query(MarketTrend).filter(
        MarketTrend.year == 2025,
        MarketTrend.region == "North America",
    ).first()

    elec_2025 = session.query(MarketTrend).filter(
        MarketTrend.year == 2025,
        MarketTrend.region == "Global - Electric Construction Equipment",
    ).first()

    elec_2030 = session.query(MarketTrend).filter(
        MarketTrend.year == 2030,
        MarketTrend.region == "Global - Electric Construction Equipment",
    ).first()

    return {
        "global_market_size_2025_b": _to_float(global_2025.market_size if global_2025 else None),
        "global_adoption_rate_2025_pct": _to_float(global_2025.adoption_rate if global_2025 else None),
        "na_market_size_2025_b": _to_float(na_2025.market_size if na_2025 else None),
        "na_adoption_rate_2025_pct": _to_float(na_2025.adoption_rate if na_2025 else None),
        "electric_equipment_market_2025_b": _to_float(elec_2025.market_size if elec_2025 else None),
        "electric_equipment_market_2030_b": _to_float(elec_2030.market_size if elec_2030 else None),
        "electric_equipment_cagr_pct": 20.5,
        "global_green_building_cagr_pct": 9.29,
    }


# =============================================================================
# TECHNOLOGIES
# =============================================================================

def get_technologies(
    session: Session,
    category: Optional[str] = None,
    maturity_level: Optional[str] = None,
    min_feasibility: Optional[float] = None,
) -> list[dict]:
    """
    Fetch technology records with optional filtering.

    Args:
        session: SQLAlchemy session
        category: Filter by category (exact match, case-insensitive)
        maturity_level: e.g., 'Emerging', 'Growing', 'Established', 'Mainstream'
        min_feasibility: Minimum feasibility score (0-100)

    Returns:
        List of technology dicts including tco_savings_pct computed field
    """
    query = session.query(Technology)

    if category:
        query = query.filter(Technology.category.ilike(f"%{category}%"))
    if maturity_level:
        query = query.filter(Technology.maturity_level.ilike(f"%{maturity_level}%"))
    if min_feasibility is not None:
        query = query.filter(Technology.feasibility_score >= min_feasibility)

    query = query.order_by(Technology.category, Technology.name)
    results = []
    for t in query.all():
        d = _model_to_dict(t)
        # Compute TCO savings as percentage
        if t.conventional_tco and t.conventional_tco != 0:
            savings_pct = float((t.conventional_tco - t.tco) / t.conventional_tco * 100)
            d["tco_savings_pct"] = round(savings_pct, 1)
        else:
            d["tco_savings_pct"] = None
        results.append(d)
    return results


def get_technology_categories(session: Session) -> list[dict]:
    """
    Get distinct technology categories with aggregate stats.

    Returns:
        List of dicts: category, count, avg_feasibility, avg_tco_savings_pct
    """
    techs = session.query(Technology).all()
    categories = {}
    for t in techs:
        cat = t.category
        if cat not in categories:
            categories[cat] = {
                "category": cat,
                "count": 0,
                "feasibility_scores": [],
                "tco_savings": [],
            }
        categories[cat]["count"] += 1
        categories[cat]["feasibility_scores"].append(float(t.feasibility_score))
        if t.conventional_tco and t.conventional_tco != 0:
            savings = float((t.conventional_tco - t.tco) / t.conventional_tco * 100)
            categories[cat]["tco_savings"].append(savings)

    result = []
    for cat, data in sorted(categories.items()):
        avg_feasibility = sum(data["feasibility_scores"]) / len(data["feasibility_scores"]) if data["feasibility_scores"] else None
        avg_savings = sum(data["tco_savings"]) / len(data["tco_savings"]) if data["tco_savings"] else None
        result.append({
            "category": cat,
            "technology_count": data["count"],
            "avg_feasibility_score": round(avg_feasibility, 1) if avg_feasibility else None,
            "avg_tco_savings_pct": round(avg_savings, 1) if avg_savings else None,
        })
    return result


def get_technology_with_roi(session: Session, technology_id: str) -> Optional[dict]:
    """
    Fetch a single technology with all 3 ROI scenarios attached.

    Args:
        session: SQLAlchemy session
        technology_id: UUID string of the technology

    Returns:
        Dict with technology fields + 'roi_scenarios' list, or None if not found
    """
    try:
        tech_uuid = UUID(technology_id)
    except (ValueError, AttributeError):
        return None

    tech = session.query(Technology).filter(Technology.id == tech_uuid).first()
    if not tech:
        return None

    d = _model_to_dict(tech)
    if tech.conventional_tco and tech.conventional_tco != 0:
        d["tco_savings_pct"] = round(float((tech.conventional_tco - tech.tco) / tech.conventional_tco * 100), 1)

    scenarios = (
        session.query(ROIScenario)
        .filter(ROIScenario.technology_id == tech_uuid)
        .order_by(ROIScenario.scenario_type)
        .all()
    )
    d["roi_scenarios"] = [_model_to_dict(s) for s in scenarios]
    return d


# =============================================================================
# ROI SCENARIOS
# =============================================================================

def get_roi_scenarios(
    session: Session,
    technology_id: Optional[str] = None,
    scenario_type: Optional[str] = None,
) -> list[dict]:
    """
    Fetch ROI scenarios with optional filtering.

    Args:
        session: SQLAlchemy session
        technology_id: Filter by technology UUID string
        scenario_type: 'conservative', 'moderate', or 'optimistic'

    Returns:
        List of roi_scenario dicts
    """
    query = session.query(ROIScenario)

    if technology_id:
        try:
            query = query.filter(ROIScenario.technology_id == UUID(technology_id))
        except (ValueError, AttributeError):
            return []
    if scenario_type:
        query = query.filter(ROIScenario.scenario_type == scenario_type.lower())

    query = query.order_by(ROIScenario.technology_id, ROIScenario.scenario_type)
    return [_model_to_dict(s) for s in query.all()]


def get_payback_analysis(session: Session) -> list[dict]:
    """
    Cross-technology payback period comparison for all scenario types.

    Returns:
        List of dicts: technology_name, category, scenario_type,
        payback_years, roi_percentage — sorted by payback_years ascending
    """
    rows = (
        session.query(
            Technology.name,
            Technology.category,
            ROIScenario.scenario_type,
            ROIScenario.payback_years,
            ROIScenario.roi_percentage,
        )
        .join(ROIScenario, ROIScenario.technology_id == Technology.id)
        .order_by(ROIScenario.scenario_type, ROIScenario.payback_years)
        .all()
    )

    return [
        {
            "technology_name": r.name,
            "category": r.category,
            "scenario_type": r.scenario_type,
            "payback_years": _to_float(r.payback_years),
            "roi_percentage": _to_float(r.roi_percentage),
        }
        for r in rows
    ]


# =============================================================================
# CASE STUDIES
# =============================================================================

def get_case_studies(
    session: Session,
    size: Optional[str] = None,
    firm_name: Optional[str] = None,
) -> list[dict]:
    """
    Fetch case studies with optional filtering.

    Args:
        session: SQLAlchemy session
        size: Filter by firm size category (partial match)
        firm_name: Filter by firm name (partial match, case-insensitive)

    Returns:
        List of case study dicts
    """
    query = session.query(CaseStudy)

    if size:
        query = query.filter(CaseStudy.size.ilike(f"%{size}%"))
    if firm_name:
        query = query.filter(CaseStudy.firm_name.ilike(f"%{firm_name}%"))

    query = query.order_by(CaseStudy.firm_name)
    return [_model_to_dict(cs) for cs in query.all()]


# =============================================================================
# REGULATORY INCENTIVES
# =============================================================================

def get_regulatory_incentives(
    session: Session,
    jurisdiction: Optional[str] = None,
    type_: Optional[str] = None,
    active_only: bool = True,
) -> list[dict]:
    """
    Fetch regulatory incentives with optional filtering.

    Args:
        session: SQLAlchemy session
        jurisdiction: Filter by jurisdiction (partial match)
        type_: Filter by type ('Tax Credit', 'Mandate', 'Standard', 'Grant')
        active_only: If True, only return active incentives

    Returns:
        List of regulatory incentive dicts
    """
    query = session.query(RegulatoryIncentive)

    if jurisdiction:
        query = query.filter(RegulatoryIncentive.jurisdiction.ilike(f"%{jurisdiction}%"))
    if type_:
        query = query.filter(RegulatoryIncentive.type.ilike(f"%{type_}%"))
    if active_only:
        query = query.filter(RegulatoryIncentive.is_active == "yes")

    query = query.order_by(RegulatoryIncentive.jurisdiction, RegulatoryIncentive.policy_name)
    return [_model_to_dict(ri) for ri in query.all()]


# =============================================================================
# GREEN CONTRACTS
# =============================================================================

def get_green_contracts(
    session: Session,
    certification_type: Optional[str] = None,
) -> list[dict]:
    """
    Fetch green contract premium data.

    Args:
        session: SQLAlchemy session
        certification_type: Filter by certification type (partial match)

    Returns:
        List of green contract dicts ordered by win_rate_premium ascending
    """
    query = session.query(GreenContract)

    if certification_type:
        query = query.filter(GreenContract.certification_type.ilike(f"%{certification_type}%"))

    query = query.order_by(GreenContract.win_rate_premium)
    return [_model_to_dict(gc) for gc in query.all()]


def get_green_contract_comparison(session: Session) -> list[dict]:
    """
    Certification comparison table for the dashboard.

    Returns:
        List ordered by win_rate_premium with normalized metrics
    """
    contracts = session.query(GreenContract).order_by(GreenContract.win_rate_premium).all()
    baseline = next((c for c in contracts if c.certification_type == "No Green Certification (Baseline)"), None)

    result = []
    for c in contracts:
        d = _model_to_dict(c)
        # Add relative advantage vs baseline
        if baseline and c.certification_type != "No Green Certification (Baseline)":
            d["win_rate_advantage_vs_baseline"] = _to_float(c.win_rate_premium)
            d["value_premium_vs_baseline"] = _to_float(c.contract_value_premium)
        result.append(d)
    return result


# =============================================================================
# DASHBOARD SUMMARY
# =============================================================================

def get_dashboard_summary(session: Session) -> dict:
    """
    Aggregate summary for the executive dashboard landing page.

    Returns a dict with:
      - market_summary: key market size and growth metrics
      - technology_categories: list of category summaries
      - top_roi_technologies: top 3 by moderate ROI
      - key_incentives: federal incentives summary
      - certification_impact: LEED Gold vs baseline comparison
    """
    # Market summary
    market_summary = get_market_trend_summary(session)

    # Technology categories
    tech_categories = get_technology_categories(session)

    # Top ROI technologies (moderate scenario, sorted by roi_percentage desc)
    top_roi_rows = (
        session.query(
            Technology.name,
            Technology.category,
            ROIScenario.roi_percentage,
            ROIScenario.payback_years,
        )
        .join(ROIScenario, ROIScenario.technology_id == Technology.id)
        .filter(ROIScenario.scenario_type == "moderate")
        .order_by(ROIScenario.roi_percentage.desc())
        .limit(5)
        .all()
    )
    top_roi = [
        {
            "technology_name": r.name,
            "category": r.category,
            "roi_percentage": _to_float(r.roi_percentage),
            "payback_years": _to_float(r.payback_years),
        }
        for r in top_roi_rows
    ]

    # Key federal incentives
    federal_incentives = (
        session.query(RegulatoryIncentive)
        .filter(RegulatoryIncentive.jurisdiction == "Federal")
        .filter(RegulatoryIncentive.is_active == "yes")
        .order_by(RegulatoryIncentive.financial_impact_b.desc())
        .all()
    )
    key_incentives = [
        {
            "policy_name": r.policy_name,
            "type": r.type,
            "financial_impact": r.financial_impact,
            "financial_impact_b": _to_float(r.financial_impact_b),
        }
        for r in federal_incentives
    ]

    # LEED Gold vs baseline
    leed_gold = session.query(GreenContract).filter(
        GreenContract.certification_type == "LEED Gold"
    ).first()
    certification_impact = _model_to_dict(leed_gold) if leed_gold else {}

    # Case study count and summary
    total_case_studies = session.query(func.count(CaseStudy.id)).scalar()

    return {
        "market_summary": market_summary,
        "technology_categories": tech_categories,
        "top_roi_technologies": top_roi,
        "key_incentives": key_incentives,
        "certification_impact_leed_gold": certification_impact,
        "total_case_studies": total_case_studies,
        "total_technologies": session.query(func.count(Technology.id)).scalar(),
        "total_incentives": session.query(func.count(RegulatoryIncentive.id)).scalar(),
    }
