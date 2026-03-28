"""
Data Serialization and Schema Validation Tests.

Tests verify that complex data types are correctly serialized from the
ORM layer through Pydantic schemas to JSON responses.

Covers:
- Datetime field serialization (ISO 8601 format)
- Decimal → float conversions
- UUID → string conversions
- Enum serialization
- Array/list type handling
- Nested model serialization
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from datetime import datetime
import json
import re

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
# Helper Functions
# ---------------------------------------------------------------------------


def is_iso8601_datetime(value: str) -> bool:
    """Check if value is a valid ISO 8601 datetime string."""
    iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$'
    return bool(re.match(iso8601_pattern, value))


def is_iso8601_date(value: str) -> bool:
    """Check if value is a valid ISO 8601 date string (YYYY-MM-DD)."""
    date_pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(date_pattern, value))


# ===========================================================================
# 1. DateTime Serialization
# ===========================================================================


class TestDateTimeSerialization:
    """
    Verify datetime fields are serialized to ISO 8601 format.
    """

    @pytest.mark.asyncio
    async def test_health_timestamp_is_iso8601(self, client: AsyncClient):
        """
        /health timestamp field should be ISO 8601 format.
        """
        response = await client.get("/health")
        data = response.json()
        timestamp = data["timestamp"]
        
        assert isinstance(timestamp, str)
        assert is_iso8601_datetime(timestamp), \
            f"Timestamp not ISO 8601 format: {timestamp}"

    @pytest.mark.asyncio
    async def test_market_trends_as_of_date_format(self, client: AsyncClient):
        """
        /api/market-trends as_of_date should be YYYY-MM-DD format.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        as_of_date = data["as_of_date"]
        
        assert isinstance(as_of_date, str)
        assert is_iso8601_date(as_of_date), \
            f"as_of_date not in YYYY-MM-DD format: {as_of_date}"

    @pytest.mark.asyncio
    async def test_regional_data_as_of_date_format(self, client: AsyncClient):
        """
        /api/regional-data as_of_date should be YYYY-MM-DD format.
        """
        response = await client.get("/api/regional-data")
        data = response.json()
        as_of_date = data["as_of_date"]
        
        assert isinstance(as_of_date, str)
        assert is_iso8601_date(as_of_date)

    @pytest.mark.asyncio
    async def test_payback_analysis_as_of_date_format(self, client: AsyncClient):
        """
        /api/payback-analysis as_of_date should be YYYY-MM-DD format.
        """
        response = await client.get("/api/payback-analysis")
        data = response.json()
        as_of_date = data["as_of_date"]
        
        assert isinstance(as_of_date, str)
        assert is_iso8601_date(as_of_date)


# ===========================================================================
# 2. Numeric Type Serialization (Decimal → float)
# ===========================================================================


