import type { ScoreBreakdownItem } from '../types/api';

type ScoreBreakdownProps = {
  items: ScoreBreakdownItem[];
};

export function ScoreBreakdown({ items }: ScoreBreakdownProps) {
  return (
    <section>
      <h3 className="section-title mb-3">Transparent Scoring</h3>
      <div className="grid gap-3 md:grid-cols-2">
        {items.map((item) => (
          <article key={item.category} className="rounded-md border border-line bg-white p-4">
            <div className="mb-3 flex items-center justify-between gap-3">
              <h4 className="text-sm font-semibold text-ink">{item.category}</h4>
              <span className="text-sm font-semibold text-accent">
                {item.earned_points}/{item.weight}
              </span>
            </div>
            <div className="mb-3 h-2 rounded-full bg-slate-100">
              <div className="h-2 rounded-full bg-accent" style={{ width: `${Math.min(item.score * 100, 100)}%` }} />
            </div>
            <p className="text-sm leading-6 text-slate-600">{item.rationale}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

