"""
Unit tests for SQLAlchemy ORM models.

Tests the structure and behavior of:
- MarketTrend model
- Technology model  
- ROIScenario model
- CaseStudy model
- RegulatoryIncentive model
- GreenContract model
"""

import pytest
from decimal import Decimal
from datetime import datetime

from db.models.models import (
    MarketTrend,
    Technology,
    ROIScenario,
    CaseStudy,
    RegulatoryIncentive,
    GreenContract,
)


class TestMarketTrendModel:
    """Test MarketTrend model validation and behavior."""

    def test_market_trend_creation(self, db_session):
        """Test creating a market trend record."""
        trend = MarketTrend(
            year=2025,
            region="North America",
            adoption_rate=Decimal("47.5"),
            market_size=Decimal("618.58"),
        )
        db_session.add(trend)
        db_session.commit()

        retrieved = db_session.query(MarketTrend).filter_by(region="North America").first()
        assert retrieved is not None
        assert retrieved.year == 2025
        assert float(retrieved.adoption_rate) == 47.5
        assert float(retrieved.market_size) == 618.58

    def test_market_trend_requires_mandatory_fields(self, db_session):
        """Test that required fields are enforced."""
        # Missing required fields should fail on insert
        trend = MarketTrend(year=2025)  # Missing region, adoption_rate, market_size
        db_session.add(trend)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_market_trend_repr(self, sample_market_trends):
        """Test __repr__ method."""
        trend = sample_market_trends[0]
        repr_str = repr(trend)
        assert "2025" in repr_str
        assert "North America" in repr_str
        assert "47.5" in repr_str

    def test_market_trend_timestamp_fields(self, db_session):
        """Test that created_at and updated_at are automatically set."""
        trend = MarketTrend(
            year=2025,
            region="Test",
            adoption_rate=Decimal("50.0"),
            market_size=Decimal("100.00"),
        )
        db_session.add(trend)
        db_session.commit()

        assert trend.created_at is not None
        assert trend.updated_at is not None
        assert isinstance(trend.created_at, datetime)
        assert isinstance(trend.updated_at, datetime)


class TestTechnologyModel:
    """Test Technology model validation and behavior."""

    def test_technology_creation(self, db_session):
        """Test creating a technology record."""
        tech = Technology(
            name="Rooftop Solar Panels",
            category="Solar Energy",
            feasibility_score=Decimal("95.0"),
            tco=Decimal("45000.00"),
            conventional_tco=Decimal("0.00"),
            maturity_level="Mainstream",
        )
        db_session.add(tech)
        db_session.commit()

        retrieved = db_session.query(Technology).filter_by(name="Rooftop Solar Panels").first()
        assert retrieved is not None
        assert retrieved.category == "Solar Energy"
        assert float(retrieved.feasibility_score) == 95.0

    def test_technology_repr(self, sample_technologies):
        """Test __repr__ method."""
        tech = sample_technologies[0]
        repr_str = repr(tech)
        assert "Rooftop Solar" in repr_str
        assert "Mainstream" in repr_str
        assert "Solar Energy" in repr_str

    def test_technology_cagr_optional(self, db_session):
        """Test that CAGR is optional."""
        tech = Technology(
            name="Test Tech",
            category="Test Category",
            feasibility_score=Decimal("50.0"),
            tco=Decimal("1000.00"),
            conventional_tco=Decimal("800.00"),
            maturity_level="Emerging",
            cagr=None,
        )
        db_session.add(tech)
        db_session.commit()

        retrieved = db_session.query(Technology).filter_by(name="Test Tech").first()
        assert retrieved.cagr is None


class TestROIScenarioModel:
    """Test ROIScenario model validation and behavior."""

    def test_roi_scenario_creation(self, db_session, sample_technologies):
        """Test creating an ROI scenario record."""
        tech = sample_technologies[0]
        scenario = ROIScenario(
            technology_id=tech.id,
            scenario_type="moderate",
            payback_years=Decimal("5.2"),
            roi_percentage=Decimal("18.5"),
            assumptions="Moderate case with average adoption",
        )
        db_session.add(scenario)
        db_session.commit()

        retrieved = db_session.query(ROIScenario).filter_by(scenario_type="moderate").first()
        assert retrieved is not None
        assert float(retrieved.roi_percentage) == 18.5
        assert float(retrieved.payback_years) == 5.2

    def test_roi_scenario_repr(self, sample_roi_scenarios):
        """Test __repr__ method."""
        scenario = sample_roi_scenarios[0]
        repr_str = repr(scenario)
        assert "conservative" in repr_str or "moderate" in repr_str or "optimistic" in repr_str

    def test_roi_scenario_financial_fields_optional(self, db_session, sample_technologies):
        """Test that NPV and IRR are optional."""
        tech = sample_technologies[0]
        scenario = ROIScenario(
            technology_id=tech.id,
            scenario_type="conservative",
            payback_years=Decimal("7.0"),
            roi_percentage=Decimal("10.0"),
            assumptions="Conservative assumptions",
            npv=None,
            irr=None,
        )
        db_session.add(scenario)
        db_session.commit()

        retrieved = db_session.query(ROIScenario).filter_by(scenario_type="conservative").first()
        assert retrieved.npv is None
        assert retrieved.irr is None


