"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface NavItem {
  href: string;
  label: string;
  icon: string;
  description: string;
}

const NAV_ITEMS: NavItem[] = [
  {
    href: "/",
    label: "Executive Summary",
    icon: "◈",
    description: "Key metrics & strategy",
  },
  {
    href: "/market-trends",
    label: "Market Trends",
    icon: "↗",
    description: "Adoption & growth data",
  },
  {
    href: "/technology",
    label: "Technology Comparison",
    icon: "⚙",
    description: "Solar, electric, green systems",
  },
  {
    href: "/financial",
    label: "Financial Analysis",
    icon: "$",
    description: "ROI calculator & scenarios",
  },
  {
    href: "/benchmarking",
    label: "Competitive Benchmarking",
    icon: "▣",
    description: "Peer case studies",
  },
  {
    href: "/regulatory",
    label: "Regulatory Incentives",
    icon: "✦",
    description: "Policies & tax credits",
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      className="w-64 min-h-screen bg-slate-900 border-r border-slate-800 flex flex-col"
      aria-label="Main navigation"
    >
      {/* Logo / Brand */}
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-emerald-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-sm font-bold">RE</span>
          </div>
          <div>
            <p className="text-white text-sm font-semibold leading-tight">
              RenewEnergy
            </p>
            <p className="text-slate-500 text-xs">Executive Dashboard</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4" aria-label="Dashboard sections">
        <ul className="space-y-1" role="list">
          {NAV_ITEMS.map((item) => {
            const isActive =
              item.href === "/"
                ? pathname === "/"
                : pathname.startsWith(item.href);

            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`group flex items-start gap-3 px-3 py-2.5 rounded-lg transition-all ${
                    isActive
                      ? "bg-emerald-900/40 border border-emerald-700/50 text-emerald-300"
                      : "text-slate-400 hover:bg-slate-800 hover:text-white border border-transparent"
                  }`}
                  aria-current={isActive ? "page" : undefined}
                >
                  <span
                    className={`mt-0.5 text-base w-5 text-center flex-shrink-0 ${
                      isActive ? "text-emerald-400" : "text-slate-500 group-hover:text-slate-300"
                    }`}
                    aria-hidden="true"
                  >
                    {item.icon}
                  </span>
                  <div className="min-w-0">
                    <p
                      className={`text-sm font-medium leading-tight ${
                        isActive ? "text-emerald-300" : ""
                      }`}
                    >
                      {item.label}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5 leading-tight">
                      {item.description}
                    </p>
                  </div>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-slate-800">
        <p className="text-xs text-slate-600 text-center">
          Data as of Q1 2025
        </p>
        <p className="text-xs text-slate-700 text-center mt-0.5">
          North American Construction
        </p>
      </div>
    </aside>
  );
}
