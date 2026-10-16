/**
 * LiveInterviewPage — the real-time interview experience.
 *
 * Flow:
 * 1. On mount, fetch the first question (POST /next).
 * 2. User types an answer in a textarea and submits.
 * 3. The answer is sent to the backend (POST /answers), which returns the
 *    evaluation immediately. We show inline feedback.
 * 4. User clicks "Next Question" → repeat until all questions answered.
 * 5. User clicks "Finish Interview" → POST /complete, redirect to report.
 *
 * Design decisions:
 * - We keep all Q&A pairs in local state so the user can scroll back.
 * - The textarea auto-focuses after each new question for fast typing.
 * - Word count is shown live as the user types (mirrors the backend's count).
 */
import { useCallback, useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { VoiceRecorder } from '@/components/ui/VoiceRecorder'

interface QAPair {
  question: api.QuestionResponse
  answer?: string
  evaluation?: api.EvaluationResponse
}

export default function LiveInterviewPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const [pairs, setPairs] = useState<QAPair[]>([])
  const [draft, setDraft] = useState('')
  const [finished, setFinished] = useState(false)
  const [voiceMetrics, setVoiceMetrics] = useState<api.VoiceAnalysisResponse | null>(null)

  const voiceMutation = useMutation({
    mutationFn: (duration: number) => api.analyzeVoice(draft, duration),
    onSuccess: (data) => setVoiceMetrics(data),
  })

  // Fetch interview metadata for the header
  const { data: interview } = useQuery({
    queryKey: ['interview', id],
    queryFn: () => api.getInterview(id!),
    enabled: !!id,
  })

  // ── Fetch next question ──
  const nextMutation = useMutation({
    mutationFn: () => api.nextQuestion(id!),
    onSuccess: (question) => {
      setPairs((prev) => [...prev, { question }])
      setDraft('')
      setTimeout(() => textareaRef.current?.focus(), 50)
    },
    onError: (err) => {
      // 503 means no more questions available (bank exhausted, no LLM)
      if (err instanceof api.ApiError && (err.status === 503 || err.status === 400)) {
        setFinished(true)
      }
    },
  })

  // ── Submit answer ──
  const answerMutation = useMutation({
    mutationFn: ({
      questionId,
      content,
    }: {
      questionId: string
      content: string
    }) => api.submitAnswer(id!, questionId, content),
    onSuccess: (result) => {
      setPairs((prev) =>
        prev.map((p) =>
          p.question.id === result.answer_id ||
          // Match by last unanswered question
          (!p.answer && p === prev[prev.length - 1])
            ? { ...p, answer: result.content, evaluation: result.evaluation }
            : p,
        ),
      )
    },
  })

  // ── Complete interview ──
  const completeMutation = useMutation({
    mutationFn: () => api.completeInterview(id!),
    onSuccess: () => navigate(`/interviews/${id}`),
  })

  // Auto-fetch first question on mount
  const fetchedFirst = useRef(false)
  useEffect(() => {
    if (id && !fetchedFirst.current) {
      fetchedFirst.current = true
      nextMutation.mutate()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id])

  const currentPair = pairs[pairs.length - 1]
  const isAnswered = !!currentPair?.answer
  const answeredCount = pairs.filter((p) => p.answer).length
  const totalTarget = interview?.target_question_count ?? 0
  const allDone = answeredCount >= totalTarget || finished

  const handleSubmitAnswer = useCallback(() => {
    if (!currentPair || isAnswered || !draft.trim()) return
    answerMutation.mutate({
      questionId: currentPair.question.id,
      content: draft.trim(),
    })
  }, [currentPair, isAnswered, draft, answerMutation])

  const wordCount = draft.trim() ? draft.trim().split(/\s+/).length : 0

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      {/* ─── Header bar ─── */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-900">
            {interview?.role ?? 'Interview'} — {interview?.interview_type}
          </h1>
          <p className="text-sm text-slate-500">
            Question {pairs.length} of {totalTarget} ·{' '}
            Difficulty: {currentPair?.question.difficulty ?? interview?.current_difficulty ?? '—'}
          </p>
        </div>
        <div className="text-sm font-medium">
          <span className="text-brand-600">{answeredCount}</span>
          <span className="text-slate-400">/{totalTarget} answered</span>
        </div>
      </div>

      {/* ─── Progress bar ─── */}
      <div className="h-2 overflow-hidden rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-brand-500 transition-all duration-500"
          style={{ width: `${totalTarget ? (answeredCount / totalTarget) * 100 : 0}%` }}
        />
      </div>

      {/* ─── Question & Answer pairs ─── */}
      <div className="space-y-6">
        {pairs.map((pair, idx) => (
          <div key={pair.question.id} className="space-y-3">
            {/* Question */}
            <div className="card border-l-4 border-l-brand-500">
              <div className="mb-1 flex items-center gap-2">
                <span className="rounded bg-brand-50 px-2 py-0.5 text-xs font-medium text-brand-700">
                  Q{idx + 1}
                </span>
                <span className="text-xs text-slate-400">
                  {pair.question.difficulty} · {pair.question.source}
                </span>
              </div>
              <p className="text-slate-900">{pair.question.prompt}</p>
            </div>

            {/* Answer (if submitted) */}
            {pair.answer && (
              <div className="card ml-4 border-l-4 border-l-slate-300 bg-slate-50">
                <p className="whitespace-pre-wrap text-sm text-slate-800">
                  {pair.answer}
                </p>
              </div>
            )}

            {/* Evaluation (if available) */}
            {pair.evaluation && (
              <EvaluationCard evaluation={pair.evaluation} />
            )}
          </div>
        ))}
      </div>

      {/* ─── Answer input (for current unanswered question) ─── */}
      {currentPair && !isAnswered && (
        <div className="card space-y-3">
          <div className="flex items-center justify-between">
            <label htmlFor="answer" className="label mb-0">
              Your Answer
            </label>
            <VoiceRecorder
              onTranscriptUpdate={(text) => setDraft(text)}
              onVoiceAnalyzed={(sec) => {
                if (draft.trim()) voiceMutation.mutate(sec)
              }}
              disabled={answerMutation.isPending}
            />
          </div>

          <textarea
            ref={textareaRef}
            id="answer"
            rows={6}
            className="input font-mono text-sm"
            placeholder="Type or speak your answer using the microphone button…"
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            disabled={answerMutation.isPending}
          />

          {voiceMetrics && (
            <div className="flex flex-wrap gap-4 rounded-lg bg-brand-50 p-3 text-xs text-brand-900">
              <span><strong>Pace:</strong> {voiceMetrics.speaking_pace_wpm} WPM ({voiceMetrics.pace_status})</span>
              <span><strong>Pauses:</strong> ~{voiceMetrics.estimated_pauses}</span>
              <span><strong>Speech Clarity:</strong> {voiceMetrics.clarity_score}/100</span>
            </div>
          )}

          <div className="flex items-center justify-between">
            <span className="text-xs text-slate-400">{wordCount} words</span>
            <button
              onClick={handleSubmitAnswer}
              disabled={answerMutation.isPending || !draft.trim()}
              className="btn-primary"
            >
              {answerMutation.isPending ? 'Evaluating…' : 'Submit Answer'}
            </button>
          </div>

          {answerMutation.isError && (
            <p className="text-sm text-bad-500">
              {answerMutation.error instanceof api.ApiError
                ? answerMutation.error.detail
                : 'Failed to submit'}
            </p>
          )}
        </div>
      )}

      {/* ─── Action buttons ─── */}
      {isAnswered && (
        <div className="flex justify-end gap-3">
          {!allDone && (
            <button
              onClick={() => nextMutation.mutate()}
              disabled={nextMutation.isPending}
              className="btn-primary"
            >
              {nextMutation.isPending ? 'Loading…' : 'Next Question →'}
            </button>
          )}
          <button
            onClick={() => completeMutation.mutate()}
            disabled={completeMutation.isPending}
            className={allDone ? 'btn-primary' : 'btn-secondary'}
          >
            {completeMutation.isPending ? 'Finishing…' : 'Finish Interview'}
          </button>
        </div>
      )}

      {/* Loading state for first question */}
      {pairs.length === 0 && nextMutation.isPending && (
        <div className="card text-center text-sm text-slate-500">
          Loading your first question…
        </div>
      )}
    </div>
  )
}

// ---------------------------------------------------------------------------
// EvaluationCard — shows scores + text features inline after each answer
// ---------------------------------------------------------------------------

function EvaluationCard({ evaluation }: { evaluation: api.EvaluationResponse }) {
  const { text_features: tf } = evaluation
  const hasLLM = evaluation.overall_score !== null

  return (
    <div className="card ml-4 space-y-4 border-l-4 border-l-good-500 bg-green-50/30">
      <h4 className="text-sm font-semibold text-slate-900">Feedback</h4>

      {/* Score bar (LLM) */}
      {hasLLM && (
        <div>
          <div className="mb-1 flex items-center justify-between">
            <span className="text-sm text-slate-600">Overall Score</span>
            <span className="text-sm font-bold text-slate-900">
              {evaluation.overall_score}/100
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-slate-200">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${evaluation.overall_score}%`,
                backgroundColor: scoreColor(evaluation.overall_score!),
              }}
            />
          </div>
        </div>
      )}

      {/* Strengths / Weaknesses / Suggestions */}
      {evaluation.strengths.length > 0 && (
        <FeedbackList title="✓ Strengths" items={evaluation.strengths} color="text-good-500" />
      )}
      {evaluation.weaknesses.length > 0 && (
        <FeedbackList title="✗ Weaknesses" items={evaluation.weaknesses} color="text-bad-500" />
      )}
      {evaluation.suggestions.length > 0 && (
        <FeedbackList title="→ Suggestions" items={evaluation.suggestions} color="text-brand-600" />
      )}

      {/* Text features (always present — deterministic NLP) */}
      <div>
        <h5 className="mb-1 text-xs font-semibold uppercase tracking-wide text-slate-500">
          Text Analysis (deterministic)
        </h5>
        <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm sm:grid-cols-4">
          <Metric label="Words" value={tf.word_count} />
          <Metric label="Sentences" value={tf.sentence_count} />
          <Metric label="Avg sent. len" value={tf.average_sentence_length.toFixed(1)} />
          <Metric label="Fillers" value={tf.filler_total} warn={tf.filler_total > 3} />
        </div>
      </div>

      {/* Method provenance */}
      <p className="text-xs text-slate-400">
        Methods: {Object.entries(evaluation.method_map).map(([k, v]) => `${k}=${v}`).join(', ')}
      </p>
    </div>
  )
}

function FeedbackList({
  title,
  items,
  color,
}: {
  title: string
  items: string[]
  color: string
}) {
  return (
    <div>
      <h5 className={`mb-1 text-sm font-medium ${color}`}>{title}</h5>
      <ul className="list-inside list-disc space-y-0.5 text-sm text-slate-700">
        {items.map((item, i) => (
          <li key={i}>{item}</li>
        ))}
      </ul>
    </div>
  )
}

function Metric({
  label,
  value,
  warn,
}: {
  label: string
  value: number | string
  warn?: boolean
}) {
  return (
    <div>
      <dt className="text-xs text-slate-500">{label}</dt>
      <dd className={`font-medium ${warn ? 'text-warn-500' : 'text-slate-900'}`}>
        {value}
      </dd>
    </div>
  )
}

function scoreColor(score: number): string {
  if (score >= 80) return '#16a34a' // good
  if (score >= 50) return '#d97706' // warn
  return '#dc2626' // bad
}
