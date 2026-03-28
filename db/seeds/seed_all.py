#!/usr/bin/env python3
"""
Seed script for the Renewable Energy Executive Dashboard database.

Data sourced from previous_output research reports:
  - market-analysis.md: Market size, adoption rates, regional data
  - competitive-benchmarking.md: Case studies (Mortenson, Gilbane, Suffolk,
    Swinerton, Hensel Phelps, Brasfield & Gorrie)
  - green-contract-correlation.md: Certification premiums, win rates
  - research-report.md: Technology data, ROI analysis, regulatory incentives

Financial precision:
  - Monetary values: 2 decimal places (NUMERIC(15,2))
  - Percentages: 1 decimal place (NUMERIC(5,1))
"""

import os
import sys
import uuid
from datetime import date

# Add workspace root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from db.models.models import (
    Base,
    MarketTrend,
    Technology,
    ROIScenario,
    CaseStudy,
    RegulatoryIncentive,
    GreenContract,
)

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://agent:agent_dev@postgres:5432/appdb")


def get_engine():
    return create_engine(DATABASE_URL, echo=False)


# =============================================================================
# MARKET TRENDS DATA
# Sources: research-report.md §1.1, market-analysis.md §1.1–1.4
# =============================================================================

MARKET_TRENDS = [
    # Global green building market
    {
        "year": 2023,
        "region": "Global",
        "adoption_rate": 42.0,
        "market_size": 560.00,
        "notes": "Global green building market value. US nonresidential construction +17.6% YoY.",
    },
    {
        "year": 2025,
        "region": "Global",
        "adoption_rate": 48.5,
        "market_size": 618.58,
        "notes": "Global green building market per Precedence Research (Feb 2026). CAGR 9.29%.",
    },
    {
        "year": 2030,
        "region": "Global",
        "adoption_rate": 60.0,
        "market_size": 950.00,
        "notes": "Projected midpoint on growth trajectory toward $1.374T by 2034.",
    },
    {
        "year": 2034,
        "region": "Global",
        "adoption_rate": 72.0,
        "market_size": 1374.23,
        "notes": "Projected global green building market per Precedence Research (Feb 2026).",
    },
    # North America
    {
        "year": 2025,
        "region": "North America",
        "adoption_rate": 47.5,
        "market_size": 200.00,
        "notes": "NA green buildings market >$200B. NA holds 35% share of global green materials market.",
    },
    {
        "year": 2025,
        "region": "North America - Materials",
        "adoption_rate": 47.5,
        "market_size": 153.87,
        "notes": "NA green building materials market specifically. 35% global share. CAGR ~3.80% to 2035.",
    },
    {
        "year": 2030,
        "region": "North America",
        "adoption_rate": 58.0,
        "market_size": 310.00,
        "notes": "Projected at 8-12% CAGR through 2030 per Mordor Intelligence.",
    },
    {
        "year": 2035,
        "region": "North America - Materials",
        "adoption_rate": 65.0,
        "market_size": 223.43,
        "notes": "Projected NA green building materials market per Precedence Research.",
    },
    # United States by firm size
    {
        "year": 2025,
        "region": "United States - Large Firms (>$500M)",
        "adoption_rate": 80.0,
        "market_size": 85.00,
        "notes": "Formal ESG/sustainability program 75-85%. LEED experience >80%. ~$85B addressable segment.",
    },
    {
        "year": 2025,
        "region": "United States - Mid-Size Firms ($50M-$500M)",
        "adoption_rate": 47.5,
        "market_size": 65.00,
        "notes": "Formal ESG 40-55%; LEED experience 35-50%. Electric equipment pilot stage 1-3% of fleet.",
    },
    {
        "year": 2025,
        "region": "United States - Small Firms (<$50M)",
        "adoption_rate": 20.0,
        "market_size": 20.00,
        "notes": "Formal ESG 15-25%; LEED experience 10-20%. Electric equipment very rare (<1%).",
    },
    # Canada
    {
        "year": 2024,
        "region": "Canada",
        "adoption_rate": 55.0,
        "market_size": 28.50,
        "notes": "Canada ranks 2nd globally in LEED-certified space: 10.07M sqm across 300 projects.",
    },
    # Mexico
    {
        "year": 2024,
        "region": "Mexico",
        "adoption_rate": 22.0,
        "market_size": 8.20,
        "notes": "Mexico ranks 6th globally: 104 LEED projects, 2.27M sqm. First LEED v5 projects worldwide.",
    },
    # Electric construction equipment (sub-market)
    {
        "year": 2025,
        "region": "Global - Electric Construction Equipment",
        "adoption_rate": 8.5,
        "market_size": 14.70,
        "notes": "Global electric construction equipment $13.63-15.77B. Electric excavators = 30% of segment.",
    },
    {
        "year": 2030,
        "region": "Global - Electric Construction Equipment",
        "adoption_rate": 22.0,
        "market_size": 34.72,
        "notes": "Projected $34.72B by 2030 (CAGR 20.5%). Electric cranes fastest at 25.2% CAGR.",
    },
    {
        "year": 2035,
        "region": "Global - Electric Construction Equipment",
        "adoption_rate": 38.0,
        "market_size": 116.08,
        "notes": "Projected $116.08B by 2035 (CAGR 22.09%) per Precedence Research (Feb 2026).",
    },
    # US Top LEED States
    {
        "year": 2025,
        "region": "United States - Massachusetts",
        "adoption_rate": 72.0,
        "market_size": 12.50,
        "notes": "#1 LEED state 2025. Life sciences campuses, strong state mandates. Stretch Energy Code.",
    },
    {
        "year": 2025,
        "region": "United States - California",
        "adoption_rate": 68.0,
        "market_size": 22.00,
        "notes": "#5 LEED state 2025. CALGreen mandatory. Net-zero mandate new homes. Buy Clean Act.",
    },
    {
        "year": 2025,
        "region": "United States - New York",
        "adoption_rate": 65.0,
        "market_size": 18.50,
        "notes": "All-Electric Buildings Act 2023. Local Law 97 emissions caps. $229B state clean energy.",
    },
    {
        "year": 2025,
        "region": "United States - Colorado",
        "adoption_rate": 58.0,
        "market_size": 7.20,
        "notes": "#3 LEED state 2025 (jumped 6 spots). GHG Pollution Reduction Roadmap.",
    },
]


# =============================================================================
# TECHNOLOGIES DATA
# Sources: research-report.md §1.5, market-analysis.md §1.3, competitive-benchmarking.md
# =============================================================================