class TestCaseStudyModel:
    """Test CaseStudy model validation and behavior.
    
    Note: ARRAY field tests are skipped for SQLite compatibility.
    Full array tests run on PostgreSQL in integration environment.
    """

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type natively")
    def test_case_study_creation(self, db_session):
        """Test creating a case study record."""
        study = CaseStudy(
            firm_name="Mortenson",
            size="Large (>$500M)",
            technologies_adopted=["Solar", "LED", "Smart Controls"],
            investment=Decimal("75.50"),
            outcomes="35% reduction in emissions",
            timeline="2019-2024",
        )
        db_session.add(study)
        db_session.commit()

        retrieved = db_session.query(CaseStudy).filter_by(firm_name="Mortenson").first()
        assert retrieved is not None
        assert len(retrieved.technologies_adopted) == 3
        assert "Solar" in retrieved.technologies_adopted

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type natively")
    def test_case_study_array_field(self, sample_case_studies):
        """Test that technologies_adopted array is properly stored and retrieved."""
        study = sample_case_studies[0]
        assert isinstance(study.technologies_adopted, list)
        assert len(study.technologies_adopted) > 0

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type natively")
    def test_case_study_repr(self, sample_case_studies):
        """Test __repr__ method."""
        study = sample_case_studies[0]
        repr_str = repr(study)
        assert study.firm_name in repr_str
        assert "Large" in repr_str

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type natively")
    def test_case_study_net_zero_year_optional(self, db_session):
        """Test that net_zero_year is optional."""
        study = CaseStudy(
            firm_name="Test Firm",
            size="Small (<$50M)",
            technologies_adopted=["Solar"],
            investment=Decimal("10.00"),
            outcomes="Test outcomes",
            timeline="2023-2024",
            net_zero_year=None,
        )
        db_session.add(study)
        db_session.commit()

        retrieved = db_session.query(CaseStudy).filter_by(firm_name="Test Firm").first()
        assert retrieved.net_zero_year is None


class TestRegulatoryIncentiveModel:
    """Test RegulatoryIncentive model validation and behavior."""

    def test_regulatory_incentive_creation(self, db_session):
        """Test creating a regulatory incentive record."""
        incentive = RegulatoryIncentive(
            policy_name="IRA Tax Credit",
            jurisdiction="Federal",
            type="Tax Credit",
            financial_impact="30% credit on renewable energy",
            is_active="yes",
        )
        db_session.add(incentive)
        db_session.commit()

        retrieved = db_session.query(RegulatoryIncentive).filter_by(jurisdiction="Federal").first()
        assert retrieved is not None
        assert retrieved.is_active == "yes"

    def test_regulatory_incentive_repr(self, sample_regulatory_incentives):
        """Test __repr__ method."""
        incentive = sample_regulatory_incentives[0]
        repr_str = repr(incentive)
        assert incentive.policy_name in repr_str
        assert incentive.jurisdiction in repr_str

    def test_regulatory_incentive_financial_impact_b_optional(self, db_session):
        """Test that financial_impact_b is optional."""
        incentive = RegulatoryIncentive(
            policy_name="State Mandate",
            jurisdiction="California",
            type="Mandate",
            financial_impact="All new buildings must be net zero",
            financial_impact_b=None,
            is_active="yes",
        )
        db_session.add(incentive)
        db_session.commit()

        retrieved = db_session.query(RegulatoryIncentive).filter_by(jurisdiction="California").first()
        assert retrieved.financial_impact_b is None


class TestGreenContractModel:
    """Test GreenContract model validation and behavior."""

    def test_green_contract_creation(self, db_session):
        """Test creating a green contract record."""
        contract = GreenContract(
            certification_type="LEED Gold",
            win_rate_premium=Decimal("12.3"),
            contract_value_premium=Decimal("4.0"),
        )
        db_session.add(contract)
        db_session.commit()

        retrieved = db_session.query(GreenContract).filter_by(certification_type="LEED Gold").first()
        assert retrieved is not None
        assert float(retrieved.win_rate_premium) == 12.3
        assert float(retrieved.contract_value_premium) == 4.0

    def test_green_contract_repr(self, sample_green_contracts):
        """Test __repr__ method."""
        contract = sample_green_contracts[0]
        repr_str = repr(contract)
        assert "LEED" in repr_str
        assert "12.3" in repr_str or "18.7" in repr_str

    def test_green_contract_optional_fields(self, db_session):
        """Test that optional fields can be null."""
        contract = GreenContract(
            certification_type="Test Cert",
            win_rate_premium=Decimal("5.0"),
            contract_value_premium=Decimal("2.0"),
            construction_cost_premium=None,
            operating_cost_savings=None,
            asset_value_increase=None,
            min_project_size_m=None,
        )
        db_session.add(contract)
        db_session.commit()

        retrieved = db_session.query(GreenContract).filter_by(certification_type="Test Cert").first()
        assert retrieved.construction_cost_premium is None
        assert retrieved.operating_cost_savings is None
        assert retrieved.asset_value_increase is None
        assert retrieved.min_project_size_m is None
