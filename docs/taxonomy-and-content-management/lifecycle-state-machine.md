# Content Lifecycle State Machines

## 1. Taxonomy Entity Lifecycle (Exams, Subjects, Topics)

```
        ┌──────────┐
        │  DRAFT   │
        └────┬─────┘
             │
             ▼
        ┌──────────┐ ◄──────┐
        │  ACTIVE  │        │
        └────┬─────┘        │
             │              │
             ▼              │
        ┌──────────┐        │
        │ INACTIVE ├────────┘
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ ARCHIVED │
        └──────────┘
```

## 2. Content Entity Lifecycle (Questions, Study Materials)

```
        ┌──────────┐
        │  DRAFT   │
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │  REVIEW  │
        └────┬─────┘
             │
             ▼
        ┌──────────┐ ◄──────┐
        │PUBLISHED │        │
        └────┬─────┘        │
             │              │
             ▼              │
        ┌──────────┐        │
        │UNPUBLISHED├───────┘
        └────┬─────┘
             │
             ▼
        ┌──────────┐
        │ ARCHIVED │
        └──────────┘
```

## Admin Lifecycle Endpoints
- `POST /api/v1/admin/questions/{id}/publish`
- `POST /api/v1/admin/questions/{id}/unpublish`
- `POST /api/v1/admin/questions/{id}/archive`
- `POST /api/v1/admin/questions/bulk-status`
