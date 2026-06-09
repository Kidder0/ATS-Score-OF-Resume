export type KeywordAnalysis = {
  skills: string[];
  tools: string[];
  responsibilities: string[];
  education: string[];
  requirements: string[];
};

export type ScoreBreakdownItem = {
  category: string;
  weight: number;
  score: number;
  earned_points: number;
  matched: string[];
  missing: string[];
  rationale: string;
};

export type EvidenceItem = {
  keyword: string;
  status: 'matched' | 'gap' | string;
  evidence: string | null;
  recommendation: string;
};

export type UploadResponse = {
  resume_id: string;
  filename: string;
  text: string;
  preview: string;
  character_count: number;
};

export type MatchReport = {
  resume_id?: string | null;
  job_keywords: KeywordAnalysis;
  match_score: number;
  fit_level: string;
  score_breakdown: ScoreBreakdownItem[];
  evidence: EvidenceItem[];
  matched_keywords: string[];
  missing_keywords: string[];
  weak_keywords: string[];
  weak_areas: string[];
  recommendations: string[];
  rewritten_summary: string;
  rewritten_bullets: string[];
  cover_letter: string;
  guardrail_warning: string;
};

export type TailoredResume = {
  name: string;
  contact_lines: string[];
  target_title: string;
  summary: string;
  supported_keywords: string[];
  rewritten_bullets: string[];
  project_or_experience_lines: string[];
  education_lines: string[];
  match_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  weak_keywords: string[];
  weak_areas: string[];
  genuine_gaps: string[];
  guardrail_warning: string;
  gap_action_plan: string[];
  section_suggestions: Array<{
    section_title: string;
    original_lines?: string[];
    suggested_lines: string[];
    as_bullets: boolean;
    note: string;
    is_gap_plan?: boolean;
  }>;
  preserved_format_note: string;
};
