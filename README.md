📌 Project Overview



AI Interview Coach is a production-style full-stack AI/ML project that simulates realistic technical and HR interviews.



The platform allows a candidate to:



• Create an account and candidate profile

• Upload and analyze a resume

• Add a target job description

• Select an interview type, role, and difficulty

• Take AI-generated mock interviews

• Answer questions using text or voice

• Receive structured AI-powered feedback

• Track interview performance over time

• Identify weak areas and skill gaps

• Get personalized recommendations



The project is being developed incrementally so that every major component can be understood, tested, and explained during technical interviews.



────────



🎯 Main Goals



The project has four primary goals:



1\. Interview Simulation

&#x20; • Generate realistic interview questions.

&#x20; • Maintain interview context.

&#x20; • Adapt question difficulty based on performance.

&#x20; • Ask relevant follow-up questions.

2\. Answer Evaluation

&#x20; • Analyze candidate answers.

&#x20; • Evaluate relevance, correctness, completeness, communication, structure, and specificity.

&#x20; • Provide actionable feedback.

&#x20; • Evaluate behavioral answers using the STAR framework.

3\. Career Intelligence

&#x20; • Analyze resumes.

&#x20; • Analyze job descriptions.

&#x20; • Compare candidate skills with job requirements.

&#x20; • Identify skill gaps.

&#x20; • Provide personalized preparation recommendations.

4\. Performance Tracking

&#x20; • Store interview history.

&#x20; • Track scores and weak areas.

&#x20; • Visualize improvement over time.

&#x20; • Generate performance reports.



────────



✨ Features



Core Features



• User registration and authentication

• Candidate profile

• Resume upload

• Resume parsing

• Interview setup

• AI-generated questions

• Text-based mock interviews

• AI answer evaluation

• Interview reports

• Interview history

• Performance dashboard



Advanced Features



• Voice-based interviews

• Speech-to-text

• Speaking-speed analysis

• Filler-word detection

• Pause analysis

• Job-description matching

• Semantic similarity using embeddings

• Skill-gap analysis

• Personalized recommendations

• Adaptive interview difficulty

• Follow-up question generation

• Advanced ML-based analytics



────────



🧠 Interview Types



The platform supports multiple interview modes:



HR Interview



Examples:



• Tell me about yourself.

• What are your strengths and weaknesses?

• Why should we hire you?

• Where do you see yourself in five years?



Technical Interview



Questions related to:



• Programming

• Data Structures \& Algorithms

• DBMS

• Operating Systems

• Computer Networks

• OOP

• Software Engineering

• Python

• Java

• C++

• Machine Learning

• Artificial Intelligence

• NLP



Behavioral Interview



Behavioral answers are evaluated using the STAR framework:



• Situation

• Task

• Action

• Result



Resume-Based Interview



Questions are generated from:



• Projects

• Skills

• Education

• Experience

• Certifications

• Achievements



Mixed Interview



Combines:



• HR

• Technical

• Behavioral

• Resume-based questions



────────



🏗️ System Architecture



High-level architecture:



&#x20;                        ┌──────────────────────┐

&#x20;                        │       Frontend       │

&#x20;                        │   React + TypeScript │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;                                   │ REST API

&#x20;                                   ▼

&#x20;                        ┌──────────────────────┐

&#x20;                        │       FastAPI        │

&#x20;                        │       Backend        │

&#x20;                        └──────────┬───────────┘

&#x20;                                   │

&#x20;              ┌────────────────────┼────────────────────┐

&#x20;              │                    │                    │

&#x20;              ▼                    ▼                    ▼

&#x20;       ┌─────────────┐      ┌─────────────┐      ┌─────────────┐

&#x20;       │ PostgreSQL  │      │ AI Services │      │ ML Services │

&#x20;       │ + pgvector  │      │    / LLM    │      │  Analytics  │

&#x20;       └─────────────┘      └─────────────┘      └─────────────┘

&#x20;                                   │

