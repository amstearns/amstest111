"""Initial schema: market_trends, technologies, roi_scenarios, case_studies,
regulatory_incentives, green_contracts

Revision ID: 001
Revises: 
Create Date: 2026-03-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all tables for the renewable energy executive dashboard."""

    # -------------------------------------------------------------------------
    # market_trends
    # -------------------------------------------------------------------------
    op.create_table(
        'market_trends',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('region', sa.String(length=100), nullable=False),
        sa.Column('adoption_rate', sa.Numeric(5, 1), nullable=False),
        sa.Column('market_size', sa.Numeric(15, 2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_market_trends_year', 'market_trends', ['year'])
    op.create_index('ix_market_trends_region', 'market_trends', ['region'])

    # -------------------------------------------------------------------------
    # technologies
    # -------------------------------------------------------------------------
    op.create_table(
        'technologies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('feasibility_score', sa.Numeric(4, 1), nullable=False),
        sa.Column('tco', sa.Numeric(15, 2), nullable=False),
        sa.Column('conventional_tco', sa.Numeric(15, 2), nullable=False),
        sa.Column('maturity_level', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cagr', sa.Numeric(5, 1), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_technologies_name', 'technologies', ['name'])
    op.create_index('ix_technologies_category', 'technologies', ['category'])

    # -------------------------------------------------------------------------
    # roi_scenarios (references technologies.id)
    # -------------------------------------------------------------------------
    op.create_table(
        'roi_scenarios',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('technology_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('scenario_type', sa.String(length=50), nullable=False),
        sa.Column('payback_years', sa.Numeric(5, 1), nullable=False),
        sa.Column('roi_percentage', sa.Numeric(6, 1), nullable=False),
        sa.Column('assumptions', sa.Text(), nullable=False),
        sa.Column('npv', sa.Numeric(15, 2), nullable=True),
        sa.Column('irr', sa.Numeric(5, 1), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['technology_id'], ['technologies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_roi_scenarios_technology_id', 'roi_scenarios', ['technology_id'])
    op.create_index('ix_roi_scenarios_scenario_type', 'roi_scenarios', ['scenario_type'])

    # -------------------------------------------------------------------------
    # case_studies
    # -------------------------------------------------------------------------
    op.create_table(
        'case_studies',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('firm_name', sa.String(length=200), nullable=False),
        sa.Column('size', sa.String(length=100), nullable=False),
        sa.Column('technologies_adopted', postgresql.ARRAY(sa.Text()), nullable=False),
        sa.Column('annual_revenue_m', sa.Numeric(10, 2), nullable=True),
        sa.Column('investment', sa.Numeric(15, 2), nullable=False),
        sa.Column('outcomes', sa.Text(), nullable=False),
        sa.Column('timeline', sa.String(length=100), nullable=False),
        sa.Column('headquarters', sa.String(length=200), nullable=True),
        sa.Column('strategy', sa.Text(), nullable=True),
        sa.Column('enr_ranking', sa.String(length=200), nullable=True),
        sa.Column('net_zero_year', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_case_studies_firm_name', 'case_studies', ['firm_name'])

    # -------------------------------------------------------------------------
    # regulatory_incentives
    # -------------------------------------------------------------------------
    op.create_table(
        'regulatory_incentives',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('policy_name', sa.String(length=300), nullable=False),
        sa.Column('jurisdiction', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('financial_impact', sa.Text(), nullable=False),
        sa.Column('financial_impact_b', sa.Numeric(15, 2), nullable=True),
        sa.Column('expiration', sa.Date(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_active', sa.String(length=10), nullable=False, server_default='yes'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_regulatory_incentives_policy_name', 'regulatory_incentives', ['policy_name'])
    op.create_index('ix_regulatory_incentives_jurisdiction', 'regulatory_incentives', ['jurisdiction'])
    op.create_index('ix_regulatory_incentives_type', 'regulatory_incentives', ['type'])

    # -------------------------------------------------------------------------
    # green_contracts
    # -------------------------------------------------------------------------
    op.create_table(
        'green_contracts',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('certification_type', sa.String(length=100), nullable=False),
        sa.Column('win_rate_premium', sa.Numeric(5, 1), nullable=False),
        sa.Column('contract_value_premium', sa.Numeric(5, 1), nullable=False),
        sa.Column('construction_cost_premium', sa.Numeric(5, 1), nullable=True),
        sa.Column('operating_cost_savings', sa.Numeric(5, 1), nullable=True),
        sa.Column('asset_value_increase', sa.Numeric(5, 1), nullable=True),
        sa.Column('min_project_size_m', sa.Numeric(10, 2), nullable=True),
        sa.Column('data_source', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_green_contracts_certification_type', 'green_contracts', ['certification_type'])


def downgrade() -> None:
    """Drop all dashboard tables in reverse dependency order."""
    op.drop_table('green_contracts')
    op.drop_table('regulatory_incentives')
    op.drop_table('case_studies')
    op.drop_table('roi_scenarios')
    op.drop_table('technologies')
    op.drop_table('market_trends')
