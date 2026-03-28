import { NavBar } from "@/components/layout/NavBar";
import { MetricCard } from "@/components/ui/MetricCard";
import { getDashboardSummary } from "@/lib/api";
import Link from "next/link";

export default async function ExecutiveSummaryPage() {
  const summary = await getDashboardSummary();

  return (
    <>
      <NavBar
        title="Executive Summary"
        subtitle="Renewable Energy Adoption — North American Construction Industry"
      />
      <div className="flex-1 p-6 space-y-8 overflow-auto">
        {/* Section: Key Metrics */}
        <section aria-labelledby="metrics-heading">
          <h2 id="metrics-heading" className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">
            Key Market Metrics
          </h2>
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
            {summary.marketMetrics.map((metric) => (
              <MetricCard key={metric.label} metric={metric} />
            ))}
          </div>
        </section>

        {/* Section: Strategic Recommendations */}
        <section aria-labelledby="recommendations-heading">
          <h2 id="recommendations-heading" className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">
            Strategic Recommendations
          </h2>
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <ul className="space-y-3" role="list">
              {summary.strategicRecommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span
                    className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-900/60 border border-emerald-700 text-emerald-400 text-xs font-bold flex items-center justify-center mt-0.5"
                    aria-hidden="true"
                  >
                    {i + 1}
                  </span>
                  <p className="text-sm text-slate-300 leading-relaxed">{rec}</p>
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Section: Quick navigation cards */}
        <section aria-labelledby="explore-heading">
          <h2 id="explore-heading" className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-4">
            Explore the Dashboard
          </h2>
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              {
                href: "/market-trends",
                title: "Market Trends",
                desc: "Adoption rates, regional heat maps, and growth projections",
                icon: "↗",
                badge: "9.29% CAGR",
              },
              {
                href: "/technology",
                title: "Technology Comparison",
                desc: "Solar vs. electric equipment vs. green building systems",
                icon: "⚙",
                badge: "3 technologies",
              },
              {
                href: "/financial",
                title: "Financial Analysis",
                desc: "Interactive ROI calculator and scenario modeling",
                icon: "$",
                badge: "12–31% ROI",
              },
              {
                href: "/benchmarking",
                title: "Competitive Benchmarking",
                desc: "Top competitor case studies with key performance metrics",
                icon: "▣",
                badge: "6 case studies",
              },
              {
                href: "/regulatory",
                title: "Regulatory Incentives",
                desc: "IRA tax credits, deductions, and mandate requirements",
                icon: "✦",
                badge: "6 programs",
              },
            ].map((card) => (
              <Link
                key={card.href}
                href={card.href}
                className="group bg-slate-800 border border-slate-700 rounded-xl p-5 hover:border-emerald-600 hover:bg-slate-800/80 transition-all"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-emerald-500 text-xl" aria-hidden="true">{card.icon}</span>
                  <span className="text-xs bg-emerald-900/40 text-emerald-400 border border-emerald-800 px-2 py-0.5 rounded-full">
                    {card.badge}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-white mb-1 group-hover:text-emerald-300 transition-colors">
                  {card.title}
                </h3>
                <p className="text-xs text-slate-400 leading-relaxed">{card.desc}</p>
              </Link>
            ))}
          </div>
        </section>

        {/* Footer note */}
        <p className="text-xs text-slate-600 text-center pb-4">
          Data sourced from ENR rankings, USGBC, IEA, Bloomberg NEF, and primary industry research — {summary.lastUpdated}
        </p>
      </div>
    </>
  );
}
