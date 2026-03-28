"""
Integration tests for Backend-Data Engineering seams.

These tests verify the contract between the data layer and backend API:
1. Query functions return data in the format expected by API endpoints
2. Data types and field names match API schema
3. All relationships are resolved (JOINs work)
4. Pagination and filtering work end-to-end
5. Error handling is consistent
"""

import pytest
from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy.orm import Session

from db.queries.queries import (
    get_market_trends,
    get_market_trend_summary,
    get_technologies,
    get_technology_categories,
    get_technology_with_roi,
    get_roi_scenarios,
    get_payback_analysis,
    get_case_studies,
    get_regulatory_incentives,
    get_green_contracts,
    get_green_contract_comparison,
    get_dashboard_summary,
)


class TestBackendMarketTrendsSeam:
    """
    Test the seam between Backend API and market trends data.
    
    The backend expects:
    - GET /api/market-trends → returns list of trends
    - GET /api/regional-data?region=X → filtered trends
    """

    def test_market_trends_endpoint_returns_correct_shape(
        self, db_session: Session, sample_market_trends
    ):
        """Verify API endpoint contract for market trends."""
        # Simulating: GET /api/market-trends
        results = get_market_trends(db_session)

        assert isinstance(results, list), "Expected list of trends"
        assert len(results) > 0, "Should have at least one trend"

        trend = results[0]
        assert isinstance(trend, dict), "Each result should be a dict"
        assert "id" in trend, "Missing id field"
        assert "year" in trend, "Missing year field"
        assert "region" in trend, "Missing region field"
        assert "adoption_rate" in trend, "Missing adoption_rate field"
        assert "market_size" in trend, "Missing market_size field"

    def test_market_trends_region_filter_endpoint(
        self, db_session: Session, sample_market_trends
    ):
        """Verify region filtering for /api/regional-data?region=X."""
        # Simulating: GET /api/regional-data?region=North%20America
        results = get_market_trends(db_session, region="North America")

        assert len(results) > 0, "Should have results for North America"
        for trend in results:
            assert "North America" in trend["region"], "Region filter not applied"

    def test_market_trends_numeric_types_correct(
        self, db_session: Session, sample_market_trends
    ):
        """Verify numeric fields are float (JSON-serializable)."""
        results = get_market_trends(db_session)
        trend = results[0]

        assert isinstance(trend["adoption_rate"], (int, float)), \
            "adoption_rate should be numeric"
        assert isinstance(trend["market_size"], (int, float)), \
            "market_size should be numeric"


class TestBackendTechnologiesSeam:
    """
    Test the seam between Backend API and technologies data.
    
    The backend expects:
    - GET /api/technologies → returns list of technologies
    - GET /api/technology/{id}/comparison → tech with ROI scenarios
    """

    def test_technologies_endpoint_returns_correct_shape(
        self, db_session: Session, sample_technologies
    ):
        """Verify API endpoint contract for technologies."""
        # Simulating: GET /api/technologies
        results = get_technologies(db_session)

        assert isinstance(results, list)
        assert len(results) > 0

        tech = results[0]
        assert isinstance(tech, dict)
        assert "id" in tech
        assert "name" in tech
        assert "category" in tech
        assert "feasibility_score" in tech
        assert "tco" in tech
        assert "conventional_tco" in tech
        assert "maturity_level" in tech

    def test_technology_with_roi_endpoint_contract(
        self, db_session: Session, sample_technologies, sample_roi_scenarios
    ):
        """Verify API contract for /api/technology/{id}/comparison."""
        tech_id = str(sample_technologies[0].id)
        # Simulating: GET /api/technology/{id}/comparison
        result = get_technology_with_roi(db_session, tech_id)

        assert isinstance(result, dict), "Should return a dict"
        assert "id" in result, "Should include technology id"
        # Should have ROI data included
        assert len(result) > 0

    def test_technology_category_filter_works(
        self, db_session: Session, sample_technologies
    ):
        """Verify filtering by category works for API."""
        # Simulating: GET /api/technologies?category=Solar%20Energy
        results = get_technologies(db_session, category="Solar Energy")

        assert len(results) > 0
        for tech in results:
            assert tech["category"] == "Solar Energy"

    def test_technology_numeric_fields_correct_type(
        self, db_session: Session, sample_technologies
    ):
        """Verify numeric fields are JSON-serializable floats."""
        results = get_technologies(db_session)
        tech = results[0]

        assert isinstance(tech["feasibility_score"], (int, float))
        assert isinstance(tech["tco"], (int, float))
        assert isinstance(tech["conventional_tco"], (int, float))
        if tech.get("cagr") is not None:
            assert isinstance(tech["cagr"], (int, float))


