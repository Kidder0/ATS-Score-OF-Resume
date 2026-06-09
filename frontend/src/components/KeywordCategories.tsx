import type { KeywordAnalysis } from '../types/api';

type KeywordCategoriesProps = {
  keywords: KeywordAnalysis;
};

const LABELS: Array<[keyof KeywordAnalysis, string]> = [
  ['skills', 'Skills'],
  ['tools', 'Tools'],
  ['responsibilities', 'Responsibilities'],
  ['education', 'Education'],
  ['requirements', 'Requirements'],
];

export function KeywordCategories({ keywords }: KeywordCategoriesProps) {
  return (
    <section className="rounded-md border border-line bg-white p-4">
      <h3 className="mb-3 text-base font-semibold">Extracted Job Signals</h3>
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-5">
        {LABELS.map(([key, label]) => (
          <div key={key} className="rounded-md border border-line bg-slate-50 p-3">
            <h4 className="mb-2 text-sm font-semibold text-slate-700">{label}</h4>
            <ul className="space-y-1 text-sm leading-5 text-slate-600">
              {keywords[key].length ? (
                keywords[key].slice(0, 6).map((item) => <li key={item}>{item}</li>)
              ) : (
                <li className="text-slate-400">None detected</li>
              )}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}

