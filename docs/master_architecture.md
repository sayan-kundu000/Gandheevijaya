# Gandheevijaya — Master System Architecture & Design Handbook

This document establishes the authoritative system architecture, technical design, and implementation strategies for the **Gandheevijaya** multi-exam preparation and online assessment platform. It serves as the primary system blueprint and single source of truth for the entire development lifecycle.

---

## 1. System Architecture

Gandheevijaya is architected as a **Modular Monolith**. This ensures simplicity of code, low maintenance overhead, and ease of deployment for a solo developer, while keeping modules decoupled enough to facilitate a microservices split in the future if scale demands it.

### Architecture Block Diagram

```mermaid
graph TD
    %% Frontend Layer
    subgraph Frontend ["React Client App (Vercel)"]
        UI["UI View Components (Tailwind & shadcn/ui)"]
        Store["State Store (Zustand)"]
        Cache["Data Cache (TanStack Query)"]
        Router["Client Routing (React Router)"]
    end

    %% Backend Layer
    subgraph Backend ["FastAPI Core Backend (Render)"]
        API["REST Controllers (FastAPI Routes)"]
        Deps["Dependencies & Middleware (JWT, Auth, CORS)"]
        Service["Service Layer (Business Logic)"]
        Repo["Repository Layer (SQLAlchemy ORM)"]
        ETL["Ingestion Pipeline (JSON ETL)"]
    end

    %% Database Layer
    subgraph Database ["Data Store (PostgreSQL)"]
        DB[("PostgreSQL Database")]
    end

    %% Data flow
    UI --> Router
    UI --> Store
    UI --> Cache
    Cache -->|HTTP REST/JSON + Bearer Token| API
    API --> Deps
    Deps --> Service
    Service --> Repo
    Repo --> DB
    ETL -->|Bulk Insert / Transactions| DB
```

### Flow of Execution (Vertical Slice)
1. **Client Action**: The user starts a quiz attempt.
2. **API Call**: The frontend client sends a secure `POST` request to `/api/v1/attempts/` containing the `quiz_id`.
3. **Authentication/Authorization**: FastAPI dependency injection verifies the JWT access token, parses the user ID, and checks the user's role.
4. **Service Execution**: The Service Layer checks authorization, creates a new attempt record with backend-calculated timestamps (`started_at`, `expires_at`), updates the attempt state, and fetches the randomized quiz questions.
5. **Data Access (Repository)**: SQLAlchemy executes queries inside a transaction, writing the attempt to PostgreSQL.
6. **Response**: FastAPI serializes the database models into a structured Pydantic response (excluding correct answers/solutions) and sends it back to the client.

---

## 2. Technology Stack

The platform is built using the following stack:

| Layer | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Backend Core** | Python | 3.13+ | Primary language environment |
| **Web Framework** | FastAPI | 0.110.0+ | Asynchronous high-performance REST APIs |
| **Web Server** | Uvicorn | 0.28.0+ | ASGI web server for local and production runtimes |
| **Data Validation** | Pydantic | v2.6.0+ | Schema parsing, strict serialization, type safety |
| **ORM** | SQLAlchemy | 2.0.0+ | Relational data access, connection pooling, and modeling |
| **Database Migrations**| Alembic | 1.13.0+ | Database schema version control |
| **Database Driver** | psycopg | v3.1.18+ | High-performance asynchronous-capable PostgreSQL driver |
| **Password Hashing** | Argon2id (passlib) | 1.7.4+ | Cryptographically secure password storage |
| **Security / JWT** | PyJWT | 2.8.0+ | Cryptographic token signing and decoding |
| **Testing Backend** | Pytest + HTTPX | 8.0.0+ | Automation testing and API client mocks |
| **Frontend Core** | React / TypeScript | 18+ / 5+ | Static single page app with strict typing |
| **Build Tool** | Vite | 5+ | Development server and static bundling compiler |
| **Styling** | Tailwind CSS | 3.4+ | Utility-first component design |
| **UI Components** | shadcn/ui & Radix | Latest | Accessible, headless custom interface elements |
| **State / Caching** | Zustand & TanStack | Latest | Client state management and REST API response caching |
| **Client Forms** | React Hook Form + Zod | Latest | Form handling and validation matching Pydantic schemas |
| **Charts** | Recharts | Latest | Clean and performant data visualization |

---

## 3. Repository Architecture

The project directory structure is laid out as follows:

