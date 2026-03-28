"""
Pydantic v2 schemas for the Renewable Energy Executive Dashboard API.

All models are production-ready with:
- Full type annotations
- Field descriptions and examples
- Optional fields where data may be absent
- Proper validation constraints
- OpenAPI-compatible metadata
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Region(str, Enum):
    """North American region identifier."""

    US = "US"
    CANADA = "Canada"
    MEXICO = "Mexico"
    NORTH_AMERICA = "North America"


class TechnologyCategory(str, Enum):
    """High-level technology category."""

    ELECTRIC_EQUIPMENT = "Electric Equipment"
    SOLAR_PV = "Solar PV"
    GREEN_BUILDING_SYSTEMS = "Green Building Systems"
    BATTERY_STORAGE = "Battery Storage"
    GREEN_HYDROGEN = "Green Hydrogen"
    MASS_TIMBER = "Mass Timber"
    ENERGY_MANAGEMENT = "Energy Management"


class ProjectionScenario(str, Enum):
    """Financial projection scenario."""

    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


class LEEDLevel(str, Enum):
    """LEED certification level."""

    CERTIFIED = "Certified"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class CertificationStandard(str, Enum):
    """Green building certification standard."""

    LEED = "LEED"
    WELL = "WELL"
    LIVING_BUILDING = "Living Building Challenge"
    GREEN_GLOBES = "Green Globes"
    ENERGY_STAR = "ENERGY STAR"
    PASSIVE_HOUSE = "Passive House"
    ISO_14001 = "ISO 14001"
    BREEAM = "BREEAM"
    ENVISION = "Envision"


class FirmSize(str, Enum):
    """Construction firm size classification."""

    SMALL = "Small (<$50M)"
    MID_SIZE = "Mid-Size ($50M-$500M)"
    LARGE = "Large (>$500M)"


class ConfidenceLevel(str, Enum):
    """Research data confidence level."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ---------------------------------------------------------------------------
# Shared / Base models
# ---------------------------------------------------------------------------


class TimeSeriesPoint(BaseModel):
    """A single data point in a time series."""

    year: int = Field(..., ge=2000, le=2040, description="Calendar year")
    value: float = Field(..., description="Metric value for this year")
    unit: str = Field(..., description="Unit of measurement (e.g. 'USD billions', '%')")
    estimated: bool = Field(
        False, description="True if this is a forward projection rather than recorded data"
    )
    confidence: Optional[ConfidenceLevel] = Field(
        None, description="Research confidence level for this data point"
    )


class SourceCitation(BaseModel):
    """Reference source for a data claim."""

    name: str = Field(..., description="Short display name of the source")
    organization: str = Field(..., description="Publishing organization")
    url: Optional[str] = Field(None, description="Public URL to the source")
    published_date: Optional[str] = Field(
        None, description="Publication or access date (YYYY-MM or YYYY-MM-DD)"
    )
    confidence: ConfidenceLevel = Field(..., description="Data confidence level")


class KeyMetric(BaseModel):
    """A single named KPI/metric."""

    label: str = Field(..., description="Human-readable label for the metric")
    value: float = Field(..., description="Numeric value")
    unit: str = Field(..., description="Unit (e.g. 'USD billions', '%', 'years')")
    description: Optional[str] = Field(None, description="Additional context")


# ---------------------------------------------------------------------------
# 1. Market Trends  —  GET /api/market-trends
# ---------------------------------------------------------------------------


class AdoptionRateByFirmSize(BaseModel):
    """Renewable energy adoption characteristics broken out by firm size."""

    firm_size: FirmSize
    formal_esg_program_pct_min: float = Field(
        ..., ge=0, le=100, description="Lower bound % of firms with formal ESG/sustainability program"
    )
    formal_esg_program_pct_max: float = Field(
        ..., ge=0, le=100, description="Upper bound % of firms with formal ESG/sustainability program"
    )
    leed_experience_pct_min: float = Field(
        ..., ge=0, le=100, description="Lower bound % with LEED or green certification experience"
    )
    leed_experience_pct_max: float = Field(
        ..., ge=0, le=100, description="Upper bound % with LEED or green certification experience"
    )
    electric_equipment_fleet_pct_min: float = Field(
        ..., ge=0, le=100, description="Lower bound % of fleet electrified"
    )
    electric_equipment_fleet_pct_max: float = Field(
        ..., ge=0, le=100, description="Upper bound % of fleet electrified"
    )
    has_dedicated_sustainability_team: str = Field(
        ..., description="Qualitative description (e.g. 'Common', 'Emerging', 'Very rare')"
    )
    on_site_solar_deployed: str = Field(
        ..., description="Qualitative description of on-site solar deployment"
    )
    confidence: ConfidenceLevel