&#x20;                    ┌──────────────┼──────────────┐

&#x20;                    │              │              │

&#x20;                    ▼              ▼              ▼

&#x20;                 LLM API      Embeddings      Speech API



────────



🛠️ Technology Stack



Frontend



• React

• TypeScript

• Vite

• HTML5

• CSS

• Modern component-based UI



Backend



• Python

• FastAPI

• Pydantic

• SQLAlchemy

• Alembic



Database



• PostgreSQL

• pgvector for vector similarity/search



AI / ML



• Large Language Models

• NLP

• Embeddings

• Semantic similarity

• Traditional ML where appropriate

• Speech-to-text

• Text analysis



Authentication



• JWT

• Password hashing

• Protected API routes



DevOps



• Docker

• Docker Compose

• GitHub Actions CI/CD

• Nginx reverse proxy

• Gunicorn production server

• Render deployment

• Environment variables

• Automated testing



────────



📂 Project Structure



ai-interview-coach/

│

├── frontend/

│

├── backend/

│   ├── app/

│   │   ├── api/

│   │   ├── core/

│   │   ├── models/

│   │   ├── schemas/

│   │   ├── services/

│   │   ├── ai/

│   │   ├── ml/

│   │   └── utils/

│   │

│   ├── tests/

│   └── requirements.txt

│

├── database/

│

├── docker/

│

├── docs/

│

├── .env.example

├── .gitignore

├── docker-compose.yml

├── DEVELOPMENT\_PLAN.md

├── PROJECT\_SPEC.md

├── README.md

└── LICENSE



The structure may evolve during development if a change improves maintainability or scalability.



────────



🔄 Basic User Flow



Register / Login

&#x20;      │

&#x20;      ▼

Create Candidate Profile

&#x20;      │

&#x20;      ▼

Upload Resume

&#x20;      │

&#x20;      ▼

Resume Parsing

&#x20;      │

&#x20;      ▼

Select Target Role

&#x20;      │

&#x20;      ▼

Add Job Description (Optional)

&#x20;      │

&#x20;      ▼

Configure Interview

&#x20;      │

&#x20;      ▼

Start Interview

&#x20;      │

&#x20;      ▼

AI Generates Question

&#x20;      │

&#x20;      ▼

Candidate Answers

&#x20;      │

&#x20;      ▼

AI Evaluates Answer

&#x20;      │

&#x20;      ▼

Follow-up / Next Question

&#x20;      │

&#x20;      ▼

Interview Complete

&#x20;      │

&#x20;      ▼

Performance Report

&#x20;      │

&#x20;      ▼

Recommendations + Skill Gaps



────────



📊 Answer Evaluation



The answer evaluation system should provide structured feedback.



Example evaluation dimensions:



|Metric              |Description                                   |

|--------------------|----------------------------------------------|

|Overall Score       |Overall quality of the answer                 |

|Relevance           |How directly the answer addresses the question|

|Technical Accuracy  |Correctness of technical information          |

|Completeness        |Whether important points were covered         |

|Communication       |Clarity and readability                       |

|Structure           |Logical organization of the response          |

|Specificity         |Use of concrete examples/details              |

|Conciseness         |Avoidance of unnecessary information          |

|Confidence Indicator|Language-based confidence signals             |



Scores should be generated from actual analysis and validated through structured schemas.



The system must not generate random scores simply to make the application look intelligent.



────────



🧠 AI Architecture



The AI system is designed as modular services instead of putting all AI logic into a single function.



Expected services include:



AIProvider

&#x20;   │

&#x20;   ├── LLMService

&#x20;   │

&#x20;   ├── EmbeddingService

&#x20;   │

&#x20;   ├── SpeechService

&#x20;   │

&#x20;   ├── ResumeParser

&#x20;   │

&#x20;   ├── QuestionGenerator

&#x20;   │

&#x20;   ├── AnswerEvaluator

&#x20;   │

&#x20;   └── RecommendationService



