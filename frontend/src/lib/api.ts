import type { MatchReport, TailoredResume, UploadResponse } from '../types/api';

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api';

async function requestJson<T>(path: string, init: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed with ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function uploadResume(file: File): Promise<UploadResponse> {
  const form = new FormData();
  form.append('file', file);
  return requestJson<UploadResponse>('/upload-resume', {
    method: 'POST',
    body: form,
  });
}

export async function analyzeMatch(resumeId: string, jobDescription: string, resumeText?: string): Promise<MatchReport> {
  return requestJson<MatchReport>('/analyze-match', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resume_id: resumeId, resume_text: resumeText, job_description: jobDescription }),
  });
}

export async function exportReport(report: MatchReport, format: 'markdown' | 'docx'): Promise<Blob> {
  const response = await fetch(`${API_BASE}/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ report, format }),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? 'Export failed');
  }
  return response.blob();
}

export async function exportTailoredResume(
  resumeId: string,
  resumeText: string,
  jobDescription: string,
  format: 'markdown' | 'docx',
): Promise<Blob> {
  const response = await fetch(`${API_BASE}/export-tailored-resume`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_id: resumeId,
      resume_text: resumeText,
      job_description: jobDescription,
      format,
    }),
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? 'Tailored resume export failed');
  }
  return response.blob();
}

export async function getTailoredResumePreview(
  resumeId: string,
  resumeText: string,
  jobDescription: string,
): Promise<TailoredResume> {
  return requestJson<TailoredResume>('/tailored-resume', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      resume_id: resumeId,
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });
}