class TestBackendROIAnalysisSeam:
    """
    Test the seam between Backend API and ROI data.
    
    The backend expects:
    - GET /api/payback-analysis → cross-tech payback comparison
    - GET /api/roi-scenarios → all ROI scenarios with filters
    """

    def test_roi_scenarios_endpoint_contract(
        self, db_session: Session, sample_roi_scenarios
    ):
        """Verify API endpoint contract for ROI scenarios."""
        # Simulating: GET /api/roi-scenarios
        results = get_roi_scenarios(db_session)

        assert isinstance(results, list)
        if len(results) > 0:
            scenario = results[0]
            assert "technology_id" in scenario
            assert "scenario_type" in scenario
            assert "payback_years" in scenario
            assert "roi_percentage" in scenario

    def test_roi_scenarios_by_type_filter(
        self, db_session: Session, sample_roi_scenarios
    ):
        """Verify filtering ROI scenarios by type."""
        # Simulating: GET /api/roi-scenarios?type=moderate
        results = get_roi_scenarios(db_session, scenario_type="moderate")

        assert len(results) > 0
        for scenario in results:
            assert scenario["scenario_type"] == "moderate"

    def test_payback_analysis_endpoint(
        self, db_session: Session, sample_roi_scenarios
    ):
        """Verify payback analysis endpoint returns comparable data."""
        # Simulating: GET /api/payback-analysis
        result = get_payback_analysis(db_session)

        assert result is not None, "Payback analysis should return data"


class TestBackendCaseStudiesSeam:
    """
    Test the seam between Backend API and case studies data.
    
    The backend expects:
    - GET /api/case-studies → all case studies
    - GET /api/case-studies?size=Large → filtered by firm size
    
    Note: Tests are skipped for SQLite compatibility. Full tests run on PostgreSQL.
    """

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type; use PostgreSQL for full integration test")
    def test_case_studies_endpoint_contract(
        self, db_session: Session, sample_case_studies
    ):
        """Verify API endpoint contract for case studies."""
        # Simulating: GET /api/case-studies
        results = get_case_studies(db_session)

        assert isinstance(results, list)
        assert len(results) > 0

        study = results[0]
        assert isinstance(study, dict)
        assert "id" in study
        assert "firm_name" in study
        assert "size" in study
        assert "technologies_adopted" in study
        assert "investment" in study
        assert "outcomes" in study
        assert "timeline" in study

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type; use PostgreSQL for full integration test")
    def test_case_studies_size_filter(
        self, db_session: Session, sample_case_studies
    ):
        """Verify size filtering for case studies."""
        # Simulating: GET /api/case-studies?size=Large
        results = get_case_studies(db_session, size="Large (>$500M)")

        assert len(results) > 0
        for study in results:
            assert study["size"] == "Large (>$500M)"

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type; use PostgreSQL for full integration test")
    def test_case_studies_array_field_serialization(
        self, db_session: Session, sample_case_studies
    ):
        """Verify technologies_adopted array is properly serialized."""
        results = get_case_studies(db_session)
        study = results[0]

        assert isinstance(study["technologies_adopted"], list)
        assert len(study["technologies_adopted"]) > 0
        # All items should be strings
        for tech in study["technologies_adopted"]:
            assert isinstance(tech, str)

    @pytest.mark.skip(reason="SQLite doesn't support ARRAY type; use PostgreSQL for full integration test")
    def test_case_studies_numeric_fields_json_safe(
        self, db_session: Session, sample_case_studies
    ):
        """Verify numeric fields can be JSON serialized."""
        results = get_case_studies(db_session)
        if len(results) > 0:
            study = results[0]
            investment = study["investment"]
            assert isinstance(investment, (int, float)), \
                "investment should be numeric for JSON serialization"


class TestBackendRegulatoryIncentivesSeam:
    """
    Test the seam between Backend API and regulatory incentives.
    
    The backend expects:
    - GET /api/incentives → all active incentives
    - GET /api/incentives?jurisdiction=Federal → filtered incentives
    """

    def test_regulatory_incentives_endpoint_contract(
        self, db_session: Session, sample_regulatory_incentives
    ):
        """Verify API endpoint contract for regulatory incentives."""
        # Simulating: GET /api/incentives
        results = get_regulatory_incentives(db_session)

        assert isinstance(results, list)
        assert len(results) > 0

        incentive = results[0]
        assert isinstance(incentive, dict)
        assert "id" in incentive
        assert "policy_name" in incentive
        assert "jurisdiction" in incentive
        assert "type" in incentive
        assert "is_active" in incentive

    def test_regulatory_incentives_jurisdiction_filter(
        self, db_session: Session, sample_regulatory_incentives
    ):
        """Verify jurisdiction filtering."""
        # Simulating: GET /api/incentives?jurisdiction=Federal
        results = get_regulatory_incentives(db_session, jurisdiction="Federal")

        assert len(results) > 0
        for incentive in results:
            assert incentive["jurisdiction"] == "Federal"

    def test_regulatory_incentives_active_only_filter(
        self, db_session: Session, sample_regulatory_incentives
    ):
        """Verify active status filtering."""
        # Simulating: GET /api/incentives?active=true
        results = get_regulatory_incentives(db_session, active_only=True)

        # All returned should be active
        for incentive in results:
            assert incentive["is_active"] == "yes"


