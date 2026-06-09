import { AlertCircle, Download, FileText, Loader2, Play, RefreshCcw, UploadCloud } from 'lucide-react';
import { DragEvent, useMemo, useState } from 'react';
import { analyzeMatch, exportReport, exportTailoredResume, getTailoredResumePreview, uploadResume } from './lib/api';
import { CopyButton } from './components/CopyButton';
import { EvidencePanel } from './components/EvidencePanel';
import { FitSummary } from './components/FitSummary';
import { KeywordCategories } from './components/KeywordCategories';
import { KeywordList } from './components/KeywordList';
import { ScoreBreakdown } from './components/ScoreBreakdown';
import { TailoredResumePreview } from './components/TailoredResumePreview';
import type { MatchReport, TailoredResume, UploadResponse } from './types/api';

const SAMPLE_RESUME = `Rakesh Candidate

Entry-level AI Engineer with hands-on project experience building AI-powered web applications.

Skills
- Python, TypeScript, JavaScript, SQL
- React, FastAPI, SQLite, GitHub
- OpenAI API, prompt engineering, GenAI, RAG, vector search
- pandas, NumPy, scikit-learn, model evaluation

Projects
- Built a GenAI RAG knowledge assistant using Python, FastAPI, React, OpenAI, Chroma, and document parsing to answer grounded questions from uploaded files.
- Developed an AI resume analyzer that extracts resume text, compares it with job descriptions, and produces ATS-style recommendations.
- Implemented prompt templates, response validation, and guardrails to reduce unsupported LLM claims.

Education
Bachelor of Science in Computer Science`;

const SAMPLE_JD = `Entry-Level AI Engineer / GenAI Developer

Responsibilities:
- Build GenAI and RAG applications using Python, FastAPI, React, OpenAI, and vector search.
- Develop prompt engineering workflows and evaluate LLM responses for accuracy and safety.
- Integrate APIs, maintain SQL-backed application data, and collaborate with product teams.

Requirements:
- Hands-on Python and JavaScript or TypeScript experience.
- Exposure to LangChain, Hugging Face, Chroma, or FAISS preferred.
- Bachelor's degree in Computer Science, Data Science, AI, or related field preferred.`;