class MarketSizeSnapshot(BaseModel):
    """Point-in-time market size figure."""

    market_name: str = Field(..., description="Name of the market segment")
    value_usd_billions: float = Field(..., description="Market size in USD billions")
    year: int = Field(..., ge=2020, le=2040)
    is_projection: bool = Field(False, description="True if this is a future projection")
    cagr_pct: Optional[float] = Field(None, description="Compound annual growth rate (%)")
    cagr_period: Optional[str] = Field(
        None, description="Period the CAGR covers (e.g. '2026–2035')"
    )
    source: str = Field(..., description="Primary source name")
    confidence: ConfidenceLevel


class MarketDriverOrBarrier(BaseModel):
    """A single market driver or barrier."""

    name: str = Field(..., description="Short name")
    description: str = Field(..., description="Detailed explanation")
    severity: str = Field(..., description="Severity/impact level: High, Medium, Low")
    trend: str = Field(..., description="Direction of change: Increasing, Stable, Declining, Mixed")
    impact_on_mid_size_firms: Optional[str] = Field(
        None, description="Specific impact qualifier for mid-size firms"
    )
    confidence: ConfidenceLevel


class MarketTrendsResponse(BaseModel):
    """Response body for GET /api/market-trends."""

    as_of_date: str = Field(
        ..., description="Date this data was last compiled (YYYY-MM-DD)"
    )

    # Global green building
    global_green_building_market_2025_usd_b: float = Field(
        ..., description="Global green building market size in 2025 (USD billions)"
    )
    global_green_building_market_2034_projected_usd_b: float = Field(
        ..., description="Projected global green building market in 2034 (USD billions)"
    )
    global_green_building_cagr_pct: float = Field(
        ..., description="Green building market CAGR 2025–2034 (%)"
    )

    # North America
    north_america_market_share_pct: float = Field(
        ..., description="North America share of global green building materials market (%)"
    )
    north_america_market_2025_usd_b: float = Field(
        ..., description="North America green building materials market in 2025 (USD billions)"
    )

    # Electric equipment
    electric_equipment_market_2025_usd_b_min: float = Field(
        ..., description="Electric construction equipment market low estimate, 2025 (USD billions)"
    )
    electric_equipment_market_2025_usd_b_max: float = Field(
        ..., description="Electric construction equipment market high estimate, 2025 (USD billions)"
    )
    electric_equipment_market_2030_projected_usd_b: float = Field(
        ..., description="Projected electric construction equipment market in 2030 (USD billions)"
    )
    electric_equipment_cagr_pct: float = Field(
        ..., description="Electric equipment market CAGR 2026–2035 (%)"
    )

    # IRA
    ira_clean_energy_incentives_usd_b: float = Field(
        ..., description="IRA tax credits allocated to renewable energy (USD billions)"
    )
    commercial_solar_adoption_boost_post_ira_pct: float = Field(
        ..., description="Percentage boost in commercial solar adoption post-IRA (%)"
    )

    # Buildings / environment
    buildings_global_co2_share_pct: float = Field(
        ..., description="Buildings share of global energy-related CO2 emissions (%)"
    )

    # Key metrics list
    key_metrics: list[KeyMetric] = Field(
        ..., description="Additional headline KPIs for dashboard display"
    )

    # Adoption by firm size
    adoption_by_firm_size: list[AdoptionRateByFirmSize] = Field(
        ..., description="Renewable energy adoption breakdown by company size"
    )

    # Time series
    global_market_time_series: list[TimeSeriesPoint] = Field(
        ..., description="Historical and projected global green building market values"
    )
    electric_equipment_time_series: list[TimeSeriesPoint] = Field(
        ..., description="Historical and projected electric construction equipment market values"
    )

    # Drivers and barriers
    drivers: list[MarketDriverOrBarrier] = Field(..., description="Key market drivers")
    barriers: list[MarketDriverOrBarrier] = Field(..., description="Key market barriers")

    sources: list[SourceCitation] = Field(..., description="Primary data sources")