This makes it possible to change AI providers without rewriting the entire application.



────────



📄 Resume Intelligence



The resume parser should extract information such as:



• Name

• Education

• Skills

• Projects

• Experience

• Certifications

• Achievements



The system must never invent information that does not exist in the resume.



Extracted information can be used to generate personalized interview questions.



Example:



Resume:

Python

Machine Learning

University Management App



&#x20;       ↓



Generated Questions:



1\. Explain how you used Python in your project.

2\. What machine learning techniques have you worked with?

3\. Explain the architecture of your University Management App.



────────



💼 Job Description Matching



The system can compare:



Candidate Resume

&#x20;      +

Job Description

&#x20;      ↓

Skill Extraction

&#x20;      ↓

Semantic Matching

&#x20;      ↓

Skill Gap Analysis

&#x20;      ↓

Personalized Recommendations



Possible output:



Overall Match: 78%



Strong Skills:

✓ Python

✓ SQL

✓ Machine Learning



Needs Improvement:

△ Docker

△ FastAPI

△ System Design



The matching system should use meaningful semantic analysis rather than simple keyword counting alone.



────────



🎤 Voice Interview



The voice pipeline is:



Microphone

&#x20;   ↓

Audio Input

&#x20;   ↓

Speech-to-Text

&#x20;   ↓

Transcript

&#x20;   ↓

Answer Evaluation

&#x20;   ↓

Speech Analysis

&#x20;   ↓

Feedback



Possible speech metrics:



• Speaking speed

• Filler words

• Pause duration

• Response duration

• Repeated words



The application should avoid claiming that these measurements can reliably diagnose emotions, personality, or psychological states.



────────



📈 Performance Dashboard



The dashboard should eventually display:



• Average interview score

• Technical score

• Communication score

• HR score

• Behavioral score

• Strongest skills

• Weakest skills

• Interview history

• Score trends

• Skill gaps

• Recommended topics



Example:



Overall Performance

████████████████░░░░ 82%



Technical

██████████████████░░ 90%



Communication

███████████████░░░░░ 76%



Behavioral

████████████████░░░░ 82%



────────



🔐 Security \& Privacy



The application should follow secure development practices.



Authentication



• Passwords must be securely hashed.

• JWT should be used for authentication.

• Protected endpoints must require authentication.



Secrets



Never hardcode:



• API keys

• Database passwords

• JWT secrets

• Service credentials



Use environment variables.



Example:



DATABASE\_URL=

SECRET\_KEY=

AI\_API\_KEY=



A .env.example file should contain variable names without real secrets.



File Upload Security



Resume uploads should include:



• File type validation

• File size limits

• Safe filenames

• Secure storage

• Appropriate error handling



Privacy



Users should eventually be able to:



• Delete resumes

• Delete interview history

• Delete recordings

• Delete their account



Audio should not be retained unnecessarily.



────────



🧪 Testing



The project should include tests for:



Backend



• Authentication

• Registration

• Login

• Protected routes

• Database operations

• Resume upload

• Interview creation

• Interview flow

• Answer evaluation



AI Services



AI services should be tested with mocked providers where appropriate.



Tests should verify:



• Structured output

• Validation

• Error handling

• Invalid AI responses

• Missing data



Frontend



Test important user flows such as:



Login

&#x20; ↓

Dashboard

&#x20; ↓

Create Interview

&#x20; ↓

Answer Question

&#x20; ↓

Complete Interview

&#x20; ↓

View Report



────────



🐳 Docker



The project should support local development using Docker.



Expected services may include:



Frontend

Backend

PostgreSQL



Redis or other infrastructure should only be added if there is a real requirement.



Example:



docker compose up



────────



🚀 Development Roadmap



The project will be developed in phases.



Phase 0 — Architecture



• Understand requirements

• Select technology stack

• Design architecture

• Design database

• Design AI architecture

• Define API structure

• Define folder structure



Phase 1 — Backend Foundation



