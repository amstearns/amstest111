"use client";

import { useState, useMemo } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { ChartCard } from "@/components/ui/ChartCard";
import type { FinancialData, ROICalculatorResult } from "@/lib/types";

interface Props {
  data: FinancialData;
}

function calculateROI(
  investmentAmount: number,
  incentiveUtilization: number,
  contractPremium: number,
  projectDuration: number
): ROICalculatorResult {
  const incentiveSavings = investmentAmount * 0.30 * incentiveUtilization;
  const netInvestment = investmentAmount - incentiveSavings;
  const annualContractRevenue = investmentAmount * contractPremium;
  const annualEnergySavings = investmentAmount * 0.08; // ~8% annual energy cost savings
  const annualSavings = annualContractRevenue + annualEnergySavings;
  const paybackPeriod = netInvestment / annualSavings;
  const totalSavings = annualSavings * projectDuration + incentiveSavings;
  const netSavings = totalSavings - investmentAmount;
  const roi = (netSavings / investmentAmount) * 100;

  return {
    paybackPeriod: Math.round(paybackPeriod * 10) / 10,
    roi: Math.round(roi * 10) / 10,
    netSavings: Math.round(netSavings),
    annualSavings: Math.round(annualSavings),
    incentiveSavings: Math.round(incentiveSavings),
  };
}

function formatCurrency(value: number): string {
  if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
  return `$${value.toFixed(0)}`;
}

const SCENARIO_COLORS: Record<string, string> = {
  Conservative: "#64748b",
  Moderate: "#10b981",
  Aggressive: "#34d399",
};

