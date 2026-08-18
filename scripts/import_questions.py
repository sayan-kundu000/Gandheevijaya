import os
import sys
import json
import argparse
from datetime import datetime
from sqlalchemy.orm import Session

# Adjust Python path to resolve imports from workspace root
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_root not in sys.path:
    sys.path.append(workspace_root)

from backend.app.core.database import SessionLocal
from backend.app.models.content import ExamCategory, Exam, Subject, Topic, Subtopic, Question
from backend.app.models.import_audit import ContentImport, ContentImportError

# Folder to Exam mapping configuration
TAXONOMY_MAP = {
    # GATE subjects
    "pds": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "C Programming"},
    "cprog": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "C Programming"},
    "dsa": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Data Structures & Algorithms"},
    "algo": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Algorithms"},
    "digitallogic": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Digital Logic"},
    "dbms": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Database Management Systems"},
    "os": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Operating Systems"},
    "toc": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Theory of Computation"},
    "cn": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Computer Networks"},
    "coa": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Computer Organization & Architecture"},
    "cd": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Compiler Design"},
    "dm": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Discrete Mathematics"},
    "la": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Linear Algebra"},
    "calc": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Calculus"},
    "probstat": {"exam_code": "GATE_CS", "exam_name": "GATE CS", "cat_slug": "gate", "cat_name": "GATE", "sub_name": "Probability & Statistics"},
    
    # SSC subjects
    "qa": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Quantitative Aptitude"},
    "lr": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Logical Reasoning"},
    "va": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Verbal Ability"},
    "gk": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "General Knowledge"},
    "ih": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Indian History"},
    "wg": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "World Geography"},
    "indp": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Indian Polity"},
    "inde": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Indian Economy"},
    "aphy": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Applied Physics"},
    "achem": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Applied Chemistry"},
    "abio": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Applied Biology"},
    "acurra": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Current Affairs"},
    "blit": {"exam_code": "SSC_CGL", "exam_name": "SSC CGL", "cat_slug": "ssc", "cat_name": "SSC", "sub_name": "Basic Literature"},
    
    # Banking subjects
    "ba": {"exam_code": "SBI_PO", "exam_name": "SBI PO", "cat_slug": "banking", "cat_name": "BANKING", "sub_name": "Banking Awareness"},
}

def get_taxonomy_by_path(path: str) -> dict:
    """Guesses taxonomy mapping from folder path names."""
    normalized_path = path.replace("\\", "/").lower()
    for key, mapping in TAXONOMY_MAP.items():
        if f"/{key}/" in normalized_path or normalized_path.endswith(f"/{key}"):
            return mapping
    # Fallback to GATE CS default
    return {
        "exam_code": "GATE_CS",
        "exam_name": "GATE CS",
        "cat_slug": "gate",
        "cat_name": "GATE",
        "sub_name": "General Subject"
    }

def get_or_create_taxonomy(db: Session, mapping: dict, subject_json_code: str) -> tuple:
    """Retrieves or inserts required category, exam, subject in DB."""
    # 1. Exam Category
    category = db.query(ExamCategory).filter(ExamCategory.slug == mapping["cat_slug"]).first()
    if not category:
        category = ExamCategory(name=mapping["cat_name"], slug=mapping["cat_slug"])
        db.add(category)
        db.flush()

    # 2. Exam
    exam = db.query(Exam).filter(Exam.code == mapping["exam_code"]).first()
    if not exam:
        exam = Exam(category_id=category.id, name=mapping["exam_name"], code=mapping["exam_code"])
        db.add(exam)
        db.flush()

    # 3. Subject (use JSON's code as Subject code to ensure consistency)
    subject_code = subject_json_code.upper()
    subject = db.query(Subject).filter(Subject.code == subject_code).first()
    if not subject:
        subject = Subject(exam_id=exam.id, name=mapping["sub_name"], code=subject_code)
        db.add(subject)
        db.flush()

    return subject

