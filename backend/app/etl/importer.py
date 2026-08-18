from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.etl.discovery import ContentDiscoverer
from backend.app.etl.normalizer import ContentNormalizer
from backend.app.etl.schemas import ContentImportReport, ImportErrorItem, NormalizedQuestionRecord
from backend.app.etl.validator import ContentValidator
from backend.app.models.content import Question, Subject, Topic
from backend.app.models.import_audit import ContentImport, ContentImportError


class QuestionImportService:
    """
    Production Content Ingestion Service.
    Coordinates discovery, normalization, structural validation, reference resolution,
    SHA-256 deduplication, and transactional database persistence.
    """

    def __init__(self, db: Session):
        self.db = db

    def run_import(
        self,
        source_path: str,
        is_dry_run: bool = False,
        strict_mode: bool = True,
        auto_create_topics: bool = True,
        upsert_mode: bool = False,
        default_subject_code: Optional[str] = None,
    ) -> ContentImportReport:
        started_at = datetime.now(timezone.utc)
        report = ContentImportReport(
            source_path=source_path,
            started_at=started_at,
            is_dry_run=is_dry_run,
        )

        # 1. Discover and load JSON file triples / combined files
        raw_items_with_file, discovery_errors = ContentDiscoverer.discover_and_load(source_path)
        report.errors.extend(discovery_errors)
        report.records_seen = len(raw_items_with_file)

        if report.records_seen == 0:
            report.completed_at = datetime.now(timezone.utc)
            return report

        # 2. Normalize and Validate Records
        normalized_records: List[NormalizedQuestionRecord] = []
        for raw_rec, source_file in raw_items_with_file:
            norm_rec = ContentNormalizer.normalize(raw_rec, source_file=source_file)
            is_valid, rec_errors = ContentValidator.validate_record(norm_rec)
            report.errors.extend(rec_errors)

            if is_valid:
                report.valid_records += 1
                normalized_records.append(norm_rec)
            else:
                report.invalid_records += 1

        # 3. Subject & Topic Resolution Mapping
        subject_map = self._get_subject_map()
        topic_map = self._get_topic_map()
        existing_fingerprints = self._get_existing_fingerprints()
        existing_ids = self._get_existing_question_ids()

        seen_batch_fingerprints: Set[str] = set()
        records_to_insert: List[Tuple[NormalizedQuestionRecord, int, Optional[int]]] = []

        for norm_rec in normalized_records:
            # Resolve Subject ID
            subj_key = (norm_rec.subject_code_or_name or default_subject_code or "CPROG").upper()
            target_subject_id = subject_map.get(subj_key) or subject_map.get(subj_key.replace(" ", "_"))

            if not target_subject_id:
                # Attempt fallback resolution
                if "PDS" in subj_key or "C" in subj_key:
                    target_subject_id = subject_map.get("CPROG") or subject_map.get("ALGO")
                elif "QA" in subj_key or "QUANT" in subj_key:
                    target_subject_id = subject_map.get("QA")
                elif "LR" in subj_key or "REASONING" in subj_key:
                    target_subject_id = subject_map.get("LR")

            if not target_subject_id:
                # Use first available subject in DB or fail resolution
                if subject_map:
                    target_subject_id = next(iter(subject_map.values()))
                else:
                    report.errors.append(
                        ImportErrorItem(
                            file=norm_rec.source_file or source_path,
                            record_id=norm_rec.id,
                            field="subject",
                            error_message=f"Could not resolve subject '{norm_rec.subject_code_or_name}' against database.",
                        )
                    )
                    report.failed += 1
                    continue

            # Resolve Topic ID
            target_topic_id = None
            if norm_rec.topic_name:
                top_key = (target_subject_id, norm_rec.topic_name.strip().lower())
                target_topic_id = topic_map.get(top_key)

                if not target_topic_id and auto_create_topics and not is_dry_run:
                    # Auto-create topic under subject
                    new_topic = Topic(subject_id=target_subject_id, name=norm_rec.topic_name.strip())
                    self.db.add(new_topic)
                    self.db.flush()
                    target_topic_id = new_topic.id
                    topic_map[top_key] = target_topic_id
            
            if not target_topic_id:
                # Assign default first topic under subject
                first_topic = self.db.scalar(select(Topic.id).where(Topic.subject_id == target_subject_id))
                if first_topic:
                    target_topic_id = first_topic
                else:
                    if auto_create_topics and not is_dry_run:
                        new_topic = Topic(subject_id=target_subject_id, name=norm_rec.topic_name or "General")
                        self.db.add(new_topic)
                        self.db.flush()
                        target_topic_id = new_topic.id

            # Deduplication Check (by ID or Fingerprint)
            is_dup = (
                norm_rec.id in existing_ids
                or norm_rec.source_fingerprint in existing_fingerprints
                or norm_rec.source_fingerprint in seen_batch_fingerprints
            )

            if is_dup:
                report.duplicates_detected += 1
                if not upsert_mode:
                    report.skipped += 1
                    continue

            seen_batch_fingerprints.add(norm_rec.source_fingerprint)
            records_to_insert.append((norm_rec, target_subject_id, target_topic_id))

        # 4. Database Persistence or Dry Run
        if not is_dry_run:
            try:
                for norm_rec, target_subj_id, target_top_id in records_to_insert:
                    if target_top_id is None:
                        continue

                    # Check if updating existing record
                    existing_q = self.db.get(Question, norm_rec.id)
                    if existing_q:
                        existing_q.question_text = norm_rec.question_text
                        existing_q.options = norm_rec.options
                        existing_q.correct_answer = norm_rec.correct_answer
                        existing_q.explanation = norm_rec.explanation
                        existing_q.difficulty = norm_rec.difficulty
                        existing_q.type = norm_rec.type
                        existing_q.tags = norm_rec.tags
                        existing_q.source_fingerprint = norm_rec.source_fingerprint
                        report.inserted += 1
                    else:
                        q_obj = Question(
                            id=norm_rec.id,
                            topic_id=target_top_id,
                            difficulty=norm_rec.difficulty,
                            type=norm_rec.type,
                            question_text=norm_rec.question_text,
                            options=norm_rec.options,
                            correct_answer=norm_rec.correct_answer,
                            explanation=norm_rec.explanation,
                            tags=norm_rec.tags,
                            source_fingerprint=norm_rec.source_fingerprint,
                        )
                        self.db.add(q_obj)
                        report.inserted += 1

                # Create ContentImport Audit record
                audit_batch = ContentImport(
                    filename=source_path,
                    content_type="QUESTIONS",
                    started_at=started_at,
                    completed_at=datetime.now(timezone.utc),
                    status="SUCCESS" if len(report.errors) == 0 else "COMPLETED_WITH_ERRORS",
                    records_found=report.records_seen,
                    records_imported=report.inserted,
                    records_updated=0,
                    records_skipped=report.skipped,
                    records_failed=report.invalid_records + report.failed,
                    error_count=len(report.errors),
                )
                self.db.add(audit_batch)
                self.db.flush()

                # Add Audit Errors
                for err in report.errors:
                    audit_err = ContentImportError(
                        import_id=audit_batch.id,
                        record_identifier=err.record_id,
                        error_type=err.field.upper(),
                        error_message=err.error_message,
                        raw_reference=err.file,
                    )
                    self.db.add(audit_err)

                self.db.commit()
            except Exception as exc:
                self.db.rollback()
                report.failed = len(records_to_insert)
                report.errors.append(
                    ImportErrorItem(
                        file=source_path,
                        field="transaction",
                        error_message=f"Database transaction failed and was rolled back: {exc}",
                    )
                )
        else:
            # Dry run report calculation
            report.inserted = len(records_to_insert)

        report.completed_at = datetime.now(timezone.utc)
        return report

    def _get_subject_map(self) -> Dict[str, int]:
        stmt = select(Subject)
        subjects = list(self.db.scalars(stmt).all())
        mapping: Dict[str, int] = {}
        for s in subjects:
            mapping[s.code.upper()] = s.id
            mapping[s.name.upper()] = s.id
        return mapping

    def _get_topic_map(self) -> Dict[Tuple[int, str], int]:
        stmt = select(Topic)
        topics = list(self.db.scalars(stmt).all())
        return {(t.subject_id, t.name.strip().lower()): t.id for t in topics}

    def _get_existing_fingerprints(self) -> Set[str]:
        stmt = select(Question.source_fingerprint).where(Question.source_fingerprint.is_not(None))
        fps = self.db.scalars(stmt).all()
        return {fp for fp in fps if fp}

    def _get_existing_question_ids(self) -> Set[str]:
        stmt = select(Question.id)
        return set(self.db.scalars(stmt).all())
