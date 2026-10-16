/**
 * GuestLayout — used for login/register pages.
 *
 * Centered card on a gradient background. The Outlet renders whichever
 * child route matched (LoginPage or RegisterPage).
 */
import { Navigate, Outlet } from 'react-router-dom'

import { useAuth } from '@/contexts/AuthContext'

export default function GuestLayout() {
  const { isAuthenticated, isLoading } = useAuth()

  // Already logged in → skip to dashboard
  if (isAuthenticated && !isLoading) {
    return <Navigate to="/dashboard" replace />
  }

  return (
    <div className="flex min-h-full items-center justify-center bg-gradient-to-br from-brand-50 to-slate-100 px-4 py-12">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-brand-700">
            AI Interview Coach
          </h1>
          <p className="mt-2 text-sm text-slate-500">
            Practice interviews, get real feedback
          </p>
        </div>
        <div className="card">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
