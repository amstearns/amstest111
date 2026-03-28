"""
Comprehensive pytest tests for the Renewable Energy Executive Dashboard FastAPI backend.

Tests every endpoint for:
- HTTP 200 responses and correct response structure
- Key data value correctness
- List/collection counts
- 404 error handling for invalid technology IDs
- CORS headers presence
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from backend.app.main import app


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
# Helper: CORS preflight origin header
# ---------------------------------------------------------------------------

CORS_ORIGIN = "http://localhost:3000"


# ===========================================================================
# 1. GET /health
# ===========================================================================


class TestHealth:
    @pytest.mark.asyncio
    async def test_health_returns_200(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_health_response_structure(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "timestamp" in data
        assert "database" in data
        assert "uptime_seconds" in data

    @pytest.mark.asyncio
    async def test_health_status_ok(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()
        assert data["status"] == "ok"

    @pytest.mark.asyncio
    async def test_health_version(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()
        assert data["version"] == "1.0.0"

    @pytest.mark.asyncio
    async def test_health_database_field(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()
        assert data["database"] == "in-memory"

    @pytest.mark.asyncio
    async def test_health_uptime_is_positive(self, client: AsyncClient):
        response = await client.get("/health")
        data = response.json()
        assert data["uptime_seconds"] >= 0


# ===========================================================================
# 2. GET /api/market-trends
# ===========================================================================


class TestMarketTrends:
    @pytest.mark.asyncio
    async def test_market_trends_returns_200(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_market_trends_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        required_fields = [
            "as_of_date",
            "global_green_building_market_2025_usd_b",
            "global_green_building_market_2034_projected_usd_b",
            "global_green_building_cagr_pct",
            "north_america_market_share_pct",
            "north_america_market_2025_usd_b",
            "electric_equipment_market_2025_usd_b_min",
            "electric_equipment_market_2025_usd_b_max",
            "electric_equipment_market_2030_projected_usd_b",
            "electric_equipment_cagr_pct",
            "ira_clean_energy_incentives_usd_b",
            "commercial_solar_adoption_boost_post_ira_pct",
            "buildings_global_co2_share_pct",
            "key_metrics",
            "adoption_by_firm_size",
            "global_market_time_series",
            "electric_equipment_time_series",
            "drivers",
            "barriers",
            "sources",
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_market_size_618_58_billion(self, client: AsyncClient):
        """Global green building market 2025 should be 618.58B."""
        response = await client.get("/api/market-trends")
        data = response.json()
        assert data["global_green_building_market_2025_usd_b"] == pytest.approx(618.58, rel=1e-3)

    @pytest.mark.asyncio
    async def test_market_2034_projection(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert data["global_green_building_market_2034_projected_usd_b"] == pytest.approx(1374.23, rel=1e-3)

    @pytest.mark.asyncio
    async def test_north_america_market_share(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert data["north_america_market_share_pct"] == pytest.approx(35.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_ira_incentives_value(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert data["ira_clean_energy_incentives_usd_b"] == pytest.approx(270.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_buildings_co2_share(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert data["buildings_global_co2_share_pct"] == pytest.approx(37.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_key_metrics_count(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert len(data["key_metrics"]) == 8

    @pytest.mark.asyncio
    async def test_adoption_by_firm_size_count(self, client: AsyncClient):
        """Should return 3 firm size entries: Small, Mid-Size, Large."""
        response = await client.get("/api/market-trends")
        data = response.json()
        assert len(data["adoption_by_firm_size"]) == 3

    @pytest.mark.asyncio
    async def test_global_market_time_series_has_data(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert len(data["global_market_time_series"]) > 0

    @pytest.mark.asyncio
    async def test_drivers_and_barriers_present(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert len(data["drivers"]) >= 1
        assert len(data["barriers"]) >= 1

    @pytest.mark.asyncio
    async def test_sources_present(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        assert len(data["sources"]) >= 1

    @pytest.mark.asyncio
    async def test_key_metric_structure(self, client: AsyncClient):
        response = await client.get("/api/market-trends")
        data = response.json()
        metric = data["key_metrics"][0]
        assert "label" in metric
        assert "value" in metric
        assert "unit" in metric


# ===========================================================================
# 3. GET /api/regional-data
# ===========================================================================


class TestRegionalData:
    @pytest.mark.asyncio
    async def test_regional_data_returns_200(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_regional_data_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        data = response.json()
        assert "as_of_date" in data
        assert "top_us_states_2025" in data
        assert "country_data" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_top_us_states_count(self, client: AsyncClient):
        """Should return 10 states."""
        response = await client.get("/api/regional-data")
        data = response.json()
        assert len(data["top_us_states_2025"]) == 10

    @pytest.mark.asyncio
    async def test_country_data_count(self, client: AsyncClient):
        """Should return 3 country entries: US, Canada, Mexico."""
        response = await client.get("/api/regional-data")
        data = response.json()
        assert len(data["country_data"]) == 3

    @pytest.mark.asyncio
    async def test_massachusetts_is_rank_1(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        data = response.json()
        states = data["top_us_states_2025"]
        mass = next((s for s in states if s["state"] == "Massachusetts"), None)
        assert mass is not None
        assert mass["leed_rank_2025"] == 1

    @pytest.mark.asyncio
    async def test_country_data_has_us_canada_mexico(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        data = response.json()
        countries = {c["country"] for c in data["country_data"]}
        assert "US" in countries
        assert "Canada" in countries
        assert "Mexico" in countries

    @pytest.mark.asyncio
    async def test_state_structure(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        data = response.json()
        state = data["top_us_states_2025"][0]
        assert "state" in state
        assert "key_drivers" in state
        assert "key_policies" in state

    @pytest.mark.asyncio
    async def test_country_structure(self, client: AsyncClient):
        response = await client.get("/api/regional-data")
        data = response.json()
        country = data["country_data"][0]
        assert "country" in country
        assert "leed_certified_space_sq_meters_m" in country
        assert "confidence" in country


# ===========================================================================
# 4. GET /api/technologies
# ===========================================================================


class TestTechnologies:
    @pytest.mark.asyncio
    async def test_technologies_returns_200(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_technologies_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        assert "as_of_date" in data
        assert "technologies" in data
        assert "summary_adoption_rates" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_technologies_count_is_6(self, client: AsyncClient):
        """Should return exactly 6 technologies."""
        response = await client.get("/api/technologies")
        data = response.json()
        assert len(data["technologies"]) == 6

    @pytest.mark.asyncio
    async def test_technology_ids_present(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        ids = {t["id"] for t in data["technologies"]}
        expected_ids = {
            "electric-construction-equipment",
            "solar-pv",
            "green-building-systems",
            "battery-energy-storage",
            "mass-timber",
            "green-hydrogen",
        }
        assert ids == expected_ids

    @pytest.mark.asyncio
    async def test_technology_structure(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        tech = data["technologies"][0]
        required_fields = [
            "id", "name", "category", "description",
            "feasibility", "roi", "key_benefits", "key_barriers",
            "confidence",
        ]
        for field in required_fields:
            assert field in tech, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_feasibility_score_structure(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        feasibility = data["technologies"][0]["feasibility"]
        assert "overall_score" in feasibility
        assert "technical_maturity" in feasibility
        assert "financial_viability" in feasibility
        assert "regulatory_support" in feasibility
        assert "workforce_readiness" in feasibility
        assert "supply_chain_maturity" in feasibility
        assert "mid_size_adoption_ease" in feasibility

    @pytest.mark.asyncio
    async def test_roi_metric_structure(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        roi = data["technologies"][0]["roi"]
        assert "payback_years_min" in roi
        assert "payback_years_max" in roi

    @pytest.mark.asyncio
    async def test_solar_pv_feasibility_overall_score(self, client: AsyncClient):
        """Solar PV should have overall feasibility score of 8.2."""
        response = await client.get("/api/technologies")
        data = response.json()
        solar = next(t for t in data["technologies"] if t["id"] == "solar-pv")
        assert solar["feasibility"]["overall_score"] == pytest.approx(8.2, rel=1e-3)

    @pytest.mark.asyncio
    async def test_green_building_systems_highest_feasibility(self, client: AsyncClient):
        """Green building systems should have highest overall feasibility (8.8)."""
        response = await client.get("/api/technologies")
        data = response.json()
        gbs = next(t for t in data["technologies"] if t["id"] == "green-building-systems")
        assert gbs["feasibility"]["overall_score"] == pytest.approx(8.8, rel=1e-3)

    @pytest.mark.asyncio
    async def test_summary_adoption_rates_present(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        adoption_rates = data["summary_adoption_rates"]
        assert isinstance(adoption_rates, dict)
        assert len(adoption_rates) >= 1
        # All rates should be numeric (0-100)
        for key, val in adoption_rates.items():
            assert 0 <= val <= 100, f"Adoption rate out of range for {key}: {val}"

    @pytest.mark.asyncio
    async def test_electric_equipment_market_size(self, client: AsyncClient):
        response = await client.get("/api/technologies")
        data = response.json()
        elec = next(t for t in data["technologies"] if t["id"] == "electric-construction-equipment")
        assert elec["market_size_2025_usd_b"] == pytest.approx(15.77, rel=1e-3)


# ===========================================================================
# 5. GET /api/technology/{id}/comparison
# ===========================================================================


class TestTechnologyComparison:
    @pytest.mark.asyncio
    async def test_electric_equipment_comparison_200(self, client: AsyncClient):
        response = await client.get("/api/technology/electric-construction-equipment/comparison")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_solar_pv_comparison_200(self, client: AsyncClient):
        response = await client.get("/api/technology/solar-pv/comparison")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_green_building_systems_comparison_200(self, client: AsyncClient):
        response = await client.get("/api/technology/green-building-systems/comparison")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_invalid_technology_id_returns_404(self, client: AsyncClient):
        response = await client.get("/api/technology/nonexistent-tech/comparison")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_id_404_error_body(self, client: AsyncClient):
        response = await client.get("/api/technology/fake-tech-id/comparison")
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_comparison_response_structure(self, client: AsyncClient):
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        required_fields = [
            "technology_id",
            "technology_name",
            "conventional_equivalent",
            "comparison_unit",
            "tco_scenarios",
            "key_financial_insights",
            "incentives_included",
            "data_confidence",
            "sources",
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_electric_equipment_technology_id(self, client: AsyncClient):
        response = await client.get("/api/technology/electric-construction-equipment/comparison")
        data = response.json()
        assert data["technology_id"] == "electric-construction-equipment"

    @pytest.mark.asyncio
    async def test_solar_pv_technology_id(self, client: AsyncClient):
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        assert data["technology_id"] == "solar-pv"

    @pytest.mark.asyncio
    async def test_green_building_technology_id(self, client: AsyncClient):
        response = await client.get("/api/technology/green-building-systems/comparison")
        data = response.json()
        assert data["technology_id"] == "green-building-systems"

    @pytest.mark.asyncio
    async def test_tco_scenarios_present(self, client: AsyncClient):
        response = await client.get("/api/technology/electric-construction-equipment/comparison")
        data = response.json()
        assert len(data["tco_scenarios"]) >= 1

    @pytest.mark.asyncio
    async def test_tco_scenario_structure(self, client: AsyncClient):
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        scenario = data["tco_scenarios"][0]
        assert "scenario_name" in scenario
        assert "analysis_period_years" in scenario
        assert "discount_rate_pct" in scenario
        assert "green_total_tco_usd_k" in scenario
        assert "conventional_total_tco_usd_k" in scenario
        assert "green_advantage_usd_k" in scenario
        assert "components" in scenario

    @pytest.mark.asyncio
    async def test_electric_equipment_has_two_scenarios(self, client: AsyncClient):
        """Electric equipment should have base case + incentivized scenario."""
        response = await client.get("/api/technology/electric-construction-equipment/comparison")
        data = response.json()
        assert len(data["tco_scenarios"]) == 2

    @pytest.mark.asyncio
    async def test_solar_pv_has_two_scenarios(self, client: AsyncClient):
        """Solar PV should have base case + ITC scenario."""
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        assert len(data["tco_scenarios"]) == 2

    @pytest.mark.asyncio
    async def test_key_financial_insights_present(self, client: AsyncClient):
        response = await client.get("/api/technology/green-building-systems/comparison")
        data = response.json()
        assert len(data["key_financial_insights"]) >= 1

    @pytest.mark.asyncio
    async def test_electric_equipment_base_green_advantage(self, client: AsyncClient):
        """Base case: electric equipment TCO advantage = $25K over 10 years."""
        response = await client.get("/api/technology/electric-construction-equipment/comparison")
        data = response.json()
        base_scenario = data["tco_scenarios"][0]
        assert base_scenario["green_advantage_usd_k"] == pytest.approx(25.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_solar_pv_20yr_conventional_tco(self, client: AsyncClient):
        """Solar base case 20-yr conventional TCO = $320K."""
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        base_scenario = data["tco_scenarios"][0]
        assert base_scenario["conventional_total_tco_usd_k"] == pytest.approx(320.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_comparison_components_structure(self, client: AsyncClient):
        response = await client.get("/api/technology/green-building-systems/comparison")
        data = response.json()
        component = data["tco_scenarios"][0]["components"][0]
        assert "component" in component
        assert "green_cost_usd_k" in component
        assert "conventional_cost_usd_k" in component
        assert "difference_usd_k" in component


# ===========================================================================
# 6. GET /api/payback-analysis
# ===========================================================================


class TestPaybackAnalysis:
    @pytest.mark.asyncio
    async def test_payback_analysis_returns_200(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_payback_analysis_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        data = response.json()
        assert "as_of_date" in data
        assert "analysis_assumptions" in data
        assert "payback_data" in data
        assert "summary_stats" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_payback_data_count_is_6(self, client: AsyncClient):
        """Should have payback data for all 6 technologies."""
        response = await client.get("/api/payback-analysis")
        data = response.json()
        assert len(data["payback_data"]) == 6

    @pytest.mark.asyncio
    async def test_payback_entry_structure(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        data = response.json()
        entry = data["payback_data"][0]
        required_fields = [
            "technology_id", "technology_name", "category",
            "payback_years_base", "payback_years_with_incentives",
            "payback_years_optimistic", "payback_years_pessimistic",
            "confidence",
        ]
        for field in required_fields:
            assert field in entry, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_summary_stats_keys(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        data = response.json()
        stats = data["summary_stats"]
        assert "avg_payback_no_incentives" in stats
        assert "avg_payback_with_incentives" in stats
        assert "min_payback" in stats
        assert "max_payback" in stats

    @pytest.mark.asyncio
    async def test_summary_stats_values(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        data = response.json()
        stats = data["summary_stats"]
        assert stats["avg_payback_no_incentives"] == pytest.approx(9.0, rel=1e-3)
        assert stats["avg_payback_with_incentives"] == pytest.approx(6.2, rel=1e-3)
        assert stats["min_payback"] == pytest.approx(3.0, rel=1e-3)
        assert stats["max_payback"] == pytest.approx(25.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_green_building_systems_lowest_base_payback(self, client: AsyncClient):
        """Green building systems should have the best base payback (5.5 years)."""
        response = await client.get("/api/payback-analysis")
        data = response.json()
        entries = {e["technology_id"]: e for e in data["payback_data"]}
        gbs = entries["green-building-systems"]
        assert gbs["payback_years_base"] == pytest.approx(5.5, rel=1e-3)
        assert gbs["payback_years_with_incentives"] == pytest.approx(4.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_green_hydrogen_highest_payback(self, client: AsyncClient):
        """Green hydrogen should have the worst payback period."""
        response = await client.get("/api/payback-analysis")
        data = response.json()
        entries = {e["technology_id"]: e for e in data["payback_data"]}
        hydrogen = entries["green-hydrogen"]
        assert hydrogen["payback_years_base"] == pytest.approx(18.0, rel=1e-3)
        assert hydrogen["payback_years_pessimistic"] == pytest.approx(25.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_solar_itc_payback_reduction(self, client: AsyncClient):
        """Solar ITC should reduce payback from 7.0 to 4.5 years."""
        response = await client.get("/api/payback-analysis")
        data = response.json()
        entries = {e["technology_id"]: e for e in data["payback_data"]}
        solar = entries["solar-pv"]
        assert solar["payback_years_base"] == pytest.approx(7.0, rel=1e-3)
        assert solar["payback_years_with_incentives"] == pytest.approx(4.5, rel=1e-3)

    @pytest.mark.asyncio
    async def test_analysis_assumptions_present(self, client: AsyncClient):
        response = await client.get("/api/payback-analysis")
        data = response.json()
        assert len(data["analysis_assumptions"]) >= 1


# ===========================================================================
# 7. GET /api/roi-scenarios
# ===========================================================================


class TestROIScenarios:
    @pytest.mark.asyncio
    async def test_roi_scenarios_returns_200(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_roi_scenarios_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        assert "as_of_date" in data
        assert "base_year" in data
        assert "representative_firm_profile" in data
        assert "discount_rate_pct" in data
        assert "scenarios" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_three_roi_scenarios(self, client: AsyncClient):
        """Should return exactly 3 scenarios: conservative, moderate, aggressive."""
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        assert len(data["scenarios"]) == 3

    @pytest.mark.asyncio
    async def test_scenario_types(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        scenario_types = {s["scenario"] for s in data["scenarios"]}
        assert scenario_types == {"conservative", "moderate", "aggressive"}

    @pytest.mark.asyncio
    async def test_roi_scenario_structure(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        scenario = data["scenarios"][0]
        required_fields = [
            "scenario", "label", "description", "technologies_included",
            "initial_investment_usd_k", "ten_year_roi_pct", "ten_year_npv_usd_k",
            "irr_pct", "breakeven_year", "annual_projections",
            "key_assumptions", "risk_factors",
        ]
        for field in required_fields:
            assert field in scenario, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_conservative_scenario_values(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        conservative = next(s for s in data["scenarios"] if s["scenario"] == "conservative")
        assert conservative["initial_investment_usd_k"] == pytest.approx(350.0, rel=1e-3)
        assert conservative["ten_year_roi_pct"] == pytest.approx(142.0, rel=1e-3)
        assert conservative["irr_pct"] == pytest.approx(18.5, rel=1e-3)

    @pytest.mark.asyncio
    async def test_moderate_scenario_values(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        moderate = next(s for s in data["scenarios"] if s["scenario"] == "moderate")
        assert moderate["initial_investment_usd_k"] == pytest.approx(1250.0, rel=1e-3)
        assert moderate["ten_year_roi_pct"] == pytest.approx(198.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_aggressive_scenario_values(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        aggressive = next(s for s in data["scenarios"] if s["scenario"] == "aggressive")
        assert aggressive["initial_investment_usd_k"] == pytest.approx(3500.0, rel=1e-3)
        assert aggressive["ten_year_roi_pct"] == pytest.approx(267.0, rel=1e-3)
        assert aggressive["ten_year_npv_usd_k"] == pytest.approx(3845.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_annual_projections_count(self, client: AsyncClient):
        """Each scenario should have 10 annual projection data points."""
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        for scenario in data["scenarios"]:
            assert len(scenario["annual_projections"]) == 10, (
                f"Scenario {scenario['scenario']} has unexpected projection count"
            )

    @pytest.mark.asyncio
    async def test_annual_projection_structure(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        projection = data["scenarios"][0]["annual_projections"][0]
        assert "year" in projection
        assert "cumulative_investment_usd_k" in projection
        assert "cumulative_savings_usd_k" in projection
        assert "net_position_usd_k" in projection
        assert "roi_pct" in projection

    @pytest.mark.asyncio
    async def test_base_year_is_2026(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        assert data["base_year"] == 2026

    @pytest.mark.asyncio
    async def test_discount_rate(self, client: AsyncClient):
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        assert data["discount_rate_pct"] == pytest.approx(7.0, rel=1e-3)


# ===========================================================================
# 8. GET /api/incentives
# ===========================================================================


class TestIncentives:
    @pytest.mark.asyncio
    async def test_incentives_returns_200(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_incentives_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        assert "as_of_date" in data
        assert "total_ira_budget_usd_b" in data
        assert "total_incentives_listed" in data
        assert "incentives" in data
        assert "political_risk_summary" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_ten_incentives(self, client: AsyncClient):
        """Should return exactly 10 incentives."""
        response = await client.get("/api/incentives")
        data = response.json()
        assert len(data["incentives"]) == 10
        assert data["total_incentives_listed"] == 10

    @pytest.mark.asyncio
    async def test_incentive_structure(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        incentive = data["incentives"][0]
        required_fields = [
            "id", "name", "program", "jurisdiction", "incentive_type",
            "applicable_technologies", "value_description",
            "eligible_firm_sizes", "status", "confidence", "source",
            "financial_impact_description",
        ]
        for field in required_fields:
            assert field in incentive, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_ira_budget_270_billion(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        assert data["total_ira_budget_usd_b"] == pytest.approx(270.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_solar_itc_incentive_present(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        incentive_ids = {i["id"] for i in data["incentives"]}
        assert "ira-solar-itc" in incentive_ids

    @pytest.mark.asyncio
    async def test_section_179d_present(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        incentive_ids = {i["id"] for i in data["incentives"]}
        assert "section-179d" in incentive_ids

    @pytest.mark.asyncio
    async def test_solar_itc_value_pct(self, client: AsyncClient):
        """IRA Solar ITC should be 30%."""
        response = await client.get("/api/incentives")
        data = response.json()
        solar_itc = next(i for i in data["incentives"] if i["id"] == "ira-solar-itc")
        assert solar_itc["value_pct"] == pytest.approx(30.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_all_incentives_have_active_or_modified_status(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        valid_statuses = {"Active", "Modified", "At Risk", "Expired"}
        for incentive in data["incentives"]:
            assert incentive["status"] in valid_statuses, (
                f"Incentive {incentive['id']} has invalid status: {incentive['status']}"
            )

    @pytest.mark.asyncio
    async def test_political_risk_summary_not_empty(self, client: AsyncClient):
        response = await client.get("/api/incentives")
        data = response.json()
        assert len(data["political_risk_summary"]) > 10


# ===========================================================================
# 9. GET /api/case-studies
# ===========================================================================


class TestCaseStudies:
    @pytest.mark.asyncio
    async def test_case_studies_returns_200(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_case_studies_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        assert "as_of_date" in data
        assert "total_firms_profiled" in data
        assert "case_studies" in data
        assert "technology_adoption_summary" in data
        assert "investment_priority_matrix" in data
        assert "sources" in data

    @pytest.mark.asyncio
    async def test_six_case_studies(self, client: AsyncClient):
        """Should return exactly 6 case studies."""
        response = await client.get("/api/case-studies")
        data = response.json()
        assert len(data["case_studies"]) == 6
        assert data["total_firms_profiled"] == 6

    @pytest.mark.asyncio
    async def test_case_study_ids(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        ids = {cs["id"] for cs in data["case_studies"]}
        expected = {"mortenson", "gilbane", "suffolk", "swinerton", "hensel-phelps", "brasfield-gorrie"}
        assert ids == expected

    @pytest.mark.asyncio
    async def test_case_study_structure(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        study = data["case_studies"][0]
        required_fields = [
            "id", "company_name", "headquarters", "annual_revenue_usd_b",
            "employees", "specializations", "sustainability_start_year",
            "primary_strategy", "has_dedicated_sustainability_team",
            "key_differentiator", "technologies_adopted", "roi_metrics",
            "key_lessons", "applicable_to_mid_size", "confidence", "sources",
        ]
        for field in required_fields:
            assert field in study, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_all_case_studies_applicable_to_mid_size(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        for study in data["case_studies"]:
            assert study["applicable_to_mid_size"] is True, (
                f"{study['company_name']} should be applicable to mid-size firms"
            )

    @pytest.mark.asyncio
    async def test_technology_adoption_summary_present(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        assert len(data["technology_adoption_summary"]) >= 1

    @pytest.mark.asyncio
    async def test_leed_100_percent_adoption(self, client: AsyncClient):
        """LEED adoption should be 100% (all 6 firms)."""
        response = await client.get("/api/case-studies")
        data = response.json()
        summary = {s["technology"]: s for s in data["technology_adoption_summary"]}
        assert "LEED Certification" in summary
        leed = summary["LEED Certification"]
        assert leed["firms_using"] == 6
        assert leed["adoption_rate_pct"] == pytest.approx(100.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_investment_priority_matrix_count(self, client: AsyncClient):
        """Should have 5 investment priority items."""
        response = await client.get("/api/case-studies")
        data = response.json()
        assert len(data["investment_priority_matrix"]) == 5

    @pytest.mark.asyncio
    async def test_investment_priority_structure(self, client: AsyncClient):
        response = await client.get("/api/case-studies")
        data = response.json()
        priority = data["investment_priority_matrix"][0]
        assert "priority" in priority
        assert "investment" in priority
        assert "annual_cost_usd_k_min" in priority
        assert "annual_cost_usd_k_max" in priority
        assert "roi_timeline_description" in priority
        assert priority["priority"] == 1

    @pytest.mark.asyncio
    async def test_mortenson_metrics(self, client: AsyncClient):
        """Mortenson should have 5B+ revenue and be ranked #1 battery storage."""
        response = await client.get("/api/case-studies")
        data = response.json()
        mortenson = next(cs for cs in data["case_studies"] if cs["id"] == "mortenson")
        assert mortenson["annual_revenue_usd_b"] == pytest.approx(5.5, rel=1e-3)


