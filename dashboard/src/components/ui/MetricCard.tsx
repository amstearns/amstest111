"use client";

import type { MarketMetric } from "@/lib/types";

interface MetricCardProps {
  metric: MarketMetric;
  className?: string;
}

export function MetricCard({ metric, className = "" }: MetricCardProps) {
  const trendIcon =
    metric.trend === "up" ? "↑" : metric.trend === "down" ? "↓" : "→";
  const trendColor =
    metric.trend === "up"
      ? "text-emerald-400"
      : metric.trend === "down"
        ? "text-amber-400"
        : "text-slate-400";

  return (
    <div
      className={`bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-emerald-600 transition-colors ${className}`}
    >
      <p className="text-xs font-medium text-slate-400 uppercase tracking-wider mb-2">
        {metric.label}
      </p>
      <p className="text-2xl font-bold text-white mb-1">{metric.value}</p>
      {metric.unit && (
        <p className="text-xs text-slate-500 mb-2">{metric.unit}</p>
      )}
      {metric.change !== undefined && (
        <div className={`flex items-center gap-1 text-xs font-medium ${trendColor}`}>
          <span>{trendIcon}</span>
          <span>
            {Math.abs(metric.change)}%{" "}
            {metric.changeLabel ?? "change"}
          </span>
        </div>
      )}
    </div>
  );
}