export function FinancialClient({ data }: Props) {
  const [investment, setInvestment] = useState(data.defaultInputs.investmentAmount);
  const [incentive, setIncentive] = useState(data.defaultInputs.incentiveUtilization);
  const [premium, setPremium] = useState(data.defaultInputs.contractPremium);
  const [duration, setDuration] = useState(data.defaultInputs.projectDuration);

  const result = useMemo(
    () => calculateROI(investment, incentive, premium, duration),
    [investment, incentive, premium, duration]
  );

  // Build cumulative cash flow chart data
  const cashFlowData = useMemo(() => {
    const rows = [];
    const incentiveSavings = investment * 0.30 * incentive;
    const netInvestment = investment - incentiveSavings;
    for (let year = 0; year <= Math.min(duration, 15); year++) {
      const savings = year === 0 ? incentiveSavings : result.annualSavings;
      const cumulative = year === 0
        ? incentiveSavings - investment
        : (year * result.annualSavings + incentiveSavings) - investment;
      rows.push({
        year: `Yr ${year}`,
        "Cumulative Cash Flow": Math.round(cumulative),
        "Annual Savings": year === 0 ? Math.round(incentiveSavings) : Math.round(result.annualSavings),
        netInvestment: Math.round(netInvestment),
      });
    }
    return rows;
  }, [investment, incentive, result.annualSavings, duration]);

  // Scenario comparison chart
  const scenarioChartData = data.scenarios.map((s) => ({
    name: s.label,
    ROI: s.roi,
    "Payback (yr)": s.paybackPeriod,
    "Annual Savings": Math.round((s.annualSavings ?? 0) / 1000),
  }));

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* ROI Calculator */}
        <div className="lg:col-span-1">
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 space-y-5">
            <h2 className="text-sm font-semibold text-white">ROI Calculator</h2>

            {/* Investment Slider */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <label htmlFor="investment-slider" className="text-xs text-slate-400">Investment Amount</label>
                <span className="text-xs font-semibold text-emerald-400">{formatCurrency(investment)}</span>
              </div>
              <input
                id="investment-slider"
                type="range"
                min={500000}
                max={50000000}
                step={500000}
                value={investment}
                onChange={(e) => setInvestment(Number(e.target.value))}
                className="w-full accent-emerald-500"
                aria-label={`Investment amount: ${formatCurrency(investment)}`}
              />
              <div className="flex justify-between text-xs text-slate-600 mt-0.5">
                <span>$500K</span><span>$50M</span>
              </div>
            </div>

            {/* Incentive Utilization Slider */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <label htmlFor="incentive-slider" className="text-xs text-slate-400">Incentive Utilization</label>
                <span className="text-xs font-semibold text-emerald-400">{Math.round(incentive * 100)}%</span>
              </div>
              <input
                id="incentive-slider"
                type="range"
                min={0}
                max={1}
                step={0.05}
                value={incentive}
                onChange={(e) => setIncentive(Number(e.target.value))}
                className="w-full accent-emerald-500"
                aria-label={`Incentive utilization: ${Math.round(incentive * 100)}%`}
              />
              <div className="flex justify-between text-xs text-slate-600 mt-0.5">
                <span>0%</span><span>100%</span>
              </div>
            </div>

            {/* Contract Premium Slider */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <label htmlFor="premium-slider" className="text-xs text-slate-400">Green Contract Premium</label>
                <span className="text-xs font-semibold text-emerald-400">{Math.round(premium * 100)}%</span>
              </div>
              <input
                id="premium-slider"
                type="range"
                min={0}
                max={0.10}
                step={0.005}
                value={premium}
                onChange={(e) => setPremium(Number(e.target.value))}
                className="w-full accent-emerald-500"
                aria-label={`Contract premium: ${Math.round(premium * 100)}%`}
              />
              <div className="flex justify-between text-xs text-slate-600 mt-0.5">
                <span>0%</span><span>10%</span>
              </div>
            </div>

            {/* Project Duration Slider */}
            <div>
              <div className="flex justify-between items-center mb-1">
                <label htmlFor="duration-slider" className="text-xs text-slate-400">Analysis Period</label>
                <span className="text-xs font-semibold text-emerald-400">{duration} years</span>
              </div>
              <input
                id="duration-slider"
                type="range"
                min={3}
                max={20}
                step={1}
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full accent-emerald-500"
                aria-label={`Analysis period: ${duration} years`}
              />
              <div className="flex justify-between text-xs text-slate-600 mt-0.5">
                <span>3yr</span><span>20yr</span>
              </div>
            </div>

            {/* Results */}
            <div className="border-t border-slate-700 pt-4 grid grid-cols-2 gap-3">
              {[
                { label: "ROI", value: `${result.roi}%`, highlight: true },
                { label: "Payback Period", value: `${result.paybackPeriod} yrs`, highlight: false },
                { label: "Net Savings", value: formatCurrency(result.netSavings), highlight: true },
                { label: "Annual Savings", value: formatCurrency(result.annualSavings), highlight: false },
                { label: "Incentive Savings", value: formatCurrency(result.incentiveSavings), highlight: false },
              ].map((item) => (
                <div key={item.label} className="bg-slate-900/60 rounded-lg p-3">
                  <p className="text-xs text-slate-500 mb-1">{item.label}</p>
                  <p className={`text-sm font-bold ${item.highlight ? "text-emerald-400" : "text-white"}`}>
                    {item.value}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Cash Flow Chart */}
        <div className="lg:col-span-2 space-y-6">
          <ChartCard
            title="Cumulative Cash Flow"
            subtitle="Net cash position over the analysis period"
          >
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={cashFlowData} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="year"
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  axisLine={{ stroke: "#334155" }}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                  tickFormatter={(v: number) => formatCurrency(v)}
                />
                <Tooltip
                  contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
                  labelStyle={{ color: "#f8fafc" }}
                  // eslint-disable-next-line @typescript-eslint/no-explicit-any
                  formatter={(value: any) => [formatCurrency(Number(value ?? 0))]}
                />
                <ReferenceLine y={0} stroke="#475569" strokeDasharray="4 4" />
                <Line
                  type="monotone"
                  dataKey="Cumulative Cash Flow"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={{ fill: "#10b981", strokeWidth: 0, r: 3 }}
                  activeDot={{ r: 5, fill: "#34d399" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Scenario comparison */}
          <ChartCard
            title="Scenario Comparison"
            subtitle="Conservative vs. Moderate vs. Aggressive assumptions — $5M baseline"
          >
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={scenarioChartData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis
                  dataKey="name"
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  axisLine={{ stroke: "#334155" }}
                  tickLine={false}
                />
                <YAxis
                  tick={{ fill: "#94a3b8", fontSize: 11 }}
                  axisLine={false}
                  tickLine={false}
                />
                <Tooltip
                  contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
                  labelStyle={{ color: "#f8fafc" }}
                />
                <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 11 }} />
                <Bar dataKey="ROI" name="ROI (%)" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="Payback (yr)" name="Payback (yrs)" fill="#334155" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>

            {/* Scenario detail table */}
            <div className="mt-4 overflow-x-auto">
              <table className="w-full text-xs" aria-label="Scenario comparison details">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left py-2 pr-4 text-slate-400 font-medium">Scenario</th>
                    <th className="text-right py-2 pr-4 text-slate-400 font-medium">Incentive Use</th>
                    <th className="text-right py-2 pr-4 text-slate-400 font-medium">Contract Premium</th>
                    <th className="text-right py-2 pr-4 text-slate-400 font-medium">ROI</th>
                    <th className="text-right py-2 text-slate-400 font-medium">Payback</th>
                  </tr>
                </thead>
                <tbody>
                  {data.scenarios.map((s) => (
                    <tr key={s.label}>
                      <td className="py-2 pr-4">
                        <span
                          className="font-medium"
                          style={{ color: SCENARIO_COLORS[s.label] ?? "#94a3b8" }}
                        >
                          {s.label}
                        </span>
                      </td>
                      <td className="py-2 pr-4 text-right text-slate-300">
                        {Math.round(s.incentiveUtilization * 100)}%
                      </td>
                      <td className="py-2 pr-4 text-right text-slate-300">
                        {Math.round(s.contractPremium * 100)}%
                      </td>
                      <td className="py-2 pr-4 text-right font-semibold text-emerald-400">
                        {s.roi}%
                      </td>
                      <td className="py-2 text-right text-slate-300">{s.paybackPeriod} yr</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </ChartCard>
        </div>
      </div>
    </div>
  );
}
