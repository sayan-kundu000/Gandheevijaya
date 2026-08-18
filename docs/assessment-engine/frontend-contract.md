# Frontend Integration Contract for Assessment Engine

## Key REST Endpoints

### 1. List Available Quizzes
```http
GET /api/v1/quizzes?exam_id=1&subject_id=2&quiz_type=TOPIC_TEST&page=1&page_size=20
```

### 2. Start / Create Quiz Attempt
```http
POST /api/v1/quizzes/{quiz_id}/start
Authorization: Bearer <student_token>
```
**Response**: `AttemptStartResponse` containing `attempt` metadata and `questions` list (with answer keys stripped).

### 3. Save Single Response
```http
POST /api/v1/attempts/{attempt_id}/responses
Authorization: Bearer <student_token>

{
  "question_id": "q_123",
  "selected_answer": "opt_a"
}
```

### 4. Resume Active Attempt
```http
GET /api/v1/attempts/{attempt_id}
Authorization: Bearer <student_token>
```
**Response**: `AttemptResumeResponse` returning `attempt`, `questions`, `answers_map`, `review_map`, and `remaining_seconds`.

### 5. Final Submit Quiz
```http
POST /api/v1/attempts/{attempt_id}/submit
Authorization: Bearer <student_token>

{
  "answers": [
    {"question_id": "q_123", "selected_answer": "opt_a"}
  ]
}
```
**Response**: `ResultResponse` with complete score breakdown, percentage, accuracy, and detailed question review.

### 6. View Finalized Result & Review
```http
GET /api/v1/attempts/{attempt_id}/result
GET /api/v1/attempts/{attempt_id}/review
```
