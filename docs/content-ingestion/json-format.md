# Source JSON Format Specification

## Dataset Triples Structure

Source datasets live in `datasets/{subject_code}/{difficulty}/` containing three parallel folders:

- `quesj/` (`*q.json`): Question details
- `ansj/` (`*a.json`): Correct answer mapping
- `solnj/` (`*s.json`): Explanation/solution mapping

### 1. Question Record (`quesj/*.json`)
```json
[
  {
    "id": "GCS27-PDS-E-MCQ-100",
    "subject": "PDS",
    "topic": "Pointers",
    "subtopic": null,
    "difficulty": "easy",
    "type": "MCQ",
    "question": "What is the output of the following C code snippet?\n```c\n#include <stdio.h>\nint main() {\n    int x = 3;\n    int *p = &x;\n    *p = *p + 5;\n    printf(\"%d\", x);\n    return 0;\n}\n```",
    "options": ["8", "3", "0", "Error"],
    "answer_id": "GCS27-PDS-E-MCQ-100",
    "reasoning_type": ["pointer dereference"]
  }
]
```

### 2. Answer Record (`ansj/*.json`)
```json
[
  {
    "id": "GCS27-PDS-E-MCQ-100",
    "correct_answer": "A"
  }
]
```

### 3. Solution Record (`solnj/*.json`)
```json
[
  {
    "id": "GCS27-PDS-E-MCQ-100",
    "explanation": "Pointer `p` points to `x`. Dereferencing `*p` modifies `x` directly from 3 to 8."
  }
]
```
