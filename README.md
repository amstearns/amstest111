# Renewable Energy Executive Dashboard

An interactive executive dashboard that visualizes renewable energy adoption research findings for the North American construction industry. Built with Next.js 15 (App Router), TypeScript, and Tailwind CSS, this dashboard targets a C-suite/executive audience with clean, professional design and a green/sustainable color palette.

## Architecture

The system is composed of a frontend dashboard that serves as the primary user interface:

- **Frontend**: Next.js 15 (App Router) + React 19 + TypeScript
- **Visualization**: Recharts for interactive data exploration
- **Styling**: Tailwind CSS with dark theme (`slate-950` background, `emerald-*` accent colors)
- **Port**: 3000
- **API Integration**: Optional backend API with automatic fallback to comprehensive mock data

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | Next.js 16.2.1 with App Router | Server/client component architecture |
| UI Library | React 19.2.4 | Component rendering |
| Styling | Tailwind CSS 4 + PostCSS | Responsive, utility-first design |
| Charts | Recharts 3.8.1 | Interactive data visualization |
| Language | TypeScript 5 | Type-safe development |
| Testing | Jest + Testing Library | Unit/component testing (21 tests) |

## Components

### Frontend Dashboard

The frontend team delivered a fully functional executive dashboard with six primary pages:

#### Pages & Features

| Route | Title | Key Features |
|-------|-------|-------------|
| `/` | Executive Summary | 6 KPI metric cards, strategic recommendations, dashboard navigation |
| `/market-trends` | Market Trends | Growth area chart (9.29% CAGR to 2034), adoption by firm size, regional LEED adoption table |
| `/technology` | Technology Comparison | Side-by-side profiles (Electric Equipment/Solar/Green Building), radar chart, payback comparison |
| `/financial` | Financial Analysis | Interactive ROI calculator (4 sliders), cumulative cash flow line chart, scenario comparisons |
| `/benchmarking` | Competitive Benchmarking | Filterable case study cards (by firm size + technology), competitive landscape |
| `/regulatory` | Regulatory Incentives | Incentive value chart, type-filtered incentive cards with financial impact |

#### Key Components

| Component | Location | Description |
|-----------|----------|-------------|
| **Sidebar** | `src/components/layout/Sidebar.tsx` | Fixed navigation sidebar with 6 links, active state highlighting |
| **MetricCard** | `src/components/ui/MetricCard.tsx` | KPI card with trend indicator, value, unit |
| **ChartCard** | `src/components/ui/ChartCard.tsx` | Consistent chart container wrapper |
| **MarketTrendsClient** | `src/app/market-trends/MarketTrendsClient.tsx` | Area + bar charts, sortable table |
| **TechnologyClient** | `src/app/technology/TechnologyClient.tsx` | Profile cards, radar + payback charts |
| **FinancialClient** | `src/app/financial/FinancialClient.tsx` | ROI calculator with 4 sliders, line chart |
| **BenchmarkingClient** | `src/app/benchmarking/BenchmarkingClient.tsx` | Filterable case study grid |
| **RegulatoryClient** | `src/app/regulatory/RegulatoryClient.tsx` | Expandable incentive cards |

### Data Layer

- **Mock Data** (`src/lib/data.ts`): Research-backed comprehensive dataset with market sizes, adoption rates, case studies, and regulatory programs
- **API Client** (`src/lib/api.ts`): Fetches from optional backend with automatic 3-second timeout fallback
- **Types** (`src/lib/types.ts`): TypeScript interfaces for all data structures

## Getting Started

### Prerequisites

- Node.js 18+ (for modern JavaScript features)
- npm or yarn
- Git (for version control)

### Installation & Running

```bash
# Install dependencies
cd dashboard
npm install

# Development server (hot reload on port 3000)
npm run dev

# Production build
npm run build

# Start production server
npm start

# Run test suite
npx jest
```

The dashboard automatically starts on **port 3000**. If a backend API is available at `http://localhost:8000/api`, data is fetched from it; otherwise, the app uses comprehensive research-backed mock data.

### API Reference

#### Backend API Endpoints

The frontend API client supports the following endpoints (all optional — mock data serves as fallback):

