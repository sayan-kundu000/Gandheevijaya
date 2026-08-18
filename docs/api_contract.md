# Gandheevijaya — API Contract Specification

This document defines the REST API contract for the **Gandheevijaya** assessment platform. All endpoints consume and return JSON payloads. Authentication uses bearer tokens in the HTTP `Authorization` header: `Authorization: Bearer <token>`.

---

## 1. Authentication (`/api/v1/auth`)

### 1.1 User Registration
* **Endpoint**: `POST /api/v1/auth/register`
* **Access**: Public
* **Request Body**:
  ```json
  {
    "email": "student@gandheevijaya.com",
    "password": "SecurePassword123",
    "full_name": "Arjuna Student"
  }
  ```
* **Response (201 Created)**:
  ```json
  {
    "id": "e0b96898-0c67-4a00-9993-4a1d7f6d2da5",
    "email": "student@gandheevijaya.com",
    "full_name": "Arjuna Student",
    "role": "STUDENT",
    "created_at": "2026-08-12T17:00:00Z"
  }
  ```

### 1.2 User Login
* **Endpoint**: `POST /api/v1/auth/login`
* **Access**: Public
* **Request Body (OAuth2 Form URL Encoded compatibility or JSON)**:
  ```json
  {
    "username": "student@gandheevijaya.com",
    "password": "SecurePassword123"
  }
  ```
* **Response (200 OK)**:
  * Sets an `HttpOnly`, `Secure`, `SameSite=Lax` cookie named `refresh_token` containing the long-lived token.
  * Returns access token in payload:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": "e0b96898-0c67-4a00-9993-4a1d7f6d2da5",
      "email": "student@gandheevijaya.com",
      "full_name": "Arjuna Student",
      "role": "STUDENT"
    }
  }
  ```

### 1.3 Refresh Access Token
* **Endpoint**: `POST /api/v1/auth/refresh`
* **Access**: Public (requires the `refresh_token` cookie)
* **Response (200 OK)**:
  ```json
  {
    "access_token": "new_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
  ```

### 1.4 Get Current User Details
* **Endpoint**: `GET /api/v1/auth/me`
* **Access**: Authenticated (Student or Admin)
* **Response (200 OK)**:
  ```json
  {
    "id": "e0b96898-0c67-4a00-9993-4a1d7f6d2da5",
    "email": "student@gandheevijaya.com",
    "full_name": "Arjuna Student",
    "role": "STUDENT"
  }
  ```

---

## 2. Multi-Exam Content Explorer (`/api/v1`)

### 2.1 List All Exam Categories & Exams
* **Endpoint**: `GET /api/v1/exams`
* **Access**: Authenticated
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Engineering Entrance",
      "slug": "engineering",
      "exams": [
        {
          "id": 1,
          "name": "GATE CS",
          "code": "GATE_CS",
          "description": "Graduate Aptitude Test in Engineering - Computer Science"
        }
      ]
    },
    {
      "id": 2,
      "name": "Government Exams",
      "slug": "government-exams",
      "exams": [
        {
          "id": 2,
          "name": "SSC CGL",
          "code": "SSC_CGL",
          "description": "Staff Selection Commission Combined Graduate Level"
        }
      ]
    }
  ]
  ```

### 2.2 Browse Subjects inside an Exam
* **Endpoint**: `GET /api/v1/exams/{exam_code}/subjects`
* **Access**: Authenticated
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "C Programming",
      "code": "CPROG",
      "exam_id": 1
    },
    {
      "id": 2,
      "name": "Data Structures & Algorithms",
      "code": "DSA",
      "exam_id": 1
    }
  ]
  ```

### 2.3 Retrieve Topics & Subtopics for a Subject
* **Endpoint**: `GET /api/v1/subjects/{subject_code}/topics`
* **Access**: Authenticated
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "name": "Pointers",
      "subject_id": 1,
      "subtopics": [
        {
          "id": 1,
          "name": "Pointer Arithmetic",
          "topic_id": 1
        },
        {
          "id": 2,
          "name": "Double Pointers",
          "topic_id": 1
        }
      ]
    }
  ]
  ```

