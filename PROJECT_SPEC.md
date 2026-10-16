\# AI Interview Coach â€” Project Specification



> \*\*Status:\*\* Active specification  

> \*\*Version:\*\* 1.0  

> \*\*Project Type:\*\* B.Tech CSE (AIML) portfolio / placement project  

> \*\*Primary Goal:\*\* Build a production-style AI-powered mock interview platform from scratch, while ensuring the developer understands every major component.



\---



\## 1. Project Overview



\*\*AI Interview Coach\*\* is a full-stack AI/ML web application that simulates realistic job interviews and gives candidates personalized, actionable feedback.



The platform should allow a candidate to:



1\. Create an account.

2\. Create a candidate profile.

3\. Upload a resume.

4\. Optionally provide a job description.

5\. Select a target role and interview configuration.

6\. Start an AI-generated mock interview.

7\. Answer questions using text and, later, voice.

8\. Receive AI/NLP-based evaluation of each answer.

9\. Receive an interview report.

10\. Track performance across interviews.

11\. Identify weak skills/topics.

12\. Receive personalized preparation recommendations.



The final product should feel like a real SaaS application, not a basic chatbot or CRUD college project.



\---



\# 2. Developer Context



The developer is a B.Tech CSE student specializing in Artificial Intelligence and Machine Learning.



The project is intended to demonstrate practical understanding of:



\- Python

\- FastAPI

\- React

\- TypeScript

\- SQL

\- PostgreSQL

\- REST APIs

\- Authentication

\- NLP

\- LLMs

\- Embeddings

\- Machine Learning

\- Recommendation systems

\- Semantic search

\- Speech processing

\- Docker

\- Testing

\- Deployment

\- Git/GitHub

\- Software architecture



The developer should be able to explain the project in a placement interview.



\---



\# 3. Critical Development Rules



These rules are mandatory.



\## 3.1 Build Incrementally



Do \*\*not\*\* generate the entire project in one response.



Build the project phase by phase.



At the beginning of each phase:



1\. Explain the objective.

2\. Explain the concepts involved.

3\. Explain the files that will be created or modified.

4\. Implement the feature.

5\. Explain important code.

6\. Provide commands to run it.

7\. Provide tests/checks.

8\. Fix issues before moving forward.



Do not skip phases unless explicitly instructed.



\## 3.2 Teach While Building



The AI coding assistant should behave as both:



\- Senior developer

\- Technical mentor



For every major component, explain:



1\. What it does.

2\. Why it is needed.

3\. The underlying concept.

4\. How it fits into the architecture.

5\. The implementation.

6\. Important code decisions.

7\. How to test it.

8\. Common errors.



Prefer readable, maintainable code over unnecessarily clever code.



\## 3.3 No Fake AI



Never create fake results using:



\- Random scores

\- Hardcoded evaluation results

\- Fake confidence values

\- Fake ML predictions

\- Pretend model outputs



Every result must come from one of:



\- An actual ML model

\- An NLP algorithm

\- An embedding/similarity method

\- An LLM evaluation

\- A deterministic algorithm

\- A clearly documented heuristic



The implementation must clearly state which method is being used.



\## 3.4 No Secret Leakage



Never hardcode:



\- API keys

\- Database passwords

\- JWT secrets

\- Tokens

\- Private credentials



Use environment variables and `.env` files.



Commit only `.env.example`, never the real `.env`.



\## 3.5 Keep the Architecture Modular



Separate:



\- API routes

\- Business logic

\- AI services

\- ML services

\- Database models

\- Validation schemas

\- Authentication

\- Configuration

\- Utilities



Do not put the entire application into a few giant files.



\## 3.6 Test Before Progressing



Each major feature should be tested before the next dependent feature is built.



\---



\# 4. Target Users



Primary users:



\- College students

\- Fresh graduates

\- Job seekers

\- Developers

\- Data analysts

\- Data scientists

\- Data/ML engineers

\- AI engineers

\- Software engineers



\---



\# 5. Supported Target Roles



Initial roles should include:



\- Software Developer

