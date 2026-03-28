"use client";

import { useState } from "react";
import type { BenchmarkData, CaseStudy } from "@/lib/types";

const FIRM_SIZES: CaseStudy["firmSize"][] = ["Small", "Mid-Size", "Mid-Large", "Large"];
const ALL_TECHS = ["Wind", "Solar", "Battery Storage", "LEED", "ESG Programs", "Carbon Neutral", "On-site Solar", "Electric Equipment", "Operations Efficiency", "Smart Building Tech", "Sustainable Design"];
const SIZE_COLORS: Record<string, string> = {
  Large: "text-emerald-400 border-emerald-700 bg-emerald-900/20",
  "Mid-Large": "text-teal-400 border-teal-700 bg-teal-900/20",
  "Mid-Size": "text-blue-400 border-blue-700 bg-blue-900/20",
  Small: "text-slate-400 border-slate-600 bg-slate-800/50",
};

function CaseStudyCard({ study }: { study: CaseStudy }) {
  return (
    <article
      className="bg-slate-800 border border-slate-700 rounded-xl p-5 flex flex-col gap-4 hover:border-emerald-700/50 transition-colors"
      aria-label={`${study.company} case study`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2">
        <div>
          <h3 className="text-sm font-bold text-white">{study.company}</h3>
          <p className="text-xs text-slate-400 mt-0.5">Revenue: {study.annualRevenue}</p>
        </div>
        <span
          className={`text-xs font-medium px-2 py-0.5 rounded-full border flex-shrink-0 ${SIZE_COLORS[study.firmSize] ?? "text-slate-400 border-slate-600"}`}
        >
          {study.firmSize}
        </span>
      </div>

      {/* Technologies */}
      <div className="flex flex-wrap gap-1.5">
        {study.technologies.map((tech) => (
          <span
            key={tech}
            className="text-xs bg-slate-700 text-slate-300 px-2 py-0.5 rounded-md"
          >
            {tech}
          </span>
        ))}
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 gap-2">
        {study.keyMetrics.map((m) => (
          <div key={m.label} className="flex justify-between items-center text-xs">
            <span className="text-slate-400">{m.label}</span>
            <span className="font-semibold text-emerald-400">{m.value}</span>
          </div>
        ))}
      </div>

      {/* Highlights */}
      <div className="border-t border-slate-700 pt-3">
        <ul className="space-y-1">
          {study.highlights.map((h) => (
            <li key={h} className="flex items-start gap-2 text-xs text-slate-300">
              <span className="text-emerald-600 mt-0.5 flex-shrink-0">→</span>
              {h}
            </li>
          ))}
        </ul>
      </div>
    </article>
  );
}

interface Props {
  data: BenchmarkData;
}

export function BenchmarkingClient({ data }: Props) {
  const [selectedSize, setSelectedSize] = useState<CaseStudy["firmSize"] | "All">("All");
  const [selectedTech, setSelectedTech] = useState<string>("All");

  const uniqueTechs = ["All", ...Array.from(new Set(data.caseStudies.flatMap((s) => s.technologies)))];
  const uniqueSizes: (CaseStudy["firmSize"] | "All")[] = ["All", ...FIRM_SIZES.filter((size) =>
    data.caseStudies.some((s) => s.firmSize === size)
  )];

  const filtered = data.caseStudies.filter((s) => {
    const sizeMatch = selectedSize === "All" || s.firmSize === selectedSize;
    const techMatch = selectedTech === "All" || s.technologies.includes(selectedTech);
    return sizeMatch && techMatch;
  });

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4">
        <div>
          <label htmlFor="size-filter" className="text-xs text-slate-400 block mb-1">
            Filter by Firm Size
          </label>
          <div className="flex gap-1.5 flex-wrap" role="group" aria-label="Filter by firm size">
            {uniqueSizes.map((size) => (
              <button
                key={size}
                onClick={() => setSelectedSize(size)}
                className={`px-3 py-1 rounded-lg text-xs font-medium border transition-colors ${
                  selectedSize === size
                    ? "bg-emerald-900/40 border-emerald-600 text-emerald-300"
                    : "bg-slate-800 border-slate-700 text-slate-400 hover:border-slate-500 hover:text-slate-300"
                }`}
                aria-pressed={selectedSize === size}
              >
                {size}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label htmlFor="tech-filter" className="text-xs text-slate-400 block mb-1">
            Filter by Technology
          </label>
          <select
            id="tech-filter"
            value={selectedTech}
            onChange={(e) => setSelectedTech(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-300 text-xs rounded-lg px-3 py-1.5 focus:outline-none focus:border-emerald-600"
          >
            {uniqueTechs.map((tech) => (
              <option key={tech} value={tech}>
                {tech}
              </option>
            ))}
          </select>
        </div>

        <div className="ml-auto">
          <span className="text-xs text-slate-500">
            {filtered.length} of {data.caseStudies.length} case studies
          </span>
        </div>
      </div>

      {/* Case Study Cards */}
      {filtered.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((study) => (
            <CaseStudyCard key={study.id} study={study} />
          ))}
        </div>
      ) : (
        <div className="bg-slate-800 border border-slate-700 rounded-xl p-12 text-center">
          <p className="text-slate-400 text-sm">No case studies match your filters.</p>
          <button
            onClick={() => { setSelectedSize("All"); setSelectedTech("All"); }}
            className="mt-3 text-xs text-emerald-400 hover:text-emerald-300 underline"
          >
            Clear filters
          </button>
        </div>
      )}

      {/* Summary Table */}
      <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-white mb-4">Competitive Landscape Summary</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-xs" aria-label="Competitive landscape summary">
            <thead>
              <tr className="border-b border-slate-700">
                <th className="text-left py-2 pr-4 text-slate-400 font-medium">Company</th>
                <th className="text-left py-2 pr-4 text-slate-400 font-medium">Size</th>
                <th className="text-left py-2 pr-4 text-slate-400 font-medium">Revenue</th>
                <th className="text-left py-2 text-slate-400 font-medium">Primary Focus</th>
              </tr>
            </thead>
            <tbody>
              {data.caseStudies.map((s, i) => (
                <tr key={s.id} className={i % 2 === 0 ? "bg-slate-900/30" : ""}>
                  <td className="py-2.5 pr-4 font-medium text-white">{s.company}</td>
                  <td className="py-2.5 pr-4">
                    <span className={`text-xs font-medium px-1.5 py-0.5 rounded border ${SIZE_COLORS[s.firmSize] ?? "text-slate-400 border-slate-600"}`}>
                      {s.firmSize}
                    </span>
                  </td>
                  <td className="py-2.5 pr-4 text-slate-300">{s.annualRevenue}</td>
                  <td className="py-2.5 text-slate-300">{s.technologies.slice(0, 2).join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
