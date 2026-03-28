"use client";

interface NavBarProps {
  title: string;
  subtitle?: string;
}

export function NavBar({ title, subtitle }: NavBarProps) {
  return (
    <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-lg font-semibold text-white">{title}</h1>
        {subtitle && (
          <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>
        )}
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs text-slate-500 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">
          Q1 2025 Research
        </span>
        <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" aria-label="Live data indicator" />
      </div>
    </header>
  );
}
