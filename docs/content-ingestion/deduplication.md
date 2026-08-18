# Deduplication & SHA-256 Fingerprinting Strategy

## Deterministic Content Fingerprinting

To prevent duplicate question insertion across repeated import runs or overlapping JSON datasets, Gandheevijaya generates a deterministic SHA-256 fingerprint from normalized content fields:

```python
fingerprint = SHA256(
    normalized_question_text
    + "|" + str(normalized_options)
    + "|" + normalized_difficulty
    + "|" + normalized_type
    + "|" + normalized_subject
)
```

## Deduplication Flow
1. The ingestion pipeline queries existing `Question.id` and `Question.source_fingerprint` values from PostgreSQL.
2. If an incoming question record's `id` or `source_fingerprint` already exists:
   - **Default Mode (`--upsert` false)**: The record is skipped and counted under `records_skipped`.
   - **Upsert Mode (`--upsert` true)**: The existing database question record is updated with latest content.
3. Repeated import runs are 100% idempotent (0 duplicates inserted).