\- Full Stack Developer

\- Python Developer

\- Java Developer

\- Data Analyst

\- Data Scientist

\- Machine Learning Engineer

\- AI Engineer

\- Backend Developer

\- Frontend Developer



The architecture must allow additional roles to be added without major code changes.



\---



\# 6. Interview Types



\## 6.1 HR Interview



Possible topics:



\- Tell me about yourself

\- Strengths

\- Weaknesses

\- Career goals

\- Teamwork

\- Leadership

\- Conflict resolution

\- Failure

\- Motivation

\- Why should we hire you?

\- Why this company?

\- Career aspirations



\## 6.2 Technical Interview



Questions may cover:



\- Programming

\- OOP

\- DSA

\- DBMS

\- Operating Systems

\- Computer Networks

\- AI/ML

\- System design

\- Role-specific technologies



The selected role should influence the topics.



\## 6.3 Behavioral Interview



Evaluate:



\- Communication

\- Problem solving

\- Leadership

\- Adaptability

\- Teamwork

\- Decision making

\- Conflict handling



\## 6.4 Resume-Based Interview



Questions should be generated from information actually present in the user's resume.



Possible sources:



\- Projects

\- Skills

\- Internships

\- Certifications

\- Education

\- Achievements

\- Technologies



The system must not invent resume facts.



\## 6.5 Mixed Interview



Combine:



\- HR

\- Technical

\- Behavioral

\- Resume-based



\---



\# 7. Interview Setup



Before an interview begins, allow the user to select:



\## Candidate Information



\- Name

\- Resume

\- Target role

\- Experience level



\## Interview Type



\- HR

\- Technical

\- Behavioral

\- Resume-based

\- Mixed



\## Difficulty



\- Beginner

\- Intermediate

\- Advanced



\## Number of Questions



\- 5

\- 10

\- 15

\- Custom



\## Answer Mode



Initially:



\- Text



Later:



\- Voice



\---



\# 8. AI Interview Engine



The AI interviewer should behave like a real interviewer.



It should:



\- Ask one question at a time.

\- Wait for the answer.

\- Analyze the answer.

\- Maintain interview context.

\- Select an appropriate next question.

\- Generate follow-up questions when appropriate.

\- Adapt question difficulty.

\- Avoid repeating questions.

\- Stay focused on the target role.

\- Use resume/job-description information when relevant.



\### Example



AI:



> Tell me about a challenging project you worked on.



Candidate:



> I built a university management system...



AI:



> What was the biggest technical challenge you faced while developing it?



Candidate:



> Database performance...



AI:



> How did you identify the performance bottleneck?



The interview should feel conversational rather than like a static questionnaire.



\---



\# 9. Question Generation



Questions should depend on:



\- Target role

\- Difficulty

\- Interview type

\- Resume

\- Job description

\- Previous questions

\- Previous answers

\- Candidate performance

\- Interview context



Maintain question history to reduce repetition.



Questions should be categorized by:



\- Topic

\- Difficulty

\- Interview type

\- Role

\- Skills

\- Source



\---



\# 10. Adaptive Difficulty



The system should adjust question difficulty based on performance.



Example:



Strong performance:



`Beginner â†’ Intermediate â†’ Advanced`



Weak performance:



`Advanced â†’ Intermediate`



The implementation must document the rules/algorithm used.



Avoid arbitrary difficulty changes.



\---



\# 11. Answer Evaluation



Every answer should be evaluated.



Generate scores from 0â€“100 for:



\### Overall Score



Overall quality of the answer.



\### Relevance



Did the answer address the question?



\### Technical Accuracy



Is the information technically correct?



\### Completeness



Did the candidate provide enough useful information?



\### Communication



Was the answer clear and understandable?



\### Confidence Indicator



Use available textual/voice signals carefully.



Do not claim to detect a person's psychological state.



\### Structure



Does the answer have a logical structure?



\### Specificity



Does the candidate use concrete examples?



\### Conciseness



Does the candidate avoid unnecessary repetition?



\---



