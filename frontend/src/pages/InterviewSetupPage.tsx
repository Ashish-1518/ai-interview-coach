/**
 * InterviewSetupPage — form to start a new interview session.
 *
 * The user picks a role, interview type, difficulty, and question count, then
 * hits "Start Interview". This calls POST /api/v1/interviews, and on success
 * we navigate to the live interview page.
 */
import { useState, type FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'

const ROLES = [
  'Python Developer',
  'Backend Developer',
  'Frontend Developer',
  'Full Stack Developer',
  'Data Scientist',
]

const INTERVIEW_TYPES = [
  { value: 'technical', label: 'Technical', description: 'Data structures, algorithms, system design' },
  { value: 'behavioral', label: 'Behavioral', description: 'STAR-format situational questions' },
  { value: 'mixed', label: 'Mixed', description: 'Both technical and behavioral' },
]

const DIFFICULTIES = [
  { value: 'beginner', label: 'Beginner', description: 'Fundamentals and basics' },
  { value: 'intermediate', label: 'Intermediate', description: 'Applied concepts' },
  { value: 'advanced', label: 'Advanced', description: 'Complex scenarios' },
]

export default function InterviewSetupPage() {
  const navigate = useNavigate()
  const [role, setRole] = useState(ROLES[0])
  const [type, setType] = useState('technical')
  const [difficulty, setDifficulty] = useState('intermediate')
  const [count, setCount] = useState(5)
  const [resumeId, setResumeId] = useState('')

  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: api.listResumes,
  })

  const mutation = useMutation({
    mutationFn: () =>
      api.createInterview({
        role,
        interview_type: type,
        difficulty,
        question_count: count,
        resume_id: resumeId || undefined,
      }),
    onSuccess: (interview) => navigate(`/interviews/${interview.id}/live`),
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    mutation.mutate()
  }

  return (
    <div className="mx-auto max-w-xl">
      <h1 className="mb-6 text-2xl font-bold text-slate-900">
        Start New Interview
      </h1>

      {mutation.isError && (
        <div className="mb-4 rounded-lg bg-bad-100 px-3 py-2 text-sm text-bad-500">
          {mutation.error instanceof api.ApiError
            ? mutation.error.detail
            : 'Failed to create interview'}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Role */}
        <div>
          <label htmlFor="role" className="label">Target Role</label>
          <select
            id="role"
            className="input"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            {ROLES.map((r) => <option key={r}>{r}</option>)}
          </select>
        </div>

        {/* Interview type */}
        <fieldset>
          <legend className="label">Interview Type</legend>
          <div className="mt-1 grid gap-2 sm:grid-cols-3">
            {INTERVIEW_TYPES.map((t) => (
              <label
                key={t.value}
                className={`card cursor-pointer text-center transition-colors ${
                  type === t.value
                    ? 'border-brand-500 ring-1 ring-brand-500'
                    : 'hover:border-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="type"
                  value={t.value}
                  checked={type === t.value}
                  onChange={() => setType(t.value)}
                  className="sr-only"
                />
                <p className="font-medium text-slate-900">{t.label}</p>
                <p className="mt-1 text-xs text-slate-500">{t.description}</p>
              </label>
            ))}
          </div>
        </fieldset>

        {/* Difficulty */}
        <fieldset>
          <legend className="label">Starting Difficulty</legend>
          <div className="mt-1 grid gap-2 sm:grid-cols-3">
            {DIFFICULTIES.map((d) => (
              <label
                key={d.value}
                className={`card cursor-pointer text-center transition-colors ${
                  difficulty === d.value
                    ? 'border-brand-500 ring-1 ring-brand-500'
                    : 'hover:border-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="difficulty"
                  value={d.value}
                  checked={difficulty === d.value}
                  onChange={() => setDifficulty(d.value)}
                  className="sr-only"
                />
                <p className="font-medium text-slate-900">{d.label}</p>
                <p className="mt-1 text-xs text-slate-500">{d.description}</p>
              </label>
            ))}
          </div>
        </fieldset>

        {/* Question count */}
        <div>
          <label htmlFor="count" className="label">
            Number of Questions ({count})
          </label>
          <input
            id="count"
            type="range"
            min={1}
            max={20}
            value={count}
            onChange={(e) => setCount(Number(e.target.value))}
            className="w-full accent-brand-600"
          />
          <div className="flex justify-between text-xs text-slate-400">
            <span>1</span>
            <span>20</span>
          </div>
        </div>

        {/* Resume (optional) */}
        {resumes && resumes.length > 0 && (
          <div>
            <label htmlFor="resume" className="label">
              Link Resume (optional)
            </label>
            <select
              id="resume"
              className="input"
              value={resumeId}
              onChange={(e) => setResumeId(e.target.value)}
            >
              <option value="">None</option>
              {resumes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.original_filename}
                </option>
              ))}
            </select>
          </div>
        )}

        <button
          type="submit"
          disabled={mutation.isPending}
          className="btn-primary w-full"
        >
          {mutation.isPending ? 'Setting up…' : 'Start Interview'}
        </button>
      </form>
    </div>
  )
}
