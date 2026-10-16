/**
 * App — sets up routing and global providers.
 *
 * Route tree:
 *   / (redirect → /dashboard)
 *   /login       ← GuestLayout
 *   /register    ← GuestLayout
 *   /dashboard   ← AppLayout (auth required)
 *   /profile     ← AppLayout
 *   /resumes     ← AppLayout
 *   /interviews        ← list
 *   /interviews/new    ← setup form
 *   /interviews/:id    ← report
 *   /interviews/:id/live ← live interview
 *   /analytics   ← AppLayout
 */
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import { AuthProvider } from '@/contexts/AuthContext'
import AppLayout from '@/components/layout/AppLayout'
import GuestLayout from '@/components/layout/GuestLayout'

import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import DashboardPage from '@/pages/DashboardPage'
import ProfilePage from '@/pages/ProfilePage'
import ResumesPage from '@/pages/ResumesPage'
import InterviewsListPage from '@/pages/InterviewsListPage'
import InterviewSetupPage from '@/pages/InterviewSetupPage'
import LiveInterviewPage from '@/pages/LiveInterviewPage'
import InterviewReportPage from '@/pages/InterviewReportPage'
import AnalyticsPage from '@/pages/AnalyticsPage'
import JobMatchPage from '@/pages/JobMatchPage'

// One QueryClient instance shared by the entire app. `staleTime` keeps
// fetched data fresh for 2 minutes — avoids needless refetches when users
// jump between tabs.
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 2 * 60 * 1000,
      refetchOnWindowFocus: false,
    },
  },
})

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public routes */}
            <Route element={<GuestLayout />}>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
            </Route>

            {/* Authenticated routes */}
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/resumes" element={<ResumesPage />} />
              <Route path="/interviews" element={<InterviewsListPage />} />
              <Route path="/interviews/new" element={<InterviewSetupPage />} />
              <Route path="/interviews/:id" element={<InterviewReportPage />} />
              <Route path="/interviews/:id/live" element={<LiveInterviewPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/job-match" element={<JobMatchPage />} />
            </Route>

            {/* Catch-all redirect */}
            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}
