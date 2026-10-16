/**
 * InterviewReportPage — detailed post-interview report.
 *
 * Uses GET /interviews/{id}/report which returns all questions, answers, and
 * evaluations bundled together, plus a computed summary with averages.
 */
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { ScoreGauge } from '@/components/ui/Charts'

export default function InterviewReportPage() {
  const { id } = useParams<{ id: string }>()

  const { data: report, isLoading, error } = useQuery({
    queryKey: ['interview', 'report', id],
    queryFn: () => api.getInterviewReport(id!),
    enabled: !!id,
  })

  if (isLoading) {
    return <p className="text-sm text-slate-500">Loading report…</p>
  }

  if (error || !report) {
    return (
      <div className="card text-center">
        <p className="text-bad-500">
          {error instanceof api.ApiError ? error.detail : 'Interview not found'}
        </p>
        <Link to="/interviews" className="mt-3 inline-block text-sm text-brand-600">
          ← Back to interviews
        </Link>
      </div>
    )
  }

  const { interview, items, summary } = report
  const isCompleted = interview.status === 'completed'

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {/* ─── Header ─── */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">
            Interview Report
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            {interview.role} · {interview.interview_type}
          </p>
        </div>
        <span
          className={`rounded-full px-3 py-1 text-xs font-medium ${
            isCompleted
              ? 'bg-good-100 text-good-500'
              : 'bg-warn-100 text-warn-500'
          }`}
        >
          {capitalize(interview.status)}
        </span>
      </div>

      {/* ─── Summary card ─── */}
      <div className="card">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <SummaryItem label="Started" value={new Date(interview.created_at).toLocaleString()} />
          <SummaryItem
            label="Completed"
            value={interview.completed_at ? new Date(interview.completed_at).toLocaleString() : '—'}
          />
          <SummaryItem label="Questions" value={`${summary.questions_answered}/${summary.questions_asked}`} />
          <SummaryItem label="Avg Word Count" value={summary.average_word_count?.toFixed(0) ?? '—'} />
        </div>

        {/* Score gauges */}
        <div className="mt-6 flex flex-wrap items-center justify-center gap-6">
          <ScoreGauge score={summary.average_overall_score} label="Overall" size={110} />
          <ScoreGauge score={summary.average_communication_score} label="Communication" size={110} />
          <ScoreGauge score={summary.average_technical_accuracy_score} label="Technical" size={110} />
        </div>

        {/* Difficulty progression */}
        {summary.difficulty_progression.length > 0 && (
          <div className="mt-4">
            <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">
              Difficulty Progression
            </dt>
            <dd className="mt-1 flex gap-1.5">
              {summary.difficulty_progression.map((d, i) => (
                <span key={i} className="rounded bg-brand-50 px-2 py-0.5 text-xs font-medium text-brand-700">
                  {capitalize(d)}
                </span>
              ))}
            </dd>
          </div>
        )}

        {/* Text quality stats */}
        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-3">
          <MiniStat label="Total Fillers" value={summary.total_filler_count} warn={summary.total_filler_count > 5} />
          <MiniStat label="Avg Filler Ratio" value={summary.average_filler_ratio != null ? `${(summary.average_filler_ratio * 100).toFixed(1)}%` : '—'} />
        </div>
      </div>

      {/* ─── Strengths & Weaknesses ─── */}
      {(summary.strengths_summary.length > 0 || summary.weaknesses_summary.length > 0) && (
        <div className="grid gap-4 sm:grid-cols-2">
          {summary.strengths_summary.length > 0 && (
            <div className="card">
              <h3 className="mb-2 text-sm font-semibold text-good-500">✓ Key Strengths</h3>
              <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
                {summary.strengths_summary.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
          {summary.weaknesses_summary.length > 0 && (
            <div className="card">
              <h3 className="mb-2 text-sm font-semibold text-bad-500">✗ Areas to Improve</h3>
              <ul className="list-inside list-disc space-y-1 text-sm text-slate-700">
                {summary.weaknesses_summary.map((w, i) => <li key={i}>{w}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* ─── Q&A Detail ─── */}
      <div>
        <h2 className="mb-3 text-lg font-semibold text-slate-900">
          Questions & Answers
        </h2>

        {items.length === 0 ? (
          <p className="text-sm text-slate-500">No questions were asked.</p>
        ) : (
          <div className="space-y-4">
            {items.map((item, idx) => (
              <div key={item.question.id} className="space-y-2">
                {/* Question */}
                <div className="card border-l-4 border-l-brand-500">
                  <div className="mb-1 flex items-center gap-2">
                    <span className="rounded bg-brand-50 px-2 py-0.5 text-xs font-medium text-brand-700">
                      Q{idx + 1}
                    </span>
                    <span className="rounded bg-slate-100 px-2 py-0.5 text-xs text-slate-500">
                      {item.question.difficulty}
                    </span>
                    <span className="text-xs text-slate-400">
                      {item.question.source} · {item.question.question_type}
                    </span>
                  </div>
                  <p className="text-slate-900">{item.question.prompt}</p>
                </div>

                {/* Answer */}
                {item.answer_content ? (
                  <div className="card ml-4 border-l-4 border-l-slate-300 bg-slate-50">
                    <div className="mb-1 flex items-center justify-between">
                      <span className="text-xs font-medium text-slate-500">Your Answer</span>
                      <span className="text-xs text-slate-400">{item.answer_word_count} words</span>
                    </div>
                    <p className="whitespace-pre-wrap text-sm text-slate-800">{item.answer_content}</p>
                  </div>
                ) : (
                  <div className="ml-4 text-sm italic text-slate-400">Not answered</div>
                )}

                {/* Evaluation */}
                {item.evaluation && (
                  <InlineEvaluation evaluation={item.evaluation} />
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ─── Actions ─── */}
      <div className="flex gap-3">
        {!isCompleted && (
          <Link to={`/interviews/${interview.id}/live`} className="btn-primary">
            Resume Interview
          </Link>
        )}
        <Link to="/analytics" className="btn-secondary">
          📊 Analytics Dashboard
        </Link>
        <Link to="/interviews" className="btn-secondary">
          ← All Interviews
        </Link>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function InlineEvaluation({ evaluation }: { evaluation: api.EvaluationResponse }) {
  const hasLLM = evaluation.overall_score !== null
  const tf = evaluation.text_features

  return (
    <div className="card ml-4 space-y-3 border-l-4 border-l-good-500 bg-green-50/30">
      <h4 className="text-sm font-semibold text-slate-900">Feedback</h4>

      {hasLLM && (
        <div className="flex flex-wrap gap-4">
          {[
            { label: 'Overall', score: evaluation.overall_score },
            { label: 'Relevance', score: evaluation.relevance_score },
            { label: 'Technical', score: evaluation.technical_accuracy_score },
            { label: 'Completeness', score: evaluation.completeness_score },
            { label: 'Communication', score: evaluation.communication_score },
          ].map(({ label, score }) =>
            score !== null ? (
              <div key={label} className="text-center">
                <div className="text-lg font-bold" style={{ color: scoreColor(score) }}>
                  {Math.round(score)}
                </div>
                <div className="text-xs text-slate-500">{label}</div>
              </div>
            ) : null,
          )}
        </div>
      )}

      {evaluation.strengths.length > 0 && (
        <FeedbackList title="✓ Strengths" items={evaluation.strengths} color="text-good-500" />
      )}
      {evaluation.weaknesses.length > 0 && (
        <FeedbackList title="✗ Weaknesses" items={evaluation.weaknesses} color="text-bad-500" />
      )}
      {evaluation.suggestions.length > 0 && (
        <FeedbackList title="→ Suggestions" items={evaluation.suggestions} color="text-brand-600" />
      )}

      <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm sm:grid-cols-4">
        <Metric label="Words" value={tf.word_count} />
        <Metric label="Sentences" value={tf.sentence_count} />
        <Metric label="Avg sent. len" value={tf.average_sentence_length.toFixed(1)} />
        <Metric label="Fillers" value={tf.filler_total} warn={tf.filler_total > 3} />
      </div>

      <p className="text-xs text-slate-400">
        Methods: {Object.entries(evaluation.method_map).map(([k, v]) => `${k}=${v}`).join(', ')}
      </p>
    </div>
  )
}

function FeedbackList({ title, items, color }: { title: string; items: string[]; color: string }) {
  return (
    <div>
      <h5 className={`mb-1 text-sm font-medium ${color}`}>{title}</h5>
      <ul className="list-inside list-disc space-y-0.5 text-sm text-slate-700">
        {items.map((item, i) => <li key={i}>{item}</li>)}
      </ul>
    </div>
  )
}

function Metric({ label, value, warn }: { label: string; value: number | string; warn?: boolean }) {
  return (
    <div>
      <dt className="text-xs text-slate-500">{label}</dt>
      <dd className={`font-medium ${warn ? 'text-warn-500' : 'text-slate-900'}`}>{value}</dd>
    </div>
  )
}

function SummaryItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</dt>
      <dd className="mt-0.5 text-sm font-medium text-slate-900">{value}</dd>
    </div>
  )
}

function MiniStat({ label, value, warn }: { label: string; value: number | string; warn?: boolean }) {
  return (
    <div>
      <dt className="text-xs text-slate-500">{label}</dt>
      <dd className={`text-lg font-bold ${warn ? 'text-warn-500' : 'text-slate-900'}`}>{value}</dd>
    </div>
  )
}

function capitalize(s: string): string {
  return s.charAt(0).toUpperCase() + s.slice(1)
}

function scoreColor(score: number): string {
  if (score >= 80) return '#16a34a'
  if (score >= 50) return '#d97706'
  return '#dc2626'
}
