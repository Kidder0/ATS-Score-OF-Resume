import { Gauge } from 'lucide-react';
import type { MatchReport } from '../types/api';

type FitSummaryProps = {
  report: MatchReport;
};

export function FitSummary({ report }: FitSummaryProps) {
  const lostPoints = Math.max(0, 100 - report.match_score).toFixed(1);

  return (
    <div className="rounded-md border border-line bg-white p-5">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-md bg-accent text-white">
            <Gauge size={28} />
          </div>
          <div>
            <p className="section-title">Match Score</p>
            <div className="mt-1 flex flex-wrap items-baseline gap-2">
              <span className="text-5xl font-semibold text-accent">{report.match_score}</span>
              <span className="text-lg font-semibold text-slate-500">/ 100</span>
              <span className="rounded-md bg-slate-100 px-2 py-1 text-sm font-semibold text-slate-700">{report.fit_level}</span>
            </div>
          </div>
        </div>
        <div className="grid gap-2 text-sm text-slate-600 sm:grid-cols-3 lg:min-w-[460px]">
          <Metric label="Matched" value={report.matched_keywords.length.toString()} />
          <Metric label="Gaps" value={report.missing_keywords.length.toString()} />
          <Metric label="Points Lost" value={lostPoints} />
        </div>
      </div>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md border border-line bg-slate-50 px-3 py-2">
      <p className="text-xs font-semibold uppercase tracking-normal text-slate-500">{label}</p>
      <p className="mt-1 text-lg font-semibold text-ink">{value}</p>
    </div>
  );
}

