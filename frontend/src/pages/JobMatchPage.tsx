/**
 * JobMatchPage — compare a job description against an uploaded resume.
 *
 * Provides:
 *  - Job description text input area
 *  - Resume selection dropdown (defaults to latest)
 *  - Overall fit, skill match, and TF-IDF semantic similarity gauges
 *  - Skill breakdown chips (matched, missing, bonus)
 *  - Actionable preparation recommendations
 *  - Transparent method provenance (method_map)
 */
import { useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { ScoreGauge } from '@/components/ui/Charts'

export default function JobMatchPage() {
  const [jdText, setJdText] = useState('')
  const [roleTitle, setRoleTitle] = useState('')
  const [resumeId, setResumeId] = useState('')

  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: api.listResumes,
  })

  const matchMutation = useMutation({
    mutationFn: () =>
      api.matchJobDescription({
        jd_text: jdText.trim(),
        role_title: roleTitle.trim() || undefined,
        resume_id: resumeId || undefined,
      }),
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!jdText.trim()) return
    matchMutation.mutate()
  }

  const result = matchMutation.data

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Job Match & Skill Gap Analysis</h1>
        <p className="mt-1 text-sm text-slate-500">
          Paste a Job Description to compare required skills and semantic fit against your resume.
        </p>
      </div>

      {/* Input Form */}
      <div className="card">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid gap-4 sm:grid-cols-2">
            <div>
              <label htmlFor="role_title" className="label">Target Role Title (optional)</label>
              <input
                id="role_title"
                type="text"
                placeholder="e.g. Senior Python Developer"
                className="input"
                value={roleTitle}
                onChange={(e) => setRoleTitle(e.target.value)}
              />
            </div>

            <div>
              <label htmlFor="resume_id" className="label">Select Resume</label>
              {resumes && resumes.length > 0 ? (
                <select
                  id="resume_id"
                  className="input"
                  value={resumeId}
                  onChange={(e) => setResumeId(e.target.value)}
                >
                  <option value="">Latest Uploaded Resume</option>
                  {resumes.map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.original_filename}
                    </option>
                  ))}
                </select>
              ) : (
                <div className="text-sm text-slate-500 py-2">
                  No resume uploaded.{' '}
                  <Link to="/resumes" className="font-medium text-brand-600 underline">
                    Upload a PDF resume first
                  </Link>
                </div>
              )}
            </div>
          </div>

          <div>
            <label htmlFor="jd_text" className="label">Job Description Text</label>
            <textarea
              id="jd_text"
              rows={6}
              required
              minLength={20}
              placeholder="Paste the full job description here (responsibilities, required qualifications, skills)..."
              className="input font-sans text-sm"
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400">
              {jdText.trim().length} characters
            </span>
            <button
              type="submit"
              disabled={matchMutation.isPending || !jdText.trim() || resumes?.length === 0}
              className="btn-primary"
            >
              {matchMutation.isPending ? 'Analyzing Fit…' : 'Analyze Job Match'}
            </button>
          </div>

          {matchMutation.isError && (
            <div className="rounded-lg bg-bad-100 p-3 text-sm text-bad-500">
              {matchMutation.error instanceof api.ApiError
                ? matchMutation.error.detail
                : 'Failed to analyze job match'}
            </div>
          )}
        </form>
      </div>

      {/* Analysis Result */}
      {result && (
        <div className="space-y-6">
          {/* Headline Score Gauges */}
          <div className="card">
            <h2 className="mb-4 text-lg font-semibold text-slate-900">Match Overview</h2>
            <div className="flex flex-wrap items-center justify-around gap-6">
              <ScoreGauge score={result.overall_fit_score} label="Overall Fit" size={130} />
              <ScoreGauge score={result.skill_gap.skill_match_percentage} label="Skill Coverage" size={130} />
              <ScoreGauge score={result.semantic_similarity_score} label="TF-IDF Semantic Fit" size={130} />
            </div>
          </div>

          {/* Skill Breakdown */}
          <div className="grid gap-6 sm:grid-cols-3">
            {/* Matched */}
            <div className="card border-l-4 border-l-good-500">
              <h3 className="mb-2 font-semibold text-good-500">
                ✓ Matched Skills ({result.skill_gap.matched_skills.length})
              </h3>
              {result.skill_gap.matched_skills.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {result.skill_gap.matched_skills.map((s) => (
                    <span key={s} className="rounded-full bg-good-100 px-2.5 py-0.5 text-xs font-medium text-good-500">
                      {s}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">No overlapping skills detected.</p>
              )}
            </div>

            {/* Missing */}
            <div className="card border-l-4 border-l-bad-500">
              <h3 className="mb-2 font-semibold text-bad-500">
                ✕ Missing Skills ({result.skill_gap.missing_skills.length})
              </h3>
              {result.skill_gap.missing_skills.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {result.skill_gap.missing_skills.map((s) => (
                    <span key={s} className="rounded-full bg-bad-100 px-2.5 py-0.5 text-xs font-medium text-bad-500">
                      {s}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">All required skills present on resume!</p>
              )}
            </div>

            {/* Bonus */}
            <div className="card border-l-4 border-l-brand-500">
              <h3 className="mb-2 font-semibold text-brand-600">
                + Bonus Skills ({result.skill_gap.bonus_skills.length})
              </h3>
              {result.skill_gap.bonus_skills.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {result.skill_gap.bonus_skills.map((s) => (
                    <span key={s} className="rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-medium text-brand-700">
                      {s}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-400">No additional skills.</p>
              )}
            </div>
          </div>

          {/* Recommendations */}
          {result.recommendations.length > 0 && (
            <div className="card">
              <h3 className="mb-3 font-semibold text-slate-900">💡 Preparation Recommendations</h3>
              <ul className="list-inside list-disc space-y-1.5 text-sm text-slate-700">
                {result.recommendations.map((rec, i) => (
                  <li key={i}>{rec}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Provenance Map */}
          <div className="rounded-lg bg-slate-100 p-4 text-xs text-slate-600">
            <span className="font-semibold text-slate-700">Method Provenance:</span>{' '}
            {Object.entries(result.method_map)
              .map(([k, v]) => `${k}=${v}`)
              .join(' · ')}
          </div>
        </div>
      )}
    </div>
  )
}