• Create FastAPI application

• Configure environment variables

• Add project configuration

• Add logging

• Add basic API structure

• Add health endpoint



Phase 2 — Database \& Authentication



• PostgreSQL setup

• SQLAlchemy

• Alembic

• User model

• Registration

• Login

• Password hashing

• JWT authentication



Phase 3 — Candidate Profile \& Resume



• Candidate profile

• Resume upload

• Resume storage

• Resume parsing

• Extract structured candidate information



Phase 4 — Interview Engine



• Interview configuration

• Question generation

• Interview sessions

• Question sequencing

• Follow-up questions

• Adaptive difficulty



Phase 5 — Answer Evaluation



• Answer submission

• LLM evaluation

• Structured evaluation schema

• Feedback generation

• Interview report



Phase 6 — Frontend



• Authentication UI

• Dashboard

• Profile

• Resume upload

• Interview setup

• Interview interface

• Results page



Phase 7 — Analytics



• Score history

• Performance trends

• Weak areas

• Strong areas

• Dashboard analytics



Phase 8 — Job Matching



• Job description parsing

• Skill extraction

• Resume-JD matching

• Embeddings

• Skill-gap analysis

• Recommendations



Phase 9 — Voice



• Microphone input

• Speech-to-text

• Transcript processing

• Speaking analysis

• Voice interview interface



Phase 10 — Advanced ML



• Meaningful ML features

• Performance prediction where justified

• Personalized recommendations

• Advanced analytics



Phase 11 — Production Readiness



• Error handling

• Security improvements

• Testing

• Docker

• Logging

• Performance optimization

• Deployment preparation



Phase 12 — Portfolio



• Final README

• Architecture documentation

• Screenshots

• Demo

• Resume bullet points

• Interview explanation

• LinkedIn/project description



────────



🎓 Learning Philosophy



This project is not intended to be a black-box AI-generated project.



The developer should understand:



• Why each technology is being used

• How the backend works

• How APIs work

• How databases work

• How authentication works

• How AI services work

• How prompts are designed

• How structured AI outputs are validated

• How embeddings work

• How ML components are integrated

• How frontend and backend communicate

• How the project is deployed



Every major implementation should be accompanied by a concise explanation.



────────



⚠️ Important Development Rules



1\. Build incrementally.

2\. Do not generate the entire project in one response.

3\. Do not skip architecture decisions.

4\. Explain important code before or alongside implementation.

5\. Do not use fake/random AI results.

6\. Do not hardcode secrets.

7\. Keep AI providers replaceable.

8\. Use structured outputs wherever possible.

9\. Validate AI-generated data using schemas.

10\. Write tests for important functionality.

11\. Keep the code modular.

12\. Avoid unnecessary dependencies.

13\. Do not add infrastructure without a reason.

14\. Prefer simple solutions before complex ones.

15\. Keep the application understandable to a student developer.



────────



📌 Non-Goals



This project should not:



• Claim to guarantee employment.

• Diagnose mental health conditions.

• Reliably determine a person’s emotions from their voice.

• Make hiring decisions.

• Store biometric information unnecessarily.

• Invent resume information.

• Generate meaningless random scores.



────────



🌱 Future Improvements



Potential future features:



• Multiple AI provider support

• Interview difficulty personalization

• Real-time voice interviewer

• Coding interview environment

• Code execution

• AI-generated coding questions

• System design interview mode

• Company-specific interview preparation

• Personalized learning roadmap

• Email reports

• PDF interview reports

• Leaderboards

• Gamification

• Mobile application



These should only be implemented if they provide real value and do not unnecessarily increase project complexity.



────────



📚 Documentation



Important project documents:



• PROJECT\_SPEC.md — Complete product and technical specification

• DEVELOPMENT\_PLAN.md — Development phases and implementation tracking

• README.md — Project overview and documentation



────────



👨‍💻 Development Approach



The recommended workflow is:



Read Specification