TECHNOLOGIES = [
    # ---- CATEGORY: Solar Energy ----
    {
        "name": "On-Site Solar PV (BIPV)",
        "category": "Solar Energy",
        "feasibility_score": 88.0,
        "tco": 185000.00,
        "conventional_tco": 240000.00,
        "maturity_level": "Established",
        "description": "Building-integrated photovoltaic systems for on-site energy generation. Post-IRA, commercial solar adoption grew 12%. LEED credits available.",
        "cagr": 12.0,
    },
    {
        "name": "Rooftop Solar with Battery Storage (BESS)",
        "category": "Solar Energy",
        "feasibility_score": 82.0,
        "tco": 320000.00,
        "conventional_tco": 420000.00,
        "maturity_level": "Growing",
        "description": "Combined solar + battery energy storage for resilience and peak shaving. Mortenson ranked #1 ENR Battery Storage. ITC + IRA incentives apply.",
        "cagr": 18.5,
    },
    {
        "name": "Solar Power Purchase Agreement (PPA)",
        "category": "Solar Energy",
        "feasibility_score": 91.0,
        "tco": 45000.00,
        "conventional_tco": 68000.00,
        "maturity_level": "Mainstream",
        "description": "Off-balance-sheet solar via PPA. No upfront CapEx. Fixed electricity rates for 15-25 years. Widely available to mid-size firms.",
        "cagr": 14.2,
    },
    # ---- CATEGORY: Electric Construction Equipment ----
    {
        "name": "Electric Excavators",
        "category": "Electric Construction Equipment",
        "feasibility_score": 72.0,
        "tco": 780000.00,
        "conventional_tco": 620000.00,
        "maturity_level": "Growing",
        "description": "Battery-electric excavators. Largest segment at 30% of electric equipment market. Higher upfront cost offset by fuel savings and incentives. CAGR 20.5%.",
        "cagr": 20.5,
    },
    {
        "name": "Electric Tower Cranes",
        "category": "Electric Construction Equipment",
        "feasibility_score": 68.0,
        "tco": 1250000.00,
        "conventional_tco": 980000.00,
        "maturity_level": "Emerging",
        "description": "Electric-powered tower cranes — fastest growing electric equipment segment at 25.2% CAGR. Grid-connected operation eliminates diesel on dense urban sites.",
        "cagr": 25.2,
    },
    {
        "name": "Battery-Electric Light Vehicles & Forklifts",
        "category": "Electric Construction Equipment",
        "feasibility_score": 85.0,
        "tco": 68000.00,
        "conventional_tco": 72000.00,
        "maturity_level": "Established",
        "description": "Electric light-duty vehicles, forklifts, and telehandlers. Near-cost-parity with ICE equivalents. Lower operating costs, simpler maintenance.",
        "cagr": 15.8,
    },
    # ---- CATEGORY: Sustainable Building Materials ----
    {
        "name": "Mass Timber / Cross-Laminated Timber (CLT)",
        "category": "Sustainable Building Materials",
        "feasibility_score": 79.0,
        "tco": 2800000.00,
        "conventional_tco": 3100000.00,
        "maturity_level": "Growing",
        "description": "CLT and mass timber for mid/high-rise construction. Building codes updated for 18-story+. 25-30% faster construction, up to 90% waste reduction. Swinerton's Timberlab is market leader.",
        "cagr": 16.4,
    },
    {
        "name": "Near-Zero Carbon Cement",
        "category": "Sustainable Building Materials",
        "feasibility_score": 58.0,
        "tco": 185.00,
        "conventional_tco": 145.00,
        "maturity_level": "Emerging",
        "description": "Low-carbon cement alternatives (e.g., PozzoCEM Vite: 92% lower emissions). Buy Clean California Act drives demand. TCO is per ton. Still 20-30% cost premium in 2025.",
        "cagr": 24.0,
    },
    {
        "name": "Prefabrication & Modular Construction",
        "category": "Sustainable Building Materials",
        "feasibility_score": 84.0,
        "tco": 3500000.00,
        "conventional_tco": 4200000.00,
        "maturity_level": "Established",
        "description": "Off-site prefab modules reduce waste 50-90%, speed delivery 25-30%. Integrated with lean construction and BIM. Enables tighter quality control for green certifications.",
        "cagr": 7.5,
    },
    # ---- CATEGORY: Building Systems & AI ----
    {
        "name": "AI Building Management System (BMS)",
        "category": "Building Systems & AI",
        "feasibility_score": 87.0,
        "tco": 420000.00,
        "conventional_tco": 380000.00,
        "maturity_level": "Mainstream",
        "description": "AI-enabled BMS delivers 25% energy savings and 20% lower maintenance costs. Prerequisite for LEED O+M certification. Supports WELL Building Standard compliance.",
        "cagr": 19.8,
    },
    {
        "name": "Microgrid & Net Zero Energy Systems",
        "category": "Building Systems & AI",
        "feasibility_score": 70.0,
        "tco": 8500000.00,
        "conventional_tco": 6200000.00,
        "maturity_level": "Growing",
        "description": "Campus or site-level microgrid combining solar, storage, and smart controls. Hensel Phelps built Sunnyvale Civic Center: $192M LEED Platinum Net Zero Energy. Federal GSA demand growing.",
        "cagr": 22.3,
    },
    {
        "name": "Green Hydrogen Infrastructure",
        "category": "Building Systems & AI",
        "feasibility_score": 45.0,
        "tco": 12000000.00,
        "conventional_tco": 8500000.00,
        "maturity_level": "Emerging",
        "description": "Green hydrogen production and storage for construction fleet or building energy. Mortenson and Swinerton active. High upfront cost; emerging electrolyzer cost reductions expected by 2028.",
        "cagr": 35.0,
    },
]


# =============================================================================
# ROI SCENARIOS DATA
# Sources: research-report.md §2.4, green-contract-correlation.md §3
# Note: technology_id populated dynamically at seed time
# =============================================================================