def validate_question_data(q: dict, ans: dict, soln: dict) -> list:
    """Performs validation checks. Returns list of error messages (empty if valid)."""
    errors = []
    
    # Check key existences
    required_q_fields = ["id", "subject", "topic", "difficulty", "type", "question"]
    for field in required_q_fields:
        if not q.get(field):
            errors.append(f"Missing question field: '{field}'")
            
    if not ans or not ans.get("correct_answer"):
        errors.append("Missing answer field: 'correct_answer'")
        
    if not soln or not soln.get("explanation"):
        errors.append("Missing solution field: 'explanation'")

    if errors:
        return errors  # Exit early if critical IDs/fields are missing

    # Validate type and options mapping
    q_type = q["type"].upper()
    if q_type not in ["MCQ", "MSQ", "NAT"]:
        errors.append(f"Invalid question type: '{q_type}'. Must be MCQ, MSQ, or NAT")
        
    difficulty = q["difficulty"].lower()
    if difficulty not in ["easy", "medium", "hard"]:
        errors.append(f"Invalid difficulty: '{difficulty}'. Must be easy, medium, or hard")

    options = q.get("options")
    if q_type in ["MCQ", "MSQ"]:
        if not isinstance(options, list) or len(options) == 0:
            errors.append(f"Options must be a non-empty list for type '{q_type}'")
    elif q_type == "NAT":
        if options is not None:
            if not isinstance(options, list):
                errors.append("Options must be a list or null for NAT type questions")
            elif len(options) > 0:
                errors.append("Options must be empty or null for NAT type questions")

    # Validate answer formatting
    correct_ans = str(ans.get("correct_answer")).strip()
    if q_type == "MCQ":
        if correct_ans not in ["A", "B", "C", "D"]:
            errors.append(f"Correct answer '{correct_ans}' must be 'A', 'B', 'C', or 'D' for MCQ")
    elif q_type == "MSQ":
        try:
            parsed_ans = json.loads(correct_ans)
            if not isinstance(parsed_ans, list) or len(parsed_ans) == 0:
                errors.append(f"Correct answer for MSQ must be a JSON array of letters, got '{correct_ans}'")
            else:
                for letter in parsed_ans:
                    if letter not in ["A", "B", "C", "D"]:
                        errors.append(f"MSQ answer contains invalid letter: '{letter}'")
        except json.JSONDecodeError:
            # Check if it is a comma separated string or single letter
            errors.append(f"MSQ correct answer '{correct_ans}' must be a JSON-encoded string list")
            
    return errors