| Function | Endpoint | Returns | Data |
|----------|----------|---------|------|
| `getMarketData()` | `GET /api/market-trends` | `MarketData` | Growth trends, projections, regional adoption |
| `getTechnologyData()` | `GET /api/technologies` | `TechnologyData` | Technology profiles, feasibility, TCO |
| `getFinancialData()` | `GET /api/financial` | `FinancialData` | ROI scenarios, calculator defaults |
| `getBenchmarkData()` | `GET /api/benchmarks` | `BenchmarkData` | Case studies, competitive metrics |
| `getRegulatoryData()` | `GET /api/regulatory` | `RegulatoryData` | Incentive programs, financial impact |
| `getDashboardSummary()` | `GET /api/summary` | `DashboardSummary` | Key metrics, strategic recommendations |

#### Environment Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000/api` | Backend API base URL (public, consumed by frontend) |

### Data Types

All TypeScript interfaces are defined in `src/lib/types.ts`:

- `MarketData` — Market trends, growth projections, regional data, firm-size segments
- `TechnologyData` — Technology profiles with feasibility scores, TCO estimates, payback periods
- `FinancialData` — ROI calculation parameters and scenario definitions
- `BenchmarkData` — Case studies with key metrics and competitive highlights
- `RegulatoryData` — Federal/state/local incentive programs with financial quantification
- `DashboardSummary` — Executive summary metrics and strategic recommendations

## Technical Decisions

### 1. Server + Client Component Architecture
The dashboard uses Next.js 15 App Router with a split between server components (data fetching) and client components (`*Client.tsx` files for interactivity). This optimizes performance by reducing JavaScript sent to the browser while maintaining rich interactivity.

### 2. Mock Data Fallback Strategy
The API client attempts to fetch from the backend with a 3-second timeout. If the backend is unavailable, the dashboard automatically falls back to comprehensive research-backed mock data. This allows the dashboard to function autonomously without external dependencies.

### 3. Dark Theme with Sustainable Branding
The interface uses a `slate-950` background with `emerald-*` accent colors. This professional, executive-appropriate aesthetic aligns with renewable energy and sustainability branding while maintaining accessibility.

### 4. Recharts for Visualization
Recharts was chosen over Chart.js because it:
- Integrates naturally with React's component model
- Has superior TypeScript support
- Produces smaller bundle size for this use case
- Provides responsive, interactive charts out-of-the-box

### 5. Accessibility-First Design
The dashboard is WCAG 2.1 AA compliant:
- Skip links for keyboard navigation
- Proper ARIA landmarks and semantic HTML
- `aria-live` regions for dynamic content (ROI calculator, filter results)
- Accessible sliders and form controls
- Color contrast ratios meet 4.5:1 standard

### 6. Research-Backed Data
All mock data (market sizes, adoption rates, case study metrics, regulatory programs) is sourced from the previous research team's analysis, leveraging HIGH/MEDIUM confidence sources from Precedence Research, USGBC, ENR, CBRE, and IEA.

## Testing

The project includes 21 unit tests covering:
- **Components**: MetricCard component with variants
- **Data layer**: Market data calculations, financial calculations
- **API client**: Fallback behavior and error handling

Run tests with:
```bash
npx jest
```

All tests pass (`21 passed, 21 total`).

## Development Workflow

### Rebuilding After Changes

```bash
# TypeScript type-checking
npm run lint

# Build verification
npm run build

# Run tests after code changes
npx jest
```

### Common Tasks

- **Add a new page**: Create a folder under `src/app/{page-name}/` with `page.tsx` and `{Page}Client.tsx`
- **Add a new component**: Create `.tsx` file in `src/components/`
- **Update mock data**: Edit `src/lib/data.ts`
- **Add a test**: Create `.test.tsx` or `.test.ts` file in `src/__tests__/`

## Project Status

✅ Build: Passing  
✅ Tests: 21/21 passing  
✅ TypeScript: No errors  
✅ Responsive Design: All breakpoints tested  
✅ Accessibility: WCAG 2.1 AA compliant  

---

*Built autonomously by [Randi](https://randi.dev) AI agents.*
