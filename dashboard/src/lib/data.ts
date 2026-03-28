// Mock data for the Renewable Energy Executive Dashboard
// Based on research into North American construction industry green adoption

import type {
  MarketData,
  TechnologyData,
  FinancialData,
  BenchmarkData,
  RegulatoryData,
  DashboardSummary,
} from "./types";

export const MARKET_DATA: MarketData = {
  trends: [
    { year: 2021, value: 45, label: "$45B" },
    { year: 2022, value: 85, label: "$85B" },
    { year: 2023, value: 153, label: "$153B (IRA)" },
    { year: 2024, value: 200, label: "$200B" },
    { year: 2025, value: 218, label: "$218B" },
  ],
  projections: [
    { year: 2025, value: 218, label: "$218B" },
    { year: 2026, value: 262, label: "$262B" },
    { year: 2027, value: 315, label: "$315B" },
    { year: 2028, value: 379, label: "$379B" },
    { year: 2029, value: 456, label: "$456B" },
    { year: 2030, value: 548, label: "$548B" },
    { year: 2031, value: 659, label: "$659B" },
    { year: 2032, value: 793, label: "$793B" },
    { year: 2033, value: 953, label: "$953B" },
    { year: 2034, value: 1374, label: "$1,374B" },
  ],
  regionalAdoption: [
    { state: "Massachusetts", adoptionRate: 92, leedProjects: 1247, region: "Northeast" },
    { state: "Illinois", adoptionRate: 88, leedProjects: 1089, region: "Midwest" },
    { state: "Colorado", adoptionRate: 85, leedProjects: 934, region: "West" },
    { state: "Virginia", adoptionRate: 84, leedProjects: 1102, region: "Southeast" },
    { state: "California", adoptionRate: 83, leedProjects: 2341, region: "West" },
    { state: "New York", adoptionRate: 81, leedProjects: 1876, region: "Northeast" },
    { state: "Georgia", adoptionRate: 78, leedProjects: 823, region: "Southeast" },
    { state: "Texas", adoptionRate: 71, leedProjects: 1432, region: "Southwest" },
    { state: "Washington", adoptionRate: 79, leedProjects: 712, region: "West" },
    { state: "Oregon", adoptionRate: 76, leedProjects: 534, region: "West" },
  ],
  adoptionByFirmSize: [
    {
      firmSize: "Large",
      revenueRange: ">$500M",
      esgPrograms: 80,
      leedExperience: 82,
      electricEquipment: 8,
    },
    {
      firmSize: "Mid-Size",
      revenueRange: "$50M–$500M",
      esgPrograms: 48,
      leedExperience: 43,
      electricEquipment: 2,
    },
    {
      firmSize: "Small",
      revenueRange: "<$50M",
      esgPrograms: 20,
      leedExperience: 15,
      electricEquipment: 1,
    },
  ],
};