\# 12. Behavioral Evaluation â€” STAR Framework



For behavioral questions, evaluate:



\- Situation

\- Task

\- Action

\- Result



Example:



```text

Situation: 18/25

Task:      20/25

Action:    22/25

Result:    14/25

```



Feedback should explain how to improve.



Example:



> Your answer clearly explains the situation and task, but the result is vague. Try describing the measurable impact of your actions.



Do not encourage memorization of generated answers.



\---



\# 13. Per-Answer Feedback



After submitting an answer, provide concise feedback.



Example:



```text

Answer Score: 78/100



Strengths:

\- Good technical explanation

\- Clear communication

\- Relevant example



Weaknesses:

\- Could provide more measurable results

\- Some unnecessary repetition



Suggested Improvement:

Try answering using the STAR framework and include measurable outcomes.

```



The system should focus on improving the candidate's own answer.



\---



\# 14. Voice Interview



Voice support should be added after the text MVP works.



Pipeline:



```text

Microphone

&#x20;   â†“

Audio Recording

&#x20;   â†“

Speech-to-Text

&#x20;   â†“

Transcript

&#x20;   â†“

Answer Analysis

&#x20;   â†“

Score

&#x20;   â†“

Feedback

```



The speech-to-text provider must be abstracted so it can be replaced later.



\---



\# 15. Communication Analysis



For voice answers, optionally analyze:



\- Speaking speed

\- Pauses

\- Filler words

\- Repetition

\- Sentence clarity

\- Approximate confidence indicators



Track filler words such as:



\- um

\- uh

\- like

\- basically

\- actually

\- you know

\- so



Possible metrics:



```text

Filler words: 12

Average speaking speed: 138 WPM

Pause frequency: Moderate

```



\### Important limitation



Do not claim:



> You are nervous.



Instead use cautious wording such as:



> Possible confidence indicator: frequent pauses.



Voice analysis must not pretend to accurately diagnose emotions or psychological states.



\---



\# 16. Resume Upload and Parsing



Allow PDF resume uploads.



Extract information such as:



\- Name

\- Education

\- Skills

\- Projects

\- Experience

\- Certifications

\- Achievements



Convert extracted content into structured data.



Example:



```json

{

&#x20; "name": "Candidate Name",

&#x20; "skills": \["Python", "SQL", "Machine Learning"],

&#x20; "projects": \[

&#x20;   {

&#x20;     "name": "Project Name",

&#x20;     "technologies": \["Python", "FastAPI"]

&#x20;   }

&#x20; ]

}

```



The parser must preserve the distinction between:



\- Extracted facts

\- AI-generated interpretation



The system must not invent candidate experience.



\---



\# 17. Job Description Analysis



Allow users to paste or upload a job description.



Extract:



\- Required skills

\- Preferred skills

\- Technologies

\- Experience requirements

\- Responsibilities

\- Domain keywords



Generate a job match analysis.



Example:



```text

Job Match Score: 78%



Strong Matches:

âœ“ Python

âœ“ SQL

âœ“ Machine Learning



Missing / Weak Skills:

âœ— Docker

âœ— AWS

âœ— FastAPI

```



Then generate personalized preparation recommendations.



\---



\# 18. Resume â†” Job Matching



Use semantic similarity/embeddings where appropriate.



Pipeline:



```text

Resume

&#x20;  â†“

Text Extraction

&#x20;  â†“

Structured Information

&#x20;  â†“

Embedding / Feature Extraction

&#x20;  â†“

Job Description

&#x20;  â†“

Similarity + Skill Analysis

&#x20;  â†“

Match Score

```



Do not represent an embedding similarity score as an absolute measure of employability.



Call it a match indicator.



\---



\# 19. Personalized Interview Generation



Combine:



\- Resume

\- Job description

\- Target role

\- Experience level

\- Interview type

\- Skill gaps

\- Previous performance



Example:



Resume:



\- Python

\- Machine Learning

\- TensorFlow



Job:



\- Python

\- PyTorch

\- Docker



The system should increase interview focus on:



\- Python

\- ML fundamentals

