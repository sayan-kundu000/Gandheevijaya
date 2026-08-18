# Taxonomy & Content Management Engine Overview

The Content Management Engine serves as the single source of truth for academic content hierarchy across GATE, SSC, and Banking examination ecosystems.

## Content Taxonomy Hierarchy

```
                      EXAM (GATE_CS, SSC_CGL, BANK_PO)
                        │
                        ▼
                      SUBJECT (CPROG, ALGO, QA, LR)
                        │
                        ▼
                      TOPIC (Pointers, Trees, Percentages)
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
       SUBTOPIC                   QUESTION / MATERIAL
```

## Core Features
1. **Multi-Exam Taxonomy**: Reusable entities (`Exam` -> `Subject` -> `Topic` -> `Question`) without hardcoded exam logic.
2. **Lifecycle State Machines**: Controlled transitions for Exams/Subjects/Topics (`DRAFT`, `ACTIVE`, `INACTIVE`, `ARCHIVED`) and Questions/Materials (`DRAFT`, `REVIEW`, `PUBLISHED`, `UNPUBLISHED`, `ARCHIVED`).
3. **Centralized Student Visibility Policy**: Content is visible to non-admin students **only if** `Exam.status == ACTIVE` AND `Subject.status == ACTIVE` AND `Topic.status == ACTIVE` AND `Question.status == PUBLISHED`.
4. **Tree Taxonomy Browsing**: `GET /api/v1/exams/{id}/taxonomy` returns hierarchical taxonomy tree in a single query.
5. **Content Health & Integrity Audit**: `GET /api/v1/admin/content/health` scans for orphan questions or inactive parent taxonomy.
