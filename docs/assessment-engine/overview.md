# Gandheevijaya Assessment Engine Overview

The Assessment Engine in Gandheevijaya manages the complete lifecycle of examination quizzes, student attempts, response validation, server-authoritative scoring, and performance analytics.

## Key Design Principles

1. **Server-Authoritative Evaluation**:
   The backend is the single source of truth for correct answers, marks, negative penalties, scores, percentages, and accuracy. Client-supplied scores are ignored.

2. **Stable Question & Option Snapshots**:
   When an attempt starts (`POST /api/v1/quizzes/{id}/start`), assigned question IDs and sequences are snapshot into `Attempt.question_order` (JSON). Mid-quiz database edits or question bank mutations cannot alter an active attempt.

3. **Answer Leakage Prevention**:
   Student-facing question payloads during an active attempt contain only question text, options, question numbers, and marks possible. Answer keys (`correct_answer`) and explanations are stripped until post-submission review.

4. **Multi-Exam Taxonomy & Quiz Types**:
   Supports GATE CS, SSC, and Banking exams with flexible quiz types: `PRACTICE`, `TOPIC_TEST`, `SUBJECT_TEST`, `MOCK_TEST`, and `EXAM_SIMULATION`.

5. **Server-Side Timer & Expiry Enforcement**:
   Expiration timestamps (`expires_at`) are calculated server-side. Attempts past expiry reject new responses and auto-finalize saved answers.