\- PyTorch

\- Docker



\---



\# 20. Performance Dashboard



The dashboard should show:



\- Overall interview score

\- Communication score

\- Technical score

\- Confidence indicator

\- Relevance score

\- Problem-solving score

\- Average answer score

\- Interview completion rate

\- Weakest topics

\- Strongest topics

\- Progress over time



Example:



```text

Technical Knowledge       82

Communication             74

Problem Solving           79

Confidence Indicator      68

Answer Relevance          88

```



Use charts where they add value.



\---



\# 21. Interview History



Store completed interviews.



Display:



\- Date

\- Target role

\- Interview type

\- Difficulty

\- Score

\- Weak areas

\- Strong areas

\- Duration

\- Questions answered



Example:



```text

Interview #1 â†’ 61

Interview #2 â†’ 69

Interview #3 â†’ 76

Interview #4 â†’ 82

```



Allow users to see improvement over time.



\---



\# 22. Personalized Recommendations



Recommendations should be based on actual performance.



Example:



Weak DBMS performance:



```text

Recommended topics:

\- SQL joins

\- Indexing

\- Normalization

\- Transactions

```



Weak communication:



```text

Recommended:

\- STAR method

\- Structured answers

\- Concise explanations

```



Weak DSA:



```text

Recommended:

\- Arrays

\- Hashing

\- Trees

\- Dynamic Programming

```



Recommendations should use measurable evidence from interview performance.



\---



\# 23. ML/NLP Requirements



The project must contain meaningful AI/ML components.



The project should not be merely an LLM API wrapper.



Potential components:



\- Resume/job semantic similarity

\- Answer semantic similarity

\- Skill-gap analysis

\- Question difficulty classification

\- Candidate performance prediction

\- Candidate clustering

\- Recommendation system

\- NLP-based text features



For every AI/ML component, explicitly document whether it uses:



\- Traditional ML

\- Deep learning

\- NLP

\- Embeddings

\- LLM

\- Rule-based logic

\- Heuristics



Do not call an LLM API a trained ML model.



\---



\# 24. Embeddings and Semantic Search



Use embeddings where they provide genuine value.



Potential uses:



\- Resume â†” job similarity

\- Answer â†” expected concept similarity

\- Semantic question retrieval

\- Skill similarity

\- Question retrieval



Preferred initial architecture:



\- PostgreSQL

\- pgvector where practical



The vector layer should be abstract enough to replace later.



\---



\# 25. AI Service Abstraction



Do not tightly couple the project to one AI provider.



Create service abstractions such as:



```text

AIProvider

LLMService

EmbeddingService

SpeechService

ResumeParser

QuestionGenerator

AnswerEvaluator

RecommendationService

```



The application should be able to switch providers without rewriting the whole system.



All provider credentials must come from environment variables.



\---



\# 26. Structured LLM Outputs



LLM evaluations must use structured output.



Example:



```json

{

&#x20; "overall\_score": 78,

&#x20; "relevance": 82,

&#x20; "technical\_accuracy": 75,

&#x20; "communication": 80,

&#x20; "completeness": 73,

&#x20; "specificity": 79,

&#x20; "strengths": \[],

&#x20; "weaknesses": \[],

&#x20; "suggestions": \[],

&#x20; "detected\_topics": \[],

&#x20; "recommended\_topics": \[]

}

```



Validate the response using Pydantic or an equivalent schema.



Handle malformed model responses safely.



Never trust raw model output blindly.



\---



\# 27. AI Cost Control



Minimize unnecessary AI calls.



Use:



\- Efficient prompts

\- Structured outputs

\- Caching where appropriate

\- Embedding caching

\- Question reuse/retrieval

\- Configurable model selection



Use deterministic code where an LLM is unnecessary.



\---



\# 28. Backend



Preferred backend stack:



\- Python

\- FastAPI

\- Pydantic

\- SQLAlchemy

\- Alembic

\- PostgreSQL

\- JWT authentication

\- Secure password hashing



Suggested service layers:



