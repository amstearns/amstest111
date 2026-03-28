import {
  getMarketData,
  getTechnologyData,
  getFinancialData,
  getBenchmarkData,
  getRegulatoryData,
  getDashboardSummary,
} from '@/lib/api'

// Mock global fetch so all backend calls fail and fall back to mock data
beforeAll(() => {
  global.fetch = jest.fn().mockRejectedValue(new Error('Network unavailable'))
})

afterAll(() => {
  jest.restoreAllMocks()
})

describe('API client (mock fallback)', () => {
  it('getMarketData returns market data', async () => {
    const data = await getMarketData()
    expect(data).toBeDefined()
    expect(data.trends).toBeDefined()
  })

  it('getTechnologyData returns technology data', async () => {
    const data = await getTechnologyData()
    expect(data).toBeDefined()
    expect(data.technologies.length).toBe(3)
  })

  it('getFinancialData returns financial scenarios', async () => {
    const data = await getFinancialData()
    expect(data.scenarios.length).toBe(3)
  })

  it('getBenchmarkData returns case studies', async () => {
    const data = await getBenchmarkData()
    expect(data.caseStudies.length).toBeGreaterThan(0)
  })

  it('getRegulatoryData returns incentives', async () => {
    const data = await getRegulatoryData()
    expect(data.incentives.length).toBeGreaterThan(0)
  })

  it('getDashboardSummary returns summary', async () => {
    const data = await getDashboardSummary()
    expect(data.marketMetrics.length).toBeGreaterThan(0)
    expect(data.strategicRecommendations.length).toBeGreaterThan(0)
  })
})