export const TECHNOLOGY_DATA: TechnologyData = {
  technologies: [
    {
      id: "electric-equipment",
      name: "Electric Construction Equipment",
      category: "Electric Equipment",
      feasibilityScore: 72,
      tcoSavingsMin: 15,
      tcoSavingsMax: 20,
      implementationTimelineMin: 18,
      implementationTimelineMax: 36,
      paybackPeriodMin: 4,
      paybackPeriodMax: 6,
      marketSize: "$13.63B (2025) → $34.72B (2030)",
      cagr: 20.5,
      description:
        "Transition from diesel to electric excavators, cranes, loaders, and compact equipment. Reduces site emissions and fuel costs with growing OEM options.",
      keyBenefits: [
        "20.5% CAGR market growth through 2030",
        "15–20% TCO savings over lifecycle",
        "Reduced on-site emissions for LEED points",
        "Lower fuel and maintenance costs",
        "Eligibility for IRA Section 48C credits",
      ],
      challenges: [
        "Higher upfront capital cost",
        "Charging infrastructure investment required",
        "Limited model availability for heavy equipment",
        "Range and battery performance in cold climates",
      ],
    },
    {
      id: "onsite-solar",
      name: "On-Site Solar Generation",
      category: "On-site Solar",
      feasibilityScore: 85,
      tcoSavingsMin: 25,
      tcoSavingsMax: 35,
      implementationTimelineMin: 6,
      implementationTimelineMax: 18,
      paybackPeriodMin: 5,
      paybackPeriodMax: 8,
      description:
        "Rooftop and ground-mounted solar PV for offices, yards, and construction trailers. Enables net-zero construction sites and powers electric equipment.",
      keyBenefits: [
        "25–35% energy cost reduction",
        "30% ITC under IRA Section 48",
        "Powers electric equipment on-site",
        "Enhances LEED certification scoring",
        "Positive brand differentiation",
      ],
      challenges: [
        "Site-specific feasibility varies by geography",
        "Permitting and grid interconnection delays",
        "Initial capital outlay before incentives",
        "Storage required for 24/7 reliability",
      ],
    },
    {
      id: "green-building-systems",
      name: "Green Building Systems",
      category: "Green Building Systems",
      feasibilityScore: 90,
      tcoSavingsMin: 16,
      tcoSavingsMax: 17,
      tcoSavingsPeriod: "over 5 years",
      implementationTimelineMin: 12,
      implementationTimelineMax: 24,
      paybackPeriodMin: 3,
      paybackPeriodMax: 7,
      description:
        "HVAC optimization, LED lighting, smart building controls, high-performance envelopes, and water efficiency systems targeting LEED Gold/Platinum certification.",
      keyBenefits: [
        "16.9% TCO savings over 5 years",
        "31% gross LEED rent premium (4% net)",
        "GSA and federal contract eligibility",
        "35+ state mandate compliance",
        "$5.65/sqft 179D deduction eligibility",
      ],
      challenges: [
        "Complexity of integrating multiple systems",
        "Requires specialized subcontractor expertise",
        "Commissioning and certification timeline",
        "Owner education and buy-in required",
      ],
    },
  ],
};

export const FINANCIAL_DATA: FinancialData = {
  scenarios: [
    {
      label: "Conservative",
      investmentAmount: 5000000,
      incentiveUtilization: 0.5,
      contractPremium: 0.02,
      roi: 12,
      paybackPeriod: 7.2,
      annualSavings: 600000,
    },
    {
      label: "Moderate",
      investmentAmount: 5000000,
      incentiveUtilization: 0.75,
      contractPremium: 0.04,
      roi: 21,
      paybackPeriod: 5.8,
      annualSavings: 1050000,
    },
    {
      label: "Aggressive",
      investmentAmount: 5000000,
      incentiveUtilization: 1.0,
      contractPremium: 0.06,
      roi: 31,
      paybackPeriod: 4.1,
      annualSavings: 1550000,
    },
  ],
  defaultInputs: {
    investmentAmount: 5000000,
    incentiveUtilization: 0.75,
    contractPremium: 0.04,
    projectDuration: 10,
  },
};

