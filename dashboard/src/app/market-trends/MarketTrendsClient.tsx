"use client";

import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { ChartCard } from "@/components/ui/ChartCard";
import type { MarketData } from "@/lib/types";

interface Props {
  data: MarketData;
}

export function MarketTrendsClient({ data }: Props) {
  // Combine historical + projections for area chart, flagging projected years
  const allTrends = [
    ...data.trends.map((d) => ({ ...d, type: "Historical" })),
    ...data.projections
      .filter((p) => p.year > Math.max(...data.trends.map((t) => t.year)))
      .map((d) => ({ ...d, type: "Projected" })),
  ];

  return (
    <div className="space-y-6">
      {/* Market Growth Chart */}
      <ChartCard
        title="North American Green Construction Market Growth"
        subtitle="Annual investment in $B — historical data and 2034 projections (9.29% CAGR)"
      >
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={allTrends} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
            <defs>
              <linearGradient id="colorGreen" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="year"
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={{ stroke: "#334155" }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v: number) => `$${v}B`}
            />
            <Tooltip
              contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
              labelStyle={{ color: "#f8fafc" }}
              itemStyle={{ color: "#10b981" }}
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              formatter={(value: any) => [`$${value ?? 0}B`, "Market Size"]}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#colorGreen)"
              dot={{ fill: "#10b981", strokeWidth: 0, r: 4 }}
              activeDot={{ r: 6, fill: "#34d399" }}
            />
          </AreaChart>
        </ResponsiveContainer>
        <p className="text-xs text-slate-500 mt-2 text-center">
          IRA (2023) marked a significant inflection point — $153B invested that year
        </p>
      </ChartCard>

      {/* Adoption by Firm Size */}
      <ChartCard
        title="Green Technology Adoption by Firm Size"
        subtitle="% of firms with active programs — ESG, LEED experience, and electric equipment"
      >
        <ResponsiveContainer width="100%" height={280}>
          <BarChart
            data={data.adoptionByFirmSize}
            margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="firmSize"
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={{ stroke: "#334155" }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: "#94a3b8", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v: number) => `${v}%`}
            />
            <Tooltip
              contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
              labelStyle={{ color: "#f8fafc" }}
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              formatter={(value: any) => [`${value ?? 0}%`]}
            />
            <Legend
              wrapperStyle={{ color: "#94a3b8", fontSize: 12 }}
            />
            <Bar dataKey="esgPrograms" name="ESG Programs" fill="#10b981" radius={[4, 4, 0, 0]} />
            <Bar dataKey="leedExperience" name="LEED Experience" fill="#34d399" radius={[4, 4, 0, 0]} />
            <Bar dataKey="electricEquipment" name="Electric Equipment" fill="#6ee7b7" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </ChartCard>

      {/* Regional Adoption Table */}
      <ChartCard
        title="Top LEED States — Regional Adoption Rates"
        subtitle="States ranked by green building adoption rate"
      >
        <div className="overflow-x-auto">
          <table className="w-full text-sm" aria-label="Regional adoption data">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-2 pr-4 text-xs font-medium text-slate-400 uppercase tracking-wide">State</th>
                <th className="text-left py-2 pr-4 text-xs font-medium text-slate-400 uppercase tracking-wide">Region</th>
                <th className="text-right py-2 pr-4 text-xs font-medium text-slate-400 uppercase tracking-wide">Adoption Rate</th>
                <th className="text-right py-2 text-xs font-medium text-slate-400 uppercase tracking-wide">LEED Projects</th>
              </tr>
            </thead>
            <tbody>
              {data.regionalAdoption
                .sort((a, b) => b.adoptionRate - a.adoptionRate)
                .map((row, i) => (
                  <tr key={row.state} className={i % 2 === 0 ? "bg-slate-800/30" : ""}>
                    <td className="py-2.5 pr-4 font-medium text-white">{row.state}</td>
                    <td className="py-2.5 pr-4 text-slate-400">{row.region}</td>
                    <td className="py-2.5 pr-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <div className="w-20 bg-slate-700 rounded-full h-1.5">
                          <div
                            className="bg-emerald-500 h-1.5 rounded-full"
                            style={{ width: `${row.adoptionRate}%` }}
                            aria-hidden="true"
                          />
                        </div>
                        <span className="text-emerald-400 font-medium w-10 text-right">
                          {row.adoptionRate}%
                        </span>
                      </div>
                    </td>
                    <td className="py-2.5 text-right text-slate-300">
                      {row.leedProjects?.toLocaleString() ?? "—"}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </ChartCard>
    </div>
  );
}