```text

API Routes

&#x20;   â†“

Schemas / Validation

&#x20;   â†“

Services

&#x20;   â†“

AI / ML Services

&#x20;   â†“

Database

```



\---



\# 29. Backend API Areas



Initial API areas:



```text

/auth

/users

/profile

/resume

/jobs

/interviews

/questions

/answers

/evaluations

/reports

/dashboard

/recommendations

```



Example endpoints:



```text

POST /auth/register

POST /auth/login



GET  /profile

PUT  /profile



POST /resume/upload

GET  /resume



POST /jobs/analyze



POST /interviews

GET  /interviews/{id}



POST /interviews/{id}/answers

GET  /interviews/{id}/report



GET  /dashboard

GET  /recommendations

```



Use FastAPI's OpenAPI documentation.



\---



\# 30. Database



Use PostgreSQL.



Suggested entities:



\- User

\- CandidateProfile

\- Resume

\- JobDescription

\- Interview

\- InterviewQuestion

\- InterviewAnswer

\- AnswerEvaluation

\- PerformanceReport

\- Skill

\- Recommendation

\- QuestionBank

\- InterviewSession



Use proper relational relationships.



Do not store the entire application state in one table.



Use migrations with Alembic.



Add indexes where justified.



\---



\# 31. Suggested Database Relationships



High-level relationship:



```text

User

&#x20;â”œâ”€â”€ CandidateProfile

&#x20;â”œâ”€â”€ Resume

&#x20;â”œâ”€â”€ JobDescription

&#x20;â”œâ”€â”€ Interview

&#x20;â”‚    â”œâ”€â”€ InterviewQuestion

&#x20;â”‚    â”‚    â””â”€â”€ InterviewAnswer

&#x20;â”‚    â”‚         â””â”€â”€ AnswerEvaluation

&#x20;â”‚    â””â”€â”€ PerformanceReport

&#x20;â””â”€â”€ Recommendation

```



The exact schema can evolve during Phase 0 after reviewing normalization and access patterns.



\---



\# 32. Frontend



Preferred stack:



\- React

\- TypeScript

\- Modern component/UI library

\- Responsive CSS



Pages:



\- Landing

\- Login

\- Register

\- Dashboard

\- Profile

\- Resume Upload

\- Job Description

\- Interview Setup

\- Live Interview

\- Answer Feedback

\- Interview Report

\- Performance History

\- Recommendations

\- Settings



The UI should be:



\- Responsive

\- Clean

\- Modern

\- Professional

\- Accessible

\- Mobile-friendly



\---



\# 33. Live Interview UI



The interview screen should feel like a real interview.



Example layout:



```text

\--------------------------------------

AI Interviewer



"Tell me about yourself."

\--------------------------------------



Your Answer



\[ Text input / microphone ]



\[ Submit Answer ]



\--------------------------------------



Interview Progress



Question 4 / 10

Difficulty: Intermediate

\--------------------------------------

```



Do not reveal evaluation scores before the answer is submitted.



\---



\# 34. Design Requirements



Use a professional SaaS aesthetic.



Avoid:



\- Excessive gradients

\- Unnecessary animations

\- Huge text

\- Visual clutter

\- Fake AI gimmicks

\- Decorative components with no purpose



Use:



\- Clear hierarchy

\- Consistent spacing

\- Accessible contrast

\- Responsive layouts

\- Subtle animation only when useful

\- Clear loading/error states



\---



\# 35. Authentication



Implement:



\- Registration

\- Login

\- JWT authentication

\- Password hashing

\- Protected routes

\- Token expiration

\- Logout behavior

\- Input validation



Never store plaintext passwords.



\---



\# 36. Security



Implement appropriate protection for:



\- File uploads

\- API endpoints

\- Authentication

\- Database queries

\- CORS

\- Rate limiting where appropriate

\- Input validation

\- Secrets



File uploads must have:



\- Allowed MIME/type validation

\- File size limits

\- Safe filenames

\- Controlled storage

\- Error handling



Do not expose stack traces to users.



\---



\# 37. Privacy



