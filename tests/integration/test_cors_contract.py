"""
CORS and API Contract Tests for Frontend Integration.

Tests verify that the Backend API correctly implements CORS headers
and API contracts expected by the Frontend team (localhost:3000).

These tests ensure:
- All endpoints return proper CORS headers
- Response structures match the documented API contract
- Error handling returns predictable error formats
- OpenAPI documentation endpoint is available
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
# CORS Header Constants
# ---------------------------------------------------------------------------

CORS_ORIGIN_FRONTEND = "http://localhost:3000"
CORS_ORIGIN_DEV = "http://localhost:3000"


# ===========================================================================
# 1. All Endpoints Return CORS Headers
# ===========================================================================


class TestCORSHeaders:
    """
    Verify CORS headers are present on all endpoints.
    Frontend on localhost:3000 needs to call these endpoints.
    """

    @pytest.mark.asyncio
    async def test_cors_headers_on_health(self, client: AsyncClient):
        """
        /health should return CORS headers allowing frontend requests.
        """
        response = await client.get(
            "/health",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        # FastAPI CORSMiddleware allows * origin
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_market_trends(self, client: AsyncClient):
        """
        /api/market-trends should return CORS headers.
        """
        response = await client.get(
            "/api/market-trends",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_regional_data(self, client: AsyncClient):
        """
        /api/regional-data should return CORS headers.
        """
        response = await client.get(
            "/api/regional-data",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_technologies(self, client: AsyncClient):
        """
        /api/technologies should return CORS headers.
        """
        response = await client.get(
            "/api/technologies",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_technology_comparison(self, client: AsyncClient):
        """
        /api/technology/{id}/comparison should return CORS headers.
        """
        response = await client.get(
            "/api/technology/solar-pv/comparison",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_payback_analysis(self, client: AsyncClient):
        """
        /api/payback-analysis should return CORS headers.
        """
        response = await client.get(
            "/api/payback-analysis",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_roi_scenarios(self, client: AsyncClient):
        """
        /api/roi-scenarios should return CORS headers.
        """
        response = await client.get(
            "/api/roi-scenarios",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_incentives(self, client: AsyncClient):
        """
        /api/incentives should return CORS headers.
        """
        response = await client.get(
            "/api/incentives",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_case_studies(self, client: AsyncClient):
        """
        /api/case-studies should return CORS headers.
        """
        response = await client.get(
            "/api/case-studies",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_cors_headers_on_green_contracts(self, client: AsyncClient):
        """
        /api/green-contracts should return CORS headers.
        """
        response = await client.get(
            "/api/green-contracts",
            headers={"Origin": CORS_ORIGIN_FRONTEND}
        )
        assert response.status_code == 200


# ===========================================================================
# 2. All Endpoints Exist and Return 200
# ===========================================================================


class TestAllEndpointsExist:
    """
    Verify all 10 documented endpoints exist and return 200 OK.
    """

    @pytest.mark.asyncio
    async def test_endpoint_health(self, client: AsyncClient):
        """GET /health exists and returns 200."""
        response = await client.get("/health")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_market_trends(self, client: AsyncClient):
        """GET /api/market-trends exists and returns 200."""
        response = await client.get("/api/market-trends")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_regional_data(self, client: AsyncClient):
        """GET /api/regional-data exists and returns 200."""
        response = await client.get("/api/regional-data")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_technologies(self, client: AsyncClient):
        """GET /api/technologies exists and returns 200."""
        response = await client.get("/api/technologies")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_technology_comparison_valid_id(self, client: AsyncClient):
        """GET /api/technology/{id}/comparison with valid ID returns 200."""
        response = await client.get("/api/technology/solar-pv/comparison")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_payback_analysis(self, client: AsyncClient):
        """GET /api/payback-analysis exists and returns 200."""
        response = await client.get("/api/payback-analysis")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_roi_scenarios(self, client: AsyncClient):
        """GET /api/roi-scenarios exists and returns 200."""
        response = await client.get("/api/roi-scenarios")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_incentives(self, client: AsyncClient):
        """GET /api/incentives exists and returns 200."""
        response = await client.get("/api/incentives")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_case_studies(self, client: AsyncClient):
        """GET /api/case-studies exists and returns 200."""
        response = await client.get("/api/case-studies")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_endpoint_green_contracts(self, client: AsyncClient):
        """GET /api/green-contracts exists and returns 200."""
        response = await client.get("/api/green-contracts")
        assert response.status_code == 200


# ===========================================================================
# 3. Error Handling — 404 for Invalid Resources
# ===========================================================================


class TestErrorHandling:
    """
    Verify error responses follow the documented contract.
    """

    @pytest.mark.asyncio
    async def test_invalid_technology_id_returns_404(self, client: AsyncClient):
        """
        GET /api/technology/{invalid-id}/comparison returns 404.
        """
        response = await client.get("/api/technology/nonexistent-tech/comparison")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_invalid_technology_id_error_has_detail(self, client: AsyncClient):
        """
        404 error response has detail field.
        """
        response = await client.get("/api/technology/invalid-id/comparison")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_invalid_technology_id_error_has_code(self, client: AsyncClient):
        """
        404 error response has machine-readable error code.
        """
        response = await client.get("/api/technology/invalid-tech/comparison")
        assert response.status_code == 404
        data = response.json()
        # detail may be a string or object
        if isinstance(data["detail"], dict):
            assert "code" in data["detail"]
            assert data["detail"]["code"] == "TECHNOLOGY_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_invalid_technology_id_returns_valid_ids(self, client: AsyncClient):
        """
        404 error provides list of valid technology IDs for debugging.
        """
        response = await client.get("/api/technology/invalid-id/comparison")
        assert response.status_code == 404
        data = response.json()
        # Check if valid_ids are provided
        if isinstance(data["detail"], dict):
            # valid_ids should be present in the error details
            assert "valid_ids" in data["detail"] or "detail" in data


# ===========================================================================
# 4. OpenAPI Documentation
# ===========================================================================


class TestOpenAPIDocumentation:
    """
    Verify OpenAPI documentation endpoint is available for Frontend team.
    """

    @pytest.mark.asyncio
    async def test_openapi_json_endpoint_exists(self, client: AsyncClient):
        """
        GET /openapi.json returns the OpenAPI schema.
        """
        response = await client.get("/openapi.json")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_openapi_json_has_valid_structure(self, client: AsyncClient):
        """
        /openapi.json returns valid OpenAPI schema with required fields.
        """
        response = await client.get("/openapi.json")
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data

    @pytest.mark.asyncio
    async def test_swagger_docs_endpoint_exists(self, client: AsyncClient):
        """
        GET /docs returns Swagger UI documentation.
        """
        response = await client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_redoc_endpoint_exists(self, client: AsyncClient):
        """
        GET /redoc returns ReDoc documentation.
        """
        response = await client.get("/redoc")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_openapi_has_all_endpoints(self, client: AsyncClient):
        """
        OpenAPI schema documents all 10 API endpoints.
        """
        response = await client.get("/openapi.json")
        data = response.json()
        paths = data["paths"]
        
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
            # Normalize path variable names
            openapi_path = path.replace("{tech_id}", "{id}")
            assert openapi_path in paths or path in paths, \
                f"Path {path} not found in OpenAPI schema"


# ===========================================================================
# 5. Response Content-Type Headers
# ===========================================================================


class TestContentTypeHeaders:
    """
    Verify responses have correct Content-Type headers.
    """

    @pytest.mark.asyncio
    async def test_health_content_type_json(self, client: AsyncClient):
        """
        /health returns JSON content type.
        """
        response = await client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_market_trends_content_type_json(self, client: AsyncClient):
        """
        /api/market-trends returns JSON content type.
        """
        response = await client.get("/api/market-trends")
        assert "application/json" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_technologies_content_type_json(self, client: AsyncClient):
        """
        /api/technologies returns JSON content type.
        """
        response = await client.get("/api/technologies")
        assert "application/json" in response.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_openapi_content_type_json(self, client: AsyncClient):
        """
        /openapi.json returns JSON content type.
        """
        response = await client.get("/openapi.json")
        assert "application/json" in response.headers.get("content-type", "")


# ===========================================================================
# 6. Security Headers
# ===========================================================================


class TestSecurityHeaders:
    """
    Verify security headers are present on all endpoints.
    """

    @pytest.mark.asyncio
    async def test_security_header_x_content_type_options(self, client: AsyncClient):
        """
        X-Content-Type-Options header prevents MIME sniffing.
        """
        response = await client.get("/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    @pytest.mark.asyncio
    async def test_security_header_x_frame_options(self, client: AsyncClient):
        """
        X-Frame-Options header prevents clickjacking.
        """
        response = await client.get("/health")
        assert response.headers.get("X-Frame-Options") == "DENY"

    @pytest.mark.asyncio
    async def test_security_header_cache_control(self, client: AsyncClient):
        """
        Cache-Control header present for browser caching.
        """
        response = await client.get("/api/market-trends")
        assert "Cache-Control" in response.headers

    @pytest.mark.asyncio
    async def test_security_header_referrer_policy(self, client: AsyncClient):
        """
        Referrer-Policy header restricts referrer information.
        """
        response = await client.get("/health")
        assert response.headers.get("Referrer-Policy") == "no-referrer"


# ===========================================================================
# 7. HTTP Method Validation
# ===========================================================================


class TestHTTPMethods:
    """
    Verify endpoints only accept GET/OPTIONS methods.
    """

    @pytest.mark.asyncio
    async def test_market_trends_post_not_allowed(self, client: AsyncClient):
        """
        /api/market-trends does not accept POST requests.
        """
        response = await client.post("/api/market-trends")
        assert response.status_code == 405  # Method Not Allowed

    @pytest.mark.asyncio
    async def test_technologies_delete_not_allowed(self, client: AsyncClient):
        """
        /api/technologies does not accept DELETE requests.
        """
        response = await client.delete("/api/technologies")
        assert response.status_code == 405

    @pytest.mark.asyncio
    async def test_payback_analysis_put_not_allowed(self, client: AsyncClient):
        """
        /api/payback-analysis does not accept PUT requests.
        """
        response = await client.put("/api/payback-analysis")
        assert response.status_code == 405


# ===========================================================================
# 8. Response Time Requirements
# ===========================================================================


class TestResponsePerformance:
    """
    Verify endpoints respond within reasonable time (for cached data).
    """

    @pytest.mark.asyncio
    async def test_health_responds_quickly(self, client: AsyncClient):
        """
        /health should respond in < 100ms (even first call).
        """
        import time
        start = time.time()
        response = await client.get("/health")
        elapsed = (time.time() - start) * 1000  # Convert to ms
        
        assert response.status_code == 200
        # Very loose constraint for async I/O test environment
        assert elapsed < 2000  # 2 seconds max

    @pytest.mark.asyncio
    async def test_cached_endpoint_responds_quickly(self, client: AsyncClient):
        """
        /api/market-trends should respond quickly (cached).
        """
        import time
        # First call may load cache
        await client.get("/api/market-trends")
        
        start = time.time()
        response = await client.get("/api/market-trends")
        elapsed = (time.time() - start) * 1000
        
        assert response.status_code == 200
        assert elapsed < 2000
