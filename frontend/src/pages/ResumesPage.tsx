/**
 * ResumesPage — upload and list PDF resumes.
 *
 * The upload uses FormData (not JSON), so the API client skips the
 * Content-Type header and lets the browser set the multipart boundary.
 */
import { useRef, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import * as api from '@/lib/api'

export default function ResumesPage() {
  const queryClient = useQueryClient()
  const fileRef = useRef<HTMLInputElement>(null)
  const [selectedResume, setSelectedResume] = useState<api.ResumeDetailResponse | null>(null)

  const { data: resumes, isLoading } = useQuery({
    queryKey: ['resumes'],
    queryFn: api.listResumes,
  })

  const uploadMutation = useMutation({
    mutationFn: (file: File) => api.uploadResume(file),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['resumes'] })
      setSelectedResume(data)
      if (fileRef.current) fileRef.current.value = ''
    },
  })

  const detailQuery = useQuery({
    queryKey: ['resume', selectedResume?.id],
    queryFn: () => api.getResume(selectedResume!.id),
    enabled: !!selectedResume?.id,
  })

  const detail = detailQuery.data ?? selectedResume

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (file) uploadMutation.mutate(file)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Resumes</h1>

      {/* ─── Upload ─── */}
      <div className="card">
        <h2 className="mb-2 font-semibold text-slate-900">Upload Resume</h2>
        <p className="mb-4 text-sm text-slate-500">
          PDF only, maximum 5 MB. Your resume is parsed to extract skills and
          tailor interview questions.
        </p>
        <input
          ref={fileRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleFileChange}
          className="text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-brand-50
            file:px-4 file:py-2 file:text-sm file:font-medium file:text-brand-700
            hover:file:bg-brand-100"
        />
        {uploadMutation.isPending && (
          <p className="mt-2 text-sm text-slate-500">Uploading…</p>
        )}
        {uploadMutation.isError && (
          <p className="mt-2 text-sm text-bad-500">
            {uploadMutation.error instanceof api.ApiError
              ? uploadMutation.error.detail
              : 'Upload failed'}
          </p>
        )}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* ─── Resume list ─── */}
        <div>
          <h2 className="mb-3 font-semibold text-slate-900">Your Resumes</h2>
          {isLoading && <p className="text-sm text-slate-500">Loading…</p>}
          {resumes?.length === 0 && (
            <p className="text-sm text-slate-500">No resumes uploaded yet.</p>
          )}
          <div className="space-y-2">
            {resumes?.map((r) => (
              <button
                key={r.id}
                onClick={() => setSelectedResume(r as api.ResumeDetailResponse)}
                className={`card w-full text-left transition-colors hover:border-brand-300 ${
                  detail?.id === r.id ? 'border-brand-400 ring-1 ring-brand-400' : ''
                }`}
              >
                <p className="font-medium text-slate-900">{r.original_filename}</p>
                <p className="text-xs text-slate-400">
                  {new Date(r.uploaded_at).toLocaleDateString()}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* ─── Selected resume detail ─── */}
        {detail && (
          <div className="card space-y-4">
            <h2 className="font-semibold text-slate-900">{detail.original_filename}</h2>

            {detail.parsed_data && (
              <>
                {detail.parsed_data.name && (
                  <Field label="Name" value={detail.parsed_data.name} />
                )}
                {detail.parsed_data.email && (
                  <Field label="Email" value={detail.parsed_data.email} />
                )}
                {detail.parsed_data.skills.length > 0 && (
                  <div>
                    <dt className="text-sm font-medium text-slate-500">Skills</dt>
                    <dd className="mt-1 flex flex-wrap gap-1.5">
                      {detail.parsed_data.skills.map((s) => (
                        <span
                          key={s}
                          className="rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-medium text-brand-700"
                        >
                          {s}
                        </span>
                      ))}
                    </dd>
                  </div>
                )}
              </>
            )}

            <div>
              <dt className="text-sm font-medium text-slate-500">Parse Method</dt>
              <dd className="mt-0.5 text-sm text-slate-700">{detail.parse_method}</dd>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-sm font-medium text-slate-500">{label}</dt>
      <dd className="mt-0.5 text-slate-900">{value}</dd>
    </div>
  )
}