export const BENCHMARK_DATA: BenchmarkData = {
  caseStudies: [
    {
      id: "mortenson",
      company: "Mortenson Construction",
      firmSize: "Large",
      technologies: ["Wind", "Solar", "Battery Storage"],
      annualRevenue: "$5.5B",
      keyMetrics: [
        { label: "Wind Capacity Built", value: "40+ GW" },
        { label: "Solar Capacity Built", value: "12+ GW" },
        { label: "ENR Ranking", value: "#1 Battery Storage" },
      ],
      highlights: [
        "ENR Top Battery Storage Contractor 2024",
        "Dedicated renewable energy division",
        "Integrated clean energy design-build capability",
      ],
    },
    {
      id: "gilbane",
      company: "Gilbane Building Company",
      firmSize: "Large",
      technologies: ["LEED", "ESG Programs"],
      annualRevenue: "$7.3B",
      keyMetrics: [
        { label: "ENR Green Ranking", value: "#7 (2024)" },
        { label: "LEED Projects", value: "500+" },
        { label: "Sustainability Rating", value: "A" },
      ],
      highlights: [
        "ENR Top 10 Green Contractor 2024",
        "Company-wide ESG reporting framework",
        "Target net-zero operations by 2040",
      ],
    },
    {
      id: "suffolk",
      company: "Suffolk Construction",
      firmSize: "Large",
      technologies: ["Carbon Neutral", "On-site Solar"],
      annualRevenue: "$5.0B",
      keyMetrics: [
        { label: "Green Revenue", value: "$2.6B" },
        { label: "Carbon Reduction", value: "35%" },
        { label: "Solar Installations", value: "150+" },
      ],
      highlights: [
        "$2.6B in green building revenue annually",
        "Carbon neutral construction target 2030",
        "Proprietary sustainability tracking platform",
      ],
    },
    {
      id: "swinerton",
      company: "Swinerton",
      firmSize: "Mid-Large",
      technologies: ["Solar", "Electric Equipment", "ESG"],
      annualRevenue: "$4.5B",
      keyMetrics: [
        { label: "SBTi Status", value: "Committed" },
        { label: "Renewable Projects", value: "200+" },
        { label: "Electric Fleet %", value: "12%" },
      ],
      highlights: [
        "Science Based Targets Initiative committed",
        "Leading electric equipment fleet adoption",
        "Swinerton Renewable Energy division",
      ],
    },
    {
      id: "hensel-phelps",
      company: "Hensel Phelps",
      firmSize: "Large",
      technologies: ["Operations Efficiency", "Smart Building Tech"],
      annualRevenue: "$5.4B",
      keyMetrics: [
        { label: "LEED Cost Savings", value: "$1M+" },
        { label: "Energy Reduction", value: "30%" },
        { label: "LEED Projects", value: "300+" },
      ],
      highlights: [
        "Over $1M in documented LEED cost savings",
        "Proprietary energy monitoring systems",
        "Federal green building preferred contractor",
      ],
    },
    {
      id: "brasfield-gorrie",
      company: "Brasfield & Gorrie",
      firmSize: "Large",
      technologies: ["LEED", "Sustainable Design"],
      annualRevenue: "$3.8B",
      keyMetrics: [
        { label: "LEED Projects", value: "150+" },
        { label: "LEED Sqft", value: "50M+" },
        { label: "Green Revenue %", value: "28%" },
      ],
      highlights: [
        "150+ LEED certified projects delivered",
        "In-house LEED AP professionals",
        "Southeast regional market leader in green",
      ],
    },
  ],
};

