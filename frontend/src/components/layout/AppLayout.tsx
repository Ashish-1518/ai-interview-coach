/**
 * AppLayout — shell for authenticated pages.
 *
 * Top navbar with user email + logout button, and an <Outlet> for the
 * active page. If the user isn't authenticated, redirect to /login.
 */
import { Navigate, NavLink, Outlet } from 'react-router-dom'

import { useAuth } from '@/contexts/AuthContext'

const NAV_LINKS = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/interviews', label: 'Interviews' },
  { to: '/analytics', label: 'Analytics' },
  { to: '/job-match', label: 'Job Match' },
  { to: '/resumes', label: 'Resumes' },
  { to: '/profile', label: 'Profile' },
] as const

export default function AppLayout() {
  const { user, isAuthenticated, isLoading, logout } = useAuth()

  if (isLoading) {
    return (
      <div className="flex min-h-full items-center justify-center">
        <p className="text-sm text-slate-500">Loading…</p>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="flex min-h-full flex-col">
      {/* ─── Top nav ─── */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
          <div className="flex items-center gap-6">
            <span className="text-lg font-bold text-brand-700">
              AI Interview Coach
            </span>
            <nav className="hidden items-center gap-1 sm:flex">
              {NAV_LINKS.map(({ to, label }) => (
                <NavLink
                  key={to}
                  to={to}
                  className={({ isActive }) =>
                    `rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
                      isActive
                        ? 'bg-brand-50 text-brand-700'
                        : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                    }`
                  }
                >
                  {label}
                </NavLink>
              ))}
            </nav>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-sm text-slate-500">{user?.email}</span>
            <button onClick={logout} className="btn-secondary text-xs">
              Log out
            </button>
          </div>
        </div>
      </header>

      {/* ─── Page content ─── */}
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