# ===========================================================================
# 10. GET /api/green-contracts
# ===========================================================================


class TestGreenContracts:
    @pytest.mark.asyncio
    async def test_green_contracts_returns_200(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_green_contracts_top_level_fields(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        required_fields = [
            "as_of_date",
            "leed_spec_prevalence_pct",
            "states_with_leed_mandates",
            "federal_leed_requirement",
            "green_certified_office_share_pct",
            "bid_win_rate_data",
            "contract_premiums",
            "certification_landscape",
            "win_factors",
            "total_leed_credential_holders",
            "leed_ap_holders",
            "leed_om_growth_pct",
            "client_preference_summary",
            "sources",
        ]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"

    @pytest.mark.asyncio
    async def test_leed_spec_prevalence_71_pct(self, client: AsyncClient):
        """LEED is specified in 71% of projects >$50M."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["leed_spec_prevalence_pct"] == pytest.approx(71.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_states_with_leed_mandates(self, client: AsyncClient):
        """35 states should have LEED mandates."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["states_with_leed_mandates"] == 35

    @pytest.mark.asyncio
    async def test_green_certified_office_share(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["green_certified_office_share_pct"] == pytest.approx(41.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_bid_win_rate_data_count(self, client: AsyncClient):
        """Should have 7 bid win rate data points."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert len(data["bid_win_rate_data"]) == 7

    @pytest.mark.asyncio
    async def test_bid_win_rate_structure(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        entry = data["bid_win_rate_data"][0]
        assert "credential_level" in entry
        assert "project_segment" in entry
        assert "notes" in entry
        assert "confidence" in entry

    @pytest.mark.asyncio
    async def test_contract_premiums_count(self, client: AsyncClient):
        """Should have 7 contract premium data points."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert len(data["contract_premiums"]) == 7

    @pytest.mark.asyncio
    async def test_leed_rent_premium_31_pct(self, client: AsyncClient):
        """LEED buildings command 31% higher rents."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        # Find the 31% rent premium entry
        rent_premiums = [
            p for p in data["contract_premiums"]
            if p.get("value_numeric") == pytest.approx(31.0)
        ]
        assert len(rent_premiums) >= 1

    @pytest.mark.asyncio
    async def test_certification_landscape_count(self, client: AsyncClient):
        """Should have 5 certifications in the landscape."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert len(data["certification_landscape"]) == 5

    @pytest.mark.asyncio
    async def test_leed_certification_present(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        cert_names = {c["certification"] for c in data["certification_landscape"]}
        assert "LEED" in cert_names

    @pytest.mark.asyncio
    async def test_leed_recommended_for_mid_size(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        leed = next(c for c in data["certification_landscape"] if c["certification"] == "LEED")
        assert leed["recommended_for_mid_size"] is True

    @pytest.mark.asyncio
    async def test_win_factors_count(self, client: AsyncClient):
        """Should have 7 win factors."""
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert len(data["win_factors"]) == 7

    @pytest.mark.asyncio
    async def test_total_leed_credential_holders(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["total_leed_credential_holders"] == 205000

    @pytest.mark.asyncio
    async def test_leed_ap_holders(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["leed_ap_holders"] == 129000

    @pytest.mark.asyncio
    async def test_leed_om_growth_pct(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        assert data["leed_om_growth_pct"] == pytest.approx(79.0, rel=1e-3)

    @pytest.mark.asyncio
    async def test_client_preference_summary_present(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        summary = data["client_preference_summary"]
        assert isinstance(summary, dict)
        assert len(summary) >= 1

    @pytest.mark.asyncio
    async def test_federal_government_client_preference(self, client: AsyncClient):
        response = await client.get("/api/green-contracts")
        data = response.json()
        summary = data["client_preference_summary"]
        assert "Federal Government" in summary


# ===========================================================================
# 11. CORS Headers
# ===========================================================================


class TestCORSHeaders:
    @pytest.mark.asyncio
    async def test_cors_header_on_health(self, client: AsyncClient):
        """CORS allow-origin header should be present on responses."""
        response = await client.get(
            "/health", headers={"Origin": CORS_ORIGIN}
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_header_on_market_trends(self, client: AsyncClient):
        response = await client.get(
            "/api/market-trends", headers={"Origin": CORS_ORIGIN}
        )
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_header_on_technologies(self, client: AsyncClient):
        response = await client.get(
            "/api/technologies", headers={"Origin": CORS_ORIGIN}
        )
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_preflight_options(self, client: AsyncClient):
        """OPTIONS preflight request should return 200 with CORS headers."""
        response = await client.options(
            "/api/market-trends",
            headers={
                "Origin": CORS_ORIGIN,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_allows_localhost_3000(self, client: AsyncClient):
        """CORS should explicitly allow localhost:3000 or wildcard."""
        response = await client.get(
            "/api/technologies", headers={"Origin": "http://localhost:3000"}
        )
        allowed_origin = response.headers.get("access-control-allow-origin", "")
        assert allowed_origin in ("http://localhost:3000", "*"), (
            f"Unexpected CORS origin: {allowed_origin}"
        )

    @pytest.mark.asyncio
    async def test_cors_header_on_roi_scenarios(self, client: AsyncClient):
        response = await client.get(
            "/api/roi-scenarios", headers={"Origin": CORS_ORIGIN}
        )
        assert "access-control-allow-origin" in response.headers

    @pytest.mark.asyncio
    async def test_cors_header_on_case_studies(self, client: AsyncClient):
        response = await client.get(
            "/api/case-studies", headers={"Origin": CORS_ORIGIN}
        )
        assert "access-control-allow-origin" in response.headers


# ===========================================================================
# 12. OpenAPI / Documentation endpoints
# ===========================================================================


class TestDocumentation:
    @pytest.mark.asyncio
    async def test_openapi_json_accessible(self, client: AsyncClient):
        response = await client.get("/openapi.json")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_openapi_contains_all_endpoints(self, client: AsyncClient):
        response = await client.get("/openapi.json")
        data = response.json()
        paths = data.get("paths", {})
        expected_paths = [
            "/health",
            "/api/market-trends",
            "/api/regional-data",
            "/api/technologies",
            "/api/technology/{tech_id}/comparison",
            "/api/payback-analysis",
            "/api/roi-scenarios",
            "/api/incentives",
            "/api/case-studies",
            "/api/green-contracts",
        ]
        for path in expected_paths:
            assert path in paths, f"Missing API path in OpenAPI spec: {path}"

    @pytest.mark.asyncio
    async def test_docs_endpoint_accessible(self, client: AsyncClient):
        response = await client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_redoc_endpoint_accessible(self, client: AsyncClient):
        response = await client.get("/redoc")
        assert response.status_code == 200