```text
Gandheevijaya/
│
├── backend/                        # FastAPI Backend Module
│   ├── app/
│   │   ├── api/                    # REST API Controllers (FastAPI Routers)
│   │   │   ├── auth.py             # User Authentication Routes
│   │   │   ├── exams.py            # Exams, Subjects, Topics Explorer API
│   │   │   ├── quizzes.py          # Quiz Management APIs
│   │   │   ├── attempts.py         # Quiz Attempt, Timer, & Submission Engine
│   │   │   ├── analytics.py        # Performance Analytics & Stats
│   │   │   ├── admin.py            # Admin Ingestion & Management
│   │   │   ├── deps.py             # FastAPI Dependencies (get_db, current_user)
│   │   │   └── router.py           # Primary Router Aggregation
│   │   │
│   │   ├── core/                   # System Configurations
│   │   │   ├── config.py           # Pydantic Settings Configurations
│   │   │   ├── database.py         # DB Engine, SessionLocal, Base Model
│   │   │   └── security.py         # Hashing & Token JWT Utilities
│   │   │
│   │   ├── models/                 # SQLAlchemy DB Models
│   │   │   ├── __init__.py         # Module Exports
│   │   │   ├── user.py             # Users
│   │   │   ├── content.py          # Exam, Subject, Topic, Subtopic, Question
│   │   │   ├── quiz.py             # Quiz & QuizQuestion Association
│   │   │   ├── attempt.py          # Attempt & AttemptAnswer
│   │   │   ├── performance.py      # Subject/Topic Performance & Snapshots
│   │   │   └── material.py         # Study Materials
│   │   │
│   │   ├── schemas/                # Pydantic Serializers / Validators
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   ├── quiz.py
│   │   │   ├── attempt.py
│   │   │   └── analytics.py
│   │   │
│   │   └── main.py                 # FastAPI ASGI Application Entry Point
│   │
│   ├── migrations/                 # Alembic Migrations
│   ├── alembic.ini                 # Migration Configuration
│   ├── requirements.txt            # Python Dependencies List
│   └── tests/                      # Pytest Suite
│
├── frontend/                       # React / TypeScript Frontend Client
│   ├── public/                     # Static Assets
│   ├── src/
│   │   ├── assets/                 # SVGs, Fonts, Images
│   │   ├── components/             # Reusable UI Elements (Buttons, Inputs)
│   │   ├── features/               # Module-wise Layouts and Pages
│   │   │   ├── auth/               # Login, Registration
│   │   │   ├── dashboard/          # Student Dashboard
│   │   │   ├── exams/              # Exam & Topic Browsers
│   │   │   ├── quiz/               # Test Interface, Countdown Timer
│   │   │   └── admin/              # Ingestion Dashboard, Manage Quizzes
│   │   ├── hooks/                  # Custom React Hooks
│   │   ├── lib/                    # Library Configs (Axios Client, TanStack)
│   │   ├── routes/                 # Routing Structure (React Router)
│   │   ├── store/                  # Zustand Global Store
│   │   ├── App.tsx                 # Core App Container
│   │   └── main.tsx                # Client Entry Point
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── datasets/                       # Question Ingestion JSON Dataset Folder
│   ├── cprog/                      # C Programming Data (quesj, ansj, solnj)
│   ├── dsa/                        # DSA Data (quesj, ansj, solnj)
│   └── ssc_banking/                # SSC and Banking Data
│
├── docs/                           # Documentation and Architecture Specs
│   ├── master_architecture.md
│   ├── database_schema.md
│   ├── api_contract.md
│   └── roadmap_and_development.md
│
└── README.md                       # Setup & Configuration Guide
```

---

## 4. Authentication & Authorization

Authentication is based on short-lived JWT access tokens and secure refresh tokens. Role-Based Access Control (RBAC) ensures strict separation between student and admin capabilities.

### Flow Diagram

```text
[Credentials] ---> [FastAPI /auth/login]
                          │
         (Verifies Argon2id Hash from PostgreSQL)
                          │
                          ▼
            [Returns tokens in Response]
            ├── access_token (Expires in 15 mins)
            └── refresh_token (Expires in 7 days, Secure HttpOnly Cookie)
```

### Security Configurations
* **Password Hashing**: Argon2id via `passlib` with default salt parameters.
* **Token Storage**: Access tokens are kept in frontend memory (or temporary state); refresh tokens are set via `HttpOnly`, `Secure`, `SameSite=Lax` cookies to prevent XSS and CSRF.
* **RBAC Roles**: 
  - `STUDENT`: Can access attempts, performance metrics, and dashboards.
  - `ADMIN`: Full read/write access, database migrations, JSON imports.
