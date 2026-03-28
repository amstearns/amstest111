"""
SQLAlchemy ORM models for the Renewable Energy Executive Dashboard.

Tables:
  - market_trends: Year/region adoption and market size data
  - technologies: Renewable technologies with TCO and feasibility scores
  - roi_scenarios: ROI analysis by technology and scenario type
  - case_studies: Construction firm case studies with outcomes
  - regulatory_incentives: Policy incentives by jurisdiction
  - green_contracts: Green certification bid/contract premium data

All monetary values stored with 2 decimal places (NUMERIC(15,2)).
All percentage values stored with 1 decimal place (NUMERIC(5,1)).
"""

import uuid
from datetime import datetime, date

from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    Date,
    DateTime,
    Text,
    ARRAY,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class MarketTrend(Base):
    """
    Market adoption and size data by year and region.

    Tracks the green/sustainable construction market growth across
    North American regions over time.
    """
    __tablename__ = "market_trends"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year = Column(Integer, nullable=False, index=True)
    region = Column(String(100), nullable=False, index=True)
    # Adoption rate as percentage (e.g., 47.5 means 47.5%)
    adoption_rate = Column(Numeric(5, 1), nullable=False)
    # Market size in billions USD
    market_size = Column(Numeric(15, 2), nullable=False)
    # Optional context/notes
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<MarketTrend {self.year} {self.region}: {self.adoption_rate}% ${self.market_size}B>"


class Technology(Base):
    """
    Renewable energy technology profiles with cost and feasibility data.

    Tracks technologies relevant to the construction industry including
    solar, wind, electric equipment, and sustainable materials.
    """
    __tablename__ = "technologies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False, index=True)
    # e.g., 'Solar', 'Electric Equipment', 'Sustainable Materials'
    category = Column(String(100), nullable=False, index=True)
    # Feasibility score 0-100 (1 decimal)
    feasibility_score = Column(Numeric(4, 1), nullable=False)
    # Total cost of ownership per unit (USD)
    tco = Column(Numeric(15, 2), nullable=False)
    # Conventional (non-green) alternative TCO for comparison (USD)
    conventional_tco = Column(Numeric(15, 2), nullable=False)
    # e.g., 'Emerging', 'Growing', 'Established', 'Mainstream'
    maturity_level = Column(String(50), nullable=False)
    # Brief description of the technology
    description = Column(Text, nullable=True)
    # CAGR as percentage (e.g., 22.1 means 22.1%)
    cagr = Column(Numeric(5, 1), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Technology {self.name} ({self.category}): {self.maturity_level}>"


class ROIScenario(Base):
    """
    ROI analysis scenarios per technology.

    Provides conservative, moderate, and optimistic ROI projections
    with payback periods and underlying assumptions.
    """
    __tablename__ = "roi_scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # FK to technologies.id (stored as UUID string for portability)
    technology_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    # e.g., 'conservative', 'moderate', 'optimistic'
    scenario_type = Column(String(50), nullable=False, index=True)
    # Payback period in years (1 decimal)
    payback_years = Column(Numeric(5, 1), nullable=False)
    # ROI percentage (1 decimal, e.g., 18.5 means 18.5%)
    roi_percentage = Column(Numeric(6, 1), nullable=False)
    # Key assumptions driving this scenario
    assumptions = Column(Text, nullable=False)
    # NPV in USD (optional)
    npv = Column(Numeric(15, 2), nullable=True)
    # IRR as percentage (optional)
    irr = Column(Numeric(5, 1), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<ROIScenario tech={self.technology_id} {self.scenario_type}: {self.roi_percentage}% in {self.payback_years}yr>"


class CaseStudy(Base):
    """
    Construction firm case studies demonstrating renewable energy adoption.

    Documents real-world implementations with investment, outcomes,
    and timeline data sourced from the competitive benchmarking research.
    """
    __tablename__ = "case_studies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firm_name = Column(String(200), nullable=False, index=True)
    # e.g., 'Large (>$500M)', 'Mid-Size ($50M-$500M)', 'Small (<$50M)'
    size = Column(String(100), nullable=False)
    # List of technologies adopted (PostgreSQL text array)
    technologies_adopted = Column(ARRAY(Text), nullable=False)
    # Annual revenue in USD millions (2 decimal places)
    annual_revenue_m = Column(Numeric(10, 2), nullable=True)
    # Total sustainability investment in USD millions (2 decimal places)
    investment = Column(Numeric(15, 2), nullable=False)
    # Key measurable outcomes (narrative)
    outcomes = Column(Text, nullable=False)
    # Timeline description (e.g., '1995-present', '2018-2024')
    timeline = Column(String(100), nullable=False)
    # Headquarters location
    headquarters = Column(String(200), nullable=True)
    # Primary sustainability strategy
    strategy = Column(Text, nullable=True)
    # ENR green ranking if applicable
    enr_ranking = Column(String(200), nullable=True)
    # Net zero commitment year (nullable)
    net_zero_year = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<CaseStudy {self.firm_name} ({self.size})>"


class RegulatoryIncentive(Base):
    """
    Government policies and financial incentives for renewable energy adoption.

    Covers federal and state-level policies with financial impact
    and expiration information.
    """
    __tablename__ = "regulatory_incentives"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_name = Column(String(300), nullable=False, index=True)
    # e.g., 'Federal', 'California', 'New York', 'Canada Federal'
    jurisdiction = Column(String(100), nullable=False, index=True)
    # e.g., 'Tax Credit', 'Grant', 'Mandate', 'Standard', 'Incentive'
    type = Column(String(100), nullable=False, index=True)
    # Financial impact description / dollar value
    financial_impact = Column(Text, nullable=False)
    # Financial impact in USD billions (nullable for mandates)
    financial_impact_b = Column(Numeric(15, 2), nullable=True)
    # Expiration date (nullable for permanent mandates)
    expiration = Column(Date, nullable=True)
    # Brief description of the policy
    description = Column(Text, nullable=True)
    # Whether currently active
    is_active = Column(String(10), nullable=False, default="yes")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<RegulatoryIncentive {self.policy_name} ({self.jurisdiction})>"


class GreenContract(Base):
    """
    Green certification win rate and contract value premium data.

    Quantifies the competitive advantage of green certifications
    in construction contract bidding.
    """
    __tablename__ = "green_contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # e.g., 'LEED Certified', 'LEED Silver', 'LEED Gold', 'LEED Platinum'
    certification_type = Column(String(100), nullable=False, index=True)
    # Bid win rate premium over non-certified (percentage points, 1 decimal)
    win_rate_premium = Column(Numeric(5, 1), nullable=False)
    # Contract value premium percentage (1 decimal, e.g., 4.0 means 4% higher)
    contract_value_premium = Column(Numeric(5, 1), nullable=False)
    # Construction cost premium over conventional (1 decimal, percentage)
    construction_cost_premium = Column(Numeric(5, 1), nullable=True)
    # Operating cost savings percentage over 5 years (1 decimal)
    operating_cost_savings = Column(Numeric(5, 1), nullable=True)
    # Asset value increase percentage (1 decimal)
    asset_value_increase = Column(Numeric(5, 1), nullable=True)
    # Minimum project value for certification (USD millions)
    min_project_size_m = Column(Numeric(10, 2), nullable=True)
    # Notes on data sources
    data_source = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<GreenContract {self.certification_type}: +{self.win_rate_premium}% win rate>"
