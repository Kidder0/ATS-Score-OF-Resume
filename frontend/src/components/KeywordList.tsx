type KeywordListProps = {
  title: string;
  items: string[];
  tone?: 'matched' | 'missing' | 'weak';
};

export function KeywordList({ title, items, tone = 'matched' }: KeywordListProps) {
  const toneClass =
    tone === 'matched'
      ? 'border-emerald-200 bg-emerald-50 text-emerald-800'
      : tone === 'weak'
        ? 'border-amber-200 bg-amber-50 text-amber-800'
        : 'border-rose-200 bg-rose-50 text-rose-800';

  return (
    <section className="min-h-40">
      <h3 className="section-title mb-3">{title}</h3>
      <div className="flex flex-wrap gap-2">
        {items.length ? (
          items.map((item) => (
            <span key={item} className={`rounded-md border px-2.5 py-1 text-sm ${toneClass}`}>
              {item}
            </span>
          ))
        ) : (
          <p className="text-sm text-slate-500">None detected</p>
        )}
      </div>
    </section>
  );
}