# ---------------------------------------------------------------------------
# 2. Regional Data  —  GET /api/regional-data
# ---------------------------------------------------------------------------


class StateRegionalData(BaseModel):
    """Green building data for a single U.S. state."""

    state: str = Field(..., description="State name or code")
    leed_rank_2025: Optional[int] = Field(
        None, ge=1, description="USGBC LEED ranking for 2025 (1 = best)"
    )
    leed_rank_2024: Optional[int] = Field(None, ge=1, description="USGBC LEED ranking for 2024")
    rank_change_yoy: Optional[int] = Field(
        None, description="Change in rank vs. prior year (negative = improved)"
    )
    key_drivers: list[str] = Field(default_factory=list, description="Primary LEED/green drivers")
    key_policies: list[str] = Field(
        default_factory=list, description="Key state/local green building policies"
    )
    leed_credential_holders: Optional[int] = Field(
        None, description="Number of LEED professional credential holders in the state"
    )
    notable_projects: list[str] = Field(
        default_factory=list, description="Notable green building projects in this state"
    )


class CountryRegionalData(BaseModel):
    """Green building data for a North American country."""

    country: Region
    leed_certified_space_sq_meters_m: float = Field(
        ..., description="Total LEED-certified space in millions of gross square meters"
    )
    leed_certified_projects: Optional[int] = Field(
        None, description="Approximate number of LEED-certified projects"
    )
    global_leed_rank: Optional[int] = Field(
        None, description="Global ranking by LEED certified space (ex-US for non-US countries)"
    )
    market_size_2025_usd_b: Optional[float] = Field(
        None, description="Green building market size (USD billions)"
    )
    market_cagr_pct: Optional[float] = Field(
        None, description="Green building market CAGR (%)"
    )
    key_strategies: list[str] = Field(
        default_factory=list, description="National green building strategies"
    )
    leading_provinces_or_states: list[str] = Field(
        default_factory=list, description="Leading sub-national jurisdictions"
    )
    key_drivers: list[str] = Field(default_factory=list, description="Country-specific market drivers")
    key_challenges: list[str] = Field(
        default_factory=list, description="Country-specific market challenges"
    )
    notable_milestones: list[str] = Field(
        default_factory=list, description="Notable recent certifications or milestones"
    )
    confidence: ConfidenceLevel


class RegionalDataResponse(BaseModel):
    """Response body for GET /api/regional-data."""

    as_of_date: str
    top_us_states_2025: list[StateRegionalData] = Field(
        ..., description="USGBC top 10 states for LEED in 2025"
    )
    country_data: list[CountryRegionalData] = Field(
        ..., description="Country-level breakdown for US, Canada, Mexico"
    )
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 3. Technologies  —  GET /api/technologies
# ---------------------------------------------------------------------------


class TechnologyROIMetric(BaseModel):
    """ROI and financial performance data for a technology."""

    payback_years_min: Optional[float] = Field(
        None, ge=0, description="Best-case payback period (years)"
    )
    payback_years_max: Optional[float] = Field(
        None, ge=0, description="Worst-case payback period (years)"
    )
    payback_years_typical: Optional[float] = Field(
        None, ge=0, description="Typical payback period (years)"
    )
    npv_20yr_usd_k_per_unit: Optional[float] = Field(
        None, description="20-year NPV per unit/system (USD thousands)"
    )
    irr_pct: Optional[float] = Field(None, description="Internal rate of return (%)")
    annual_savings_usd_k: Optional[float] = Field(
        None, description="Estimated annual savings (USD thousands)"
    )
    upfront_cost_premium_pct: Optional[float] = Field(
        None, description="Cost premium vs. conventional equivalent (%)"
    )
    operating_cost_reduction_pct: Optional[float] = Field(
        None, description="Operating cost reduction vs. baseline (%)"
    )


class FeasibilityScore(BaseModel):
    """Technology feasibility scoring for mid-size construction firms."""

    overall_score: float = Field(
        ..., ge=0, le=10, description="Overall feasibility score out of 10"
    )
    technical_maturity: float = Field(
        ..., ge=0, le=10, description="Technical maturity and reliability (0–10)"
    )
    financial_viability: float = Field(
        ..., ge=0, le=10, description="Financial viability for mid-size firms (0–10)"
    )
    regulatory_support: float = Field(
        ..., ge=0, le=10, description="Regulatory support and incentive availability (0–10)"
    )
    workforce_readiness: float = Field(
        ..., ge=0, le=10, description="Workforce skill availability (0–10)"
    )
    supply_chain_maturity: float = Field(
        ..., ge=0, le=10, description="Supply chain maturity (0–10)"
    )
    mid_size_adoption_ease: float = Field(
        ..., ge=0, le=10, description="Ease of adoption for mid-size firms specifically (0–10)"
    )


