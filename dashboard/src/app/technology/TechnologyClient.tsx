"use client";

import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";
import { ChartCard } from "@/components/ui/ChartCard";
import type { TechnologyData, TechnologyProfile } from "@/lib/types";

const COLORS = ["#10b981", "#34d399", "#6ee7b7"];
const CATEGORY_COLORS: Record<string, string> = {
  "Electric Equipment": "#10b981",
  "On-site Solar": "#34d399",
  "Green Building Systems": "#6ee7b7",
};

interface Props {
  data: TechnologyData;
}

function TechCard({ tech, color }: { tech: TechnologyProfile; color: string }) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-xl p-6 flex flex-col gap-4">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <span
            className="text-xs font-medium px-2 py-0.5 rounded-full border"
            style={{ color, borderColor: color, background: `${color}15` }}
          >
            {tech.category}
          </span>
          {tech.cagr && (
            <span className="text-xs text-slate-400">{tech.cagr}% CAGR</span>
          )}
        </div>
        <h3 className="text-base font-semibold text-white">{tech.name}</h3>
        <p className="text-xs text-slate-400 mt-1 leading-relaxed">{tech.description}</p>
      </div>

      {/* Feasibility Score */}
      <div>
        <div className="flex justify-between items-center mb-1">
          <span className="text-xs text-slate-400">Feasibility Score</span>
          <span className="text-sm font-bold" style={{ color }}>{tech.feasibilityScore}/100</span>
        </div>
        <div className="w-full bg-slate-700 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all"
            style={{ width: `${tech.feasibilityScore}%`, background: color }}
            role="progressbar"
            aria-valuenow={tech.feasibilityScore}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-label={`Feasibility score: ${tech.feasibilityScore} out of 100`}
          />
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-slate-900/60 rounded-lg p-3">
          <p className="text-xs text-slate-500 mb-1">TCO Savings</p>
          <p className="text-sm font-bold text-white">
            {tech.tcoSavingsMin}–{tech.tcoSavingsMax}%
          </p>
          {tech.tcoSavingsPeriod && (
            <p className="text-xs text-slate-500">{tech.tcoSavingsPeriod}</p>
          )}
        </div>
        <div className="bg-slate-900/60 rounded-lg p-3">
          <p className="text-xs text-slate-500 mb-1">Timeline</p>
          <p className="text-sm font-bold text-white">
            {tech.implementationTimelineMin}–{tech.implementationTimelineMax}mo
          </p>
        </div>
        <div className="bg-slate-900/60 rounded-lg p-3">
          <p className="text-xs text-slate-500 mb-1">Payback</p>
          <p className="text-sm font-bold text-white">
            {tech.paybackPeriodMin}–{tech.paybackPeriodMax}yr
          </p>
        </div>
      </div>

      {/* Benefits */}
      <div>
        <p className="text-xs font-medium text-slate-400 uppercase tracking-wide mb-2">Key Benefits</p>
        <ul className="space-y-1">
          {tech.keyBenefits.slice(0, 3).map((b) => (
            <li key={b} className="flex items-start gap-2 text-xs text-slate-300">
              <span className="text-emerald-500 mt-0.5 flex-shrink-0">✓</span>
              {b}
            </li>
          ))}
        </ul>
      </div>

      {/* Challenges */}
      <div>
        <p className="text-xs font-medium text-slate-400 uppercase tracking-wide mb-2">Challenges</p>
        <ul className="space-y-1">
          {tech.challenges.slice(0, 2).map((c) => (
            <li key={c} className="flex items-start gap-2 text-xs text-slate-400">
              <span className="text-amber-500 mt-0.5 flex-shrink-0">!</span>
              {c}
            </li>
          ))}
        </ul>
      </div>

      {tech.marketSize && (
        <p className="text-xs text-slate-500 border-t border-slate-700 pt-3">
          Market size: {tech.marketSize}
        </p>
      )}
    </div>
  );
}

export function TechnologyClient({ data }: Props) {
  const radarData = [
    {
      metric: "Feasibility",
      "Electric Equipment": data.technologies[0]?.feasibilityScore ?? 0,
      "On-site Solar": data.technologies[1]?.feasibilityScore ?? 0,
      "Green Building Systems": data.technologies[2]?.feasibilityScore ?? 0,
    },
    {
      metric: "TCO Savings",
      "Electric Equipment": 17.5,
      "On-site Solar": 30,
      "Green Building Systems": 16.9,
    },
    {
      metric: "Speed (inv)",
      "Electric Equipment": 100 - 65,
      "On-site Solar": 100 - 25,
      "Green Building Systems": 100 - 45,
    },
    {
      metric: "Market Growth",
      "Electric Equipment": 90,
      "On-site Solar": 75,
      "Green Building Systems": 70,
    },
    {
      metric: "Incentive Access",
      "Electric Equipment": 70,
      "On-site Solar": 95,
      "Green Building Systems": 85,
    },
  ];

  const paybackData = data.technologies.map((t) => ({
    name: t.category,
    Min: t.paybackPeriodMin,
    Max: t.paybackPeriodMax,
  }));

  return (
    <div className="space-y-6">
      {/* Technology Cards */}
      <section aria-labelledby="tech-cards-heading">
        <h2 id="tech-cards-heading" className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">
          Technology Profiles
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {data.technologies.map((tech, i) => (
            <TechCard key={tech.id} tech={tech} color={COLORS[i] ?? "#10b981"} />
          ))}
        </div>
      </section>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Multi-Dimensional Comparison"
          subtitle="Relative performance across 5 dimensions (higher = better)"
        >
          <ResponsiveContainer width="100%" height={280}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#1e293b" />
              <PolarAngleAxis
                dataKey="metric"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
              />
              <PolarRadiusAxis
                angle={30}
                domain={[0, 100]}
                tick={{ fill: "#64748b", fontSize: 10 }}
              />
              <Tooltip
                contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
                labelStyle={{ color: "#f8fafc" }}
              />
              {data.technologies.map((tech, i) => (
                <Radar
                  key={tech.id}
                  name={tech.category}
                  dataKey={tech.category}
                  stroke={CATEGORY_COLORS[tech.category] ?? COLORS[i]}
                  fill={CATEGORY_COLORS[tech.category] ?? COLORS[i]}
                  fillOpacity={0.15}
                  strokeWidth={2}
                />
              ))}
              <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 11 }} />
            </RadarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard
          title="Payback Period Ranges"
          subtitle="Years to breakeven — minimum and maximum estimates"
        >
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={paybackData} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis
                dataKey="name"
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                axisLine={{ stroke: "#334155" }}
                tickLine={false}
                width={80}
              />
              <YAxis
                tick={{ fill: "#94a3b8", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                tickFormatter={(v: number) => `${v}yr`}
              />
              <Tooltip
                contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
                labelStyle={{ color: "#f8fafc" }}
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                formatter={(value: any, name: any) => [`${value ?? 0} years`, name]}
              />
              <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 11 }} />
              <Bar dataKey="Min" name="Optimistic" fill="#10b981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Max" name="Conservative" fill="#334155" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
}
