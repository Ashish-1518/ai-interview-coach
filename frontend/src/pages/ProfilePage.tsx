/**
 * ProfilePage — view and edit the candidate profile.
 *
 * If no profile exists yet, shows a create form. Otherwise shows the existing
 * profile with an "Edit" toggle. Uses TanStack Query mutations so the cache
 * is automatically updated after a save.
 */
import { useEffect, useState, type FormEvent } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import * as api from '@/lib/api'

const ROLES = [
  'Python Developer',
  'Backend Developer',
  'Frontend Developer',
  'Full Stack Developer',
  'Data Scientist',
  'ML Engineer',
  'DevOps Engineer',
  'Software Engineer',
]

const LEVELS = ['junior', 'mid', 'senior']

export default function ProfilePage() {
  const queryClient = useQueryClient()
  const { data: profile, isLoading, error } = useQuery({
    queryKey: ['profile'],
    queryFn: api.getProfile,
    retry: false,
  })

  const isNew = !profile && (error instanceof api.ApiError && error.status === 404)

  const createMutation = useMutation({
    mutationFn: (data: api.ProfilePayload) => api.createProfile(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['profile'] }),
  })

  const updateMutation = useMutation({
    mutationFn: (data: Partial<api.ProfilePayload>) => api.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['profile'] })
      setEditing(false)
    },
  })

  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState<api.ProfilePayload>({
    full_name: '',
    target_role: ROLES[0],
    experience_level: LEVELS[0],
    bio: '',
  })

  // Sync form when profile loads
  useEffect(() => {
    if (profile) {
      setForm({
        full_name: profile.full_name,
        target_role: profile.target_role,
        experience_level: profile.experience_level,
        bio: profile.bio ?? '',
      })
    }
  }, [profile])

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (isNew) {
      createMutation.mutate(form)
    } else {
      updateMutation.mutate(form)
    }
  }

  const saving = createMutation.isPending || updateMutation.isPending
  const mutationError = createMutation.error || updateMutation.error

  if (isLoading) {
    return <p className="text-sm text-slate-500">Loading profile…</p>
  }

  // Show form if new or editing
  if (isNew || editing) {
    return (
      <div className="mx-auto max-w-lg">
        <h1 className="mb-6 text-2xl font-bold text-slate-900">
          {isNew ? 'Create Your Profile' : 'Edit Profile'}
        </h1>

        {mutationError && (
          <div className="mb-4 rounded-lg bg-bad-100 px-3 py-2 text-sm text-bad-500">
            {mutationError instanceof api.ApiError
              ? mutationError.detail
              : 'Something went wrong'}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="full_name" className="label">Full Name</label>
            <input
              id="full_name"
              required
              className="input"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            />
          </div>

          <div>
            <label htmlFor="target_role" className="label">Target Role</label>
            <select
              id="target_role"
              className="input"
              value={form.target_role}
              onChange={(e) => setForm({ ...form, target_role: e.target.value })}
            >
              {ROLES.map((r) => (
                <option key={r}>{r}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="experience_level" className="label">Experience Level</label>
            <select
              id="experience_level"
              className="input"
              value={form.experience_level}
              onChange={(e) => setForm({ ...form, experience_level: e.target.value })}
            >
              {LEVELS.map((l) => (
                <option key={l} value={l}>
                  {l.charAt(0).toUpperCase() + l.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="bio" className="label">Bio (optional)</label>
            <textarea
              id="bio"
              rows={3}
              className="input"
              placeholder="Brief intro about yourself…"
              value={form.bio}
              onChange={(e) => setForm({ ...form, bio: e.target.value })}
            />
          </div>

          <div className="flex gap-3">
            <button type="submit" disabled={saving} className="btn-primary">
              {saving ? 'Saving…' : isNew ? 'Create Profile' : 'Save Changes'}
            </button>
            {!isNew && (
              <button
                type="button"
                onClick={() => setEditing(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </div>
    )
  }

  // Display mode
  return (
    <div className="mx-auto max-w-lg">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Your Profile</h1>
        <button onClick={() => setEditing(true)} className="btn-secondary">
          Edit
        </button>
      </div>

      <div className="card mt-6 space-y-4">
        <Field label="Full Name" value={profile!.full_name} />
        <Field label="Target Role" value={profile!.target_role} />
        <Field
          label="Experience Level"
          value={profile!.experience_level.charAt(0).toUpperCase() + profile!.experience_level.slice(1)}
        />
        {profile!.bio && <Field label="Bio" value={profile!.bio} />}
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