class Technology(BaseModel):
    """Full detail for a single renewable energy / green technology."""

    id: str = Field(..., description="URL-safe unique identifier (e.g. 'solar-pv')")
    name: str = Field(..., description="Display name")
    category: TechnologyCategory
    description: str = Field(..., description="1-2 sentence summary")
    market_size_2025_usd_b: Optional[float] = Field(
        None, description="Total addressable market in 2025 (USD billions)"
    )
    market_size_2030_projected_usd_b: Optional[float] = Field(
        None, description="Projected market in 2030 (USD billions)"
    )
    market_cagr_pct: Optional[float] = Field(None, description="Market CAGR (%)")
    market_cagr_period: Optional[str] = Field(None, description="CAGR measurement period")
    north_america_market_share_pct: Optional[float] = Field(
        None, description="North American share of global market (%)"
    )
    feasibility: FeasibilityScore
    roi: TechnologyROIMetric
    key_benefits: list[str] = Field(default_factory=list, description="Primary value propositions")
    key_barriers: list[str] = Field(default_factory=list, description="Main adoption obstacles")
    leading_vendors: list[str] = Field(
        default_factory=list, description="Notable product/vendor examples"
    )
    applicable_firm_sizes: list[FirmSize] = Field(
        default_factory=list, description="Firm sizes for which this tech is currently viable"
    )
    relevant_certifications: list[str] = Field(
        default_factory=list, description="Certifications this technology supports"
    )
    energy_savings_pct: Optional[float] = Field(
        None, description="Typical energy savings vs. baseline (%)"
    )
    co2_reduction_pct: Optional[float] = Field(
        None, description="Typical CO2 reduction vs. baseline (%)"
    )
    confidence: ConfidenceLevel
    sources: list[str] = Field(default_factory=list, description="Source names for this technology")


class TechnologiesResponse(BaseModel):
    """Response body for GET /api/technologies."""

    as_of_date: str
    technologies: list[Technology]
    summary_adoption_rates: dict[str, float] = Field(
        ...,
        description=(
            "Technology name → adoption rate (%) among top firms as percentage of case-study cohort"
        ),
    )
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 4. Technology Comparison  —  GET /api/technology/{id}/comparison
# ---------------------------------------------------------------------------


class TCOComponent(BaseModel):
    """A single component of a total cost of ownership analysis."""

    component: str = Field(..., description="Cost component name (e.g. 'Capital Expenditure')")
    green_cost_usd_k: float = Field(..., description="Green/renewable option cost (USD thousands)")
    conventional_cost_usd_k: float = Field(
        ..., description="Conventional option cost (USD thousands)"
    )
    difference_usd_k: float = Field(
        ..., description="Green minus conventional (negative = green is cheaper)"
    )
    notes: Optional[str] = Field(None, description="Explanatory notes")


class TCOScenario(BaseModel):
    """Full TCO breakdown for a defined scenario."""

    scenario_name: str = Field(..., description="Scenario label (e.g. 'Base Case 10-year TCO')")
    analysis_period_years: int = Field(
        ..., ge=1, le=30, description="Analysis horizon in years"
    )
    discount_rate_pct: float = Field(..., description="Discount rate applied to NPV (%)")
    green_total_tco_usd_k: float = Field(
        ..., description="Total cost of ownership, green option (USD thousands)"
    )
    conventional_total_tco_usd_k: float = Field(
        ..., description="Total cost of ownership, conventional option (USD thousands)"
    )
    green_advantage_usd_k: float = Field(
        ...,
        description=(
            "Conventional TCO minus green TCO (positive = green is cheaper over analysis period)"
        ),
    )
    breakeven_year: Optional[float] = Field(
        None, description="Year in which cumulative green savings exceed upfront premium"
    )
    components: list[TCOComponent]
    assumptions: list[str] = Field(default_factory=list, description="Key modeling assumptions")