* **Backend Enforcement**: Checked via FastAPI dependencies:
  ```python
  def get_current_active_admin(current_user: User = Depends(get_current_user)):
      if current_user.role != "ADMIN":
          raise HTTPException(status_code=403, detail="Not enough privileges")
      return current_user
  ```

---

## 5. JSON ETL Architecture

The ETL (Extract, Transform, Load) pipeline imports questions from existing JSON files distributed across directories. It guarantees data integrity and maintains idempotency.

### Processing Pipeline

```text
JSON Files Directory (quesj, ansj, solnj)
                │
                ▼
  [Parser (Read files matching by name)]
                │
                ▼
  [Validator (Verify required fields and data types)]
                │
                ▼
  [Duplicate Detector (Check existing ID and Text hash)]
                │
                ▼
  [Taxonomy Mapper (Link to database Exam/Subject/Topic)]
                │
                ▼
  [Database Transaction (Atomicity: rollback on failure)]
                │
                ▼
  [Import Report (Audit logs of processed/skipped/errors)]
```

### Parsing Rules
* **Inputs**: The parser reads question files (`*q.json`), answer files (`*a.json`), and solution files (`*s.json`) matching their IDs.
* **Validation**: Checks for:
  - Valid question text, nonempty options lists (for MCQs/MSQs), correctness of solutions.
  - Valid JSON formatting.
  - Uniqueness of `id` (e.g., `GCS27-PDS-E-MCQ-100`).
* **Idempotency**: Runs database `UPSERT` queries. If a question ID already exists, its fields are updated rather than creating a duplicate entry.
* **Reporting**: Ingestion outputs a JSON report outlining the counts of processed files, successes, warnings, and malformed files skipped.

---

## 6. Multi-Exam Content Architecture

Gandheevijaya structures content hierarchically, separating exam categories from specific exam configurations. This allows the system to easily support GATE, SSC, Banking, and other curricula without modifying the core database.

```text
Exam Category (e.g., "Engineering", "Government", "Finance")
  └── Exam (e.g., "GATE CS", "SSC CGL", "SBI PO")
        └── Subject (e.g., "C Programming", "Quantitative Aptitude")
              └── Topic (e.g., "Pointers", "Ratio & Proportion")
                    └── Subtopic (e.g., "Pointer Arithmetic", "Partnership")
                          ├── Study Material (Markdown, PDF Links)
                          └── Quiz (Title, Duration, Marks)
                                └── QuizQuestions (Association)
                                      └── Question (Text, Options, Correct Answer, Explanation)
```

* **Exams**: Support unique marking schemes (e.g., negative marking in GATE, variable scoring).
* **Topics & Subtopics**: Ensure modular taxonomy. All analytics reports roll up through this tree.

---

## 7. Quiz Lifecycle & Engine

The Quiz Engine manages the execution of quizzes. The state of quiz execution is completely controlled and validated on the backend.

### Attempt State Machine

```mermaid
stateDiagram-v2
    [*] --> STARTED : User clicks "Start Quiz"
    STARTED --> SUBMITTED : User submits before timer expires
    STARTED --> EXPIRED : Server detects current time > expires_at
    SUBMITTED --> [*] : Results generated
    EXPIRED --> [*] : Auto-submitted / score finalized
```

### Engine Protocols
1. **Initiate Quiz (`POST /api/v1/attempts/`)**:
   - Backend checks if the user has an active, incomplete attempt.
   - Calculates `started_at = datetime.utcnow()` and `expires_at = started_at + duration_minutes`.
   - Records state as `STARTED`. Returns questions *without* correct answers or explanations.
2. **Answer Checkpoint (`PATCH /api/v1/attempts/{id}/answers`)**:
   - Allows students to save intermediate answers. Saves selected options to database.
3. **Submit Quiz (`POST /api/v1/attempts/{id}/submit`)**:
   - Enforces backend validation: Checks if `utcnow() <= expires_at + grace_period`.
   - Compares answers against correct answers.
   - Evaluates marks obtained, negative marking configurations, and updates status to `SUBMITTED`.
   - Returns final score, accuracy, and detailed solutions.
4. **Auto-Submit (Cron/On-demand)**:
   - When retrieving an attempt or loading the dashboard, if `utcnow() > expires_at` and state is still `STARTED`, the engine automatically submits the quiz, calculating scores up to the point of expiry.

