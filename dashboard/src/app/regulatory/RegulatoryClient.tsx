"use client";

import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { ChartCard } from "@/components/ui/ChartCard";
import type { RegulatoryData, RegulatoryIncentive } from "@/lib/types";

const TYPE_COLORS: Record<string, string> = {
  "Federal Tax Credit": "text-emerald-400 border-emerald-700 bg-emerald-900/20",
  "Federal Deduction": "text-teal-400 border-teal-700 bg-teal-900/20",
  "Federal Mandate": "text-blue-400 border-blue-700 bg-blue-900/20",
  "State Mandate": "text-violet-400 border-violet-700 bg-violet-900/20",
  "State Incentive": "text-amber-400 border-amber-700 bg-amber-900/20",
};

const TYPE_BAR_COLORS: Record<string, string> = {
  "Federal Tax Credit": "#10b981",
  "Federal Deduction": "#14b8a6",
  "Federal Mandate": "#3b82f6",
  "State Mandate": "#8b5cf6",
  "State Incentive": "#f59e0b",
};

const ALL_TYPES = [
  "All",
  "Federal Tax Credit",
  "Federal Deduction",
  "Federal Mandate",
  "State Mandate",
  "State Incentive",
] as const;

type FilterType = (typeof ALL_TYPES)[number];

function IncentiveCard({ incentive }: { incentive: RegulatoryIncentive }) {
  const [expanded, setExpanded] = useState(false);
  const colorClass = TYPE_COLORS[incentive.type] ?? "text-slate-400 border-slate-600";

  return (
    <article
      className="bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-slate-600 transition-colors"
      aria-label={`${incentive.name} incentive`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1">
          <h3 className="text-sm font-bold text-white">{incentive.name}</h3>
          <p className="text-lg font-bold text-emerald-400 mt-1">{incentive.value}</p>
        </div>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded-full border flex-shrink-0 ${colorClass}`}
        >
          {incentive.type}
        </span>
      </div>

      <div className="space-y-2 mb-3">
        <div className="flex items-start gap-2 text-xs">
          <span className="text-slate-500 flex-shrink-0 w-16">Eligibility</span>
          <span className="text-slate-300">{incentive.eligibility}</span>
        </div>
        {incentive.effectiveDate && (
          <div className="flex items-start gap-2 text-xs">
            <span className="text-slate-500 flex-shrink-0 w-16">Effective</span>
            <span className="text-slate-300">
              {incentive.effectiveDate}
              {incentive.expirationDate && ` – ${incentive.expirationDate}`}
            </span>
          </div>
        )}
      </div>

      <div className="bg-emerald-900/20 border border-emerald-800/40 rounded-lg p-3 mb-3">
        <p className="text-xs font-medium text-emerald-400 mb-0.5">Financial Impact</p>
        <p className="text-xs text-slate-300">{incentive.financialImpact}</p>
      </div>

      <button
        onClick={() => setExpanded(!expanded)}
        className="text-xs text-slate-400 hover:text-slate-200 transition-colors flex items-center gap-1"
        aria-expanded={expanded}
        aria-controls={`desc-${incentive.id}`}
      >
        <span>{expanded ? "▲" : "▼"}</span>
        <span>{expanded ? "Hide" : "Show"} details</span>
      </button>

      {expanded && (
        <div id={`desc-${incentive.id}`} className="mt-3 pt-3 border-t border-slate-700">
          <p className="text-xs text-slate-400 leading-relaxed">{incentive.description}</p>
        </div>
      )}
    </article>
  );
}

interface Props {
  data: RegulatoryData;
}

export function RegulatoryClient({ data }: Props) {
  const [filter, setFilter] = useState<FilterType>("All");

  const filtered = data.incentives.filter(
    (i) => filter === "All" || i.type === filter
  );

  const chartData = data.incentives
    .filter((i) => i.valueNumeric !== undefined)
    .map((i) => ({
      name: i.name.replace("IRA ", "").replace("Section ", "§"),
      value: i.valueNumeric,
      type: i.type,
      fill: TYPE_BAR_COLORS[i.type] ?? "#10b981",
    }));

  return (
    <div className="space-y-6">
      {/* Summary chart */}
      {chartData.length > 0 && (
        <ChartCard
          title="Incentive Value Comparison"
          subtitle="Quantified financial value of key programs"
        >
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 0, bottom: 50 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey="name"
                tick={{ fill: "#94a3b8", fontSize: 10 }}
                axisLine={{ stroke: "#334155" }}
                tickLine={false}
                angle={-30}
                textAnchor="end"
                interval={0}
              />
              <YAxis
                tick={{ fill: "#94a3b8", fontSize: 10 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip
                contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
                labelStyle={{ color: "#f8fafc" }}
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                formatter={(value: any) => [`${value ?? 0}`, "Value"]}
              />
              <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, index) => (
                  <rect key={`bar-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          <p className="text-xs text-slate-500 mt-1 text-center">
            Values shown: % for tax credits, $/sqft for 179D, $/unit for 45L
          </p>
        </ChartCard>
      )}

      {/* Filters */}
      <div>
        <p className="text-xs text-slate-400 mb-2">Filter by Type</p>
        <div className="flex flex-wrap gap-2" role="group" aria-label="Filter incentives by type">
          {ALL_TYPES.map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-3 py-1 rounded-lg text-xs font-medium border transition-colors ${
                filter === type
                  ? "bg-emerald-900/40 border-emerald-600 text-emerald-300"
                  : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-300"
              }`}
              aria-pressed={filter === type}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* Incentive Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((incentive) => (
          <IncentiveCard key={incentive.id} incentive={incentive} />
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-12 text-center">
          <p className="text-slate-400 text-sm">No incentives match the selected filter.</p>
          <button
            onClick={() => setFilter("All")}
            className="mt-3 text-xs text-emerald-400 hover:text-emerald-300 underline"
          >
            Clear filter
          </button>
        </div>
      )}

      {/* Key Takeaways */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-white mb-4">Key Policy Takeaways</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              title: "IRA Creates Historic Incentive Window",
              body: "The Inflation Reduction Act (2022) allocated $369B for clean energy. Construction firms should maximize ITC, PTC, and manufacturing credits before political landscape shifts.",
            },
            {
              title: "Federal Contract Access via LEED",
              body: "GSA's LEED Gold mandate opens the $70B+ annual federal construction market. Firms without LEED capability are excluded from this segment entirely.",
            },
            {
              title: "35+ State Mandates Create Pipeline",
              body: "Most major U.S. construction markets now require green building certification. This is not an emerging trend — it is current market reality.",
            },
            {
              title: "Stack Multiple Incentives Per Project",
              body: "A single project may qualify for 48C (30% ITC), 179D ($5.65/sqft), state rebates, and utility incentives simultaneously — dramatically improving project economics.",
            },
          ].map((item) => (
            <div key={item.title} className="bg-slate-900/50 rounded-lg p-4">
              <p className="text-xs font-semibold text-emerald-400 mb-1.5">{item.title}</p>
              <p className="text-xs text-slate-400 leading-relaxed">{item.body}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