ROI_SCENARIOS_BY_TECH_NAME = {
    "On-Site Solar PV (BIPV)": [
        {
            "scenario_type": "conservative",
            "payback_years": 9.0,
            "roi_percentage": 8.5,
            "assumptions": "Moderate sun exposure (4.5 peak sun hours/day). No IRA tax credits (non-qualifying project). Standard utility rates $0.12/kWh. 20-year asset life. 80% capacity factor.",
            "npv": 28000.00,
            "irr": 7.8,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 6.5,
            "roi_percentage": 15.2,
            "assumptions": "Good sun exposure (5.5 peak sun hours/day). IRA Investment Tax Credit (30%) applied. Grid electricity at $0.15/kWh. 25-year asset life. LEED credit value included.",
            "npv": 62000.00,
            "irr": 14.1,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 4.2,
            "roi_percentage": 24.8,
            "assumptions": "High sun exposure (6.5+ peak sun hours). Full IRA ITC (30%) + bonus credits (domestic content +10%). Utility rate $0.18/kWh with escalation. PPA arbitrage. LEED Gold achieved, winning $500K additional contracts.",
            "npv": 115000.00,
            "irr": 22.5,
        },
    ],
    "Rooftop Solar with Battery Storage (BESS)": [
        {
            "scenario_type": "conservative",
            "payback_years": 12.0,
            "roi_percentage": 6.2,
            "assumptions": "Battery replacement after 10 years ($80K). Grid charges $0.10/kWh. Demand charge reduction 15%. No IRA incentives applied. No grid export revenue.",
            "npv": 18500.00,
            "irr": 5.5,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 8.5,
            "roi_percentage": 12.8,
            "assumptions": "IRA Investment Tax Credit (30%) on both solar and storage. Demand charge reduction 30%. Virtual net metering where available. Battery degrades 2% annually. Resilience value $15K/yr for critical loads.",
            "npv": 55000.00,
            "irr": 11.9,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 5.8,
            "roi_percentage": 21.5,
            "assumptions": "Full IRA credits (30% ITC + 10% domestic content bonus). Peak shaving reduces demand charges 45%. Grid export revenue at retail rates. Battery costs declining 15%/yr by 2027. LEED Platinum achieved adding 3% contract premium.",
            "npv": 98000.00,
            "irr": 19.8,
        },
    ],
    "Solar Power Purchase Agreement (PPA)": [
        {
            "scenario_type": "conservative",
            "payback_years": 1.5,
            "roi_percentage": 5.0,
            "assumptions": "PPA rate $0.085/kWh vs. grid $0.12/kWh (29% savings). 15-year contract with 2% escalator. No upfront CapEx. Limited coverage (50% of load).",
            "npv": 12000.00,
            "irr": None,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 0.5,
            "roi_percentage": 11.5,
            "assumptions": "PPA rate $0.075/kWh vs. grid $0.15/kWh (50% savings). 20-year contract with 1.5% escalator. Full load coverage. LEED energy credit achieved.",
            "npv": 38000.00,
            "irr": None,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 0.1,
            "roi_percentage": 18.0,
            "assumptions": "PPA rate $0.065/kWh vs. grid $0.18/kWh (64% savings). 25-year contract. Green procurement marketing value $25K/yr. ESG reporting benefit. Multiple projects bundled for better PPA rate.",
            "npv": 72000.00,
            "irr": None,
        },
    ],
    "Electric Excavators": [
        {
            "scenario_type": "conservative",
            "payback_years": 8.5,
            "roi_percentage": 7.5,
            "assumptions": "Purchase price 25% premium over diesel. Diesel at $3.50/gal. Limited charging infrastructure on sites. Battery replacement at year 6 ($120K). Operator retraining costs $8K.",
            "npv": 22000.00,
            "irr": 6.8,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 6.0,
            "roi_percentage": 13.2,
            "assumptions": "Diesel savings $42K/yr at $4.00/gal. Lower maintenance costs (no engine oil, filters: -$8K/yr). IRA clean vehicle credits applied ($7,500 federal). Carbon credit revenue $5K/yr. Qualifies for California CARB zero-emission incentives.",
            "npv": 48000.00,
            "irr": 12.1,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 4.0,
            "roi_percentage": 22.8,
            "assumptions": "Diesel at $5.00/gal (+fuel cost escalation). California/NY urban site access restrictions favor electric. Avoided diesel generator costs $25K/yr. Green procurement preference wins $250K additional annual contracts. Battery tech improving: 20% cost reduction by 2027.",
            "npv": 89000.00,
            "irr": 21.0,
        },
    ],
    "Electric Tower Cranes": [
        {
            "scenario_type": "conservative",
            "payback_years": 10.0,
            "roi_percentage": 6.8,
            "assumptions": "30% cost premium over diesel. Urban site electricity at $0.18/kWh. Grid connection costs $45K. Limited market availability in Tier 2 cities. Maintenance savings 10%.",
            "npv": 35000.00,
            "irr": 6.2,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 7.5,
            "roi_percentage": 11.5,
            "assumptions": "Fuel savings 60% vs. diesel. Maintenance savings 20%. Urban emission zone compliance ($15K/yr avoided penalties). 3 projects/yr utilization. NYC Local Law 97 compliance value.",
            "npv": 68000.00,
            "irr": 10.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 5.5,
            "roi_percentage": 19.2,
            "assumptions": "Dense urban markets (NYC, LA, Chicago) where diesel is restricted. Crane rental premium for green projects +8%. IRA investment credits. Avoided idle diesel emissions fines. Carbon credits $8K/yr.",
            "npv": 125000.00,
            "irr": 17.8,
        },
    ],
    "Battery-Electric Light Vehicles & Forklifts": [
        {
            "scenario_type": "conservative",
            "payback_years": 4.5,
            "roi_percentage": 10.5,
            "assumptions": "Near cost-parity with ICE ($68K vs $72K). Fuel savings $4.2K/yr at $3.50/gal. Maintenance savings $2.5K/yr. Simple swap with existing fleet. 5-year asset life.",
            "npv": 14500.00,
            "irr": 9.8,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 3.0,
            "roi_percentage": 16.8,
            "assumptions": "Federal EV tax credit $7,500. Fuel savings $6K/yr at $4.50/gal. Reduced maintenance 35%. Job site air quality improvements ($3K/yr indoor productivity). Fleet of 10 vehicles.",
            "npv": 28500.00,
            "irr": 15.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 2.0,
            "roi_percentage": 28.5,
            "assumptions": "State rebates on top of federal (CA HVIP, NY Truck Voucher). Fuel at $5.50/gal. Indoor jobsite (warehouses, data centers) where diesel prohibited. Zero-emission fleet marketing wins green contracts. Fleet of 25 vehicles.",
            "npv": 58000.00,
            "irr": 26.2,
        },
    ],
    "Mass Timber / Cross-Laminated Timber (CLT)": [
        {
            "scenario_type": "conservative",
            "payback_years": 7.5,
            "roi_percentage": 9.2,
            "assumptions": "5% cost premium in early projects (design learning curve). Limited CLT suppliers (3 in NA). Structural engineer unfamiliarity adds $50K. Achieves LEED Certified but not higher levels.",
            "npv": 85000.00,
            "irr": 8.5,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 5.0,
            "roi_percentage": 14.5,
            "assumptions": "CLT at cost-parity or 2% premium vs. concrete for 6-12 story buildings. 20% faster construction schedule (saves $150K carrying costs). LEED Gold or WELL certification achieved. Embodied carbon reduction qualifies for Buy Clean incentives.",
            "npv": 185000.00,
            "irr": 13.2,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 3.5,
            "roi_percentage": 22.0,
            "assumptions": "Swinerton Timberlab model: dedicated CLT division creates premium pricing power. 30% faster delivery. Biophilic design premium rents +8%. LEED Platinum achievable. Replicable on 5+ projects/yr. State embodied carbon mandates (WA, CA) create competitive moat.",
            "npv": 380000.00,
            "irr": 20.5,
        },
    ],
    "Near-Zero Carbon Cement": [
        {
            "scenario_type": "conservative",
            "payback_years": 12.0,
            "roi_percentage": 4.5,
            "assumptions": "20% cost premium per ton vs. OPC. Limited regional availability. Spec approval delays 3 months. No carbon credit revenue yet. Achieves LEED Materials credits only.",
            "npv": 8500.00,
            "irr": 4.0,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 7.0,
            "roi_percentage": 11.8,
            "assumptions": "Buy Clean California Act preferred supplier status (+5% bid score). Carbon credits at $25/ton saved. 15% premium, declining to 8% by 2027. Qualifies for IRA domestic manufacturing incentives if US-sourced.",
            "npv": 32000.00,
            "irr": 10.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 4.5,
            "roi_percentage": 19.5,
            "assumptions": "Carbon price rises to $50/ton by 2028. Federal Buy Clean mandate expanded. Cement cost parity by 2027 (92% emissions reduction already demonstrated by PozzoCEM Vite). Required for net-zero building certifications premium contracts.",
            "npv": 78000.00,
            "irr": 18.0,
        },
    ],
    "Prefabrication & Modular Construction": [
        {
            "scenario_type": "conservative",
            "payback_years": 3.5,
            "roi_percentage": 12.0,
            "assumptions": "10% cost premium for factory setup. 15% schedule compression on first 2 projects. 50% waste reduction. Savings on site labor $80K/project. Initial 3 projects to recoup tooling investment.",
            "npv": 120000.00,
            "irr": 11.2,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 2.5,
            "roi_percentage": 19.5,
            "assumptions": "25% faster delivery saves $200K carrying costs/project. 70% waste reduction (LEED Materials credit). Predictable quality reduces rework 20%. Workforce efficiency +30%. 6 projects/yr at maturity.",
            "npv": 285000.00,
            "irr": 18.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 1.8,
            "roi_percentage": 32.5,
            "assumptions": "90% waste reduction enables LEED Platinum. Schedule compression 30% wins repeat clients. Affordable housing mandate premium for modular. 12 projects/yr at scale. Technology gap widens vs. competitors. ESG investor preference for modular contractors.",
            "npv": 580000.00,
            "irr": 30.8,
        },
    ],
    "AI Building Management System (BMS)": [
        {
            "scenario_type": "conservative",
            "payback_years": 5.0,
            "roi_percentage": 10.2,
            "assumptions": "System cost $280K for mid-size building. 15% energy savings (vs. 25% optimistic). Integration with existing legacy systems costs $85K extra. Maintenance contract $22K/yr.",
            "npv": 38000.00,
            "irr": 9.5,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 3.5,
            "roi_percentage": 17.8,
            "assumptions": "25% energy savings per TBRC data. 20% lower maintenance costs. LEED O+M certification achievable. Smart building premium rents +3-5%. Carbon reporting automation saves 120 hrs/yr staff time.",
            "npv": 88000.00,
            "irr": 16.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 2.5,
            "roi_percentage": 26.5,
            "assumptions": "30% energy savings + demand response revenue $18K/yr. WELL Gold certification adds 8% rent premium. Predictive maintenance reduces unplanned downtime 40%. NYC Local Law 97 compliance value $120K/yr avoided fines. Tenant retention improvement.",
            "npv": 165000.00,
            "irr": 24.8,
        },
    ],
    "Microgrid & Net Zero Energy Systems": [
        {
            "scenario_type": "conservative",
            "payback_years": 15.0,
            "roi_percentage": 5.5,
            "assumptions": "High upfront cost $8.5M. Complex permitting adds 18 months. Grid interconnection delays. Limited federal project opportunities without GSA experience. Conservative energy savings 20%.",
            "npv": 280000.00,
            "irr": 5.0,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 10.0,
            "roi_percentage": 12.8,
            "assumptions": "Federal GSA contracts (Net Zero Energy required). IRA Section 48 ITC (30%) on storage. Resilience value for critical facilities $250K/yr. LEED Platinum + Net Zero certification premium. Similar to Hensel Phelps Sunnyvale model ($192M).",
            "npv": 820000.00,
            "irr": 11.5,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 7.0,
            "roi_percentage": 21.0,
            "assumptions": "Carbon markets at $50/ton + SREC revenue. DOE Clean Energy Rule (new federal buildings 2024). Data center and healthcare demand surge. Export revenue from grid services (FERC Order 841). Hensel Phelps replication model: 5 microgrids/yr.",
            "npv": 2100000.00,
            "irr": 19.5,
        },
    ],
    "Green Hydrogen Infrastructure": [
        {
            "scenario_type": "conservative",
            "payback_years": 20.0,
            "roi_percentage": 3.2,
            "assumptions": "Very high upfront cost. Green hydrogen at $8-12/kg (vs. diesel energy equivalent $4/kg). Limited fueling infrastructure. Technology risk. Only viable at scale >$50M projects.",
            "npv": 85000.00,
            "irr": 2.8,
        },
        {
            "scenario_type": "moderate",
            "payback_years": 12.0,
            "roi_percentage": 9.5,
            "assumptions": "Green hydrogen cost declining to $4-6/kg by 2028. IRA Section 45V Production Tax Credit ($3/kg). Mortenson/Swinerton early-mover positioning. DOE Hydrogen Hubs funding. Avoiding diesel in emission-restricted zones.",
            "npv": 380000.00,
            "irr": 8.8,
        },
        {
            "scenario_type": "optimistic",
            "payback_years": 7.0,
            "roi_percentage": 18.5,
            "assumptions": "Green hydrogen at $2/kg by 2030 (DOE Hydrogen Shot target). Full IRA credits + state incentives. Proprietary fueling infrastructure creates competitive moat. Heavy equipment (long-haul cranes, mining) where battery-electric impractical. Carbon credit revenue.",
            "npv": 1200000.00,
            "irr": 17.2,
        },
    ],
}


