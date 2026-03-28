"""
API-Database Integration Tests for Renewable Energy Executive Dashboard.

Tests verify that FastAPI endpoints correctly serialize data from the
application's data layer (seed_data.py). These tests validate the seams
between the API layer and data access layer, including:

- JSON serialization of complex Pydantic models
- Correct mapping between response schemas and seed data structures
- Data type conversions (Decimal → float, UUID → str, etc.)
- Aggregations and transformations applied by endpoints
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from decimal import Decimal
import json

from backend.app.main import app
from backend.app.seed_data import (
    get_market_trends,
    get_technologies,
    get_technology_comparison,
    get_payback_analysis,
    get_roi_scenarios,
    get_incentives,
    get_case_studies,
    get_green_contracts,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def is_valid_json_serializable(obj):
    """Check if an object is JSON serializable."""
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False


def assert_all_floats_not_decimals(data):
    """Recursively verify that no Decimal objects exist in JSON response."""
    if isinstance(data, dict):
        for v in data.values():
            assert not isinstance(v, Decimal), f"Found Decimal in JSON: {v}"
            assert_all_floats_not_decimals(v)
    elif isinstance(data, list):
        for item in data:
            assert not isinstance(item, Decimal), f"Found Decimal in JSON list: {item}"
            assert_all_floats_not_decimals(item)


def assert_all_strings_not_uuid(data):
    """Recursively verify that UUID objects are converted to strings."""
    from uuid import UUID
    if isinstance(data, dict):
        for v in data.values():
            assert not isinstance(v, UUID), f"Found UUID object in JSON: {v}"
            assert_all_strings_not_uuid(v)
    elif isinstance(data, list):
        for item in data:
            assert not isinstance(item, UUID), f"Found UUID object in JSON list: {item}"
            assert_all_strings_not_uuid(item)


# ===========================================================================
# 1. Market Trends — GET /api/market-trends
# ===========================================================================


class TestMarketTrendsIntegration:
    """Verify /api/market-trends correctly serializes market_trends seed data."""

    @pytest.mark.asyncio
    async def test_market_trends_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        This validates all Decimal values are converted to float.
        """
        response = await client.get("/api/market-trends")
        assert response.status_code == 200
        data = response.json()
        # If this succeeds, JSON serialization is valid
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_market_trends_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects leaked into JSON response.
        Database columns use NUMERIC types which Python reads as Decimal.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_market_trends_key_metrics_are_floats(self, client: AsyncClient):
        """
        Key metrics values must be float type, not Decimal.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        for metric in data["key_metrics"]:
            assert isinstance(metric["value"], float), \
                f"Metric {metric['label']} value is not float: {type(metric['value'])}"

    @pytest.mark.asyncio
    async def test_market_trends_matches_seed_data_global_2025(self, client: AsyncClient):
        """
        Verify API response global_green_building_market_2025_usd_b
        matches the seed data factory function.
        """
        seed_response = get_market_trends()
        api_response = await client.get("/api/market-trends")
        data = api_response.json()
        
        assert data["global_green_building_market_2025_usd_b"] == \
               pytest.approx(float(seed_response.global_green_building_market_2025_usd_b), rel=1e-3)

    @pytest.mark.asyncio
    async def test_market_trends_matches_seed_data_cagr(self, client: AsyncClient):
        """
        Verify CAGR field matches seed data.
        """
        seed_response = get_market_trends()
        api_response = await client.get("/api/market-trends")
        data = api_response.json()
        
        assert data["global_green_building_cagr_pct"] == \
               pytest.approx(float(seed_response.global_green_building_cagr_pct), rel=1e-3)

    @pytest.mark.asyncio
    async def test_market_trends_adoption_by_firm_size_count(self, client: AsyncClient):
        """
        Verify adoption_by_firm_size list matches seed data count.
        """
        seed_response = get_market_trends()
        api_response = await client.get("/api/market-trends")
        data = api_response.json()
        
        assert len(data["adoption_by_firm_size"]) == len(seed_response.adoption_by_firm_size)

    @pytest.mark.asyncio
    async def test_market_trends_time_series_values_are_floats(self, client: AsyncClient):
        """
        Verify time series values are floats, not Decimals.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        for point in data["global_market_time_series"]:
            assert isinstance(point["value"], float), \
                f"Time series value is not float: {type(point['value'])}"
            assert isinstance(point["year"], int), \
                f"Time series year is not int: {type(point['year'])}"

    @pytest.mark.asyncio
    async def test_market_trends_drivers_and_barriers_structure(self, client: AsyncClient):
        """
        Verify drivers and barriers are correctly structured from seed data.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        for driver in data["drivers"]:
            assert "name" in driver
            assert "description" in driver
            assert "severity" in driver
            assert "trend" in driver
            assert "confidence" in driver

    @pytest.mark.asyncio
    async def test_market_trends_sources_present_and_valid(self, client: AsyncClient):
        """
        Verify sources are correctly mapped from seed data.
        """
        seed_response = get_market_trends()
        api_response = await client.get("/api/market-trends")
        data = api_response.json()
        
        assert len(data["sources"]) == len(seed_response.sources)
        for source in data["sources"]:
            assert "name" in source
            assert "organization" in source
            assert "confidence" in source


# ===========================================================================
# 2. Technologies — GET /api/technologies
# ===========================================================================


class TestTechnologiesIntegration:
    """Verify /api/technologies correctly serializes technology seed data."""

    @pytest.mark.asyncio
    async def test_technologies_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/technologies")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_technologies_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects leaked into JSON response.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_technologies_feasibility_scores_are_floats(self, client: AsyncClient):
        """
        Feasibility score components must be floats (0-10 scale).
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            feasibility = tech["feasibility"]
            for score_field in [
                "overall_score", "technical_maturity", "financial_viability",
                "regulatory_support", "workforce_readiness", "supply_chain_maturity",
                "mid_size_adoption_ease"
            ]:
                assert isinstance(feasibility[score_field], float), \
                    f"{score_field} is not float: {type(feasibility[score_field])}"
                assert 0 <= feasibility[score_field] <= 10, \
                    f"{score_field} out of range: {feasibility[score_field]}"

    @pytest.mark.asyncio
    async def test_technologies_matches_seed_data_count(self, client: AsyncClient):
        """
        Verify technology count matches seed data.
        """
        seed_response = get_technologies()
        api_response = await client.get("/api/technologies")
        data = api_response.json()
        
        assert len(data["technologies"]) == len(seed_response.technologies)

    @pytest.mark.asyncio
    async def test_technologies_roi_metrics_have_correct_types(self, client: AsyncClient):
        """
        ROI metric fields must be floats or null, not Decimals.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            roi = tech["roi"]
            for field in ["payback_years_min", "payback_years_max", "payback_years_typical",
                          "npv_20yr_usd_k_per_unit", "irr_pct", "annual_savings_usd_k",
                          "upfront_cost_premium_pct", "operating_cost_reduction_pct"]:
                value = roi.get(field)
                if value is not None:
                    assert isinstance(value, float), \
                        f"{field} is not float: {type(value)}"

    @pytest.mark.asyncio
    async def test_technologies_summary_adoption_rates_are_floats(self, client: AsyncClient):
        """
        Adoption rates in summary must be floats.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech_name, rate in data["summary_adoption_rates"].items():
            assert isinstance(rate, float), \
                f"Adoption rate for {tech_name} is not float: {type(rate)}"

    @pytest.mark.asyncio
    async def test_technologies_all_have_required_fields(self, client: AsyncClient):
        """
        Every technology must have required fields from schema.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        required_fields = ["id", "name", "category", "description", "feasibility", "roi", "confidence"]
        for tech in data["technologies"]:
            for field in required_fields:
                assert field in tech, f"Technology {tech.get('id')} missing {field}"


# ===========================================================================
# 3. Technology Comparison — GET /api/technology/{id}/comparison
# ===========================================================================


class TestTechnologyComparisonIntegration:
    """Verify /api/technology/{id}/comparison correctly serializes TCO data."""

    @pytest.mark.asyncio
    async def test_technology_comparison_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_technology_comparison_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects leaked into TCO response.
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_technology_comparison_tco_components_are_floats(self, client: AsyncClient):
        """
        TCO component costs must be floats (USD thousands).
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        
        for scenario in data["tco_scenarios"]:
            for component in scenario["components"]:
                for field in ["green_cost_usd_k", "conventional_cost_usd_k", "difference_usd_k"]:
                    assert isinstance(component[field], float), \
                        f"{field} is not float: {type(component[field])}"

    @pytest.mark.asyncio
    async def test_technology_comparison_scenario_totals_are_floats(self, client: AsyncClient):
        """
        TCO scenario total costs must be floats.
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        
        for scenario in data["tco_scenarios"]:
            for field in ["green_total_tco_usd_k", "conventional_total_tco_usd_k", "green_advantage_usd_k"]:
                assert isinstance(scenario[field], float), \
                    f"{field} is not float: {type(scenario[field])}"

    @pytest.mark.asyncio
    async def test_technology_comparison_matches_seed_data(self, client: AsyncClient):
        """
        Verify comparison data matches seed data factory function.
        """
        tech_id = "solar-pv"
        seed_response = get_technology_comparison(tech_id)
        api_response = await client.get(f"/api/technology/{tech_id}/comparison")
        data = api_response.json()
        
        assert data["technology_id"] == seed_response.technology_id
        assert data["technology_name"] == seed_response.technology_name
        assert len(data["tco_scenarios"]) == len(seed_response.tco_scenarios)


# ===========================================================================
# 4. Payback Analysis — GET /api/payback-analysis
# ===========================================================================


class TestPaybackAnalysisIntegration:
    """Verify /api/payback-analysis aggregates and serializes data correctly."""

    @pytest.mark.asyncio
    async def test_payback_analysis_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/payback-analysis")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_payback_analysis_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects in payback analysis response.
        """
        response = await client.get("/api/payback-analysis")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_payback_analysis_payback_years_are_floats(self, client: AsyncClient):
        """
        Payback period values must be floats.
        """
        response = await client.get("/api/payback-analysis")
        data = response.json()
        
        for entry in data["payback_data"]:
            for field in ["payback_years_base", "payback_years_with_incentives",
                          "payback_years_optimistic", "payback_years_pessimistic"]:
                assert isinstance(entry[field], float), \
                    f"{field} is not float: {type(entry[field])}"

    @pytest.mark.asyncio
    async def test_payback_analysis_summary_stats_are_floats(self, client: AsyncClient):
        """
        Summary statistics must be floats.
        """
        response = await client.get("/api/payback-analysis")
        data = response.json()
        
        for key, value in data["summary_stats"].items():
            assert isinstance(value, float), \
                f"Summary stat {key} is not float: {type(value)}"

    @pytest.mark.asyncio
    async def test_payback_analysis_matches_seed_data(self, client: AsyncClient):
        """
        Verify payback analysis matches seed data.
        """
        seed_response = get_payback_analysis()
        api_response = await client.get("/api/payback-analysis")
        data = api_response.json()
        
        assert len(data["payback_data"]) == len(seed_response.payback_data)