class TestBackendGreenContractsSeam:
    """
    Test the seam between Backend API and green contracts data.
    
    The backend expects:
    - GET /api/green-contracts → all certifications with premiums
    - GET /api/green-contracts/comparison → premium comparison table
    """

    def test_green_contracts_endpoint_contract(
        self, db_session: Session, sample_green_contracts
    ):
        """Verify API endpoint contract for green contracts."""
        # Simulating: GET /api/green-contracts
        results = get_green_contracts(db_session)

        assert isinstance(results, list)
        assert len(results) > 0

        contract = results[0]
        assert isinstance(contract, dict)
        assert "id" in contract
        assert "certification_type" in contract
        assert "win_rate_premium" in contract
        assert "contract_value_premium" in contract

    def test_green_contracts_comparison_endpoint(
        self, db_session: Session, sample_green_contracts
    ):
        """Verify comparison endpoint returns tabular data."""
        # Simulating: GET /api/green-contracts/comparison
        result = get_green_contract_comparison(db_session)

        assert result is not None, "Should return comparison data"
        assert isinstance(result, (list, dict)), "Should be list or dict"

    def test_green_contracts_numeric_field_types(
        self, db_session: Session, sample_green_contracts
    ):
        """Verify premium fields are numeric and JSON-serializable."""
        results = get_green_contracts(db_session)
        contract = results[0]

        assert isinstance(contract["win_rate_premium"], (int, float))
        assert isinstance(contract["contract_value_premium"], (int, float))
        if contract.get("construction_cost_premium") is not None:
            assert isinstance(contract["construction_cost_premium"], (int, float))


class TestDashboardSummarySeam:
    """
    Test the seam for the all-in-one dashboard summary endpoint.
    
    The backend expects:
    - GET /api/dashboard/summary → aggregated data for dashboard
    
    Note: Tests are skipped for SQLite compatibility. Full tests run on PostgreSQL.
    """

    @pytest.mark.skip(reason="Requires ARRAY support; use PostgreSQL for full test")
    def test_dashboard_summary_returns_aggregated_data(
        self,
        db_session: Session,
        sample_market_trends,
        sample_technologies,
        sample_roi_scenarios,
        sample_case_studies,
        sample_regulatory_incentives,
        sample_green_contracts,
    ):
        """Verify dashboard summary includes all needed data types."""
        # Simulating: GET /api/dashboard/summary
        summary = get_dashboard_summary(db_session)

        assert isinstance(summary, dict), "Dashboard summary should be a dict"
        # Should have non-empty data
        assert len(summary) > 0, "Dashboard summary should have content"

    @pytest.mark.skip(reason="Requires ARRAY support; use PostgreSQL for full test")
    def test_dashboard_summary_json_serializable(
        self,
        db_session: Session,
        sample_market_trends,
        sample_technologies,
        sample_roi_scenarios,
        sample_case_studies,
        sample_regulatory_incentives,
        sample_green_contracts,
    ):
        """Verify dashboard summary is JSON-serializable for FastAPI."""
        import json

        summary = get_dashboard_summary(db_session)
        # Should not raise TypeError
        json_str = json.dumps(summary)
        assert len(json_str) > 0


class TestErrorHandling:
    """Test error handling and edge cases in data layer."""

    def test_get_technologies_with_nonexistent_category(self, db_session: Session):
        """Verify behavior when filtering by nonexistent category."""
        results = get_technologies(db_session, category="NonexistentCategory")
        # Should return empty list, not error
        assert isinstance(results, list)
        assert len(results) == 0

    def test_get_case_studies_with_nonexistent_size(self, db_session: Session):
        """Verify behavior when filtering by nonexistent size."""
        results = get_case_studies(db_session, size="NonexistentSize")
        # Should return empty list, not error
        assert isinstance(results, list)
        assert len(results) == 0

    def test_get_regulatory_incentives_with_nonexistent_jurisdiction(
        self, db_session: Session
    ):
        """Verify behavior with nonexistent jurisdiction."""
        results = get_regulatory_incentives(db_session, jurisdiction="Atlantis")
        # Should return empty list, not error
        assert isinstance(results, list)
        assert len(results) == 0