&#x20;      ↓

Understand Architecture

&#x20;      ↓

Implement One Phase

&#x20;      ↓

Run Tests

&#x20;      ↓

Fix Problems

&#x20;      ↓

Understand Implementation

&#x20;      ↓

Commit to Git

&#x20;      ↓

Move to Next Phase



Each phase should be completed and understood before moving to the next one.



────────



🧾 Git Workflow



Use meaningful commits.



Examples:



git commit -m "Initialize FastAPI backend"

git commit -m "Add PostgreSQL database configuration"

git commit -m "Implement user authentication"

git commit -m "Add resume upload service"

git commit -m "Implement interview session API"

git commit -m "Add AI answer evaluation"

git commit -m "Create interview dashboard"



Avoid commits such as:



update

final

final2

changes

new code



────────



⭐ Portfolio Value



This project demonstrates knowledge of:



• Python

• FastAPI

• REST APIs

• React

• TypeScript

• PostgreSQL

• Authentication

• NLP

• LLM integration

• Prompt engineering

• Embeddings

• Semantic search

• Machine Learning

• Speech processing

• Data analysis

• Docker

• Testing

• Software architecture



More importantly, the project is designed to demonstrate how these technologies work together in a real-world application.



────────



🚀 Getting Started



Prerequisites



• Docker & Docker Compose

• Node.js 22+ (for local frontend development)

• Python 3.13+ (for local backend development)

• PostgreSQL 16 with pgvector (or use Docker)



Local Development (Quick Start)



```bash
# Clone the repo
git clone https://github.com/your-username/ai-interview-coach.git
cd ai-interview-coach

# Copy environment variables and edit as needed
cp .env.example .env

# Start PostgreSQL with Docker
docker compose up db -d

# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head       # run database migrations
python seed_db.py          # seed the question bank
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

The frontend runs at http://localhost:5173 and proxies API calls to the backend at http://localhost:8000.



Production Deployment (Docker)



```bash
# Copy and fill in production environment variables
cp .env.production.example .env

# Build and start all services
docker compose -f docker-compose.prod.yml up --build -d
```

This starts three containers:

• **db** — PostgreSQL 16 with pgvector

• **backend** — FastAPI served by Gunicorn with Uvicorn workers; runs Alembic migrations on startup

• **frontend** — React SPA served by Nginx; reverse-proxies `/api` to the backend

The app is accessible at http://localhost.



Deploy to Render (Free Tier)



1. Push this repo to GitHub.

2. Go to https://dashboard.render.com → **New** → **Blueprint**.

3. Connect the GitHub repo — Render reads `render.yaml` and provisions:

   • PostgreSQL database (free tier)

   • Backend web service (Docker)

   • Frontend static site

4. Set `AI_API_KEY` in the Render dashboard if you want LLM features.



Running Tests



```bash
cd backend
pytest -v
```

Tests use SQLite in-memory (no PostgreSQL needed). AI calls are not configured in tests, so LLM-based scores will be `None` while NLP/deterministic features still run.



Environment Variables



| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development`, `test`, or `production` |
| `APP_DEBUG` | `false` | Enable debug mode |
| `DATABASE_URL` | — | PostgreSQL connection string |
| `JWT_SECRET_KEY` | — | Secret for signing JWT tokens |
| `AI_API_KEY` | _(empty)_ | OpenAI API key (optional — disables LLM features when empty) |
| `AI_MODEL` | `gpt-4o-mini` | Model to use for AI evaluation |
| `BACKEND_CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed origins |

See `.env.example` and `.env.production.example` for the full list.



CI/CD



The project uses GitHub Actions (`.github/workflows/ci.yml`):

• **Backend job** — installs dependencies, runs `pytest`

• **Frontend job** — installs dependencies, runs lint + build

• **Docker job** _(main branch only)_ — builds both Docker images



────────



📜 License



This project is intended for educational and portfolio purposes.



A suitable open-source license can be selected before public release.

