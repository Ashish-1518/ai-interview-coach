/**
 * AnalyticsPage — performance dashboard with charts and stats.
 *
 * Fetches GET /api/v1/analytics/summary and renders:
 *  - Headline stats (total interviews, questions answered, avg score, time)
 *  - Score trend line chart
 *  - Difficulty and interview-type distribution bar charts
 *  - Strongest / weakest topics lists
 *  - Interview history table
 */
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { BarChart, ScoreGauge, ScoreTrendChart } from '@/components/ui/Charts'

export default function AnalyticsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['analytics', 'summary'],
    queryFn: api.getAnalyticsSummary,
  })

  if (isLoading) {
    return <p className="text-sm text-slate-500">Loading analytics…</p>
  }

  if (error) {
    return (
      <div className="card text-center text-bad-500">
        {error instanceof api.ApiError ? error.detail : 'Failed to load analytics'}
      </div>
    )
  }

  if (!data || data.total_interviews === 0) {
    return (
      <div className="card mx-auto max-w-md text-center">
        <h1 className="mb-2 text-xl font-bold text-slate-900">No Data Yet</h1>
        <p className="mb-4 text-sm text-slate-500">
          Complete your first interview to see performance analytics here.
        </p>
        <Link to="/interviews/new" className="btn-primary">
          Start an Interview
        </Link>
      </div>
    )
  }

  const diffDist = Object.entries(data.difficulty_distribution).map(([label, value]) => ({
    label: label.charAt(0).toUpperCase() + label.slice(1),
    value,
  }))
  const typeDist = Object.entries(data.interview_type_distribution).map(([label, value]) => ({
    label: label.charAt(0).toUpperCase() + label.slice(1),
    value,
  }))

  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-slate-900">Performance Analytics</h1>

      {/* ─── Headline stats ─── */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Total Interviews" value={data.total_interviews} />
        <StatCard label="Completed" value={data.completed_interviews} />
        <StatCard label="Questions Answered" value={data.total_questions_answered} />
        <StatCard
          label="Practice Time"
          value={`${data.total_practice_time_estimate_minutes} min`}
        />
      </div>

      {/* ─── Score overview ─── */}
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="card lg:col-span-2">
          <h2 className="mb-4 font-semibold text-slate-900">Score Trend</h2>
          <ScoreTrendChart scores={data.score_trend} label="Interview # → Average Score" />
        </div>
        <div className="card flex items-center justify-center">
          <ScoreGauge score={data.average_overall_score} label="Overall Average" size={140} />
        </div>
      </div>

      {/* ─── Distributions ─── */}
      <div className="grid gap-6 sm:grid-cols-2">
        {diffDist.length > 0 && (
          <div className="card">
            <h2 className="mb-3 font-semibold text-slate-900">Difficulty Distribution</h2>
            <BarChart data={diffDist} />
          </div>
        )}
        {typeDist.length > 0 && (
          <div className="card">
            <h2 className="mb-3 font-semibold text-slate-900">Interview Types</h2>
            <BarChart data={typeDist} />
          </div>
        )}
      </div>

      {/* ─── Strongest / Weakest topics ─── */}
      {(data.strongest_topics.length > 0 || data.weakest_topics.length > 0) && (
        <div className="grid gap-6 sm:grid-cols-2">
          {data.strongest_topics.length > 0 && (
            <div className="card">
              <h2 className="mb-3 font-semibold text-good-500">✓ Strongest Topics</h2>
              <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
                {data.strongest_topics.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            </div>
          )}
          {data.weakest_topics.length > 0 && (
            <div className="card">
              <h2 className="mb-3 font-semibold text-warn-500">⚠ Topics to Improve</h2>
              <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
                {data.weakest_topics.map((t) => (
                  <li key={t}>{t}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* ─── History table ─── */}
      {data.history.length > 0 && (
        <div className="card overflow-x-auto">
          <h2 className="mb-3 font-semibold text-slate-900">Interview History</h2>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500">
                <th className="pb-2 pr-4">Date</th>
                <th className="pb-2 pr-4">Role</th>
                <th className="pb-2 pr-4">Type</th>
                <th className="pb-2 pr-4">Difficulty</th>
                <th className="pb-2 pr-4">Questions</th>
                <th className="pb-2 pr-4">Avg Score</th>
                <th className="pb-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.history.map((h) => (
                <tr key={h.interview_id} className="border-b border-slate-100 last:border-0">
                  <td className="py-2 pr-4 text-slate-600">
                    {new Date(h.created_at).toLocaleDateString()}
                  </td>
                  <td className="py-2 pr-4">
                    <Link
                      to={`/interviews/${h.interview_id}`}
                      className="font-medium text-brand-600 hover:text-brand-700"
                    >
                      {h.role}
                    </Link>
                  </td>
                  <td className="py-2 pr-4 text-slate-600">{h.interview_type}</td>
                  <td className="py-2 pr-4 text-slate-600">{h.difficulty}</td>
                  <td className="py-2 pr-4 text-slate-600">
                    {h.questions_answered}/{h.questions_asked}
                  </td>
                  <td className="py-2 pr-4 font-medium">
                    {h.average_overall_score !== null
                      ? `${Math.round(h.average_overall_score)}/100`
                      : '—'}
                  </td>
                  <td className="py-2">
                    <span
                      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                        h.status === 'completed'
                          ? 'bg-good-100 text-good-500'
                          : 'bg-warn-100 text-warn-500'
                      }`}
                    >
                      {h.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

function StatCard({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="card">
      <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</dt>
      <dd className="mt-1 text-2xl font-bold text-slate-900">{value}</dd>
    </div>
  )
}