# =============================================================================
# CASE STUDIES DATA
# Sources: competitive-benchmarking.md, research-report.md §2.2–2.4
# 6 firms: Mortenson, Gilbane, Suffolk, Swinerton, Hensel Phelps, Brasfield & Gorrie
# =============================================================================

CASE_STUDIES = [
    {
        "firm_name": "Mortenson Construction",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "Wind Energy Infrastructure (40 GW, 270+ projects)",
            "Solar Energy Construction (12+ GW, 100+ projects, 17 states)",
            "Battery Energy Storage Systems (BESS) — #1 ENR nationally",
            "Green Hydrogen Infrastructure (emerging)",
            "Electric Vehicle & Microgrid Infrastructure",
            "Center for Energy Performance (in-house energy consulting)",
            "Offsite Manufacturing & Prefabrication",
        ],
        "annual_revenue_m": 5500.00,
        "investment": 285.00,
        "outcomes": "40 GW wind capacity built across 270+ projects (30 years). 12+ GW solar across 100+ projects in 17 states. #1 ENR Battery Storage (2024). #2 ENR Wind. #8 Solar Power World 2025. Renewable energy represents significant and growing share of $5.5B annual revenue. Early mover advantage since 1995 wind entry built decades of expertise before market boom.",
        "timeline": "1995-present",
        "headquarters": "Minneapolis, MN",
        "strategy": "Dual strategy: (1) Build renewable energy infrastructure (wind, solar, storage, hydrogen) as a primary business line. (2) Integrate sustainability into operations via Center for Energy Performance. Early mover advantage (wind since 1995) created decades of expertise before market boom.",
        "enr_ranking": "#1 ENR Battery Storage 2024; #2 ENR Wind; #8 Solar Power World 2025",
        "net_zero_year": None,
    },
    {
        "firm_name": "Gilbane Building Company",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "LEED Certification Management (all levels)",
            "On-site Solar Arrays with BESS (38kW + battery storage)",
            "Recycled/Low-Carbon Materials (90% recycled steel: 6,000 tons on Baird Center)",
            "Stormwater Management (320,000-gallon StormTrap system)",
            "Smart Building Systems (LED + occupancy/daylight sensors)",
            "ORCA Food Digesters (438 tons/yr landfill diversion)",
            "Embodied Carbon Tracking (proprietary Environmental Planning Checklist)",
            "Supplier Relationship Management (SRM) for value chain carbon",
        ],
        "annual_revenue_m": 7300.00,
        "investment": 45.00,
        "outcomes": "92.3% waste diversion rate on California project (Next 150 Construction). Baird Center solar: 98,130 kWh annual savings (equivalent to 7.5M smartphone charges). #7 ENR Top 100 Green Contractors 2024 (up from #10 in 2023). #1 ENR Green Educational Facilities. 438 tons/yr food waste diverted from landfills. Net Zero Emissions by 2040 commitment (SBTi validated). 40% potable water reduction by 2040 target.",
        "timeline": "2008-present",
        "headquarters": "Providence, RI",
        "strategy": "Regenerative construction philosophy beyond net-zero. Three pillars: (1) Sustainability Action Plans required on every project. (2) SBTi Net Zero by 2040. (3) Third-party verification (EcoVadis, CDP, GRESB). Environmental Planning Checklists normalize sustainability as standard practice company-wide.",
        "enr_ranking": "#7 ENR Top 100 Green Contractors 2024; #1 Green Educational Facilities 2025",
        "net_zero_year": 2040,
    },
    {
        "firm_name": "Suffolk Construction",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "LEED & Green Certification Management (150+ certified projects)",
            "End-to-End Integrated Sustainability Group (dedicated team)",
            "Suffolk Technologies (venture arm investing in climate tech)",
            "Building Decarbonization (43M+ sq ft experience)",
            "Advanced Construction Analytics & Digital Twin",
            "Electric Equipment Integration",
        ],
        "annual_revenue_m": 5000.00,
        "investment": 180.00,
        "outcomes": "$2.6B annual green revenue (representing >50% of total revenue). 150+ LEED-certified projects in portfolio. 43M+ sq ft of building decarbonization experience. Top 10 ENR Green Contractor nationally (2023, 2024). Suffolk Technologies venture arm invests in climate tech startups creating future revenue streams. Dedicated Sustainability Group (vs. ad-hoc) signals market commitment and attracts ESG-conscious clients.",
        "timeline": "2018-present",
        "headquarters": "Boston, MA",
        "strategy": "End-to-end integrated sustainability with dedicated Sustainability Group. Venture arm (Suffolk Technologies) invests in climate tech. Focused on digital integration across entire project lifecycle. 'Intelligent Sustainability' — using technology to make green construction faster and cheaper.",
        "enr_ranking": "Top 10 ENR Green Contractor 2023, 2024",
        "net_zero_year": None,
    },
    {
        "firm_name": "Swinerton",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "Mass Timber / CLT (Timberlab division — national leader)",
            "Solar Energy Construction (200 MW solar farm built)",
            "Renewable Natural Gas Infrastructure (nationwide RNG projects)",
            "Swinerton Energy (dedicated renewable energy division)",
            "Contractor's Commitment Signatory (AGC sustainability pledge)",
            "Embodied Carbon Reduction Programs",
        ],
        "annual_revenue_m": 4500.00,
        "investment": 120.00,
        "outcomes": "Timberlab: America's leading mass timber specialty contractor with national reach. 200 MW solar farm constructed (demonstrating renewable energy construction at scale). Nationwide RNG infrastructure projects. Two separate business units (Timberlab, Swinerton Energy) generating new revenue streams from sustainability. Contractor's Commitment signatory demonstrating industry leadership.",
        "timeline": "2010-present",
        "headquarters": "San Francisco, CA",
        "strategy": "Product line diversification strategy: create separate business units from sustainability specialties. Timberlab = mass timber division (CLT, glulam). Swinerton Energy = renewable energy construction division. Model: Each green specialty becomes a standalone revenue stream rather than a cost center.",
        "enr_ranking": "N/A (specialty rankings in timber and renewables)",
        "net_zero_year": None,
    },
    {
        "firm_name": "Hensel Phelps",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "Microgrid Design & Construction (Net Zero Energy specialization)",
            "Federal LEED Gold/Platinum Construction (GSA mandate expertise)",
            "Net Zero Energy Building Systems",
            "Green Badger LEED Management Platform ($1M+ claimed savings)",
            "EV Infrastructure Integration",
            "Renewable Energy Integration on Federal Campuses",
        ],
        "annual_revenue_m": 7400.00,
        "investment": 35.00,
        "outcomes": "Sunnyvale Civic Center microgrid: $192M project, LEED Platinum, Net Zero Energy certified. $1M+ LEED management savings via Green Badger platform (vendor-sourced claim). Multiple federal sustainability awards. GSA mandates forced early competency development (LEED Gold required since 2010) that now differentiates in commercial markets. Multiple DOE and GSA sustainability awards.",
        "timeline": "2009-present",
        "headquarters": "Greeley, CO",
        "strategy": "Federal green building expertise with microgrid and Net Zero Energy specialization. Strategy: Federal GSA mandates (LEED Gold required) forced early competency development that now differentiates in commercial markets. Microgrid expertise is the key differentiator — complex, high-value federal projects that few competitors can execute.",
        "enr_ranking": "Multiple federal sustainability awards; microgrid specialty leader",
        "net_zero_year": None,
    },
    {
        "firm_name": "Brasfield & Gorrie",
        "size": "Large (>$500M)",
        "technologies_adopted": [
            "LEED Certification Portfolio (all levels — Certified through Platinum)",
            "Federal Green Building Compliance (GSA LEED Gold standard)",
            "Systematic Sustainability Upselling (Silver→Gold, Gold→Platinum)",
            "Waste Diversion Programs",
            "Energy Efficient MEP Systems",
            "Green Material Sourcing",
        ],
        "annual_revenue_m": 6500.00,
        "investment": 28.00,
        "outcomes": "Consistently exceeded LEED targets on federal projects: Silver→Gold, Gold→Platinum. Strong repeat client business driven by exceeding sustainability targets. Reputation for surpassing client green expectations creates competitive advantage in procurement. Southeastern market leader in sustainable construction. Federal work portfolio provides steady LEED revenue.",
        "timeline": "Early 2000s-present",
        "headquarters": "Birmingham, AL",
        "strategy": "LEED certification expertise through federal work with systematic upselling of sustainability levels. Key lesson: Exceeding client sustainability targets (delivering Gold when Silver was specified) builds reputation and wins repeat business. Strategy is primarily market-facing (certification expertise) rather than technology-focused.",
        "enr_ranking": "N/A (market reputation in Southeast US)",
        "net_zero_year": None,
    },
]


