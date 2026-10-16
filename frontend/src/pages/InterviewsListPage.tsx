/**
 * InterviewsListPage — shows all past and active interviews.
 *
 * Active interviews can be resumed; completed ones link to the report page.
 */
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'

export default function InterviewsListPage() {
  const { data: interviews, isLoading } = useQuery({
    queryKey: ['interviews'],
    queryFn: api.listInterviews,
  })

  const active = interviews?.filter((i) => i.status === 'active') ?? []
  const completed = interviews?.filter((i) => i.status === 'completed') ?? []

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Interviews</h1>
        <Link to="/interviews/new" className="btn-primary">
          + New Interview
        </Link>
      </div>

      {isLoading && <p className="text-sm text-slate-500">Loading…</p>}

      {/* Active interviews */}
      {active.length > 0 && (
        <Section title="Active">
          {active.map((i) => (
            <InterviewCard key={i.id} interview={i} linkTo={`/interviews/${i.id}/live`} badge="Resume" />
          ))}
        </Section>
      )}

      {/* Completed interviews */}
      {completed.length > 0 && (
        <Section title="Completed">
          {completed.map((i) => (
            <InterviewCard key={i.id} interview={i} linkTo={`/interviews/${i.id}`} badge="View Report" />
          ))}
        </Section>
      )}

      {interviews && interviews.length === 0 && (
        <div className="card text-center">
          <p className="text-slate-500">No interviews yet.</p>
          <Link to="/interviews/new" className="mt-3 inline-block text-sm font-medium text-brand-600 hover:text-brand-700">
            Start your first interview →
          </Link>
        </div>
      )}
    </div>
  )
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div>
      <h2 className="mb-3 text-lg font-semibold text-slate-900">{title}</h2>
      <div className="space-y-2">{children}</div>
    </div>
  )
}

function InterviewCard({
  interview,
  linkTo,
  badge,
}: {
  interview: api.InterviewResponse
  linkTo: string
  badge: string
}) {
  return (
    <Link
      to={linkTo}
      className="card flex items-center justify-between transition-colors hover:border-brand-300"
    >
      <div>
        <p className="font-medium text-slate-900">{interview.role}</p>
        <p className="text-sm text-slate-500">
          {interview.interview_type} · {interview.starting_difficulty} ·{' '}
          {interview.target_question_count} questions
        </p>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-xs text-slate-400">
          {new Date(interview.created_at).toLocaleDateString()}
        </span>
        <span className="rounded-full bg-brand-50 px-3 py-1 text-xs font-medium text-brand-700">
          {badge}
        </span>
      </div>
    </Link>
  )
}
