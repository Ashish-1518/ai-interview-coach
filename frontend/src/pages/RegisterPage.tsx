/**
 * RegisterPage — creates a new account via POST /api/v1/auth/register.
 *
 * Nearly identical to LoginPage. The mutation calls `api.register` which
 * returns a token directly (backend logs you in on registration), so the user
 * lands on the dashboard without a separate login step.
 */
import { useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'

export default function RegisterPage() {
  const { setToken } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [localError, setLocalError] = useState('')

  const mutation = useMutation({
    mutationFn: () => api.register(email, password),
    onSuccess: (data) => setToken(data.access_token),
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLocalError('')
    if (password !== confirm) {
      setLocalError('Passwords do not match')
      return
    }
    mutation.mutate()
  }

  const errorMsg =
    localError ||
    (mutation.isError
      ? mutation.error instanceof api.ApiError
        ? mutation.error.detail
        : 'Something went wrong'
      : '')

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-xl font-semibold text-slate-900">Create account</h2>

      {errorMsg && (
        <div className="rounded-lg bg-bad-100 px-3 py-2 text-sm text-bad-500">
          {errorMsg}
        </div>
      )}

      <div>
        <label htmlFor="email" className="label">Email</label>
        <input
          id="email"
          type="email"
          required
          className="input"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="password" className="label">Password</label>
        <input
          id="password"
          type="password"
          required
          minLength={8}
          maxLength={72}
          className="input"
          placeholder="Min. 8 characters"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="confirm" className="label">Confirm password</label>
        <input
          id="confirm"
          type="password"
          required
          minLength={8}
          className="input"
          placeholder="Re-enter password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="btn-primary w-full"
      >
        {mutation.isPending ? 'Creating account…' : 'Create account'}
      </button>

      <p className="text-center text-sm text-slate-500">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-brand-600 hover:text-brand-700">
          Sign in
        </Link>
      </p>
    </form>
  )
}
