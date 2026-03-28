"""
Pytest configuration and shared fixtures for the dashboard test suite.

This module provides:
- Database session fixtures for testing
- Mock data and sample records
- Utility functions for test setup
"""

import os
import sys
from decimal import Decimal
from typing import Generator
from uuid import uuid4
import json

import pytest
from sqlalchemy import create_engine, event, text, TypeDecorator, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Add workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.models.models import (
    Base,
    MarketTrend,
    Technology,
    ROIScenario,
    CaseStudy,
    RegulatoryIncentive,
    GreenContract,
)


# Patch for SQLite ARRAY handling
# We'll handle this at the engine level with event listeners


# Test database configuration
def pytest_configure(config):
    """Configure pytest with markers and settings."""
    config.addinivalue_line(
        "markers", "database: mark test as requiring database connection"
    )


@pytest.fixture(scope="session")
def test_engine():
    """
    Create an in-memory SQLite test database for isolated testing.
    This engine is used for all database tests in the session.
    
    Note: We use SQLite for testing instead of PostgreSQL to avoid
    database availability issues. SQLite's ARRAY limitations are
    handled by converting ARRAY columns to JSON strings.
    """
    # Use in-memory SQLite for speed and isolation
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    # Handle ARRAY types for SQLite (convert to JSON)
    @event.listens_for(engine, "before_cursor_execute")
    def handle_array_for_sqlite(conn, cursor, statement, parameters, context, executemany):
        if executemany and isinstance(parameters, list):
            # Handle multiple parameter sets
            new_params = []
            for param_set in parameters:
                if isinstance(param_set, dict):
                    new_set = {}
                    for k, v in param_set.items():
                        if isinstance(v, list):
                            new_set[k] = json.dumps(v)
                        else:
                            new_set[k] = v
                    new_params.append(new_set)
                else:
                    new_params.append(param_set)
            # Modify in place isn't possible, but cursor handles it
        elif isinstance(parameters, dict):
            # Handle single parameter set
            for k, v in list(parameters.items()):
                if isinstance(v, list):
                    parameters[k] = json.dumps(v)

    # Create a test-specific Base with ARRAY replaced by JSON
    from sqlalchemy import ARRAY as PG_ARRAY, event as sa_event
    from sqlalchemy.orm import declarative_base
    
    # Monkey-patch ARRAY handling for SQLite
    def _adapt_array_for_sqlite(sqltype, compiler):
        # Replace PostgreSQL ARRAY with JSON string for SQLite
        if hasattr(sqltype, '__class__') and 'ARRAY' in str(sqltype.__class__):
            return String()
        return sqltype

    # Compile the schema - SQLite will adapt ARRAY to TEXT
    with engine.begin() as conn:
        # Create raw SQL to define tables with JSON arrays instead of ARRAY type
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS market_trends (
                id TEXT PRIMARY KEY,
                year INTEGER NOT NULL,
                region TEXT NOT NULL,
                adoption_rate REAL NOT NULL,
                market_size REAL NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS technologies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                feasibility_score REAL NOT NULL,
                tco REAL NOT NULL,
                conventional_tco REAL NOT NULL,
                maturity_level TEXT NOT NULL,
                description TEXT,
                cagr REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS roi_scenarios (
                id TEXT PRIMARY KEY,
                technology_id TEXT NOT NULL,
                scenario_type TEXT NOT NULL,
                payback_years REAL NOT NULL,
                roi_percentage REAL NOT NULL,
                assumptions TEXT NOT NULL,
                npv REAL,
                irr REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS case_studies (
                id TEXT PRIMARY KEY,
                firm_name TEXT NOT NULL,
                size TEXT NOT NULL,
                technologies_adopted TEXT NOT NULL,
                annual_revenue_m REAL,
                investment REAL NOT NULL,
                outcomes TEXT NOT NULL,
                timeline TEXT NOT NULL,
                headquarters TEXT,
                strategy TEXT,
                enr_ranking TEXT,
                net_zero_year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS regulatory_incentives (
                id TEXT PRIMARY KEY,
                policy_name TEXT NOT NULL,
                jurisdiction TEXT NOT NULL,
                type TEXT NOT NULL,
                financial_impact TEXT NOT NULL,
                financial_impact_b REAL,
                expiration DATE,
                description TEXT,
                is_active TEXT DEFAULT 'yes',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS green_contracts (
                id TEXT PRIMARY KEY,
                certification_type TEXT NOT NULL,
                win_rate_premium REAL NOT NULL,
                contract_value_premium REAL NOT NULL,
                construction_cost_premium REAL,
                operating_cost_savings REAL,
                asset_value_increase REAL,
                min_project_size_m REAL,
                data_source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

    yield engine

    # Cleanup
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS green_contracts"))
        conn.execute(text("DROP TABLE IF EXISTS regulatory_incentives"))
        conn.execute(text("DROP TABLE IF EXISTS case_studies"))
        conn.execute(text("DROP TABLE IF EXISTS roi_scenarios"))
        conn.execute(text("DROP TABLE IF EXISTS technologies"))
        conn.execute(text("DROP TABLE IF EXISTS market_trends"))


@pytest.fixture
def db_session(test_engine) -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test.
    Rolls back after test to ensure isolation.
    """
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()

    yield session

    session.rollback()
    session.close()


# ============================================================================
# SAMPLE DATA FIXTURES
# ============================================================================


@pytest.fixture
def sample_market_trends(db_session: Session) -> list[MarketTrend]:
    """Create sample market trend records for testing."""
    trends = [
        MarketTrend(
            year=2025,
            region="North America",
            adoption_rate=Decimal("47.5"),
            market_size=Decimal("618.58"),
            notes="Global green building market 2025 baseline",
        ),
        MarketTrend(
            year=2025,
            region="US",
            adoption_rate=Decimal("52.1"),
            market_size=Decimal("350.00"),
            notes="US market projection 2025",
        ),
        MarketTrend(
            year=2030,
            region="North America",
            adoption_rate=Decimal("68.3"),
            market_size=Decimal("850.00"),
            notes="North America market projection 2030",
        ),
    ]
    for trend in trends:
        db_session.add(trend)
    db_session.commit()
    return trends


@pytest.fixture
def sample_technologies(db_session: Session) -> list[Technology]:
    """Create sample technology records for testing."""
    techs = [
        Technology(
            name="Rooftop Solar Panels",
            category="Solar Energy",
            feasibility_score=Decimal("95.0"),
            tco=Decimal("45000.00"),
            conventional_tco=Decimal("0.00"),
            maturity_level="Mainstream",
            description="Standard rooftop PV installation",
            cagr=Decimal("22.1"),
        ),
        Technology(
            name="Electric Concrete Mixers",
            category="Electric Construction Equipment",
            feasibility_score=Decimal("78.5"),
            tco=Decimal("85000.00"),
            conventional_tco=Decimal("65000.00"),
            maturity_level="Growing",
            description="Battery-powered construction equipment",
            cagr=Decimal("18.5"),
        ),
        Technology(
            name="Cross-Laminated Timber",
            category="Sustainable Building Materials",
            feasibility_score=Decimal("72.0"),
            tco=Decimal("1200.00"),
            conventional_tco=Decimal("900.00"),
            maturity_level="Established",
            description="Sustainable wood alternative to steel/concrete",
            cagr=Decimal("12.3"),
        ),
    ]
    for tech in techs:
        db_session.add(tech)
    db_session.commit()
    return techs


@pytest.fixture
def sample_roi_scenarios(
    db_session: Session, sample_technologies: list[Technology]
) -> list[ROIScenario]:
    """Create sample ROI scenario records for testing."""
    scenarios = []
    for tech in sample_technologies:
        for scenario_type, payback, roi in [
            ("conservative", Decimal("6.5"), Decimal("12.4")),
            ("moderate", Decimal("5.2"), Decimal("18.5")),
            ("optimistic", Decimal("3.8"), Decimal("25.7")),
        ]:
            scenario = ROIScenario(
                technology_id=tech.id,
                scenario_type=scenario_type,
                payback_years=payback,
                roi_percentage=roi,
                npv=Decimal("150000.00") if scenario_type == "optimistic" else None,
                irr=Decimal("15.2") if scenario_type == "optimistic" else None,
                assumptions=f"{scenario_type.capitalize()} case assumptions for {tech.name}",
            )
            scenarios.append(scenario)
            db_session.add(scenario)
    db_session.commit()
    return scenarios


@pytest.fixture
def sample_case_studies(db_session: Session) -> list[CaseStudy]:
    """Create sample case study records for testing."""
    studies = []
    
    study1 = CaseStudy(
        firm_name="Mortenson",
        size="Large (>$500M)",
        technologies_adopted=["Rooftop Solar", "LED Lighting", "Smart Building Controls"],
        annual_revenue_m=Decimal("3500.00"),
        investment=Decimal("75.50"),
        outcomes="35% reduction in operational emissions by 2024",
        timeline="2019-2024",
        headquarters="Minneapolis, MN",
        strategy="Net zero by 2030 commitment",
        enr_ranking="Top 10 Green Builders",
        net_zero_year=2030,
    )
    
    study2 = CaseStudy(
        firm_name="Suffolk",
        size="Large (>$500M)",
        technologies_adopted=["Ground Source Heat Pump", "Recycled Steel", "Solar Canopy"],
        annual_revenue_m=Decimal("2800.00"),
        investment=Decimal("62.00"),
        outcomes="40% energy cost reduction on pilot projects",
        timeline="2018-2023",
        headquarters="Boston, MA",
        strategy="Carbon-neutral operations by 2025",
        enr_ranking="Top 5 Green Builders",
        net_zero_year=2025,
    )
    
    studies = [study1, study2]
    
    for study in studies:
        db_session.add(study)
    db_session.commit()
    return studies


@pytest.fixture
def sample_regulatory_incentives(db_session: Session) -> list[RegulatoryIncentive]:
    """Create sample regulatory incentive records for testing."""
    incentives = [
        RegulatoryIncentive(
            policy_name="Inflation Reduction Act (IRA) ITC",
            jurisdiction="Federal",
            type="Tax Credit",
            financial_impact="Up to 30% tax credit for renewable energy projects",
            financial_impact_b=Decimal("369.75"),
            description="Investment Tax Credit for solar, wind, and other renewables",
            is_active="yes",
        ),
        RegulatoryIncentive(
            policy_name="GSA LEED Gold Mandate",
            jurisdiction="Federal",
            type="Mandate",
            financial_impact="Requires all new federal buildings to be LEED Gold certified",
            description="Executive Order 14057 compliance for federal construction",
            is_active="yes",
        ),
        RegulatoryIncentive(
            policy_name="California CALGreen",
            jurisdiction="California",
            type="Standard",
            financial_impact="Updated green building standards for all new construction",
            description="California Green Building Standards Code requirements",
            is_active="yes",
        ),
    ]
    for incentive in incentives:
        db_session.add(incentive)
    db_session.commit()
    return incentives


@pytest.fixture
def sample_green_contracts(db_session: Session) -> list[GreenContract]:
    """Create sample green contract records for testing."""
    contracts = [
        GreenContract(
            certification_type="LEED Gold",
            win_rate_premium=Decimal("12.3"),
            contract_value_premium=Decimal("4.0"),
            construction_cost_premium=Decimal("2.8"),
            operating_cost_savings=Decimal("18.5"),
            asset_value_increase=Decimal("7.2"),
            min_project_size_m=Decimal("5.00"),
            data_source="CBRE 2022 Green Building Impact Report",
        ),
        GreenContract(
            certification_type="LEED Platinum",
            win_rate_premium=Decimal("18.7"),
            contract_value_premium=Decimal("6.5"),
            construction_cost_premium=Decimal("4.2"),
            operating_cost_savings=Decimal("22.1"),
            asset_value_increase=Decimal("10.5"),
            min_project_size_m=Decimal("10.00"),
            data_source="CBRE 2022 Green Building Impact Report",
        ),
    ]
    for contract in contracts:
        db_session.add(contract)
    db_session.commit()
    return contracts
