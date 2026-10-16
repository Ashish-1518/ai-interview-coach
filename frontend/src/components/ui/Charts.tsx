/**
 * Lightweight SVG chart components — no external chart library needed.
 *
 * WHY BUILD OUR OWN (for your viva):
 * Chart.js / Recharts add 100–200 kB to the bundle. For the 2–3 chart types
 * we need, raw SVG is ~50 lines each and renders instantly. It also shows you
 * understand coordinate maths — an examiner will ask "how does this work?"
 * and you can answer: "I map data values to pixel positions with linear
 * interpolation" instead of "I imported a library."
 *
 * These components are pure — they take data as props and return SVG. No
 * internal state, no side effects.
 */

// ---------------------------------------------------------------------------
// ScoreTrendChart — line chart of scores over time
// ---------------------------------------------------------------------------

interface ScoreTrendProps {
  /** Chronological score values (null entries are skipped). */
  scores: (number | null)[]
  /** Pixel width of the SVG. */
  width?: number
  /** Pixel height of the SVG. */
  height?: number
  /** Label shown below the chart. */
  label?: string
}

export function ScoreTrendChart({
  scores,
  width = 400,
  height = 160,
  label = 'Score Trend',
}: ScoreTrendProps) {
  const padding = { top: 16, right: 16, bottom: 28, left: 36 }
  const chartW = width - padding.left - padding.right
  const chartH = height - padding.top - padding.bottom

  // Filter out nulls for the actual line, but keep index for x spacing
  const points = scores
    .map((v, i) => ({ i, v }))
    .filter((p): p is { i: number; v: number } => p.v !== null)

  if (points.length === 0) {
    return (
      <div className="text-center text-sm text-slate-400">
        No score data yet
      </div>
    )
  }

  const maxIdx = scores.length - 1
  const minV = 0
  const maxV = 100

  function x(idx: number) {
    return padding.left + (maxIdx > 0 ? (idx / maxIdx) * chartW : chartW / 2)
  }
  function y(val: number) {
    return padding.top + chartH - ((val - minV) / (maxV - minV)) * chartH
  }

  const pathD = points
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${x(p.i)} ${y(p.v)}`)
    .join(' ')

  return (
    <div>
      <svg viewBox={`0 0 ${width} ${height}`} className="w-full" role="img" aria-label={label}>
        {/* Y-axis gridlines */}
        {[0, 25, 50, 75, 100].map((v) => (
          <g key={v}>
            <line
              x1={padding.left} y1={y(v)}
              x2={width - padding.right} y2={y(v)}
              stroke="#e2e8f0" strokeWidth="1"
            />
            <text x={padding.left - 4} y={y(v) + 4} textAnchor="end" className="fill-slate-400 text-[10px]">
              {v}
            </text>
          </g>
        ))}

        {/* Line */}
        <path d={pathD} fill="none" stroke="#4f46e5" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />

        {/* Dots */}
        {points.map((p) => (
          <circle key={p.i} cx={x(p.i)} cy={y(p.v)} r="4" fill="#4f46e5" />
        ))}

        {/* X-axis label */}
        <text x={width / 2} y={height - 4} textAnchor="middle" className="fill-slate-500 text-[11px] font-medium">
          {label}
        </text>
      </svg>
    </div>
  )
}

// ---------------------------------------------------------------------------
// BarChart — horizontal bars for distributions
// ---------------------------------------------------------------------------

interface BarChartProps {
  data: { label: string; value: number }[]
  /** Color class for bars (Tailwind fill- class). */
  barColor?: string
  maxValue?: number
}

export function BarChart({ data, barColor = 'fill-brand-500', maxValue }: BarChartProps) {
  const max = maxValue ?? Math.max(...data.map((d) => d.value), 1)

  return (
    <div className="space-y-2">
      {data.map(({ label, value }) => (
        <div key={label} className="flex items-center gap-3">
          <span className="w-24 truncate text-right text-xs text-slate-600">{label}</span>
          <div className="flex-1">
            <div className="h-5 overflow-hidden rounded bg-slate-100">
              <div
                className={`h-full rounded transition-all ${barColor}`}
                style={{
                  width: `${(value / max) * 100}%`,
                  backgroundColor: barColor.startsWith('fill-') ? undefined : barColor,
                }}
              />
            </div>
          </div>
          <span className="w-8 text-right text-xs font-medium text-slate-700">{value}</span>
        </div>
      ))}
    </div>
  )
}

// ---------------------------------------------------------------------------
// ScoreGauge — circular gauge for a single 0-100 score
// ---------------------------------------------------------------------------

interface ScoreGaugeProps {
  score: number | null
  label: string
  size?: number
}

export function ScoreGauge({ score, label, size = 100 }: ScoreGaugeProps) {
  const radius = (size - 12) / 2
  const circumference = 2 * Math.PI * radius
  const offset = score !== null ? circumference * (1 - score / 100) : circumference

  const color =
    score === null ? '#94a3b8' : score >= 80 ? '#16a34a' : score >= 50 ? '#d97706' : '#dc2626'

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        {/* Background ring */}
        <circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke="#e2e8f0" strokeWidth="8"
        />
        {/* Score ring */}
        <circle
          cx={size / 2} cy={size / 2} r={radius}
          fill="none" stroke={color} strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
          className="transition-all duration-700"
        />
        {/* Score text */}
        <text
          x={size / 2} y={size / 2 + 5}
          textAnchor="middle"
          className="fill-slate-900 text-lg font-bold"
        >
          {score !== null ? Math.round(score) : '—'}
        </text>
      </svg>
      <span className="text-xs font-medium text-slate-600">{label}</span>
    </div>
  )
}
