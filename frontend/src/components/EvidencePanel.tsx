import { AlertTriangle, CheckCircle2 } from 'lucide-react';
import type { EvidenceItem } from '../types/api';

type EvidencePanelProps = {
  items: EvidenceItem[];
};

export function EvidencePanel({ items }: EvidencePanelProps) {
  const visibleItems = items.slice(0, 16);

  return (
    <section className="rounded-md border border-line bg-white p-4">
      <div className="mb-3">
        <h3 className="text-base font-semibold">Evidence Map</h3>
        <p className="mt-1 text-sm text-slate-500">Matched keywords show resume evidence; gaps stay clearly labeled.</p>
      </div>
      <div className="grid gap-3 lg:grid-cols-2">
        {visibleItems.map((item) => {
          const isMatch = item.status === 'matched';
          return (
            <article key={`${item.status}-${item.keyword}`} className="rounded-md border border-line bg-slate-50 p-3">
              <div className="mb-2 flex items-center gap-2">
                {isMatch ? <CheckCircle2 size={16} className="text-emerald-700" /> : <AlertTriangle size={16} className="text-amber-700" />}
                <h4 className="text-sm font-semibold text-ink">{item.keyword}</h4>
                <span className={`rounded px-2 py-0.5 text-xs font-semibold ${isMatch ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                  {isMatch ? 'Evidence' : 'Gap'}
                </span>
              </div>
              <p className="text-sm leading-6 text-slate-600">{item.evidence ?? item.recommendation}</p>
            </article>
          );
        })}
      </div>
    </section>
  );
}