# =============================================================================
# REGULATORY INCENTIVES DATA
# Sources: research-report.md §1.4, market-analysis.md §3.2, green-contract-correlation.md §2
# =============================================================================

REGULATORY_INCENTIVES = [
    # Federal — IRA
    {
        "policy_name": "Inflation Reduction Act (IRA) — Clean Energy Tax Credits",
        "jurisdiction": "Federal",
        "type": "Tax Credit",
        "financial_impact": "$300B+ in clean energy tax incentives through 2032. Investment Tax Credit (ITC) 30% base for solar/storage. Production Tax Credit (PTC) for wind. Section 45V: $3/kg green hydrogen PTC.",
        "financial_impact_b": 300.00,
        "expiration": date(2032, 12, 31),
        "description": "Landmark climate legislation passed August 2022. Major catalyst: 12% boost in commercial solar adoption. 170,000+ clean energy manufacturing jobs created. Domestic content bonus (+10% ITC). Prevailing wage bonus (+10% ITC). Energy community bonus (+10% ITC). Political uncertainty: OBBBA may scale back some credits.",
        "is_active": "yes",
    },
    {
        "policy_name": "IRA — Section 48 Investment Tax Credit (Solar + Storage)",
        "jurisdiction": "Federal",
        "type": "Tax Credit",
        "financial_impact": "30% ITC base rate on solar PV and battery storage. 40% total with domestic content + energy community bonuses. Transferable credits (monetizable by non-tax-equity players).",
        "financial_impact_b": 85.00,
        "expiration": date(2032, 12, 31),
        "description": "Most impactful IRA provision for construction industry. Applies to: rooftop solar, ground-mount solar, BESS storage, microgrid components. Transferable and direct pay options reduce financing complexity. 10% bonus for domestic content (US-manufactured equipment). 10% bonus for Energy Community location (former fossil fuel regions).",
        "is_active": "yes",
    },
    {
        "policy_name": "IRA — Section 45V Green Hydrogen Production Tax Credit",
        "jurisdiction": "Federal",
        "type": "Tax Credit",
        "financial_impact": "Up to $3.00/kg for qualifying green hydrogen production. Lifecycle GHG analysis required (45VH2-GREET model). Stackable with Section 48 ITC for electrolyzer equipment.",
        "financial_impact_b": 8.00,
        "expiration": date(2032, 12, 31),
        "description": "Critical enabler for green hydrogen in construction fleet applications. Mortenson and Swinerton positioning for hydrogen infrastructure. DOE Hydrogen Hubs ($7B federal investment) create demand centers. Qualifying requires <0.45 kg CO2e per kg H2 produced.",
        "is_active": "yes",
    },
    # Federal — GSA / Building Standards
    {
        "policy_name": "GSA Federal Building LEED Gold Requirement",
        "jurisdiction": "Federal",
        "type": "Mandate",
        "financial_impact": "Access to federal construction market ($40B+/yr). Contractors without LEED expertise excluded from bids. Annual federal construction spending: $40B+ in public buildings.",
        "financial_impact_b": 40.00,
        "expiration": None,
        "description": "GSA has required LEED Gold (or equivalent) for all new federal buildings since 2010. Executive Order 14057 directs federal procurement toward net-zero buildings. DOE Clean Energy Rule (2024): new federal buildings must meet net-zero energy standards. 35+ states have adopted LEED or equivalent for public buildings.",
        "is_active": "yes",
    },
    {
        "policy_name": "Executive Order 14057 — Federal Sustainability",
        "jurisdiction": "Federal",
        "type": "Mandate",
        "financial_impact": "Directs $650B/yr in federal procurement toward net-zero buildings, clean vehicles, and sustainable products. Creates massive demand for green construction contractors.",
        "financial_impact_b": 650.00,
        "expiration": None,
        "description": "Signed December 2021. Directs federal agencies to: achieve net-zero emissions in buildings by 2045, purchase only zero-emission vehicles by 2035, and achieve 100% clean electricity by 2030. Creates sustained demand for green-certified construction contractors on federal work.",
        "is_active": "yes",
    },
    # California
    {
        "policy_name": "California CALGreen Code (Mandatory)",
        "jurisdiction": "California",
        "type": "Mandate",
        "financial_impact": "Mandatory compliance for all new California construction. Market access to California construction ($120B+/yr). Non-compliance = project rejection.",
        "financial_impact_b": 120.00,
        "expiration": None,
        "description": "California Green Building Standards Code — mandatory for all new construction and major renovations. Includes: mandatory EV charging infrastructure, water use reduction, construction waste management, energy efficiency beyond Title 24. CALGreen Tier 1 and Tier 2 optional levels exceed LEED standards.",
        "is_active": "yes",
    },
    {
        "policy_name": "California Buy Clean California Act",
        "jurisdiction": "California",
        "type": "Mandate",
        "financial_impact": "Preferred supplier status in state procurement (adds 5-10% bid score). Access to $15B+/yr state infrastructure spending. First-mover advantage in low-carbon materials market.",
        "financial_impact_b": 15.00,
        "expiration": None,
        "description": "Requires state agencies to consider embodied carbon in procurement of structural steel, rebar, flat glass, and mineral wool board insulation. Drives demand for near-zero carbon cement and steel. Expanding to more material categories. Washington State has similar legislation.",
        "is_active": "yes",
    },
    {
        "policy_name": "California Net-Zero New Homes Mandate (Title 24)",
        "jurisdiction": "California",
        "type": "Mandate",
        "financial_impact": "All new residential construction must include solar PV. Creates $3B+/yr solar rooftop installation market in California.",
        "financial_impact_b": 3.00,
        "expiration": None,
        "description": "Effective January 2020 (Title 24, Part 6 energy code update). All new single-family and low-rise multifamily homes must include solar photovoltaic systems. Expanding to commercial in progressive code updates. Positions solar-capable contractors for residential market growth.",
        "is_active": "yes",
    },
    # New York
    {
        "policy_name": "New York All-Electric Buildings Act (2023)",
        "jurisdiction": "New York",
        "type": "Mandate",
        "financial_impact": "All new buildings must be all-electric (no gas hookups). Creates demand for EV infrastructure, heat pumps, and electric construction expertise. $229B state clean energy investment over 10 years.",
        "financial_impact_b": 229.00,
        "expiration": None,
        "description": "Effective December 2023. New buildings under 7 stories must be all-electric starting 2026; larger buildings by 2029. Eliminates natural gas in new construction. Drives demand for: electric HVAC, heat pumps, EV charging infrastructure, smart electrical systems. NYC already has Local Law 97 emissions caps for existing buildings >25K sqft.",
        "is_active": "yes",
    },
    {
        "policy_name": "NYC Local Law 97 — Building Emissions Caps",
        "jurisdiction": "New York City",
        "type": "Mandate",
        "financial_impact": "Buildings >25,000 sqft face penalties of $268/ton CO2 above caps. Retrofit market estimated $4B+ by 2030. Green contractors with energy retrofit expertise command premium.",
        "financial_impact_b": 4.00,
        "expiration": None,
        "description": "Part of NYC Climate Mobilization Act. Carbon emission caps for buildings >25,000 sqft beginning 2024. Phase 1 (2024-2029) and Phase 2 (2030+) with progressively tighter caps. Building owners must retrofit or pay penalties up to $268/ton CO2 excess. Creates massive retrofit market for green-certified contractors.",
        "is_active": "yes",
    },
    # Canada Federal
    {
        "policy_name": "Canada Green Buildings Strategy (CGBS)",
        "jurisdiction": "Canada Federal",
        "type": "Standard",
        "financial_impact": "Part of Canada 2030 Emissions Reduction Plan. $6.3B Canada Greener Homes Initiative. National building code modernization driving $45B+ construction market transition.",
        "financial_impact_b": 6.30,
        "expiration": date(2050, 12, 31),
        "description": "Released July 2024. Targets building decarbonization by 2050 through: modernized national model building codes, Canada Greener Homes Initiative retrofit support, zero-carbon-ready building code requirements, heat pump deployment incentives. BC Energy Step Code leads provinces. Positions green-certified contractors for growing Canadian market.",
        "is_active": "yes",
    },
    # Colorado
    {
        "policy_name": "Colorado GHG Pollution Reduction Roadmap",
        "jurisdiction": "Colorado",
        "type": "Standard",
        "financial_impact": "Colorado jumped 6 spots to #3 LEED state in 2025. Rapidly expanding green building market. Building performance standards drive retrofit demand.",
        "financial_impact_b": 2.80,
        "expiration": None,
        "description": "Comprehensive GHG reduction plan including building performance standards. Colorado's rapid rise in LEED rankings (6 spots to #3 in 2025) reflects policy-driven adoption. Commercial building benchmarking and performance standards. Energy code updates aligned with net-zero goals.",
        "is_active": "yes",
    },
    # IRA Clean Vehicle
    {
        "policy_name": "IRA Section 30D — Clean Vehicle Tax Credit",
        "jurisdiction": "Federal",
        "type": "Tax Credit",
        "financial_impact": "$7,500 federal tax credit per qualifying electric vehicle. Commercial vehicle (45W) credit up to $40,000 for heavy trucks. Applies to electric construction vehicles and fleet.",
        "financial_impact_b": 3.90,
        "expiration": date(2032, 12, 31),
        "description": "Applies to commercial fleets including construction companies purchasing electric vehicles. Section 45W provides Commercial Clean Vehicle Credit: 15-30% of cost for qualifying vehicles, up to $7,500 for light vehicles and $40,000 for heavy vehicles. California HVIP and NY Truck Voucher programs provide additional state-level incentives.",
        "is_active": "yes",
    },
]