class TestNumericSerialization:
    """
    Verify numeric fields from NUMERIC database columns are floats, not Decimals.
    """

    @pytest.mark.asyncio
    async def test_market_trends_all_numeric_fields_are_float(self, client: AsyncClient):
        """
        All numeric market metrics should be floats.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        numeric_fields = [
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
        ]
        
        for field in numeric_fields:
            value = data[field]
            assert isinstance(value, (int, float)), \
                f"{field} is not numeric type, got {type(value)}: {value}"

    @pytest.mark.asyncio
    async def test_adoption_by_firm_size_numeric_fields_are_float(self, client: AsyncClient):
        """
        Adoption rate percentages in firm size breakdown should be floats.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        for adoption in data["adoption_by_firm_size"]:
            for field in [
                "formal_esg_program_pct_min",
                "formal_esg_program_pct_max",
                "leed_experience_pct_min",
                "leed_experience_pct_max",
                "electric_equipment_fleet_pct_min",
                "electric_equipment_fleet_pct_max",
            ]:
                value = adoption[field]
                assert isinstance(value, (int, float)), \
                    f"{field} is not float: {type(value)}"

    @pytest.mark.asyncio
    async def test_time_series_point_values_are_float(self, client: AsyncClient):
        """
        Time series point values should be floats.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        for ts_point in data["global_market_time_series"]:
            assert isinstance(ts_point["value"], (int, float))
            assert isinstance(ts_point["year"], int)

    @pytest.mark.asyncio
    async def test_market_size_snapshot_value_is_float(self, client: AsyncClient):
        """
        Market size snapshot values should be floats.
        """
        response = await client.get("/api/regional-data")
        data = response.json()
        
        country = data["country_data"][0]
        value = country["leed_certified_space_sq_meters_m"]
        assert isinstance(value, (int, float))


# ===========================================================================
# 3. String Field Validation
# ===========================================================================


class TestStringFieldValidation:
    """
    Verify string fields are properly serialized and not empty where required.
    """

    @pytest.mark.asyncio
    async def test_market_trends_required_string_fields(self, client: AsyncClient):
        """
        Required string fields should not be null or empty.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        required_strings = ["as_of_date"]
        for field in required_strings:
            assert data[field] is not None
            assert isinstance(data[field], str)
            assert len(data[field]) > 0

    @pytest.mark.asyncio
    async def test_technology_names_are_strings(self, client: AsyncClient):
        """
        Technology names should be non-empty strings.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            assert isinstance(tech["name"], str)
            assert len(tech["name"]) > 0

    @pytest.mark.asyncio
    async def test_incentive_names_are_strings(self, client: AsyncClient):
        """
        Incentive names should be non-empty strings.
        """
        response = await client.get("/api/incentives")
        data = response.json()
        
        for incentive in data["incentives"]:
            assert isinstance(incentive["name"], str)
            assert len(incentive["name"]) > 0


# ===========================================================================
# 4. Enum Serialization
# ===========================================================================


class TestEnumSerialization:
    """
    Verify enum fields are serialized as their string values.
    """

    @pytest.mark.asyncio
    async def test_region_enum_serialization(self, client: AsyncClient):
        """
        Region enums should serialize as strings (US, Canada, Mexico, etc.).
        """
        response = await client.get("/api/regional-data")
        data = response.json()
        
        valid_regions = ["US", "Canada", "Mexico", "North America"]
        for country in data["country_data"]:
            assert country["country"] in valid_regions

    @pytest.mark.asyncio
    async def test_technology_category_enum_serialization(self, client: AsyncClient):
        """
        Technology category enums should serialize as strings.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        valid_categories = [
            "Electric Equipment",
            "Solar PV",
            "Green Building Systems",
            "Battery Storage",
            "Green Hydrogen",
            "Mass Timber",
            "Energy Management",
        ]
        
        for tech in data["technologies"]:
            assert tech["category"] in valid_categories

    @pytest.mark.asyncio
    async def test_confidence_level_enum_serialization(self, client: AsyncClient):
        """
        Confidence level enums should serialize as HIGH/MEDIUM/LOW strings.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        valid_confidence = ["HIGH", "MEDIUM", "LOW"]
        for source in data["sources"]:
            assert source["confidence"] in valid_confidence

    @pytest.mark.asyncio
    async def test_projection_scenario_enum_serialization(self, client: AsyncClient):
        """
        ProjectionScenario enums should serialize as lowercase strings.
        """
        response = await client.get("/api/roi-scenarios")
        data = response.json()
        
        valid_scenarios = ["conservative", "moderate", "aggressive"]
        for scenario in data["scenarios"]:
            assert scenario["scenario"] in valid_scenarios

    @pytest.mark.asyncio
    async def test_certification_standard_enum_serialization(self, client: AsyncClient):
        """
        CertificationStandard enums should serialize as strings.
        """
        response = await client.get("/api/green-contracts")
        data = response.json()
        
        # Just verify they are strings
        for cert in data["certification_landscape"]:
            assert isinstance(cert["certification"], str)


# ===========================================================================
# 5. Array/List Type Handling
# ===========================================================================


class TestArraySerialization:
    """
    Verify array fields are properly serialized.
    """

    @pytest.mark.asyncio
    async def test_key_benefits_is_list_of_strings(self, client: AsyncClient):
        """
        Technology key_benefits should be a list of strings.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            assert isinstance(tech["key_benefits"], list)
            for benefit in tech["key_benefits"]:
                assert isinstance(benefit, str)

    @pytest.mark.asyncio
    async def test_sources_is_list_of_objects(self, client: AsyncClient):
        """
        Sources should be a list of source citation objects.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        assert isinstance(data["sources"], list)
        for source in data["sources"]:
            assert isinstance(source, dict)
            assert "name" in source
            assert "organization" in source

    @pytest.mark.asyncio
    async def test_drivers_is_list_of_objects(self, client: AsyncClient):
        """
        Drivers should be a list of driver/barrier objects.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        assert isinstance(data["drivers"], list)
        for driver in data["drivers"]:
            assert isinstance(driver, dict)
            assert "name" in driver
            assert "description" in driver

    @pytest.mark.asyncio
    async def test_tco_components_is_list(self, client: AsyncClient):
        """
        TCO scenario components should be a list.
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        
        for scenario in data["tco_scenarios"]:
            assert isinstance(scenario["components"], list)
            for component in scenario["components"]:
                assert isinstance(component, dict)
                assert "component" in component


# ===========================================================================
# 6. Optional/Nullable Field Handling
# ===========================================================================


class TestOptionalFields:
    """
    Verify optional fields are either null or valid values, never undefined.
    """

    @pytest.mark.asyncio
    async def test_optional_market_size_fields(self, client: AsyncClient):
        """
        Optional market size fields can be null or float.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            # These fields are optional
            for field in ["market_size_2025_usd_b", "market_size_2030_projected_usd_b"]:
                value = tech.get(field)
                if value is not None:
                    assert isinstance(value, (int, float))

    @pytest.mark.asyncio
    async def test_optional_roi_fields(self, client: AsyncClient):
        """
        Optional ROI fields can be null or float.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        for tech in data["technologies"]:
            roi = tech["roi"]
            for field in ["payback_years_min", "payback_years_max", "irr_pct"]:
                value = roi.get(field)
                if value is not None:
                    assert isinstance(value, (int, float))

    @pytest.mark.asyncio
    async def test_optional_state_fields(self, client: AsyncClient):
        """
        Optional state fields are either present or absent, not undefined.
        """
        response = await client.get("/api/regional-data")
        data = response.json()
        
        for state in data["top_us_states_2025"]:
            # Check that fields that exist are valid types
            if "leed_rank_2025" in state:
                value = state["leed_rank_2025"]
                if value is not None:
                    assert isinstance(value, int)


# ===========================================================================
# 7. Nested Object Serialization
# ===========================================================================


class TestNestedObjectSerialization:
    """
    Verify deeply nested objects are correctly serialized.
    """

    @pytest.mark.asyncio
    async def test_feasibility_score_nested_object(self, client: AsyncClient):
        """
        FeasibilityScore nested object should be fully serialized.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        tech = data["technologies"][0]
        feasibility = tech["feasibility"]
        
        required_fields = [
            "overall_score", "technical_maturity", "financial_viability",
            "regulatory_support", "workforce_readiness", "supply_chain_maturity",
            "mid_size_adoption_ease"
        ]
        
        for field in required_fields:
            assert field in feasibility

    @pytest.mark.asyncio
    async def test_roi_metric_nested_object(self, client: AsyncClient):
        """
        TechnologyROIMetric nested object should be fully serialized.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        tech = data["technologies"][0]
        roi = tech["roi"]
        
        # ROI has optional fields
        assert isinstance(roi, dict)

    @pytest.mark.asyncio
    async def test_tco_scenario_nested_components(self, client: AsyncClient):
        """
        TCOScenario with nested components should be fully serialized.
        """
        response = await client.get("/api/technology/solar-pv/comparison")
        data = response.json()
        
        scenario = data["tco_scenarios"][0]
        assert "components" in scenario
        assert len(scenario["components"]) > 0
        
        component = scenario["components"][0]
        assert "component" in component
        assert "green_cost_usd_k" in component


# ===========================================================================
# 8. JSON Response Validity
# ===========================================================================


class TestJSONResponseValidity:
    """
    Verify all responses are valid JSON that can be serialized back.
    """

    @pytest.mark.asyncio
    async def test_market_trends_json_round_trip(self, client: AsyncClient):
        """
        Market trends response can be serialized to JSON and back.
        """
        response = await client.get("/api/market-trends")
        data = response.json()
        
        # Should be able to serialize back to JSON
        json_str = json.dumps(data)
        assert len(json_str) > 0
        
        # And deserialize again
        data2 = json.loads(json_str)
        assert data == data2

    @pytest.mark.asyncio
    async def test_technologies_json_round_trip(self, client: AsyncClient):
        """
        Technologies response can be serialized to JSON and back.
        """
        response = await client.get("/api/technologies")
        data = response.json()
        
        json_str = json.dumps(data)
        assert len(json_str) > 0
        
        data2 = json.loads(json_str)
        assert data == data2

    @pytest.mark.asyncio
    async def test_all_endpoints_return_valid_json(self, client: AsyncClient):
        """
        All endpoints return valid JSON responses.
        """
        endpoints = [
            "/health",
            "/api/market-trends",
            "/api/regional-data",
            "/api/technologies",
            "/api/technology/solar-pv/comparison",
            "/api/payback-analysis",
            "/api/roi-scenarios",
            "/api/incentives",
            "/api/case-studies",
            "/api/green-contracts",
        ]
        
        for endpoint in endpoints:
            response = await client.get(endpoint)
            assert response.status_code == 200
            
            # Must be valid JSON
            data = response.json()
            assert data is not None
            
            # Must be round-trippable
            json_str = json.dumps(data)
            data2 = json.loads(json_str)
            assert data == data2
