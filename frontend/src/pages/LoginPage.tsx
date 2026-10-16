/**
 * LoginPage — email + password form that calls POST /api/v1/auth/login.
 *
 * On success we store the JWT via `setToken` and React Router redirects to
 * /dashboard (GuestLayout handles the redirect when isAuthenticated flips).
 */
import { useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'

export default function LoginPage() {
  const { setToken } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const mutation = useMutation({
    mutationFn: () => api.login(email, password),
    onSuccess: (data) => setToken(data.access_token),
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    mutation.mutate()
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h2 className="text-xl font-semibold text-slate-900">Welcome back</h2>

      {mutation.isError && (
        <div className="rounded-lg bg-bad-100 px-3 py-2 text-sm text-bad-500">
          {mutation.error instanceof api.ApiError
            ? mutation.error.detail
            : 'Something went wrong'}
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
          className="input"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <button
        type="submit"
        disabled={mutation.isPending}
        className="btn-primary w-full"
      >
        {mutation.isPending ? 'Signing in…' : 'Sign in'}
      </button>

      <p className="text-center text-sm text-slate-500">
        Don&apos;t have an account?{' '}
        <Link to="/register" className="font-medium text-brand-600 hover:text-brand-700">
          Register
        </Link>
      </p>
    </form>
  )
}