# =============================================================================
# GREEN CONTRACTS DATA
# Sources: green-contract-correlation.md §2, §3
# =============================================================================

GREEN_CONTRACTS = [
    {
        "certification_type": "No Green Certification (Baseline)",
        "win_rate_premium": 0.0,
        "contract_value_premium": 0.0,
        "construction_cost_premium": 0.0,
        "operating_cost_savings": 0.0,
        "asset_value_increase": 0.0,
        "min_project_size_m": None,
        "data_source": "Baseline for comparison. No certification. Effectively excluded from 71% of projects >$50M per USGBC data.",
    },
    {
        "certification_type": "LEED Certified",
        "win_rate_premium": 15.0,
        "contract_value_premium": 1.5,
        "construction_cost_premium": 1.0,
        "operating_cost_savings": 10.5,
        "asset_value_increase": 4.0,
        "min_project_size_m": 5.00,
        "data_source": "USGBC/CBRE data. LEED referenced in 71% of project specs >$50M. Certified level often at cost parity with conventional. 1st year operating cost savings 10.5% (World Green Building Council).",
    },
    {
        "certification_type": "LEED Silver",
        "win_rate_premium": 22.0,
        "contract_value_premium": 2.5,
        "construction_cost_premium": 1.5,
        "operating_cost_savings": 13.0,
        "asset_value_increase": 6.0,
        "min_project_size_m": 10.00,
        "data_source": "World Bank and Whole Building Design Guide (Kats study). 1.8-2% average cost premium for Certified/Silver. Federal GSA requires minimum LEED Gold but Silver competitive for state mandates (35+ states).",
    },
    {
        "certification_type": "LEED Gold",
        "win_rate_premium": 35.0,
        "contract_value_premium": 4.0,
        "construction_cost_premium": 3.0,
        "operating_cost_savings": 16.9,
        "asset_value_increase": 9.0,
        "min_project_size_m": 25.00,
        "data_source": "CBRE 2022 study (20,000 buildings). 31% higher rents vs non-certified nationally. 4% direct rent premium LEED Platinum. 9%+ asset value increase. 16.9% lower operating costs over 5 years. Federal GSA minimum standard since 2010.",
    },
    {
        "certification_type": "LEED Platinum",
        "win_rate_premium": 48.0,
        "contract_value_premium": 8.0,
        "construction_cost_premium": 10.0,
        "operating_cost_savings": 24.5,
        "asset_value_increase": 14.0,
        "min_project_size_m": 50.00,
        "data_source": "CBRE 2022: LEED Platinum ~4% direct rent premium over non-LEED. 10-12% construction premium at high end. WELL Building complement achieves 8%+ rent premium. Vornado: first to achieve 100% LEED across 26.1M sqft portfolio (2025). Empire State Building: first NYC LEED v5 Platinum.",
    },
    {
        "certification_type": "WELL Building Standard (Gold/Platinum)",
        "win_rate_premium": 28.0,
        "contract_value_premium": 5.5,
        "construction_cost_premium": 4.5,
        "operating_cost_savings": 12.0,
        "asset_value_increase": 8.0,
        "min_project_size_m": 20.00,
        "data_source": "IWBI data. 25,000+ WELL AP professionals worldwide. Growing complement to LEED (not replacement). Occupant health focus drives corporate tenant demand. 79% increase in LEED O+M certifications post-COVID across 215M sqft — WELL converging trend.",
    },
    {
        "certification_type": "Living Building Challenge (Full Certification)",
        "win_rate_premium": 55.0,
        "contract_value_premium": 12.0,
        "construction_cost_premium": 20.0,
        "operating_cost_savings": 35.0,
        "asset_value_increase": 18.0,
        "min_project_size_m": 100.00,
        "data_source": "ILFI data. Most rigorous certification: net-zero energy, water, materials Red List. ~130 fully certified globally. Very rare; extreme competitive moat. 12 months actual performance data required. Primarily for institutional clients (universities, government).",
    },
    {
        "certification_type": "ENERGY STAR Certified Building",
        "win_rate_premium": 10.0,
        "contract_value_premium": 1.8,
        "construction_cost_premium": 0.5,
        "operating_cost_savings": 8.0,
        "asset_value_increase": 3.5,
        "min_project_size_m": 2.00,
        "data_source": "EPA ENERGY STAR data. 35,000+ certified buildings in US. Score ≥75 required. Free benchmarking (Portfolio Manager). Lower bar than LEED but widely recognized. Often combined with LEED. Strong in office, retail, hospitality markets.",
    },
    {
        "certification_type": "Green Globes (3-4 Globes)",
        "win_rate_premium": 12.0,
        "contract_value_premium": 2.0,
        "construction_cost_premium": 1.5,
        "operating_cost_savings": 11.0,
        "asset_value_increase": 4.5,
        "min_project_size_m": 5.00,
        "data_source": "GBI/GSA data. Accepted by GSA as LEED equivalent for federal buildings. Simpler than LEED; lower administrative burden. Preferred in some Canadian markets. Competitive alternative to LEED for federal and institutional work.",
    },
    {
        "certification_type": "B Corp Certification (Company-Level)",
        "win_rate_premium": 8.0,
        "contract_value_premium": 3.0,
        "construction_cost_premium": 0.0,
        "operating_cost_savings": 5.0,
        "asset_value_increase": 12.0,
        "min_project_size_m": None,
        "data_source": "B Lab data. Company-level certification (not project). Very few construction B Corps (Earth Bound Homes CA, Birdsmouth Design-Build OR). Emerging ESG investor differentiator. $1,000-$50,000/yr based on revenue. Recertified every 3 years.",
    },
]