function App() {
  const [resume, setResume] = useState<UploadResponse | null>(null);
  const [jobDescription, setJobDescription] = useState(SAMPLE_JD);
  const [report, setReport] = useState<MatchReport | null>(null);
  const [tailoredResume, setTailoredResume] = useState<TailoredResume | null>(null);
  const [isUploading, setUploading] = useState(false);
  const [isAnalyzing, setAnalyzing] = useState(false);
  const [isExporting, setExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canAnalyze = Boolean(resume?.resume_id && jobDescription.trim().length > 40 && !isAnalyzing);
  const reportMarkdown = useMemo(() => {
    if (!report) return '';
    return [
      report.rewritten_summary,
      '',
      ...report.rewritten_bullets.map((bullet) => `- ${bullet}`),
      '',
      report.cover_letter,
    ].join('\n');
  }, [report]);

  function handleUseSampleResume() {
    const sample: UploadResponse = {
      resume_id: 'sample-resume',
      filename: 'sample-entry-level-ai-engineer.md',
      text: SAMPLE_RESUME,
      preview: SAMPLE_RESUME.slice(0, 1200),
      character_count: SAMPLE_RESUME.length,
    };
    setResume(sample);
    setReport(null);
    setTailoredResume(null);
    setError(null);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    handleUpload(event.dataTransfer.files?.[0] ?? null);
  }

  async function handleUpload(file: File | null) {
    if (!file) return;
    setError(null);
    setReport(null);
    setTailoredResume(null);
    setUploading(true);
    try {
      setResume(await uploadResume(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Resume upload failed');
    } finally {
      setUploading(false);
    }
  }

  async function handleAnalyze() {
    if (!resume) return;
    setError(null);
    setAnalyzing(true);
    try {
      const [nextReport, nextTailoredResume] = await Promise.all([
        analyzeMatch(resume.resume_id, jobDescription, resume.text),
        getTailoredResumePreview(resume.resume_id, resume.text, jobDescription),
      ]);
      setReport(nextReport);
      setTailoredResume(nextTailoredResume);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  }

  function handleReset() {
    setResume(null);
    setReport(null);
    setTailoredResume(null);
    setError(null);
    setJobDescription(SAMPLE_JD);
  }

  async function handleExport(format: 'markdown' | 'docx') {
    if (!report) return;
    setError(null);
    setExporting(true);
    try {
      const blob = await exportReport(report, format);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `ai-resume-match-report.${format === 'markdown' ? 'md' : 'docx'}`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    } finally {
      setExporting(false);
    }
  }

  async function handleTailoredResumeExport(format: 'markdown' | 'docx') {
    if (!resume) return;
    setError(null);
    setExporting(true);
    try {
      const blob = await exportTailoredResume(resume.resume_id, resume.text, jobDescription, format);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `tailored-resume.${format === 'markdown' ? 'md' : 'docx'}`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Tailored resume export failed');
    } finally {
      setExporting(false);
    }
  }

  return (
    <main className="min-h-screen bg-panel text-ink">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-5 sm:px-6 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-2xl font-semibold">AI Resume & Job Matcher</h1>
            <p className="mt-1 text-sm text-slate-600">
              Grounded ATS scoring and tailored resume guidance for AI, GenAI, and LLM app roles.
            </p>
          </div>
          <div className="flex items-center gap-2 rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
            <AlertCircle size={16} />
            <span>Do not invent experience.</span>
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-5 px-4 py-5 sm:px-6 lg:grid-cols-[360px_minmax(0,1fr)]">
        <aside className="space-y-4">
          <section className="rounded-md border border-line bg-white p-4">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-base font-semibold">Resume</h2>
              <FileText size={18} className="text-slate-500" />
            </div>
            <label
              className="flex min-h-36 cursor-pointer flex-col items-center justify-center rounded-md border border-dashed border-line bg-slate-50 px-4 py-5 text-center transition hover:border-accent"
              onDragOver={(event) => event.preventDefault()}
              onDrop={handleDrop}
            >
              {isUploading ? (
                <Loader2 size={28} className="animate-spin text-accent" />
              ) : (
                <UploadCloud size={30} className="text-accent" />
              )}
              <span className="mt-3 text-sm font-semibold">Upload PDF or DOCX</span>
              <span className="mt-1 text-xs text-slate-500">Drop a file here or browse. Maximum file size: 8 MB</span>
              <input
                className="sr-only"
                type="file"
                accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={(event) => handleUpload(event.target.files?.[0] ?? null)}
              />
            </label>
            <div className="mt-3 flex gap-2">
              <button className="secondary-button flex-1" type="button" onClick={handleUseSampleResume}>
                <FileText size={16} />
                Sample
              </button>
              <button className="secondary-button flex-1" type="button" onClick={handleReset}>
                <RefreshCcw size={16} />
                Reset
              </button>
            </div>
            {resume && (
              <div className="mt-4 rounded-md border border-line bg-slate-50 p-3">
                <p className="text-sm font-semibold">{resume.filename}</p>
                <p className="mt-1 text-xs text-slate-500">{resume.character_count.toLocaleString()} characters parsed</p>
              </div>
            )}
          </section>

          <section className="rounded-md border border-line bg-white p-4">
            <h2 className="mb-3 text-base font-semibold">Parsed Preview</h2>
            <div className="max-h-[460px] overflow-auto rounded-md border border-line bg-slate-50 p-3 text-sm leading-6 text-slate-700">
              {resume?.preview ?? 'Upload a resume to preview extracted text.'}
            </div>
          </section>
        </aside>

        <section className="space-y-5">
          {error && (
            <div className="rounded-md border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-800">{error}</div>
          )}

          <section className="rounded-md border border-line bg-white p-4">
            <div className="mb-3 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-base font-semibold">Job Description</h2>
                <p className="mt-1 text-sm text-slate-500">Paste the target role description and run the matcher.</p>
              </div>
              <div className="flex gap-2">
                <button className="secondary-button" type="button" onClick={() => setJobDescription(SAMPLE_JD)}>
                  <RefreshCcw size={16} />
                  Sample JD
                </button>
                <button className="primary-button" type="button" disabled={!canAnalyze} onClick={handleAnalyze}>
                  {isAnalyzing ? <Loader2 size={16} className="animate-spin" /> : <Play size={16} />}
                  Analyze
                </button>
              </div>
            </div>
            <textarea
              className="min-h-72 w-full rounded-md border border-line bg-slate-50 p-3 text-sm leading-6 outline-none transition focus:border-accent focus:bg-white"
              value={jobDescription}
              onChange={(event) => setJobDescription(event.target.value)}
            />
          </section>

          {isAnalyzing && (
            <section className="rounded-md border border-line bg-white p-6">
              <div className="flex items-center gap-3 text-sm text-slate-600">
                <Loader2 size={18} className="animate-spin text-accent" />
                Extracting keywords, scoring ATS alignment, and generating grounded recommendations.
              </div>
            </section>
          )}

          {report && (
            <section className="space-y-5">
              <div className="rounded-md border border-line bg-white p-4">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <p className="rounded-md border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-amber-900">
                    {report.guardrail_warning}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <button className="secondary-button" type="button" disabled={isExporting} onClick={() => handleTailoredResumeExport('docx')}>
                      <Download size={16} />
                      Tailored Resume
                    </button>
                    <button className="secondary-button" type="button" disabled={isExporting} onClick={() => handleTailoredResumeExport('markdown')}>
                      <Download size={16} />
                      Resume MD
                    </button>
                    <button className="secondary-button" type="button" disabled={isExporting} onClick={() => handleExport('markdown')}>
                      <Download size={16} />
                      Report MD
                    </button>
                    <button className="secondary-button" type="button" disabled={isExporting} onClick={() => handleExport('docx')}>
                      <Download size={16} />
                      Report DOCX
                    </button>
                  </div>
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-600">
                  Tailored resume downloads add only resume-supported keywords and bullets. Genuine gaps are kept in a truthfulness review instead of being inserted as fake experience.
                </p>
              </div>

              <FitSummary report={report} />
              <ScoreBreakdown items={report.score_breakdown} />
              <KeywordCategories keywords={report.job_keywords} />

              <div className="grid gap-4 lg:grid-cols-3">
                <KeywordList title="Matched Keywords" items={report.matched_keywords} />
                <KeywordList title="Missing Keywords" items={report.missing_keywords} tone="missing" />
                <KeywordList title="Weak Keywords" items={report.weak_keywords} tone="weak" />
              </div>

              <EvidencePanel items={report.evidence} />
              {tailoredResume && (
                <TailoredResumePreview
                  resume={tailoredResume}
                  exporting={isExporting}
                  onDownload={handleTailoredResumeExport}
                />
              )}
              <GeneratedSection title="Tailored Professional Summary" value={report.rewritten_summary} />
              <GeneratedSection title="Rewritten Resume Bullets" value={report.rewritten_bullets.map((bullet) => `- ${bullet}`).join('\n')} />
              <GeneratedSection title="Short Tailored Cover Letter" value={report.cover_letter} />
              <GeneratedSection title="Recommendations" value={report.recommendations.map((item) => `- ${item}`).join('\n')} />

              <div className="sr-only" aria-live="polite">
                {reportMarkdown}
              </div>
            </section>
          )}
        </section>
      </div>
    </main>
  );
}

function GeneratedSection({ title, value }: { title: string; value: string }) {
  return (
    <section className="rounded-md border border-line bg-white p-4">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-base font-semibold">{title}</h3>
        <CopyButton value={value} label={`Copy ${title}`} />
      </div>
      <pre className="whitespace-pre-wrap rounded-md border border-line bg-slate-50 p-3 text-sm leading-6 text-slate-700">{value}</pre>
    </section>
  );
}

export default App;
