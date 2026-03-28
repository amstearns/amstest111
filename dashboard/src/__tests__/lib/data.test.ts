import {
  MARKET_DATA,
  FINANCIAL_DATA,
  BENCHMARK_DATA,
  REGULATORY_DATA,
  DASHBOARD_SUMMARY,
  TECHNOLOGY_DATA,
} from '@/lib/data'

describe('Mock Data', () => {
  it('MARKET_DATA has trends and projections', () => {
    expect(MARKET_DATA.trends.length).toBeGreaterThan(0)
    expect(MARKET_DATA.projections.length).toBeGreaterThan(0)
    expect(MARKET_DATA.regionalAdoption.length).toBeGreaterThan(0)
    expect(MARKET_DATA.adoptionByFirmSize.length).toBe(3)
  })

  it('TECHNOLOGY_DATA has 3 technologies', () => {
    expect(TECHNOLOGY_DATA.technologies.length).toBe(3)
    TECHNOLOGY_DATA.technologies.forEach((tech) => {
      expect(tech.feasibilityScore).toBeGreaterThan(0)
      expect(tech.feasibilityScore).toBeLessThanOrEqual(100)
    })
  })

  it('FINANCIAL_DATA has 3 scenarios', () => {
    expect(FINANCIAL_DATA.scenarios.length).toBe(3)
    expect(FINANCIAL_DATA.scenarios[0].label).toBe('Conservative')
    expect(FINANCIAL_DATA.scenarios[1].label).toBe('Moderate')
    expect(FINANCIAL_DATA.scenarios[2].label).toBe('Aggressive')
  })

  it('BENCHMARK_DATA has 6 case studies', () => {
    expect(BENCHMARK_DATA.caseStudies.length).toBe(6)
  })

  it('REGULATORY_DATA has incentives', () => {
    expect(REGULATORY_DATA.incentives.length).toBeGreaterThan(0)
  })

  it('DASHBOARD_SUMMARY has metrics and recommendations', () => {
    expect(DASHBOARD_SUMMARY.marketMetrics.length).toBeGreaterThan(0)
    expect(DASHBOARD_SUMMARY.strategicRecommendations.length).toBeGreaterThan(0)
  })
})
