-- =============================================================================
-- Renewable Energy Executive Dashboard — Initial Schema
-- =============================================================================
-- Run: psql $DATABASE_URL -f 001_initial_schema.sql
-- =============================================================================

-- Ensure pgcrypto for gen_random_uuid() is available
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Alembic version table (managed by alembic upgrade head)
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- =============================================================================
-- market_trends
-- =============================================================================
CREATE TABLE IF NOT EXISTS market_trends (
    id          UUID        NOT NULL DEFAULT gen_random_uuid(),
    year        INTEGER     NOT NULL,
    region      VARCHAR(100) NOT NULL,
    adoption_rate NUMERIC(5,1) NOT NULL,
    market_size NUMERIC(15,2) NOT NULL,
    notes       TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_market_trends_year   ON market_trends(year);
CREATE INDEX IF NOT EXISTS ix_market_trends_region ON market_trends(region);

-- =============================================================================
-- technologies
-- =============================================================================
CREATE TABLE IF NOT EXISTS technologies (
    id               UUID         NOT NULL DEFAULT gen_random_uuid(),
    name             VARCHAR(200) NOT NULL,
    category         VARCHAR(100) NOT NULL,
    feasibility_score NUMERIC(4,1) NOT NULL,
    tco              NUMERIC(15,2) NOT NULL,
    conventional_tco NUMERIC(15,2) NOT NULL,
    maturity_level   VARCHAR(50)  NOT NULL,
    description      TEXT,
    cagr             NUMERIC(5,1),
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at       TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_technologies_name     ON technologies(name);
CREATE INDEX IF NOT EXISTS ix_technologies_category ON technologies(category);

-- =============================================================================
-- roi_scenarios
-- =============================================================================
CREATE TABLE IF NOT EXISTS roi_scenarios (
    id             UUID        NOT NULL DEFAULT gen_random_uuid(),
    technology_id  UUID        NOT NULL REFERENCES technologies(id) ON DELETE CASCADE,
    scenario_type  VARCHAR(50) NOT NULL,
    payback_years  NUMERIC(5,1) NOT NULL,
    roi_percentage NUMERIC(6,1) NOT NULL,
    assumptions    TEXT        NOT NULL,
    npv            NUMERIC(15,2),
    irr            NUMERIC(5,1),
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_roi_scenarios_technology_id ON roi_scenarios(technology_id);
CREATE INDEX IF NOT EXISTS ix_roi_scenarios_scenario_type ON roi_scenarios(scenario_type);

-- =============================================================================
-- case_studies
-- =============================================================================
CREATE TABLE IF NOT EXISTS case_studies (
    id                  UUID         NOT NULL DEFAULT gen_random_uuid(),
    firm_name           VARCHAR(200) NOT NULL,
    size                VARCHAR(100) NOT NULL,
    technologies_adopted TEXT[]       NOT NULL,
    annual_revenue_m    NUMERIC(10,2),
    investment          NUMERIC(15,2) NOT NULL,
    outcomes            TEXT         NOT NULL,
    timeline            VARCHAR(100) NOT NULL,
    headquarters        VARCHAR(200),
    strategy            TEXT,
    enr_ranking         VARCHAR(200),
    net_zero_year       INTEGER,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_case_studies_firm_name ON case_studies(firm_name);

-- =============================================================================
-- regulatory_incentives
-- =============================================================================
CREATE TABLE IF NOT EXISTS regulatory_incentives (
    id                  UUID         NOT NULL DEFAULT gen_random_uuid(),
    policy_name         VARCHAR(300) NOT NULL,
    jurisdiction        VARCHAR(100) NOT NULL,
    type                VARCHAR(100) NOT NULL,
    financial_impact    TEXT         NOT NULL,
    financial_impact_b  NUMERIC(15,2),
    expiration          DATE,
    description         TEXT,
    is_active           VARCHAR(10)  NOT NULL DEFAULT 'yes',
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_regulatory_incentives_policy_name  ON regulatory_incentives(policy_name);
CREATE INDEX IF NOT EXISTS ix_regulatory_incentives_jurisdiction ON regulatory_incentives(jurisdiction);
CREATE INDEX IF NOT EXISTS ix_regulatory_incentives_type         ON regulatory_incentives(type);

-- =============================================================================
-- green_contracts
-- =============================================================================
CREATE TABLE IF NOT EXISTS green_contracts (
    id                       UUID        NOT NULL DEFAULT gen_random_uuid(),
    certification_type       VARCHAR(100) NOT NULL,
    win_rate_premium         NUMERIC(5,1) NOT NULL,
    contract_value_premium   NUMERIC(5,1) NOT NULL,
    construction_cost_premium NUMERIC(5,1),
    operating_cost_savings   NUMERIC(5,1),
    asset_value_increase     NUMERIC(5,1),
    min_project_size_m       NUMERIC(10,2),
    data_source              TEXT,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (id)
);
CREATE INDEX IF NOT EXISTS ix_green_contracts_certification_type ON green_contracts(certification_type);

-- Mark migration as applied
INSERT INTO alembic_version (version_num) VALUES ('001')
ON CONFLICT DO NOTHING;
