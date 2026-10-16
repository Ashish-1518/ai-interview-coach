/**
 * DashboardPage — landing page after login.
 *
 * Shows a welcome message, quick stats (recent interviews, resume count),
 * and action cards to start a new interview or upload a resume.
 */
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'

export default function DashboardPage() {
  const { user } = useAuth()

  const { data: interviews } = useQuery({
    queryKey: ['interviews'],
    queryFn: api.listInterviews,
  })

  const { data: resumes } = useQuery({
    queryKey: ['resumes'],
    queryFn: api.listResumes,
  })

  const completed = interviews?.filter((i) => i.status === 'completed') ?? []
  const active = interviews?.filter((i) => i.status === 'active') ?? []

  return (
    <div className="space-y-8">
      {/* ─── Header ─── */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Welcome back{user?.email ? `, ${user.email.split('@')[0]}` : ''}!
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Here's an overview of your interview practice progress.
        </p>
      </div>

      {/* ─── Stats row ─── */}
      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard label="Completed" value={completed.length} color="good" />
        <StatCard label="Active" value={active.length} color="brand" />
        <StatCard label="Resumes" value={resumes?.length ?? 0} color="warn" />
      </div>

      {/* ─── Action cards ─── */}
      <div className="grid gap-6 sm:grid-cols-3">
        <ActionCard
          title="Start New Interview"
          description="Choose a role and difficulty, then practice with AI-generated questions."
          to="/interviews/new"
          cta="Begin Interview"
        />
        <ActionCard
          title="Upload Resume"
          description="Upload your PDF resume so interview questions can be tailored to your background."
          to="/resumes"
          cta="Manage Resumes"
        />
        <ActionCard
          title="View Analytics"
          description="Track your performance trends, scores, and identify areas to improve."
          to="/analytics"
          cta="Analytics Dashboard"
        />
      </div>

      {/* ─── Recent interviews ─── */}
      {completed.length > 0 && (
        <div>
          <h2 className="mb-3 text-lg font-semibold text-slate-900">
            Recent Interviews
          </h2>
          <div className="space-y-2">
            {completed.slice(0, 5).map((interview) => (
              <Link
                key={interview.id}
                to={`/interviews/${interview.id}`}
                className="card flex items-center justify-between hover:border-brand-300 transition-colors"
              >
                <div>
                  <p className="font-medium text-slate-900">{interview.role}</p>
                  <p className="text-sm text-slate-500">
                    {interview.interview_type} · {interview.starting_difficulty}
                  </p>
                </div>
                <span className="text-xs text-slate-400">
                  {new Date(interview.created_at).toLocaleDateString()}
                </span>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sub-components (kept in the same file — small, page-specific)
// ---------------------------------------------------------------------------

function StatCard({
  label,
  value,
  color,
}: {
  label: string
  value: number
  color: 'good' | 'brand' | 'warn'
}) {
  const colorClasses = {
    good: 'bg-good-100 text-good-500',
    brand: 'bg-brand-100 text-brand-600',
    warn: 'bg-warn-100 text-warn-500',
  }

  return (
    <div className="card flex items-center gap-4">
      <div className={`flex h-12 w-12 items-center justify-center rounded-lg ${colorClasses[color]}`}>
        <span className="text-xl font-bold">{value}</span>
      </div>
      <p className="text-sm font-medium text-slate-600">{label}</p>
    </div>
  )
}

function ActionCard({
  title,
  description,
  to,
  cta,
}: {
  title: string
  description: string
  to: string
  cta: string
}) {
  return (
    <div className="card flex flex-col justify-between gap-4">
      <div>
        <h3 className="font-semibold text-slate-900">{title}</h3>
        <p className="mt-1 text-sm text-slate-500">{description}</p>
      </div>
      <Link to={to} className="btn-primary self-start">
        {cta}
      </Link>
    </div>
  )
}
