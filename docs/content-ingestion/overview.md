# Question Bank ETL & Ingestion Subsystem Overview

The Gandheevijaya Question Bank ETL subsystem discovers, parses, validates, normalizes, deduplicates, and ingests question datasets from JSON files into PostgreSQL.

## Architecture Pipeline

```
                 Source JSON Datasets (datasets/)
                               │
                               ▼
               Multi-File Discovery (discovery.py)
            Pairs quesj/*q.json, ansj/*a.json, solnj/*s.json
                               │
                               ▼
              Normalization (normalizer.py)
            SHA-256 Content Fingerprint Generation
                               │
                               ▼
               Validation Engine (validator.py)
            C code integrity, answer consistency
                               │
                               ▼
             Subject & Topic Reference Resolution
                               │
                               ▼
               Deduplication & Audit Reporting
            Skipping existing fingerprints in DB
                               │
                               ▼
              Transactional Database Persistence
            (or Dry-Run Preview Reporting)
```

## CLI Usage

```bash
# Preview import (Dry Run)
python backend/scripts/import_questions.py --directory datasets --dry-run

# Execute Live Import
python backend/scripts/import_questions.py --directory datasets
```