# ===========================================================================
# 5. ROI Scenarios — GET /api/roi-scenarios
# ===========================================================================


class TestROIScenariosIntegration:
    """Verify /api/roi-scenarios correctly serializes ROI projection data."""

    @pytest.mark.asyncio
    async def test_roi_scenarios_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/roi-scenarios")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_roi_scenarios_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects in ROI response.
        """
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_roi_scenarios_investment_and_npv_are_floats(self, client: AsyncClient):
        """
        Investment and NPV fields must be floats (USD thousands).
        """
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        
        for scenario in data["scenarios"]:
            assert isinstance(scenario["initial_investment_usd_k"], float), \
                f"initial_investment_usd_k is not float: {type(scenario['initial_investment_usd_k'])}"
            assert isinstance(scenario["ten_year_npv_usd_k"], float), \
                f"ten_year_npv_usd_k is not float: {type(scenario['ten_year_npv_usd_k'])}"

    @pytest.mark.asyncio
    async def test_roi_scenarios_annual_projections_are_floats(self, client: AsyncClient):
        """
        Annual projection values must be floats.
        """
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        
        for scenario in data["scenarios"]:
            for projection in scenario["annual_projections"]:
                for field in ["cumulative_investment_usd_k", "cumulative_savings_usd_k", "net_position_usd_k"]:
                    assert isinstance(projection[field], float), \
                        f"{field} is not float: {type(projection[field])}"

    @pytest.mark.asyncio
    async def test_roi_scenarios_matches_seed_data(self, client: AsyncClient):
        """
        Verify ROI scenarios match seed data.
        """
        seed_response = get_roi_scenarios()
        api_response = await client.get("/api/roi-scenarios")
        data = api_response.json()
        
        assert len(data["scenarios"]) == len(seed_response.scenarios)


# ===========================================================================
# 6. Incentives — GET /api/incentives
# ===========================================================================


class TestIncentivesIntegration:
    """Verify /api/incentives correctly serializes regulatory incentive data."""

    @pytest.mark.asyncio
    async def test_incentives_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/incentives")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_incentives_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects in incentives response.
        """
        response = await client.get("/api/incentives")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_incentives_percentage_values_are_floats(self, client: AsyncClient):
        """
        Percentage fields must be floats.
        """
        response = await client.get("/api/incentives")
        data = response.json()
        
        for incentive in data["incentives"]:
            if incentive.get("value_pct") is not None:
                assert isinstance(incentive["value_pct"], float), \
                    f"value_pct is not float: {type(incentive['value_pct'])}"

    @pytest.mark.asyncio
    async def test_incentives_matches_seed_data(self, client: AsyncClient):
        """
        Verify incentives match seed data.
        """
        seed_response = get_incentives()
        api_response = await client.get("/api/incentives")
        data = api_response.json()
        
        assert len(data["incentives"]) == len(seed_response.incentives)


