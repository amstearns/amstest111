# Frontend — Renewable Energy Executive Dashboard

## Overview

An interactive executive dashboard built with Next.js 15 (App Router), TypeScript, and Tailwind CSS that visualizes renewable energy adoption research findings for the North American construction industry. The dashboard targets a C-suite/executive audience with a clean, professional design using a green/sustainable color palette.

## Architecture

### Tech Stack

- **Framework**: Next.js 15 (App Router) with React 19 server components
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS with dark theme (`slate-950` background, `emerald-*` accent)
- **Charts**: Recharts — AreaChart, BarChart, LineChart, RadarChart
- **Testing**: Jest + Testing Library (21 tests)
- **Port**: 3000

### Directory Structure

```
dashboard/
├── src/
│   ├── app/
│   │   ├── layout.tsx                     # Root layout with sidebar nav
│   │   ├── page.tsx                       # Executive Summary (home)
│   │   ├── market-trends/
│   │   │   ├── page.tsx                   # Server component
│   │   │   └── MarketTrendsClient.tsx     # Interactive charts
│   │   ├── technology/
│   │   │   ├── page.tsx
│   │   │   └── TechnologyClient.tsx       # Radar + bar charts
│   │   ├── financial/
│   │   │   ├── page.tsx
│   │   │   └── FinancialClient.tsx        # ROI calculator + charts
│   │   ├── benchmarking/
│   │   │   ├── page.tsx
│   │   │   └── BenchmarkingClient.tsx     # Filterable case study cards
│   │   └── regulatory/
│   │       ├── page.tsx
│   │       └── RegulatoryClient.tsx       # Incentive cards + chart
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx                # Main navigation sidebar
│   │   │   └── NavBar.tsx                 # Page header bar
│   │   └── ui/
│   │       ├── MetricCard.tsx             # KPI metric card
│   │       └── ChartCard.tsx              # Chart wrapper with title
│   └── lib/
│       ├── types.ts                       # TypeScript interfaces
│       ├── data.ts                        # Mock data (research-backed)
│       └── api.ts                         # API client with fallback
├── src/__tests__/                         # 21 unit tests (all passing)
├── __mocks__/                             # Jest mocks (recharts, next/*)
└── jest.config.ts
```

### Key Components

| Component | Description |
|-----------|-------------|
| `Sidebar` | Fixed sidebar with 6 navigation links, active state highlighting |
| `MetricCard` | KPI card with trend arrow, value, unit, and accessible trend label |
| `ChartCard` | Consistent chart container with title/subtitle |
| `MarketTrendsClient` | Area chart (market growth to 2034) + grouped bar (adoption by firm size) + sortable regional table |
| `TechnologyClient` | 3 side-by-side technology profile cards + radar chart + payback range bar chart |
| `FinancialClient` | 4-slider ROI calculator with live results + cumulative cash flow line chart + scenario comparison |
| `BenchmarkingClient` | Filterable (by size + technology) case study card grid + summary table |
| `RegulatoryClient` | Type-filtered incentive cards with expand/collapse + value comparison bar chart |

## Setup & Running

```bash
cd dashboard
npm install
npm run dev      # Development server on port 3000
npm run build    # Production build
npm test         # Run 21 unit tests
```

The app runs on **port 3000** by default. If the backend API at `http://localhost:8000/api` is available, data is fetched from it; otherwise it falls back to comprehensive mock data automatically (3s timeout).

## API / Interfaces

### Backend API Consumption

The API client (`src/lib/api.ts`) attempts to fetch from the backend with automatic fallback:

| Function | Backend Endpoint | Returns |
|----------|-----------------|---------|
| `getMarketData()` | `GET /api/market-trends` | `MarketData` |
| `getTechnologyData()` | `GET /api/technologies` | `TechnologyData` |
| `getFinancialData()` | `GET /api/financial` | `FinancialData` |
| `getBenchmarkData()` | `GET /api/benchmarks` | `BenchmarkData` |
| `getRegulatoryData()` | `GET /api/regulatory` | `RegulatoryData` |
| `getDashboardSummary()` | `GET /api/summary` | `DashboardSummary` |

### TypeScript Types

All data types are defined in `src/lib/types.ts`:
- `MarketData` — market trends, projections, regional adoption, firm size data
- `TechnologyData` — technology profiles with feasibility scores, TCO, payback
- `FinancialData` — ROI scenarios and calculator defaults
- `BenchmarkData` — case studies with metrics and highlights
- `RegulatoryData` — incentive programs with financial impact
- `DashboardSummary` — key metrics and strategic recommendations

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api` | Backend API base URL |

## Pages

| Route | Title | Features |
|-------|-------|---------|
| `/` | Executive Summary | 6 KPI metric cards, 6 strategic recommendations, dashboard navigation |
| `/market-trends` | Market Trends | Growth area chart (historical + 9.29% CAGR projections to 2034), adoption by firm size bar chart, regional LEED table |
| `/technology` | Technology Comparison | Side-by-side cards (Electric Equipment/Solar/Green Building), radar chart, payback period comparison |
| `/financial` | Financial Analysis | Interactive ROI calculator (4 sliders), cumulative cash flow line chart, Conservative/Moderate/Aggressive scenario comparison |
| `/benchmarking` | Competitive Benchmarking | Filterable case study cards (by firm size + technology), competitive landscape table |
| `/regulatory` | Regulatory Incentives | Incentive value chart, type-filtered incentive cards with financial impact, key policy takeaways |

## Key Decisions

1. **Server + Client component split**: Server components fetch data; `*Client.tsx` files handle interactivity. This follows Next.js 15 App Router best practices for optimal performance.

2. **Mock data fallback**: The API client tries the backend with a 3s timeout, then falls back to comprehensive research-backed mock data. The dashboard works standalone without a running backend.

3. **Dark theme design**: Uses `slate-950` background with `emerald-*` accent colors for a professional, executive-appropriate aesthetic aligned with sustainability branding.

4. **Recharts over Chart.js**: Recharts integrates more naturally with React's component model, supports TypeScript better, and has smaller bundle size for this use case.

5. **Accessibility-first**: WCAG 2.1 AA compliant — skip link, proper ARIA landmarks, `aria-live` regions for dynamic content (ROI calculator, filter results), accessible sliders.

6. **Data from research**: All mock data (market sizes, adoption rates, case study metrics, regulatory programs) is sourced from the previous research team's analysis (Precedence Research, USGBC, ENR, CBRE, IEA sources with HIGH/MEDIUM confidence ratings).
