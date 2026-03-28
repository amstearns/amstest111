// TypeScript interfaces for the Renewable Energy Executive Dashboard

export interface MarketMetric {
  readonly label: string;
  readonly value: string;
  readonly unit?: string;
  readonly change?: number;
  readonly changeLabel?: string;
  readonly trend?: "up" | "down" | "neutral";
}

export interface MarketTrendDataPoint {
  year: number;
  value: number;
  label?: string;
}

export interface RegionalAdoptionData {
  state: string;
  adoptionRate: number;
  leedProjects?: number;
  region: "Northeast" | "Southeast" | "Midwest" | "West" | "Southwest";
}

export interface AdoptionByFirmSize {
  firmSize: string;
  revenueRange: string;
  esgPrograms: number;
  leedExperience: number;
  electricEquipment: number;
}

export interface TechnologyProfile {
  id: string;
  name: string;
  category: "Electric Equipment" | "On-site Solar" | "Green Building Systems";
  feasibilityScore: number;
  tcoSavingsMin: number;
  tcoSavingsMax: number;
  tcoSavingsPeriod?: string;
  implementationTimelineMin: number;
  implementationTimelineMax: number;
  paybackPeriodMin: number;
  paybackPeriodMax: number;
  description: string;
  keyBenefits: string[];
  challenges: string[];
  marketSize?: string;
  cagr?: number;
}

export interface FinancialScenario {
  label: "Conservative" | "Moderate" | "Aggressive";
  investmentAmount: number;
  incentiveUtilization: number;
  contractPremium: number;
  roi: number;
  paybackPeriod: number;
  npv?: number;
  annualSavings?: number;
}

export interface CaseStudy {
  id: string;
  company: string;
  firmSize: "Small" | "Mid-Size" | "Mid-Large" | "Large";
  technologies: string[];
  annualRevenue: string;
  keyMetrics: {
    label: string;
    value: string;
  }[];
  highlights: string[];
  enrRanking?: string;
}

export interface RegulatoryIncentive {
  id: string;
  name: string;
  type: "Federal Tax Credit" | "Federal Deduction" | "Federal Mandate" | "State Mandate" | "State Incentive";
  value: string;
  valueNumeric?: number;
  eligibility: string;
  description: string;
  effectiveDate?: string;
  expirationDate?: string;
  financialImpact: string;
}

export interface DashboardSummary {
  marketMetrics: MarketMetric[];
  strategicRecommendations: string[];
  lastUpdated: string;
}

export interface ROICalculatorInputs {
  investmentAmount: number;
  incentiveUtilization: number;
  contractPremium: number;
  projectDuration: number;
}

export interface ROICalculatorResult {
  paybackPeriod: number;
  roi: number;
  netSavings: number;
  annualSavings: number;
  incentiveSavings: number;
}

export interface MarketData {
  trends: MarketTrendDataPoint[];
  regionalAdoption: RegionalAdoptionData[];
  adoptionByFirmSize: AdoptionByFirmSize[];
  projections: MarketTrendDataPoint[];
}

export interface TechnologyData {
  technologies: TechnologyProfile[];
}

export interface FinancialData {
  scenarios: FinancialScenario[];
  defaultInputs: ROICalculatorInputs;
}

export interface BenchmarkData {
  caseStudies: CaseStudy[];
}

export interface RegulatoryData {
  incentives: RegulatoryIncentive[];
}