---

## 8. Data Science Layer

The Data Science layer provides students with actionable analytics based on attempt history and accuracy profiles. It focuses on identifying weaknesses and recommending study materials.

### Metrics Definitions
* **Accuracy**: $\frac{\text{Correct Answers}}{\text{Total Questions Attempted}} \times 100$
* **Attempt Rate**: $\frac{\text{Questions Attempted}}{\text{Total Questions In Quiz}} \times 100$
* **Weakness Index (WI)**: Calculated per topic:
  $$WI = 1.0 - \left( \frac{\text{Correct Attempts}}{\text{Total Attempts}} \times \text{Difficulty Weight} \right)$$
  Where `Difficulty Weight` is: Easy = 0.5, Medium = 1.0, Hard = 1.5. Higher indices highlight target areas for revision.
* **Practice Recommendations**: Heuristic-based algorithm:
  1. Identify top 3 subjects/topics with accuracy below 60%.
  2. Query database for unattempted questions matching those topics.
  3. Fetch related `study_materials` (Markdown/PDF guides) for recommendation cards.

---

## 9. Frontend Architecture

The frontend is a single-page application focused on high performance and clean UI design.

### Structural Concepts
* **State Management**:
  - `Zustand`: Lightweight store for global authentication state, active attempts, and client theme (Dark/Light modes).
* **Caching**:
  - `TanStack Query`: Manages cache lifetime for exam catalogs, quiz descriptions, and leaderboard statistics to minimize database load.
* **Styling**:
  - CSS variables mapped to design tokens (HSL tailored colors).
  - UI is clean, accessibility-compliant (WCAG AA), and optimized for tablets and desktop browsers.
* **Routing**:
  - `React Router` containing protected routes. Unauthorized requests redirect to `/login`. Admins are routed to `/admin`.

---

## 10. Testing Strategy

High coverage testing ensures stability when importing data or changing score rules.

### Test Domains
1. **Authentication API**: Verification of registration, correct token payload issuance, and secure cookie storage.
2. **JSON Import Parser**: Integration tests validation parsing of correct formatting and rejecting malformed/corrupted files.
3. **Quiz Engine & Scoring**:
   - Simulating correct, incorrect, and unanswered queries.
   - Verifying negative marking scoring.
   - Simulating late submissions to verify server-side rejection.
4. **Data Science Aggregations**: Mocking attempt histories and verifying that the weakness indices match calculations.

---

## 11. Security Strategy

* **Input Validation**: Strict schema enforcement using Pydantic (Backend) and Zod (Frontend) to eliminate malformed payloads.
* **SQL Injection**: Parameterized SQL queries via SQLAlchemy 2.0 ORM. Direct raw queries are prohibited.
* **Rate Limiting**: Implementation of middleware to block brute force authentication attempts.
* **CORS Policies**: Strict whitelist validation using domain configuration parameters.

---

## 12. Deployment Architecture

```text
   Developer Push ---> GitHub Repository
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   Vercel Deployment                 Render Deployment
   [React SPA Frontend]             [FastAPI Backend Web Service]
            │                                 │
     (Static Assets)                  (PostgreSQL Driver)
            │                                 │
            ▼                                 ▼
   User Browsers <--------------------> PostgreSQL Instance (Neon / Render)
```

* **Frontend**: Handled automatically by Vercel from root `/frontend`.
* **Backend**: Deployed to Render as a Python Web Service. Runs database migrations automatically on deployment (`alembic upgrade head`).
* **Database**: High-availability Managed PostgreSQL.

---

## 13. Environment Variable Specification

A `.env` file must be created locally (and configured in production) containing:

### Backend `.env`
```env
# System Configuration
PROJECT_NAME=GANDHEEVIJAYA
API_V1_STR=/api/v1

# Security
JWT_SECRET=production_secret_key_make_it_extremely_long_and_random_12345!
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database Connection
# Local: sqlite:///./gandheevijaya.db
# Production: postgresql://user:password@host:port/dbname?sslmode=require
DATABASE_URL=sqlite:///./gandheevijaya.db

# CORS Allowed Origins (Comma-separated or JSON string)
ALLOWED_CORS_ORIGINS=["http://localhost:5173","https://gandheevijaya.vercel.app"]
```

### Frontend `.env`
```env
# API URL Endpoint
VITE_API_URL=http://localhost:8000/api/v1
```