# =============================================================================
# SEED FUNCTION
# =============================================================================

def seed_database(session: Session) -> dict:
    """
    Seed all tables. Returns dict with counts of inserted records.
    Idempotent: clears existing data before inserting.
    """
    print("Clearing existing data...")
    session.execute(text("DELETE FROM roi_scenarios"))
    session.execute(text("DELETE FROM green_contracts"))
    session.execute(text("DELETE FROM regulatory_incentives"))
    session.execute(text("DELETE FROM case_studies"))
    session.execute(text("DELETE FROM technologies"))
    session.execute(text("DELETE FROM market_trends"))
    session.flush()

    # ---- market_trends ----
    print(f"Seeding {len(MARKET_TRENDS)} market trends...")
    trend_objects = [MarketTrend(**t) for t in MARKET_TRENDS]
    session.add_all(trend_objects)
    session.flush()

    # ---- technologies ----
    print(f"Seeding {len(TECHNOLOGIES)} technologies...")
    tech_objects = [Technology(**t) for t in TECHNOLOGIES]
    session.add_all(tech_objects)
    session.flush()

    # Build name → id map for ROI scenarios
    tech_id_map = {t.name: t.id for t in tech_objects}

    # ---- roi_scenarios ----
    roi_count = 0
    roi_objects = []
    print("Seeding ROI scenarios...")
    for tech_name, scenarios in ROI_SCENARIOS_BY_TECH_NAME.items():
        tech_id = tech_id_map.get(tech_name)
        if tech_id is None:
            print(f"  WARNING: Technology '{tech_name}' not found, skipping ROI scenarios")
            continue
        for scenario in scenarios:
            roi_objects.append(ROIScenario(technology_id=tech_id, **scenario))
            roi_count += 1
    session.add_all(roi_objects)
    session.flush()

    # ---- case_studies ----
    print(f"Seeding {len(CASE_STUDIES)} case studies...")
    study_objects = [CaseStudy(**cs) for cs in CASE_STUDIES]
    session.add_all(study_objects)
    session.flush()

    # ---- regulatory_incentives ----
    print(f"Seeding {len(REGULATORY_INCENTIVES)} regulatory incentives...")
    incentive_objects = [RegulatoryIncentive(**ri) for ri in REGULATORY_INCENTIVES]
    session.add_all(incentive_objects)
    session.flush()

    # ---- green_contracts ----
    print(f"Seeding {len(GREEN_CONTRACTS)} green contract records...")
    contract_objects = [GreenContract(**gc) for gc in GREEN_CONTRACTS]
    session.add_all(contract_objects)
    session.flush()

    session.commit()

    counts = {
        "market_trends": len(trend_objects),
        "technologies": len(tech_objects),
        "roi_scenarios": roi_count,
        "case_studies": len(study_objects),
        "regulatory_incentives": len(incentive_objects),
        "green_contracts": len(contract_objects),
    }
    return counts


def main():
    engine = get_engine()
    with Session(engine) as session:
        counts = seed_database(session)

    print("\n=== Seed Complete ===")
    for table, count in counts.items():
        print(f"  {table}: {count} rows")
    print("====================\n")


if __name__ == "__main__":
    main()
