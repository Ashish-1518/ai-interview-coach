/**
 * AuthContext — manages login state across the React tree.
 *
 * HOW IT WORKS (important for your viva):
 *
 * 1. The JWT token lives in a React ref (`tokenRef`), NOT in localStorage.
 *    - Refs survive re-renders but vanish on page refresh.
 *    - This is intentional: XSS attacks can't read `document.cookie` or
 *      `localStorage` to steal the token because it only exists in JS memory.
 *    - Tradeoff: the user must log in again after a page refresh. For a
 *      demo/interview tool, that's acceptable and the more secure default.
 *
 * 2. We register a "token getter" with the API client so `api.ts` can attach
 *    the Authorization header without importing React or this context.
 *
 * 3. `user` is fetched via TanStack Query (useQuery) — it caches the /me
 *    response and refetches automatically when the window regains focus.
 */
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react'

import { useQuery, useQueryClient } from '@tanstack/react-query'

import * as api from '@/lib/api'
import { setTokenGetter } from '@/lib/api'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface AuthState {
  /** Current user, null while loading or logged out. */
  user: api.UserResponse | null
  /** True while the initial /me call is in-flight. */
  isLoading: boolean
  /** True when the user holds a valid token. */
  isAuthenticated: boolean
  /** Store token from login/register response, then refetch user. */
  setToken: (token: string) => void
  /** Clear token and cached user. */
  logout: () => void
}

const AuthContext = createContext<AuthState | null>(null)

// ---------------------------------------------------------------------------
// Provider
// ---------------------------------------------------------------------------

export function AuthProvider({ children }: { children: ReactNode }) {
  const tokenRef = useRef<string | null>(null)
  // We keep a counter so changing the token triggers a React re-render (refs
  // alone don't) which lets useQuery know it should re-run.
  const [tokenVersion, setTokenVersion] = useState(0)
  const queryClient = useQueryClient()

  // Register the getter once — the closure captures the ref.
  useMemo(() => setTokenGetter(() => tokenRef.current), [])

  const setToken = useCallback(
    (token: string) => {
      tokenRef.current = token
      setTokenVersion((v) => v + 1)
    },
    [],
  )

  const logout = useCallback(() => {
    tokenRef.current = null
    setTokenVersion((v) => v + 1)
    queryClient.clear()
  }, [queryClient])

  // Fetch current user whenever the token changes.
  const { data: user, isLoading } = useQuery({
    queryKey: ['auth', 'me', tokenVersion],
    queryFn: api.getMe,
    enabled: tokenRef.current !== null,
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 min — don't spam /me
  })

  const value = useMemo<AuthState>(
    () => ({
      user: user ?? null,
      isLoading: tokenRef.current !== null && isLoading,
      isAuthenticated: !!user,
      setToken,
      logout,
    }),
    [user, isLoading, setToken, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// ---------------------------------------------------------------------------
// Hook
// ---------------------------------------------------------------------------

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used inside <AuthProvider>')
  }
  return ctx
}