class TechnologyComparisonResponse(BaseModel):
    """Response body for GET /api/technology/{id}/comparison."""

    technology_id: str
    technology_name: str
    conventional_equivalent: str = Field(
        ..., description="The conventional technology being compared against"
    )
    comparison_unit: str = Field(
        ..., description="Unit of comparison (e.g. 'per machine', 'per 1,000 sq ft')"
    )
    tco_scenarios: list[TCOScenario]
    key_financial_insights: list[str] = Field(
        ..., description="Top 3-5 insights from the TCO analysis"
    )
    incentives_included: list[str] = Field(
        ..., description="Incentives factored into the green TCO calculation"
    )
    data_confidence: ConfidenceLevel
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 5. Payback Analysis  —  GET /api/payback-analysis
# ---------------------------------------------------------------------------


class PaybackEntry(BaseModel):
    """Payback period data for a single technology."""

    technology_id: str
    technology_name: str
    category: TechnologyCategory
    payback_years_base: float = Field(
        ..., ge=0, description="Payback period without incentives (years)"
    )
    payback_years_with_incentives: float = Field(
        ..., ge=0, description="Payback period with available incentives (years)"
    )
    payback_years_optimistic: float = Field(
        ..., ge=0, description="Best-case payback period (years)"
    )
    payback_years_pessimistic: float = Field(
        ..., ge=0, description="Worst-case payback period (years)"
    )
    primary_incentive_used: Optional[str] = Field(
        None, description="Name of the main incentive modeled"
    )
    incentive_value_pct: Optional[float] = Field(
        None, description="Incentive as % of project cost"
    )
    typical_project_cost_usd_k_min: Optional[float] = Field(
        None, description="Typical minimum project cost (USD thousands)"
    )
    typical_project_cost_usd_k_max: Optional[float] = Field(
        None, description="Typical maximum project cost (USD thousands)"
    )
    annual_savings_usd_k: Optional[float] = Field(
        None, description="Estimated annual savings (USD thousands)"
    )
    notes: Optional[str] = Field(None, description="Context or caveats")
    confidence: ConfidenceLevel


class PaybackAnalysisResponse(BaseModel):
    """Response body for GET /api/payback-analysis."""

    as_of_date: str
    analysis_assumptions: list[str] = Field(
        ..., description="Global assumptions applied to all payback calculations"
    )
    payback_data: list[PaybackEntry]
    summary_stats: dict[str, float] = Field(
        ...,
        description=(
            "Summary statistics: avg_payback_no_incentives, avg_payback_with_incentives, "
            "min_payback, max_payback"
        ),
    )
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 6. ROI Scenarios  —  GET /api/roi-scenarios
# ---------------------------------------------------------------------------


class AnnualROIProjection(BaseModel):
    """Single year ROI projection within a scenario."""

    year: int = Field(..., ge=2024, le=2040)
    cumulative_investment_usd_k: float = Field(
        ..., description="Cumulative investment to date (USD thousands)"
    )
    cumulative_savings_usd_k: float = Field(
        ..., description="Cumulative savings/returns to date (USD thousands)"
    )
    net_position_usd_k: float = Field(
        ..., description="Net financial position (savings minus investment, USD thousands)"
    )
    roi_pct: float = Field(..., description="ROI percentage at this point in time")


class ROIScenario(BaseModel):
    """Full ROI projection for a single scenario."""

    scenario: ProjectionScenario
    label: str = Field(..., description="Human-friendly label (e.g. 'Conservative Case')")
    description: str = Field(..., description="Assumptions narrative for this scenario")
    technologies_included: list[str] = Field(
        ..., description="Technologies bundled in this portfolio scenario"
    )
    initial_investment_usd_k: float = Field(
        ..., description="Year 0 capital outlay (USD thousands)"
    )
    ten_year_roi_pct: float = Field(..., description="10-year projected ROI (%)")
    ten_year_npv_usd_k: float = Field(..., description="10-year NPV (USD thousands)")
    irr_pct: float = Field(..., description="Internal rate of return (%)")
    breakeven_year: float = Field(..., description="Expected breakeven year")
    annual_projections: list[AnnualROIProjection]
    key_assumptions: list[str] = Field(..., description="Scenario-specific assumptions")
    risk_factors: list[str] = Field(..., description="Key risks that could affect the scenario")