### 2.4 Get Study Material details for a Subject/Topic
* **Endpoint**: `GET /api/v1/materials`
* **Access**: Authenticated
* **Query Params**: `subject_id` (Required), `topic_id` (Optional)
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 10,
      "subject_id": 1,
      "topic_id": 1,
      "subtopic_id": null,
      "title": "Mastering Pointer Declarations in C",
      "content": "# Pointer Mechanics\nEvery variable has an address...",
      "media_urls": ["https://assets.gandheevijaya.com/docs/pointers_ref.pdf"],
      "created_at": "2026-08-12T10:00:00Z"
    }
  ]
  ```

---

## 3. Quiz Management & Ingestion (`/api/v1/quizzes`)

### 3.1 List Quizzes under a Subject
* **Endpoint**: `GET /api/v1/quizzes`
* **Access**: Authenticated
* **Query Params**: `subject_id` (Required), `is_published` (Optional, defaults to true for students)
* **Response (200 OK)**:
  ```json
  [
    {
      "id": 5,
      "subject_id": 1,
      "title": "C Programming Pointer & Array Mechanics",
      "description": "Test covering pointer allocations and multi-dimensional matrices",
      "duration_minutes": 45,
      "total_marks": 20.0,
      "passing_score": 10.0,
      "is_published": true,
      "created_at": "2026-08-12T12:00:00Z"
    }
  ]
  ```

### 3.2 Get Details of a Quiz (For Discovery Screen)
* **Endpoint**: `GET /api/v1/quizzes/{id}`
* **Access**: Authenticated
* **Response (200 OK)**:
  ```json
  {
    "id": 5,
    "subject_id": 1,
    "title": "C Programming Pointer & Array Mechanics",
    "description": "Test covering pointer allocations and multi-dimensional matrices",
    "duration_minutes": 45,
    "total_marks": 20.0,
    "passing_score": 10.0,
    "total_questions": 15
  }
  ```

---

## 4. Quiz Attempt Engine (`/api/v1/attempts`)

### 4.1 Start a Quiz Attempt
* **Endpoint**: `POST /api/v1/attempts`
* **Access**: Authenticated (Student)
* **Request Body**:
  ```json
  {
    "quiz_id": 5
  }
  ```
* **Response (201 Created)**:
  * Returns questions *without* the `correct_answer` or `explanation` fields.
  ```json
  {
    "attempt_id": "4a7372cf-be9d-4760-b6f1-a1bf18ad836f",
    "quiz_id": 5,
    "status": "STARTED",
    "started_at": "2026-08-12T17:01:00Z",
    "expires_at": "2026-08-12T17:46:00Z",
    "questions": [
      {
        "id": "GCS27-PDS-E-MCQ-100",
        "type": "MCQ",
        "question_text": "What is the output of the following C code snippet?\n...",
        "options": ["8", "3", "0", "Error"],
        "marks": 1.0,
        "negative_marks": 0.33
      }
    ]
  }
  ```

### 4.2 Save Intermediate Answers (Checkpoint)
* **Endpoint**: `PATCH /api/v1/attempts/{id}/answers`
* **Access**: Authenticated (Student)
* **Request Body**:
  ```json
  {
    "answers": [
      {
        "question_id": "GCS27-PDS-E-MCQ-100",
        "selected_answer": "A"
      }
    ]
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "status": "saved",
    "saved_count": 1
  }
  ```

### 4.3 Submit Attempt for Scoring
* **Endpoint**: `POST /api/v1/attempts/{id}/submit`
* **Access**: Authenticated (Student)
* **Response (200 OK)**:
  * Evaluates choices on the server and returns final results.
  ```json
  {
    "attempt_id": "4a7372cf-be9d-4760-b6f1-a1bf18ad836f",
    "status": "SUBMITTED",
    "started_at": "2026-08-12T17:01:00Z",
    "completed_at": "2026-08-12T17:25:00Z",
    "score": 15.67,
    "passed": true,
    "passing_score": 10.0,
    "total_marks": 20.0,
    "answers": [
      {
        "question_id": "GCS27-PDS-E-MCQ-100",
        "selected_answer": "A",
        "correct_answer": "A",
        "is_correct": true,
        "marks_awarded": 1.0,
        "explanation": "Pointer `p` points to `x`..."
      }
    ]
  }
  ```

---

## 5. Analytics & Leaderboard (`/api/v1`)

### 5.1 Student Dashboard Analytics
* **Endpoint**: `GET /api/v1/analytics/dashboard`
* **Access**: Authenticated (Student)
* **Response (200 OK)**:
  ```json
  {
    "overall_accuracy": 78.5,
    "quizzes_taken": 12,
    "study_time_hours": 18.2,
    "performance_trend": [
      { "date": "2026-08-01", "score": 65 },
      { "date": "2026-08-05", "score": 72 },
      { "date": "2026-08-12", "score": 85 }
    ],
    "weakest_topics": [
      { "topic_name": "Pointers", "accuracy": 45.0, "total_attempts": 20 },
      { "topic_name": "Recursion", "accuracy": 55.2, "total_attempts": 10 }
    ],
    "recommendations": [
      {
        "type": "revision",
        "topic": "Pointers",
        "material_title": "Mastering Pointer Declarations in C",
        "material_id": 10
      }
    ]
  }
  ```

### 5.2 Leaderboard Statistics
* **Endpoint**: `GET /api/v1/leaderboard`
* **Access**: Authenticated
* **Query Params**: `subject_id` (Optional)
* **Response (200 OK)**:
  ```json
  [
    { "rank": 1, "username": "DronaCoder", "score": 98.5 },
    { "rank": 2, "username": "Bhishma99", "score": 95.0 },
    { "rank": 3, "username": "ArjunaStudent", "score": 92.5 }
  ]
  ```

---

## 6. Admin Endpoints (`/api/v1/admin`)

### 6.1 JSON Ingestion Parser Trigger
* **Endpoint**: `POST /api/v1/admin/import`
* **Access**: Admin (Restricted)
* **Query Params**: `exam_code` (e.g. GATE_CS), `subject_code` (e.g. CPROG)
* **Request Body**:
  ```json
  {
    "dataset_directory": "datasets/cprog/ej"
  }
  ```
* **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "report": {
      "files_processed": 3,
      "records_found": 9,
      "successfully_imported": 9,
      "updated": 0,
      "skipped": 0,
      "duplicates": 0,
      "invalid_records": 0,
      "errors": []
    }
  }
  ```

### 6.2 Create/Update/Delete Quiz
* **Endpoint**: `POST /api/v1/admin/quizzes`
* **Access**: Admin
* **Request Body**:
  ```json
  {
    "subject_id": 1,
    "title": "C Programming Variables and Structures",
    "description": "Elementary C programming test",
    "duration_minutes": 30,
    "total_marks": 10.0,
    "passing_score": 5.0,
    "is_published": true,
    "questions": [
      {
        "question_id": "GCS27-PDS-E-MCQ-100",
        "sort_order": 1,
        "marks": 2.0,
        "negative_marks": 0.66
      }
    ]
  }
  ```
* **Response (201 Created)**:
  ```json
  {
    "id": 6,
    "subject_id": 1,
    "title": "C Programming Variables and Structures",
    "total_questions": 1
  }
  ```
