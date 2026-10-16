# Development Plan

## Phase 0 — Architecture
- [x] System architecture
- [x] Tech stack
- [x] Database schema
- [x] Folder structure

## Phase 1 — Backend Foundation
- [x] FastAPI setup
- [x] Configuration
- [x] Database connection
- [x] Basic API (health endpoint)
- [x] Logging
- [x] CORS middleware
- [x] Alembic migrations

## Phase 2 — Authentication
- [x] Registration
- [x] Login
- [x] JWT
- [x] Protected routes
- [x] User model & migration
- [x] Tests (test_auth, test_security)

## Phase 3 — Resume & Profile System
- [x] Candidate profile model & API
- [x] PDF upload
- [x] Text extraction
- [x] Resume parsing
- [x] Structured resume data
- [x] Migration (profiles & resumes)
- [x] Tests (test_profile, test_resume_parser, test_resume_api)

## Phase 4 — Interview Engine
- [x] Question bank model & seed data
- [x] Interview model & migration
- [x] Interview service (create, get next question)
- [x] Question selection service
- [x] Adaptive difficulty algorithm
- [x] Tests (test_interview_engine, test_difficulty)

## Phase 5 — Answer Evaluation
- [x] AI evaluation prompts & provider
- [x] Evaluation service
- [x] NLP text features (filler words, structure, etc.)
- [x] Answer & evaluation schemas
- [x] Evaluation model & migration
- [x] Tests (test_evaluation, test_text_features)

## Phase 6 — Interview Reports & Analytics
- [x] Report service & schema
- [x] Analytics API endpoint
- [x] Frontend: InterviewReportPage
- [x] Frontend: AnalyticsPage
- [x] Frontend: Charts component

## Phase 7 — Job Matching
- [x] Job match service & schema
- [x] Job match API endpoint
- [x] ML similarity (embeddings)
- [x] Frontend: JobMatchPage

## Phase 8 — Voice Interviews
- [x] Voice service & schema
- [x] Voice API endpoint
- [x] Frontend: VoiceRecorder component
- [x] Frontend: LiveInterviewPage

## Phase 9 — ML Difficulty Classifier
- [x] Difficulty classifier model
- [x] Difficulty ML API endpoint & schema

## Phase 10 — Deployment
- [x] Dockerfile (multi-stage backend build with Gunicorn)
- [x] docker-compose.yml (PostgreSQL + backend — local dev)
- [x] docker-compose.prod.yml (PostgreSQL + backend + Nginx frontend — production)
- [x] Frontend Dockerfile & Nginx config
- [x] Gunicorn production config
- [x] Entrypoint script (Alembic migrations on startup)
- [x] Production environment config (.env.production.example)
- [x] Render deployment config (render.yaml)
- [x] CI/CD pipeline (GitHub Actions — test + lint + Docker build)
- [x] End-to-end testing (test_e2e_flow.py)
- [x] README deployment documentation

## Frontend (built across Phases 1–9)
- [x] React + TypeScript + Vite setup
- [x] AuthContext & API client
- [x] GuestLayout / AppLayout
- [x] LoginPage & RegisterPage
- [x] DashboardPage
- [x] ProfilePage
- [x] ResumesPage
- [x] InterviewsListPage & InterviewSetupPage
- [x] LiveInterviewPage
- [x] InterviewReportPage
- [x] AnalyticsPage
- [x] JobMatchPage
- [x] VoiceRecorder component
- [x] Charts component