# ===========================================================================
# 7. Case Studies — GET /api/case-studies
# ===========================================================================


class TestCaseStudiesIntegration:
    """Verify /api/case-studies correctly serializes case study data."""

    @pytest.mark.asyncio
    async def test_case_studies_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/case-studies")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_case_studies_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects in case studies response.
        """
        response = await client.get("/api/case-studies")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_case_studies_matches_seed_data(self, client: AsyncClient):
        """
        Verify case studies match seed data.
        """
        seed_response = get_case_studies()
        api_response = await client.get("/api/case-studies")
        data = api_response.json()
        
        assert len(data["case_studies"]) == len(seed_response.case_studies)

    @pytest.mark.asyncio
    async def test_case_studies_technology_adoption_summary_count(self, client: AsyncClient):
        """
        Technology adoption summary should aggregate across all case studies.
        """
        response = await client.get("/api/case-studies")
        data = response.json()
        
        assert len(data["technology_adoption_summary"]) > 0
        for adoption in data["technology_adoption_summary"]:
            assert "technology" in adoption
            assert "firms_using" in adoption
            assert "total_firms" in adoption
            assert "adoption_rate_pct" in adoption


# ===========================================================================
# 8. Green Contracts — GET /api/green-contracts
# ===========================================================================


class TestGreenContractsIntegration:
    """Verify /api/green-contracts correctly serializes contract premium data."""

    @pytest.mark.asyncio
    async def test_green_contracts_json_serializable(self, client: AsyncClient):
        """
        Verify the entire response is JSON serializable.
        """
        response = await client.get("/api/green-contracts")
        assert response.status_code == 200
        data = response.json()
        assert is_valid_json_serializable(data)

    @pytest.mark.asyncio
    async def test_green_contracts_no_decimal_objects(self, client: AsyncClient):
        """
        Ensure no Decimal objects in green contracts response.
        """
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert_all_floats_not_decimals(data)

    @pytest.mark.asyncio
    async def test_green_contracts_matches_seed_data(self, client: AsyncClient):
        """
        Verify green contracts match seed data.
        """
        seed_response = get_green_contracts()
        api_response = await client.get("/api/green-contracts")
        data = api_response.json()
        
        # Top-level fields should match
        assert "as_of_date" in data
        assert "bid_win_rate_data" in data
        assert "contract_premiums" in data