export const REGULATORY_DATA: RegulatoryData = {
  incentives: [
    {
      id: "ira-48c",
      name: "IRA Section 48C",
      type: "Federal Tax Credit",
      value: "30% Investment Tax Credit",
      valueNumeric: 30,
      eligibility: "Clean energy manufacturing and industrial facilities",
      description:
        "Advanced Energy Project Credit for qualifying clean energy manufacturing, recycling, and industrial decarbonization projects. Expanded by IRA 2022.",
      effectiveDate: "2022",
      financialImpact: "Up to 30% of capital investment; $10B+ allocated under IRA",
    },
    {
      id: "ira-45l",
      name: "IRA Section 45L",
      type: "Federal Tax Credit",
      value: "$2,500–$5,000 per unit",
      valueNumeric: 5000,
      eligibility: "Energy-efficient residential construction",
      description:
        "New Energy Efficient Home Credit for builders of energy-efficient homes meeting ENERGY STAR or Zero Energy Ready Home standards.",
      effectiveDate: "2023",
      expirationDate: "2032",
      financialImpact: "$2,500 per ENERGY STAR unit; $5,000 per Zero Energy Ready unit",
    },
    {
      id: "179d",
      name: "179D Commercial Buildings Deduction",
      type: "Federal Deduction",
      value: "Up to $5.65/sqft",
      valueNumeric: 5.65,
      eligibility: "Commercial building energy efficiency improvements",
      description:
        "Immediate expensing deduction for energy-efficient commercial building improvements. Enhanced by IRA 2022 to $5.65/sqft maximum for highest performers.",
      effectiveDate: "2023",
      financialImpact: "Up to $5.65/sqft — significant for large commercial projects",
    },
    {
      id: "leed-federal",
      name: "LEED Gold Federal Mandate",
      type: "Federal Mandate",
      value: "Required for federal contracts",
      eligibility: "All GSA-funded construction projects",
      description:
        "GSA mandate requiring LEED Gold certification for all new federal buildings since 2010. Creates reliable pipeline of green contract opportunities.",
      effectiveDate: "2010",
      financialImpact: "Access to $70B+ annual federal construction market",
    },
    {
      id: "state-mandates",
      name: "State Green Building Mandates",
      type: "State Mandate",
      value: "35+ states with requirements",
      eligibility: "State-funded construction projects",
      description:
        "Over 35 states have adopted LEED or equivalent green building requirements for state-funded projects, creating a substantial market opportunity.",
      financialImpact: "Substantial state contract pipeline across 35+ jurisdictions",
    },
    {
      id: "ira-48",
      name: "IRA Section 48 Solar ITC",
      type: "Federal Tax Credit",
      value: "30% Investment Tax Credit",
      valueNumeric: 30,
      eligibility: "Commercial solar PV installations",
      description:
        "Solar Investment Tax Credit for commercial and industrial solar installations. Extended through 2032 under IRA with bonus credits for domestic content.",
      effectiveDate: "2022",
      expirationDate: "2032",
      financialImpact: "30% of solar installation cost; 40%+ with domestic content bonus",
    },
  ],
};

export const DASHBOARD_SUMMARY: DashboardSummary = {
  marketMetrics: [
    {
      label: "Global Green Building Market",
      value: "$618.58B",
      unit: "2025 Estimate",
      trend: "up",
      change: 9.29,
      changeLabel: "CAGR to 2034",
    },
    {
      label: "North America Market Share",
      value: "$153.87B",
      unit: "35% of global",
      trend: "up",
      change: 8.5,
      changeLabel: "YoY Growth",
    },
    {
      label: "Average Payback Period",
      value: "5.8 yrs",
      unit: "Green investments",
      trend: "down",
      change: -0.4,
      changeLabel: "vs. prior year",
    },
    {
      label: "Green Contract Premium",
      value: "4% Net",
      unit: "31% gross LEED",
      trend: "up",
      change: 0.5,
      changeLabel: "vs. prior year",
    },
    {
      label: "ROI Range",
      value: "12–31%",
      unit: "Depending on scenario",
      trend: "up",
    },
    {
      label: "Electric Equipment Market",
      value: "$13.63B",
      unit: "2025; 20.5% CAGR",
      trend: "up",
      change: 20.5,
      changeLabel: "CAGR to 2030",
    },
  ],
  strategicRecommendations: [
    "Prioritize on-site solar adoption (85/100 feasibility score) as highest ROI entry point with fastest implementation timeline",
    "Develop LEED certification capability to access $70B+ federal contract pipeline requiring LEED Gold minimum",
    "Pilot electric equipment on 1-2 projects to build operational expertise ahead of market inflection",
    "Establish ESG reporting framework to meet growing client RFP requirements (80% of large clients now require ESG data)",
    "Leverage IRA incentives immediately — 30% ITC and 179D deductions dramatically improve project economics",
    "Target mid-size firm segment for competitive differentiation, as only 48% have ESG programs vs. 80% of large firms",
  ],
  lastUpdated: "2025-Q1",
};