Resume data and interview recordings are sensitive.



Users should eventually be able to:



\- Delete their resume

\- Delete interview history

\- Delete recordings

\- Delete their account



Avoid retaining audio unnecessarily.



Clearly document data retention.



Do not expose one user's data to another user.



\---



\# 38. Error Handling



Handle:



\- Invalid resume

\- Unsupported file

\- Oversized file

\- AI API failure

\- Speech recognition failure

\- Database failure

\- Network failure

\- Invalid answer

\- Expired session

\- Malformed AI response



Provide useful user-facing errors.



Log technical details securely on the backend.



\---



\# 39. Logging



Use structured backend logging.



Log:



\- Request failures

\- AI service failures

\- Authentication failures

\- Important application events



Never log:



\- Passwords

\- API keys

\- JWT secrets

\- Full private resumes

\- Sensitive audio contents

\- Other sensitive user information



\---



\# 40. Testing



Include:



\- Unit tests

\- API tests

\- Authentication tests

\- Database tests

\- Resume upload tests

\- Interview flow tests

\- AI service tests using mocks

\- Evaluation schema tests



AI provider calls should be mockable during tests.



At minimum, demonstrate meaningful coverage of critical paths.



\---



\# 41. Docker



Provide:



\- Backend Dockerfile

\- Frontend Dockerfile

\- PostgreSQL service

\- Optional Redis service only if genuinely needed

\- Docker Compose



The local development environment should be startable with a simple documented command.



\---



\# 42. Deployment



Prepare the application for:



```text

Frontend â†’ Cloud hosting

Backend  â†’ Cloud hosting

Database â†’ Managed PostgreSQL

AI       â†’ External provider

```



Separate:



\- Development

\- Testing

\- Production



Use environment variables.



Provide deployment documentation.



\---



\# 43. Repository Structure



Recommended structure:



```text

ai-interview-coach/

â”‚

â”œâ”€â”€ frontend/

â”‚

â”œâ”€â”€ backend/

â”‚   â”œâ”€â”€ app/

â”‚   â”‚   â”œâ”€â”€ api/

â”‚   â”‚   â”œâ”€â”€ core/

â”‚   â”‚   â”œâ”€â”€ models/

â”‚   â”‚   â”œâ”€â”€ schemas/

â”‚   â”‚   â”œâ”€â”€ services/

â”‚   â”‚   â”œâ”€â”€ ai/

â”‚   â”‚   â”œâ”€â”€ ml/

â”‚   â”‚   â””â”€â”€ utils/

â”‚   â”‚

â”‚   â”œâ”€â”€ tests/

â”‚   â””â”€â”€ requirements.txt

â”‚

â”œâ”€â”€ database/

â”œâ”€â”€ docker/

â”œâ”€â”€ docs/

â”‚

â”œâ”€â”€ .env.example

â”œâ”€â”€ docker-compose.yml

â”œâ”€â”€ DEVELOPMENT\_PLAN.md

â”œâ”€â”€ PROJECT\_SPEC.md

â”œâ”€â”€ README.md

â””â”€â”€ LICENSE

```



Adjust the structure if a better architecture is justified.



\---



\# 44. Documentation Requirements



The final README must include:



\- Project overview

\- Problem statement

\- Features

\- Architecture

\- Tech stack

\- Database schema

\- AI architecture

\- ML pipeline

\- API documentation

\- Installation

\- Environment variables

\- Local development

\- Docker setup

\- Testing

\- Deployment

\- Screenshots

\- Future improvements



\---



\# 45. Architecture Diagram



The conceptual architecture should resemble:



```text

&#x20;                        USER

&#x20;                          |

&#x20;                          v

&#x20;                 React + TypeScript

&#x20;                          |

&#x20;                          v

&#x20;                    FastAPI API

&#x20;                          |

&#x20;       +------------------+------------------+

&#x20;       |                  |                  |

&#x20;       v                  v                  v

&#x20;Authentication      Interview Engine    Resume/Job Engine

&#x20;       |                  |                  |

&#x20;       v                  v                  v

&#x20;  PostgreSQL       +------+-------+      NLP/Embeddings

&#x20;                   |      |       |

&#x20;                   v      v       v

&#x20;                  LLM    ML    Speech

&#x20;                   |      |       |

&#x20;                   +------+-------+

&#x20;                          |

&#x20;                          v

&#x20;                  Evaluation Engine

&#x20;                          |

&#x20;                          v

&#x20;                 Recommendation Engine

&#x20;                          |

&#x20;                          v

&#x20;                     PostgreSQL

```



Document the final architecture in `/docs`.



\---



\# 46. MVP



The first working MVP must include:



1\. Authentication

2\. Candidate profile

3\. Resume upload

4\. Resume parsing

5\. Job role selection

6\. Interview setup

7\. AI question generation

8\. Text-based interview

9\. AI answer evaluation

10\. Interview report

11\. Performance dashboard

12\. Interview history



Only after the MVP is stable should advanced features be added.



\---



\# 47. Advanced Features



After MVP:



13\. Voice interviews

14\. Speech-to-text

15\. Speech analysis

16\. Job description matching

17\. Personalized recommendations

18\. Embedding-based semantic search

19\. Skill-gap analysis

20\. Advanced ML components



\---



\# 48. Future Features



Keep architecture extensible for:



\- Real-time AI avatar

\- Video interviews

\- Coding interview environment

\- Company-specific interview preparation

\- Interview question prediction

\- Leaderboards

\- Mentor dashboard

\- Recruiter dashboard

\- Multi-language interviews

\- Collaborative interviews



Do not implement these during the initial MVP unless explicitly requested.



\---



\# 49. Development Phases



\## Phase 0 â€” Architecture



Deliver:



\- Requirements review

\- Architecture

\- Tech stack

\- Folder structure

\- Database schema

\- AI/ML architecture

\- API architecture

\- Development roadmap

\- Local setup requirements

\- Git strategy



\## Phase 1 â€” Backend Foundation



Build:



\- FastAPI application

\- Configuration

\- Environment handling

\- Database connection

\- Basic health endpoint

\- Initial project structure



\## Phase 2 â€” Database and Authentication



Build:



\- PostgreSQL integration

\- SQLAlchemy models

\- Alembic migrations

\- Registration

\- Login

\- JWT

\- Password hashing

\- Protected routes



\## Phase 3 â€” Candidate Profile and Resume



Build:



\- Profile

\- PDF upload

\- File validation

\- Text extraction

\- Resume parsing

\- Structured resume storage



\## Phase 4 â€” Interview Engine



Build:



\- Interview configuration

\- Question generation

\- Interview session

\- Question history

\- Context management

\- Adaptive difficulty foundation



\## Phase 5 â€” Answer Evaluation



Build:



\- Answer submission

\- LLM evaluation

\- Structured output

\- Pydantic validation

\- Feedback

\- STAR evaluation

\- Score persistence



\## Phase 6 â€” Frontend



Build:



\- Authentication UI

\- Dashboard

\- Resume upload

\- Interview setup

\- Live interview UI

\- Feedback UI

\- Report UI



\## Phase 7 â€” Analytics



Build:



\- Performance dashboard

\- Interview history

\- Progress charts

\- Weak topic detection

\- Strong topic detection



\## Phase 8 â€” Job Matching



Build:



\- Job description input

\- Skill extraction

\- Resume â†” job comparison

\- Semantic similarity

\- Skill-gap analysis

\- Preparation recommendations



\## Phase 9 â€” Voice



Build:



\- Browser microphone

\- Audio handling

\- Speech-to-text

\- Transcript processing

\- Speaking metrics

\- Filler-word detection



\## Phase 10 â€” Advanced ML



Select meaningful components based on available data.



Possible options:



\- Question difficulty classifier

\- Candidate performance prediction

\- Candidate clustering

\- Recommendation system

\- Semantic answer analysis



Do not add an ML model simply for appearance.



\## Phase 11 â€” Production Readiness



Build:



\- Tests

\- Docker

\- Logging

