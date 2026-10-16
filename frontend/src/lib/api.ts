/**
 * Typed API client — one place that handles every backend call.
 *
 * Why not axios? `fetch` is built into every modern browser and the edge
 * runtime.  We only need JSON + auth headers, so a thin wrapper is cleaner
 * than pulling in a 40 kB dependency.
 *
 * Every function here returns typed data or throws an `ApiError`. That means
 * callers can just `const data = await login(email, password)` — the error
 * path is handled by TanStack Query's `onError` in the UI layer.
 */

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------

export class ApiError extends Error {
  status: number
  detail: string

  constructor(status: number, detail: string) {
    super(detail)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

// ---------------------------------------------------------------------------
// Core fetch wrapper
// ---------------------------------------------------------------------------

/**
 * API base URL.  In development Vite proxies `/api` to the FastAPI backend, so
 * an empty string works.  In production (Render static site) the env var
 * `VITE_API_URL` points to the backend's public URL.
 */
const API_BASE = import.meta.env.VITE_API_URL ?? ''

/** A token getter injected by AuthContext so this module stays stateless. */
let _getToken: (() => string | null) | null = null

export function setTokenGetter(fn: () => string | null) {
  _getToken = fn
}

async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string>),
  }

  // Don't set Content-Type for FormData (browser sets multipart boundary).
  if (!(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  const token = _getToken?.()
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const url = `${API_BASE}${path}`
  const response = await fetch(url, { ...options, headers })

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`
    try {
      const body = await response.json()
      detail = body.detail ?? detail
    } catch {
      // non-JSON error body — keep the generic message
    }
    throw new ApiError(response.status, detail)
  }

  // 204 No Content returns no body
  if (response.status === 204) return undefined as T

  return response.json() as Promise<T>
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UserResponse {
  id: string
  email: string
  is_active: boolean
  created_at: string
}

export function register(email: string, password: string) {
  return request<TokenResponse>('/api/v1/auth/register', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function login(email: string, password: string) {
  return request<TokenResponse>('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
}

export function getMe() {
  return request<UserResponse>('/api/v1/auth/me')
}

// ---------------------------------------------------------------------------
// Profile
// ---------------------------------------------------------------------------

export interface ProfileResponse {
  id: string
  user_id: string
  full_name: string
  target_role: string
  experience_level: string
  bio: string | null
}

export interface ProfilePayload {
  full_name: string
  target_role: string
  experience_level: string
  bio?: string
}

export function getProfile() {
  return request<ProfileResponse>('/api/v1/profile')
}

export function createProfile(data: ProfilePayload) {
  return request<ProfileResponse>('/api/v1/profile', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function updateProfile(data: Partial<ProfilePayload>) {
  return request<ProfileResponse>('/api/v1/profile', {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

// ---------------------------------------------------------------------------
// Resume
// ---------------------------------------------------------------------------

export interface ResumeResponse {
  id: string
  original_filename: string
  uploaded_at: string
}

export interface ResumeDetailResponse extends ResumeResponse {
  raw_text: string
  parsed_data: {
    name: string | null
    email: string | null
    phone: string | null
    skills: string[]
    sections: Record<string, string>
  }
  parse_method: string
}

export function uploadResume(file: File) {
  const form = new FormData()
  form.append('file', file)
  return request<ResumeDetailResponse>('/api/v1/resumes', {
    method: 'POST',
    body: form,
  })
}

export function listResumes() {
  return request<ResumeResponse[]>('/api/v1/resumes')
}

export function getResume(id: string) {
  return request<ResumeDetailResponse>(`/api/v1/resumes/${id}`)
}

// ---------------------------------------------------------------------------
// Interview
// ---------------------------------------------------------------------------

export interface InterviewResponse {
  id: string
  role: string
  interview_type: string
  starting_difficulty: string
  current_difficulty: string
  target_question_count: number
  status: string
  created_at: string
  completed_at: string | null
  questions: QuestionResponse[]
}

export interface QuestionResponse {
  id: string
  position: number
  prompt: string
  topic: string | null
  difficulty: string
  question_type: string
  source: string
  concepts: string[]
}

export interface InterviewCreatePayload {
  role: string
  interview_type: string
  difficulty?: string
  question_count?: number
  resume_id?: string
}

export function createInterview(data: InterviewCreatePayload) {
  return request<InterviewResponse>('/api/v1/interviews', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function listInterviews() {
  return request<InterviewResponse[]>('/api/v1/interviews')
}

export function getInterview(id: string) {
  return request<InterviewResponse>(`/api/v1/interviews/${id}`)
}

export function nextQuestion(interviewId: string) {
  return request<QuestionResponse>(
    `/api/v1/interviews/${interviewId}/next`,
    { method: 'POST' },
  )
}

export function completeInterview(interviewId: string) {
  return request<InterviewResponse>(
    `/api/v1/interviews/${interviewId}/complete`,
    { method: 'POST' },
  )
}

// ---------------------------------------------------------------------------
// Answer & Evaluation
// ---------------------------------------------------------------------------

export interface TextFeatures {
  word_count: number
  sentence_count: number
  average_sentence_length: number
  filler_total: number
  filler_ratio: number
  filler_breakdown: Record<string, number>
  repeated_word_ratio: number
  repeated_phrases: string[]
}

export interface EvaluationResponse {
  id: string
  overall_score: number | null
  relevance_score: number | null
  technical_accuracy_score: number | null
  completeness_score: number | null
  communication_score: number | null
  structure_score: number | null
  specificity_score: number | null
  strengths: string[]
  weaknesses: string[]
  suggestions: string[]
  star_evaluation: {
    situation_score: number
    task_score: number
    action_score: number
    result_score: number
    total_score: number
    feedback: string[]
  } | null
  text_features: TextFeatures
  method_map: Record<string, string>
}

export interface AnswerWithEvaluationResponse {
  answer_id: string
  content: string
  word_count: number
  evaluation: EvaluationResponse
}

export function submitAnswer(
  interviewId: string,
  questionId: string,
  content: string,
) {
  return request<AnswerWithEvaluationResponse>(
    `/api/v1/interviews/${interviewId}/questions/${questionId}/answers`,
    { method: 'POST', body: JSON.stringify({ content }) },
  )
}

// ---------------------------------------------------------------------------
// Report — full Q&A dump for one interview
// ---------------------------------------------------------------------------

export interface QuestionReportItem {
  question: QuestionResponse
  answer_content: string | null
  answer_word_count: number | null
  evaluation: EvaluationResponse | null
}

export interface ReportSummary {
  questions_asked: number
  questions_answered: number
  average_overall_score: number | null
  average_communication_score: number | null
  average_technical_accuracy_score: number | null
  average_word_count: number | null
  total_filler_count: number
  average_filler_ratio: number | null
  difficulty_progression: string[]
  strengths_summary: string[]
  weaknesses_summary: string[]
}

export interface InterviewReportResponse {
  interview: InterviewResponse
  items: QuestionReportItem[]
  summary: ReportSummary
}

export function getInterviewReport(id: string) {
  return request<InterviewReportResponse>(`/api/v1/interviews/${id}/report`)
}

// ---------------------------------------------------------------------------
// Analytics — cross-interview aggregates
// ---------------------------------------------------------------------------

export interface InterviewHistoryItem {
  interview_id: string
  role: string
  interview_type: string
  difficulty: string
  status: string
  created_at: string
  questions_asked: number
  questions_answered: number
  average_overall_score: number | null
  average_word_count: number | null
}

export interface AnalyticsSummaryResponse {
  total_interviews: number
  completed_interviews: number
  total_questions_answered: number
  total_practice_time_estimate_minutes: number
  average_overall_score: number | null
  score_trend: (number | null)[]
  strongest_topics: string[]
  weakest_topics: string[]
  difficulty_distribution: Record<string, number>
  interview_type_distribution: Record<string, number>
  history: InterviewHistoryItem[]
}

export function getAnalyticsSummary() {
  return request<AnalyticsSummaryResponse>('/api/v1/analytics/summary')
}

// ---------------------------------------------------------------------------
// Job Matching & Skill Gap Analysis
// ---------------------------------------------------------------------------

export interface SkillGapAnalysis {
  matched_skills: string[]
  missing_skills: string[]
  bonus_skills: string[]
  skill_match_percentage: number
}

export interface JobMatchResponse {
  resume_id: string
  role_title: string | null
  extracted_jd_skills: string[]
  extracted_resume_skills: string[]
  skill_gap: SkillGapAnalysis
  semantic_similarity_score: number
  overall_fit_score: number
  recommendations: string[]
  method_map: Record<string, string>
}

export interface JobMatchPayload {
  jd_text: string
  resume_id?: string
  role_title?: string
}

export function matchJobDescription(data: JobMatchPayload) {
  return request<JobMatchResponse>('/api/v1/job-match', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

// ---------------------------------------------------------------------------
// Voice Analytics
// ---------------------------------------------------------------------------

export interface VoiceAnalysisResponse {
  speaking_pace_wpm: number
  pace_status: 'too_slow' | 'optimal' | 'too_fast'
  estimated_pauses: number
  clarity_score: number
  text_features: TextFeatures
  method_map: Record<string, string>
}

export function analyzeVoice(transcript: string, durationSeconds: number) {
  return request<VoiceAnalysisResponse>('/api/v1/voice/analyze', {
    method: 'POST',
    body: JSON.stringify({ transcript, duration_seconds: durationSeconds }),
  })
}

// ---------------------------------------------------------------------------
// ML Difficulty Classifier
// ---------------------------------------------------------------------------

export interface DifficultyPredictResponse {
  prompt: string
  predicted_difficulty: 'beginner' | 'intermediate' | 'advanced'
  confidence: number
  class_probabilities: Record<string, number>
  method: string
}

export function predictDifficulty(prompt: string) {
  return request<DifficultyPredictResponse>('/api/v1/ml/predict-difficulty', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  })
}