class ROIScenariosResponse(BaseModel):
    """Response body for GET /api/roi-scenarios."""

    as_of_date: str
    base_year: int = Field(..., description="Base year for all projections")
    representative_firm_profile: str = Field(
        ...,
        description="Description of the representative firm modeled (size, revenue, geography)",
    )
    discount_rate_pct: float = Field(..., description="Discount rate used in NPV calculations (%)")
    scenarios: list[ROIScenario]
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 7. Incentives  —  GET /api/incentives
# ---------------------------------------------------------------------------


class Incentive(BaseModel):
    """A regulatory or financial incentive for renewable energy adoption."""

    id: str = Field(..., description="URL-safe unique identifier")
    name: str = Field(..., description="Official incentive name")
    program: str = Field(
        ..., description="Legislation or program (e.g. 'Inflation Reduction Act')"
    )
    jurisdiction: str = Field(
        ..., description="Applicable jurisdiction (e.g. 'Federal', 'California', 'Canada')"
    )
    incentive_type: str = Field(
        ...,
        description="Type: Tax Credit, Tax Deduction, Grant, Rebate, Loan, Mandate, Rate Incentive",
    )
    applicable_technologies: list[str] = Field(
        ..., description="Technologies or project types eligible for this incentive"
    )
    value_description: str = Field(
        ...,
        description="Human-readable value description (e.g. '30% investment tax credit')",
    )
    value_pct: Optional[float] = Field(
        None, ge=0, le=100, description="Incentive value as percentage of project cost"
    )
    value_usd_k_max: Optional[float] = Field(
        None, description="Maximum dollar value per project (USD thousands)"
    )
    total_program_budget_usd_b: Optional[float] = Field(
        None, description="Total program budget if capped (USD billions)"
    )
    eligible_firm_sizes: list[FirmSize] = Field(
        ..., description="Firm sizes eligible for this incentive"
    )
    prevailing_wage_required: bool = Field(
        False,
        description="Whether prevailing wage requirements must be met for full incentive value",
    )
    domestic_content_bonus_available: bool = Field(
        False, description="Whether a domestic content bonus is available"
    )
    expiration_year: Optional[int] = Field(
        None, description="Year the incentive expires (if known)"
    )
    political_risk: Optional[str] = Field(
        None, description="Political stability risk note (e.g. 'OBBBA may reduce credits')"
    )
    financial_impact_description: str = Field(
        ..., description="How this incentive affects project economics"
    )
    payback_reduction_years: Optional[float] = Field(
        None, description="Estimated reduction in payback period from this incentive alone (years)"
    )
    status: str = Field(..., description="Current status: Active, Modified, At Risk, Expired")
    confidence: ConfidenceLevel
    source: str = Field(..., description="Primary source name")


class IncentivesResponse(BaseModel):
    """Response body for GET /api/incentives."""

    as_of_date: str
    total_ira_budget_usd_b: float = Field(
        ..., description="Total IRA clean energy tax credit allocation (USD billions)"
    )
    total_incentives_listed: int = Field(..., description="Total number of incentives in this dataset")
    incentives: list[Incentive]
    political_risk_summary: str = Field(
        ...,
        description="High-level summary of legislative risk to incentive programs",
    )
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 8. Case Studies  —  GET /api/case-studies
# ---------------------------------------------------------------------------


class CaseStudyROIMetric(BaseModel):
    """Concrete ROI data point from a case study."""

    metric_name: str = Field(..., description="Name of the metric (e.g. 'Annual green revenue')")
    value: str = Field(..., description="Value as a formatted string (e.g. '$2.6B')")
    value_numeric: Optional[float] = Field(
        None, description="Numeric value for sorting/charting"
    )
    unit: Optional[str] = Field(None, description="Unit (e.g. 'USD billions/year')")
    confidence: ConfidenceLevel
    notes: Optional[str] = Field(None, description="Caveats (e.g. 'vendor-sourced figure')")


class TechnologyAdoptionItem(BaseModel):
    """Technology adopted by a case-study firm."""

    technology: str = Field(..., description="Technology name")
    adoption_level: str = Field(
        ..., description="Adoption level: Pilot, Partial, Full, Leading"
    )
    notes: Optional[str] = Field(None, description="Specific deployment details")