\- Security hardening

\- Error handling

\- Performance improvements

\- Deployment configuration



\## Phase 12 â€” Portfolio



Complete:



\- README

\- Architecture diagrams

\- Screenshots

\- Demo

\- Resume bullets

\- LinkedIn description

\- Interview preparation

\- Technical explanation



\---



\# 50. Git/GitHub Strategy



Use Git from the beginning.



Suggested branch strategy:



```text

main

develop

feature/\*

```



Commit meaningful milestones.



Examples:



```text

feat: initialize FastAPI backend

feat: add PostgreSQL integration

feat: implement JWT authentication

feat: add resume upload

feat: implement resume parsing

feat: add interview session model

feat: add AI question generation

feat: implement answer evaluation

```



Do not commit:



\- `.env`

\- Secrets

\- API keys

\- Large generated files

\- Private resumes

\- User recordings



Maintain a useful `.gitignore`.



\---



\# 51. Environment Variables



Use `.env.example`.



Possible variables:



```text

APP\_ENV=

DATABASE\_URL=

JWT\_SECRET\_KEY=

JWT\_ALGORITHM=

ACCESS\_TOKEN\_EXPIRE\_MINUTES=



AI\_PROVIDER=

AI\_API\_KEY=

AI\_MODEL=



EMBEDDING\_PROVIDER=

EMBEDDING\_MODEL=



STORAGE\_PROVIDER=

STORAGE\_BUCKET=

```



Only include variables actually required by the chosen implementation.



\---



\# 52. Performance



Consider:



\- Async FastAPI endpoints

\- Database indexes

\- Pagination

\- Caching

\- Background tasks

\- Efficient file processing

\- Embedding caching

\- AI request minimization



Do not prematurely optimize.



Explain important performance decisions.



\---



\# 53. Non-Goals



The initial version should NOT attempt to:



\- Diagnose mental health

\- Reliably infer emotions

\- Guarantee interview success

\- Predict whether someone will get hired

\- Replace a human recruiter

\- Store unnecessary biometric data

\- Claim scientifically validated psychological measurements without evidence



The system provides interview preparation and feedback, not employment decisions.



\---



\# 54. Quality Standards



The final application should demonstrate:



\- Clean architecture

\- Meaningful AI/ML

\- Proper backend engineering

\- Secure authentication

\- Good database design

\- Professional UI

\- Testability

\- Deployment readiness

\- Good documentation

\- Explainable design decisions



The project should be something the developer can confidently demonstrate and explain during a technical interview.



\---



\# 55. Final Resume Deliverables



After the project is genuinely implemented, generate:



1\. Two-line resume description

2\. Three strong resume bullets

3\. 60-second project explanation

4\. Two-minute project explanation

5\. Detailed technical explanation

6\. Possible interviewer questions

7\. Strong answers

8\. GitHub README

9\. LinkedIn project description



Do not exaggerate features.



Only describe features that are actually implemented.



\---



\# 56. Source of Truth



This file is the primary project specification.



When implementing the project:



1\. Read `PROJECT\_SPEC.md`.

2\. Read `DEVELOPMENT\_PLAN.md` if available.

3\. Follow the current phase.

4\. Do not skip requirements silently.

5\. If a requirement conflicts with a technical constraint, explain the conflict before changing it.

6\. Prefer minimal justified changes.

7\. Keep documentation synchronized with implementation.



\---



\# 57. First Instruction to the AI Coding Assistant



Before writing application code:



\## Phase 0 â€” Architecture \& Development Plan



Provide:



1\. Final recommended tech stack with justification.

2\. System architecture.

3\. Backend architecture.

4\. Frontend architecture.

5\. Database ER/schema design.

6\. AI/ML architecture.

7\. API architecture.

8\. Folder structure.

9\. MVP vs advanced feature separation.

10\. Local development requirements.

11\. Environment setup.

12\. Git/GitHub strategy.

13\. Development phases.

14\. Risks and technical trade-offs.



Then stop and wait for explicit approval to begin Phase 1.



Do not generate the complete project at once.