def import_single_file(db: Session, q_file: str, args, audit_run: ContentImport) -> dict:
    """Parses and ingests a matched trio of question, answer, and solution files."""
    report = {"imported": 0, "updated": 0, "skipped": 0, "failed": 0}
    
    # Calculate matching answer and solution file paths
    base_dir = os.path.dirname(os.path.dirname(q_file))
    filename = os.path.basename(q_file)
    base_name = filename[:-7] # Remove suffix 'eq.json', 'mq.json', or 'hq.json' (length 7)
    suffix = filename[-7:] # e.g. 'eq.json', 'mq.json', 'hq.json'
    
    ans_suffix = suffix[0] + "a.json" # e.g. 'ea.json', 'ma.json', 'ha.json'
    sol_suffix = suffix[0] + "s.json" # e.g. 'es.json', 'ms.json', 'hs.json'
    
    ans_file = os.path.join(base_dir, "ansj", base_name + ans_suffix)
    sol_file = os.path.join(base_dir, "solnj", base_name + sol_suffix)

    if not os.path.exists(ans_file):
        error_msg = f"Missing matching answer file at: {ans_file}"
        print(error_msg)
        log_import_error(db, audit_run.id, base_name, "FILE_NOT_FOUND", error_msg)
        report["failed"] += 1
        return report
        
    if not os.path.exists(sol_file):
        error_msg = f"Missing matching solution file at: {sol_file}"
        print(error_msg)
        log_import_error(db, audit_run.id, base_name, "FILE_NOT_FOUND", error_msg)
        report["failed"] += 1
        return report

    try:
        with open(q_file, 'r', encoding='utf-8') as f:
            q_data_list = json.load(f)
        with open(ans_file, 'r', encoding='utf-8') as f:
            ans_data_list = json.load(f)
        with open(sol_file, 'r', encoding='utf-8') as f:
            sol_data_list = json.load(f)
    except Exception as e:
        print(f"JSON Decode Error for {base_name}: {e}")
        log_import_error(db, audit_run.id, base_name, "JSON_DECODE_ERROR", str(e))
        report["failed"] += 1
        return report

    # Make dictionaries to lookup answers and solutions by question ID
    ans_dict = {item["id"]: item for item in ans_data_list if "id" in item}
    sol_dict = {item["id"]: item for item in sol_data_list if "id" in item}

    taxonomy_mapping = get_taxonomy_by_path(q_file)

    for q_item in q_data_list:
        q_id = q_item.get("id")
        if not q_id:
            log_import_error(db, audit_run.id, "UNKNOWN", "VALIDATION_ERROR", "Question is missing 'id' key")
            report["failed"] += 1
            continue

        ans_item = ans_dict.get(q_id)
        sol_item = sol_dict.get(q_id)

        # 1. Validation Only
        validation_errors = validate_question_data(q_item, ans_item, sol_item)
        if validation_errors:
            error_msg = "; ".join(validation_errors)
            print(f"Validation failed for {q_id}: {error_msg}")
            log_import_error(db, audit_run.id, q_id, "VALIDATION_ERROR", error_msg, raw=json.dumps(q_item))
            report["failed"] += 1
            continue

        if args.validate_only:
            report["imported"] += 1
            continue

        # 2. Check Deduplication
        existing_q = db.query(Question).filter(
            (Question.id == q_id) | (Question.question_text == q_item["question"])
        ).first()
        if existing_q:
            if args.update:
                # Resolve subject/topic/subtopic mappings
                subject = get_or_create_taxonomy(db, taxonomy_mapping, q_item["subject"])
                topic = get_or_create_topic(db, subject.id, q_item["topic"])
                subtopic = get_or_create_subtopic(db, topic.id, q_item.get("subtopic"))
                
                # Perform update
                existing_q.topic_id = topic.id
                existing_q.subtopic_id = subtopic.id if subtopic else None
                existing_q.difficulty = q_item["difficulty"].lower()
                existing_q.type = q_item["type"].upper()
                existing_q.question_text = q_item["question"]
                existing_q.options = q_item.get("options")
                existing_q.correct_answer = str(ans_item["correct_answer"]).strip()
                existing_q.explanation = sol_item["explanation"]
                existing_q.tags = q_item.get("reasoning_type", []) + q_item.get("representation", [])
                
                report["updated"] += 1
            else:
                report["skipped"] += 1
            continue

        # 3. Create new record
        subject = get_or_create_taxonomy(db, taxonomy_mapping, q_item["subject"])
        topic = get_or_create_topic(db, subject.id, q_item["topic"])
        subtopic = get_or_create_subtopic(db, topic.id, q_item.get("subtopic"))

        new_q = Question(
            id=q_id,
            topic_id=topic.id,
            subtopic_id=subtopic.id if subtopic else None,
            difficulty=q_item["difficulty"].lower(),
            type=q_item["type"].upper(),
            question_text=q_item["question"],
            options=q_item.get("options"),
            correct_answer=str(ans_item["correct_answer"]).strip(),
            explanation=sol_item["explanation"],
            tags=q_item.get("reasoning_type", []) + q_item.get("representation", [])
        )
        db.add(new_q)
        report["imported"] += 1

    return report

def get_or_create_topic(db: Session, subject_id: int, name: str) -> Topic:
    topic = db.query(Topic).filter(Topic.subject_id == subject_id, Topic.name == name).first()
    if not topic:
        topic = Topic(subject_id=subject_id, name=name)
        db.add(topic)
        db.flush()
    return topic

def get_or_create_subtopic(db: Session, topic_id: int, name: str) -> Subtopic:
    if not name:
        return None
    subtopic = db.query(Subtopic).filter(Subtopic.topic_id == topic_id, Subtopic.name == name).first()
    if not subtopic:
        subtopic = Subtopic(topic_id=topic_id, name=name)
        db.add(subtopic)
        db.flush()
    return subtopic

