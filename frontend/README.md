# Gandheevijaya — Frontend Architecture & UI/UX Foundation

Gandheevijaya is a high-performance examination preparation and assessment platform for **GATE CS**, **SSC**, and **Banking Examinations**.

This frontend is built with **React**, **TypeScript**, **Vite**, **TanStack Query**, **React Router**, **React Hook Form**, **Zod**, and **Tailwind CSS**.

---

## 🚀 Key Features & Architecture

- **Data-Driven Taxonomy**: Examination streams (GATE CS, SSC, Banking) are loaded dynamically from REST APIs (`/api/v1/exams`, `/api/v1/subjects`, `/api/v1/topics`).
- **Feature-Oriented Architecture**: Modular structure dividing components into domain features (`exams`, `subjects`, `topics`, `quizzes`, `attempts`, `results`, `dashboard`, `analytics`, `admin`).
- **Resilient API Layer**: Centralized Axios client (`apiClient.ts`) with automatic JWT access/refresh token rotation, error mapping (`errorMapper.ts`), and global error boundaries.
- **Adaptive Quiz Engine**: High-performance quiz player supporting question palette navigation, keyboard shortcuts (`1`-`4`, `N`, `P`, `M`), response autosaving, timer countdown, submission confirmation, and solution explanations.
- **Performance Intelligence**: Dashboard & Analytics powered by Recharts visualizing accuracy trends, speed vs accuracy quadrants, topic weak areas, and prescriptive recommendations.
- **Role-Aware Security**: Student and Admin navigation guards based on JWT roles (`STUDENT`, `ADMIN`).

---

## 🛠️ Technology Stack

| Role | Technology |
|---|---|
| Framework & Language | React 18 + TypeScript 5 |
| Build Tool | Vite 5 |
| Router | React Router DOM 6 |
| Server State & Caching | TanStack React Query 5 |
| Form Validation | React Hook Form 7 + Zod |
| Styling & UI Tokens | Tailwind CSS 3 |
| Icons | Lucide React |
| Data Visualization | Recharts |
| Unit Testing | Vitest + React Testing Library |

---

## 📋 Environment Configuration

Create a `.env` file in the `frontend` root directory based on `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

For production deployment on Vercel, set `VITE_API_BASE_URL` to your live FastAPI backend domain (e.g. Render backend URL).

---

## 💻 Local Development Setup

```bash
# 1. Install dependencies
npm install

# 2. Start Vite development server
npm run dev

# 3. Run unit tests
npm test

# 4. Build production bundle
npm run build

# 5. Preview production build
npm run preview
```

---

## 🚢 Deployment

### Vercel (Frontend)
- Build Command: `npm run build`
- Output Directory: `dist`
- Framework Preset: `Vite`
- SPA Fallback: Managed via `vercel.json` rewrites to prevent 404 on direct route navigation.

---

## 🔒 Security & Guidelines

- Client-side checks act as UX guidance only. Backend REST APIs remain the ultimate source of truth for authorization and scoring.
- Passwords and secrets are never logged or stored in local state.
