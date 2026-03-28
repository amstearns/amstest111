// API client with backend fetch and mock data fallback
import {
  MARKET_DATA,
  TECHNOLOGY_DATA,
  FINANCIAL_DATA,
  BENCHMARK_DATA,
  REGULATORY_DATA,
  DASHBOARD_SUMMARY,
} from "./data";
import type {
  MarketData,
  TechnologyData,
  FinancialData,
  BenchmarkData,
  RegulatoryData,
  DashboardSummary,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";
const FETCH_TIMEOUT_MS = 3000;

async function fetchWithTimeout<T>(url: string): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      signal: controller.signal,
      headers: { "Content-Type": "application/json" },
      cache: "no-store",
    });
    clearTimeout(timeoutId);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return (await res.json()) as T;
  } catch {
    clearTimeout(timeoutId);
    throw new Error("Backend unavailable");
  }
}

export async function getMarketData(): Promise<MarketData> {
  try {
    return await fetchWithTimeout<MarketData>(`${API_BASE_URL}/market-trends`);
  } catch {
    return MARKET_DATA;
  }
}

export async function getTechnologyData(): Promise<TechnologyData> {
  try {
    return await fetchWithTimeout<TechnologyData>(`${API_BASE_URL}/technologies`);
  } catch {
    return TECHNOLOGY_DATA;
  }
}

export async function getFinancialData(): Promise<FinancialData> {
  try {
    return await fetchWithTimeout<FinancialData>(`${API_BASE_URL}/financial`);
  } catch {
    return FINANCIAL_DATA;
  }
}

export async function getBenchmarkData(): Promise<BenchmarkData> {
  try {
    return await fetchWithTimeout<BenchmarkData>(`${API_BASE_URL}/benchmarking`);
  } catch {
    return BENCHMARK_DATA;
  }
}

export async function getRegulatoryData(): Promise<RegulatoryData> {
  try {
    return await fetchWithTimeout<RegulatoryData>(`${API_BASE_URL}/regulatory`);
  } catch {
    return REGULATORY_DATA;
  }
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  try {
    return await fetchWithTimeout<DashboardSummary>(`${API_BASE_URL}/summary`);
  } catch {
    return DASHBOARD_SUMMARY;
  }
}