def log_import_error(db: Session, import_id: int, identifier: str, err_type: str, msg: str, raw: str = None):
    err = ContentImportError(
        import_id=import_id,
        record_identifier=identifier,
        error_type=err_type,
        error_message=msg,
        raw_reference=raw
    )
    db.add(err)

def main():
    parser = argparse.ArgumentParser(description="Gandheevijaya JSON Dataset Ingestion Importer")
    parser.add_argument("--file", type=str, help="Ingest a specific question file ending in *q.json")
    parser.add_argument("--dir", type=str, help="Walk a directory and ingest all matching question files recursively")
    parser.add_argument("--dry-run", action="store_true", help="Perform full parsing and mock insertions but roll back transaction")
    parser.add_argument("--validate-only", action="store_true", help="Validate schema formatting without accessing the database")
    parser.add_argument("--update", action="store_true", help="Overwrite question fields if its unique ID already exists")
    
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    db = SessionLocal()

    # Create content import audit entry
    source_name = args.file if args.file else args.dir
    audit_run = ContentImport(
        filename=os.path.basename(source_name),
        content_type="BATCH" if args.dir else "FILE",
        status="PENDING"
    )
    
    if not args.validate_only:
        db.add(audit_run)
        db.commit()
        db.refresh(audit_run)

    # Walk directory or resolve file target
    question_files = []
    if args.file:
        if args.file.endswith("q.json"):
            question_files.append(os.path.abspath(args.file))
        else:
            print("Error: Targeted question file must end in 'q.json' (e.g. 'cprog01eq.json').")
            sys.exit(1)
    elif args.dir:
        for root, dirs, files in os.walk(args.dir):
            if "quesj" in root:
                for file in files:
                    if file.endswith("q.json"):
                        question_files.append(os.path.join(root, file))

    if not question_files:
        print(f"No valid question files (ending in 'q.json' inside 'quesj' folders) found for source: {source_name}")
        sys.exit(0)

    total_discovered = 0
    total_imported = 0
    total_updated = 0
    total_skipped = 0
    total_failed = 0

    print(f"Discovered {len(question_files)} question file(s) for ingestion.")
    
    try:
        for q_file in question_files:
            total_discovered += 1
            file_report = import_single_file(db, q_file, args, audit_run)
            total_imported += file_report["imported"]
            total_updated += file_report["updated"]
            total_skipped += file_report["skipped"]
            total_failed += file_report["failed"]
            
        if not args.validate_only:
            # Retrieve error count
            error_count = db.query(ContentImportError).filter(ContentImportError.import_id == audit_run.id).count()
            audit_run.completed_at = datetime.utcnow()
            audit_run.records_found = total_discovered
            audit_run.records_imported = total_imported
            audit_run.records_updated = total_updated
            audit_run.records_skipped = total_skipped
            audit_run.records_failed = total_failed
            audit_run.error_count = error_count
            
            if args.dry_run:
                db.rollback()
                audit_run.status = "DRY_RUN"
                print("\n[DRY RUN ACTIVE] Ingestion completed. All database alterations rolled back.")
            else:
                db.commit()
                audit_run.status = "SUCCESS" if total_failed == 0 else "PARTIAL_SUCCESS"
                print("\nIngestion completed successfully. Database updated.")
    except Exception as e:
        print(f"\nCritical Ingestion Failure: {e}")
        if not args.validate_only:
            db.rollback()
            audit_run.completed_at = datetime.utcnow()
            audit_run.status = "FAILED"
            log_import_error(db, audit_run.id, "CRITICAL", "SYSTEM_ERROR", str(e))
            db.commit()
        sys.exit(1)
    finally:
        db.close()

    # Ingestion Validation Report Output
    print("=====================================")
    print(" GANDHEEVIJAYA CONTENT IMPORT REPORT")
    print("=====================================")
    print(f"Source:             {source_name}")
    print(f"Files discovered:   {total_discovered}")
    print(f"Questions imported: {total_imported}")
    print(f"Questions updated:  {total_updated}")
    print(f"Questions skipped:  {total_skipped}")
    print(f"Questions failed:   {total_failed}")
    print(f"Status:             {audit_run.status if not args.validate_only else 'VALIDATED'}")
    print("=====================================")

if __name__ == "__main__":
    main()
