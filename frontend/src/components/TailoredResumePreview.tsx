import { Download, ShieldCheck } from 'lucide-react';
import { CopyButton } from './CopyButton';
import type { TailoredResume } from '../types/api';

type TailoredResumePreviewProps = {
  resume: TailoredResume;
  exporting: boolean;
  onDownload: (format: 'markdown' | 'docx') => void;
};

export function TailoredResumePreview({ resume, exporting, onDownload }: TailoredResumePreviewProps) {
  const markdown = [
    `# ${resume.name}`,
    '',
    ...resume.section_suggestions.flatMap((section) => [
      `## ${section.section_title}`,
      ...section.suggested_lines.map((line) => (section.as_bullets ? `- ${line}` : line)),
      '',
    ]),
  ].join('\n');

  return (
    <section className="rounded-md border border-line bg-white p-4">
      <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-start lg:justify-between">
        <div>
          <h3 className="text-base font-semibold">Gap-Focused Tailored Resume Preview</h3>
          <p className="mt-1 text-sm leading-6 text-slate-600">
            {resume.preserved_format_note}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <CopyButton value={markdown} label="Copy tailored resume preview" />
          <button className="secondary-button" type="button" disabled={exporting} onClick={() => onDownload('docx')}>
            <Download size={16} />
            DOCX
          </button>
          <button className="secondary-button" type="button" disabled={exporting} onClick={() => onDownload('markdown')}>
            <Download size={16} />
            Markdown
          </button>
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
        <article className="rounded-md border border-line bg-slate-50 p-4">
          <div className="mb-4 border-b border-line pb-3">
            <h4 className="text-xl font-semibold text-ink">{resume.name}</h4>
            <p className="mt-1 text-sm font-semibold text-accent">Resume-format suggestions</p>
          </div>
          {resume.section_suggestions
            .filter((section) => !section.is_gap_plan)
            .map((section) => (
              <SectionPreview key={section.section_title} section={section} />
            ))}
        </article>

        <aside className="rounded-md border border-amber-200 bg-amber-50 p-4">
          <div className="mb-3 flex items-center gap-2 text-amber-900">
            <ShieldCheck size={18} />
            <h4 className="text-sm font-semibold">Truthfulness Review</h4>
          </div>
          <p className="mb-3 text-sm leading-6 text-amber-900">{resume.guardrail_warning}</p>
          <h5 className="mb-2 text-sm font-semibold text-amber-950">Genuine gaps not added to resume sections</h5>
          <ul className="space-y-2 text-sm leading-6 text-amber-950">
            {resume.gap_action_plan.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </aside>
      </div>
    </section>
  );
}

function SectionPreview({
  section,
}: {
  section: TailoredResume['section_suggestions'][number];
}) {
  if (!section.suggested_lines.length) return null;

  return (
    <div className="mb-4">
      <h5 className="mb-1 text-sm font-semibold text-slate-700">{section.section_title}</h5>
      <p className="mb-2 text-xs leading-5 text-slate-500">{section.note}</p>
      <ul className="space-y-1 text-sm leading-6 text-slate-700">
        {section.suggested_lines.map((item) =>
          section.as_bullets ? <li key={item}>- {item}</li> : <li key={item}>{item}</li>,
        )}
      </ul>
    </div>
  );
}