class CaseStudy(BaseModel):
    """Competitive benchmarking profile for a construction firm."""

    id: str = Field(..., description="URL-safe identifier (e.g. 'mortenson')")
    company_name: str
    headquarters: str = Field(..., description="City, State/Province")
    annual_revenue_usd_b: float = Field(..., description="Approximate annual revenue (USD billions)")
    employees: int = Field(..., description="Approximate headcount")
    specializations: list[str] = Field(..., description="Primary construction specializations")
    enr_green_rank: Optional[str] = Field(
        None, description="ENR Top 100 Green Contractors ranking"
    )
    sustainability_start_year: int = Field(
        ..., description="Year the firm began systematic sustainability efforts"
    )
    primary_strategy: str = Field(..., description="One-sentence description of sustainability strategy")
    net_zero_target_year: Optional[int] = Field(None, description="Net zero commitment year if any")
    sbti_committed: bool = Field(False, description="Has committed to Science Based Targets initiative")
    has_dedicated_sustainability_team: bool = Field(
        ..., description="Whether a dedicated sustainability team exists"
    )
    key_differentiator: str = Field(..., description="Single most distinctive sustainability capability")
    technologies_adopted: list[TechnologyAdoptionItem]
    roi_metrics: list[CaseStudyROIMetric]
    key_lessons: list[str] = Field(..., description="Replicable insights for mid-size firms")
    applicable_to_mid_size: bool = Field(
        ..., description="Whether this case study's approach is relevant for $50M-$500M firms"
    )
    replication_investment_min_usd_k: Optional[float] = Field(
        None,
        description="Minimum investment needed for a mid-size firm to replicate key strategies (USD thousands)",
    )
    replication_investment_max_usd_k: Optional[float] = Field(
        None,
        description="Maximum investment needed for a mid-size firm to replicate key strategies (USD thousands)",
    )
    confidence: ConfidenceLevel
    sources: list[str] = Field(..., description="Primary source names for this case study")


class InvestmentPriorityItem(BaseModel):
    """Recommended investment priority for mid-size firms."""

    priority: int = Field(..., ge=1, description="Priority rank (1 = highest priority)")
    investment: str = Field(..., description="Investment type or action")
    annual_cost_usd_k_min: float = Field(..., description="Minimum annual cost (USD thousands)")
    annual_cost_usd_k_max: float = Field(..., description="Maximum annual cost (USD thousands)")
    roi_timeline_description: str = Field(
        ..., description="Expected timeline to realize ROI (e.g. '6–12 months')"
    )
    confidence: ConfidenceLevel


class TechnologyAdoptionSummary(BaseModel):
    """Aggregate technology adoption across all case study firms."""

    technology: str
    firms_using: int = Field(..., description="Number of case study firms using this technology")
    total_firms: int = Field(..., description="Total case study firms in cohort")
    adoption_rate_pct: float = Field(..., description="Adoption rate (%)")


class CaseStudiesResponse(BaseModel):
    """Response body for GET /api/case-studies."""

    as_of_date: str
    total_firms_profiled: int
    case_studies: list[CaseStudy]
    technology_adoption_summary: list[TechnologyAdoptionSummary] = Field(
        ..., description="Aggregate technology adoption across all profiled firms"
    )
    investment_priority_matrix: list[InvestmentPriorityItem] = Field(
        ..., description="Prioritized investment recommendations for mid-size firms"
    )
    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 9. Green Contracts  —  GET /api/green-contracts
# ---------------------------------------------------------------------------


class BidWinRateDataPoint(BaseModel):
    """Correlation data point between green credential level and bid win rates."""

    credential_level: str = Field(
        ...,
        description="Credential/certification level (e.g. 'LEED AP BD+C Staff', 'No LEED')",
    )
    win_rate_multiplier: Optional[float] = Field(
        None, description="Win rate multiplier vs. baseline non-credentialed firm"
    )
    project_segment: str = Field(
        ...,
        description="Project segment (e.g. 'Federal >$50M', 'State/Municipal', 'Corporate ESG')",
    )
    inclusion_in_bid_pool_pct: Optional[float] = Field(
        None, ge=0, le=100, description="% of RFPs for which the firm qualifies to bid (%)"
    )
    notes: str = Field(..., description="Narrative context for this data point")
    confidence: ConfidenceLevel


class ContractPremiumData(BaseModel):
    """Premium data for a category of green building contracts."""

    category: str = Field(..., description="Category (e.g. 'LEED Rent Premium', 'Cost Premium')")
    metric: str = Field(..., description="Specific metric name")
    value: str = Field(..., description="Value as formatted string")
    value_numeric: Optional[float] = Field(None)
    unit: Optional[str] = Field(None)
    context: str = Field(..., description="Methodological context")
    confidence: ConfidenceLevel
    source: str


