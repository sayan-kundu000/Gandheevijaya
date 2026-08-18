import argparse
import sys
import time
from pathlib import Path

# Ensure workspace root is in sys.path
workspace_root = Path(__file__).resolve().parent.parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from backend.app.core.database import SessionLocal
from backend.app.etl.importer import QuestionImportService


def main():
    parser = argparse.ArgumentParser(
        description="Gandheevijaya Question Bank JSON ETL & Import Subsystem CLI"
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default="datasets",
        help="Directory path containing JSON question datasets (Default: 'datasets')",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        default=None,
        help="Specific single JSON file path to import",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run validation, reference resolution, and deduplication without modifying database",
    )
    parser.add_argument(
        "--subject",
        type=str,
        default=None,
        help="Default subject code or name override (e.g., 'CPROG', 'ALGO')",
    )
    parser.add_argument(
        "--upsert",
        action="store_true",
        help="Update existing question records if modified duplicate match found",
    )

    args = parser.parse_args()

    target_path = args.file if args.file else args.directory
    print("=" * 60)
    print(" GANDHEEVIJAYA CONTENT INGESTION PIPELINE")
    print("=" * 60)
    print(f" Source Path : {target_path}")
    print(f" Import Mode : {'DRY RUN (Preview)' if args.dry_run else 'LIVE TRANSACTIONAL IMPORT'}")
    print(f" Subject Tag : {args.subject or 'Auto-Detect'}")
    print(f" Upsert Mode : {'Enabled' if args.upsert else 'Disabled'}")
    print("=" * 60)

    db = SessionLocal()
    try:
        t0 = time.time()
        service = QuestionImportService(db)
        report = service.run_import(
            source_path=target_path,
            is_dry_run=args.dry_run,
            upsert_mode=args.upsert,
            default_subject_code=args.subject,
        )
        elapsed = time.time() - t0

        print("\n" + "=" * 60)
        print(" IMPORT REPORT SUMMARY")
        print("=" * 60)
        print(f" Files Processed    : {report.files_processed or 1}")
        print(f" Records Discovered : {report.records_seen}")
        print(f" Valid Records      : {report.valid_records}")
        print(f" Invalid Records    : {report.invalid_records}")
        print(f" Duplicates Detected: {report.duplicates_detected}")
        print(f" Records Inserted   : {report.inserted}")
        print(f" Records Skipped    : {report.skipped}")
        print(f" Records Failed     : {report.failed}")
        print(f" Errors Encountered : {len(report.errors)}")
        print(f" Execution Time     : {elapsed:.2f} seconds")
        print("=" * 60)

        if report.errors:
            print("\n---------------- ERROR DETAILS (Top 10) ----------------")
            for idx, err in enumerate(report.errors[:10], start=1):
                print(f" [{idx}] [{err.severity}] File: {err.file} | Record: {err.record_id or 'N/A'}")
                print(f"     Field: {err.field} | Message: {err.error_message}")
            if len(report.errors) > 10:
                print(f" ... and {len(report.errors) - 10} more error messages.")
            print("-------------------------------------------------------")

    finally:
        db.close()


if __name__ == "__main__":
    main()
