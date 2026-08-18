# Quizzes & Attempt Flow API Specification

## 1. Flow Sequence Diagram

```
Student                        FastAPI API Server                  PostgreSQL DB
   |                                   |                                 |
   |--- POST /quizzes/{id}/start ----->|                                 |
   |                                   |--- Create Attempt (STARTED) --->|
   |                                   |<-- Return Attempt + Questions --|
   |<-- Return Attempt & Questions ----|                                 |
   |   (no correct answers exposed!)   |                                 |
   |                                   |                                 |
   | [Student completes quiz offline]  |                                 |
   |                                   |                                 |
   |--- POST /attempts/{id}/submit --->|                                 |
   |    (answers payload)              |--- Transactional Evaluation --->|
   |                                   |    - Check correct answers      |
   |                                   |    - Calculate score & marks    |
   |                                   |    - Mark status = SUBMITTED    |
   |                                   |    - Update performance metrics |
   |<-- Return Final Result & Review --|<--------------------------------|
```

## 2. API Endpoints

### Start Quiz
`POST /api/v1/quizzes/{quiz_id}/start` (Requires `STUDENT` role)
Response:
```json
{
  "attempt": {
    "id": "att-uuid-1234",
    "user_id": "usr-uuid-5678",
    "quiz_id": 1,
    "started_at": "2026-08-14T15:00:00Z",
    "expires_at": "2026-08-14T15:30:00Z",
    "score": 0.0,
    "passed": false,
    "status": "STARTED"
  },
  "questions": [
    {
      "id": "GCS27-ALGO-E-MCQ-001",
      "difficulty": "easy",
      "type": "MCQ",
      "question_text": "What is the time complexity of binary search?",
      "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"]
    }
  ]
}
```

### Submit Attempt
`POST /api/v1/attempts/{attempt_id}/submit` (Requires `STUDENT` role)
Request:
```json
{
  "answers": [
    {
      "question_id": "GCS27-ALGO-E-MCQ-001",
      "selected_answer": "O(log n)"
    }
  ]
}
```

Response: Returns `ResultResponse` containing total score, percentage, passed status, and detailed explanations.