class CertificationMarketData(BaseModel):
    """Market penetration data for a certification standard."""

    certification: CertificationStandard
    global_projects: Optional[int] = Field(None, description="Approximate global certified projects")
    na_adoption_scale: str = Field(..., description="Qualitative North American adoption scale")
    typical_cost_min_usd_k: Optional[float] = Field(
        None, description="Minimum certification cost (USD thousands)"
    )
    typical_cost_max_usd_k: Optional[float] = Field(
        None, description="Maximum certification cost (USD thousands)"
    )
    federal_acceptance: bool = Field(..., description="Accepted by US federal agencies (GSA)")
    leed_spec_prevalence_pct: Optional[float] = Field(
        None,
        description="% of project specs >$50M that reference this certification",
    )
    credential_holders_worldwide: Optional[int] = Field(
        None, description="Global professional credential holders"
    )
    key_benefit: str = Field(..., description="Primary competitive benefit of this certification")
    recommended_for_mid_size: bool = Field(
        ..., description="Recommended as priority for mid-size firms"
    )


class GreenContractWinFactors(BaseModel):
    """Factors that drive green contract win rates."""

    factor: str = Field(..., description="Factor name")
    description: str = Field(..., description="How this factor improves win rates")
    importance: str = Field(..., description="Importance: Critical, High, Medium, Low")
    mid_size_applicability: str = Field(
        ..., description="How applicable this factor is for mid-size firms"
    )


class GreenContractsResponse(BaseModel):
    """Response body for GET /api/green-contracts."""

    as_of_date: str

    # Market access summary
    leed_spec_prevalence_pct: float = Field(
        ...,
        description="% of project specs for projects >$50M that reference LEED (%)",
    )
    states_with_leed_mandates: int = Field(
        ..., description="Number of US states that have adopted LEED or equivalent for public buildings"
    )
    federal_leed_requirement: str = Field(
        ..., description="Federal LEED requirement level (e.g. 'LEED Gold for new federal buildings')"
    )
    green_certified_office_share_pct: float = Field(
        ..., description="% of office space in top 30 US markets that is green-certified (%)"
    )

    # Win rate correlation
    bid_win_rate_data: list[BidWinRateDataPoint]

    # Contract premiums
    contract_premiums: list[ContractPremiumData]

    # Certification landscape
    certification_landscape: list[CertificationMarketData]

    # Win factors
    win_factors: list[GreenContractWinFactors]

    # LEED credential landscape
    total_leed_credential_holders: int = Field(..., description="Total LEED credentials worldwide")
    leed_ap_holders: int = Field(..., description="LEED Accredited Professionals worldwide")
    leed_om_growth_pct: float = Field(
        ...,
        description=(
            "% growth in LEED O+M certifications 2019–2024 (post-COVID acceleration)"
        ),
    )

    # Client preferences summary
    client_preference_summary: dict[str, str] = Field(
        ...,
        description=(
            "Client segment → key green credential requirements "
            "(e.g. 'Federal Government' → 'LEED Gold required')"
        ),
    )

    sources: list[SourceCitation]


# ---------------------------------------------------------------------------
# 10. Health Check  —  GET /health
# ---------------------------------------------------------------------------


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str = Field("ok", description="Service status")
    version: str = Field(..., description="API version string")
    timestamp: str = Field(..., description="Current server UTC timestamp (ISO 8601)")
    database: str = Field(..., description="Database connection status: ok | degraded | down")
    uptime_seconds: Optional[float] = Field(None, description="Process uptime in seconds")


# ---------------------------------------------------------------------------
# Error response
# ---------------------------------------------------------------------------


class ErrorDetail(BaseModel):
    """Standard error response body."""

    detail: str = Field(..., description="Human-readable error message")
    code: Optional[str] = Field(None, description="Machine-readable error code")
    field: Optional[str] = Field(None, description="Field name if this is a validation error")


# ---------------------------------------------------------------------------
# Pagination wrapper (for future list expansion)
# ---------------------------------------------------------------------------


class PaginatedResponse(BaseModel):
    """Generic paginated list wrapper."""

    items: list = Field(..., description="Page of results")
    total: int = Field(..., description="Total number of matching items")
    page: int = Field(1, ge=1, description="Current page number")
    page_size: int = Field(50, ge=1, le=200, description="Items per page")
    has_next: bool = Field(..., description="True if more pages are available")
