import argparse
import sys
import time
from pathlib import Path

# Ensure workspace root is in sys.path
workspace_root = Path(__file__).resolve().parent.parent.parent
if str(workspace_root) not in sys.path:
    sys.path.insert(0, str(workspace_root))

from backend.app.core.database import SessionLocal
from backend.app.services.taxonomy_service import TaxonomyService


def main():
    parser = argparse.ArgumentParser(
        description="Gandheevijaya Taxonomy & Content Health Inspection CLI"
    )
    args = parser.parse_args()

    print("=" * 60)
    print(" GANDHEEVIJAYA TAXONOMY & CONTENT HEALTH REPORT")
    print("=" * 60)

    db = SessionLocal()
    try:
        t0 = time.time()
        service = TaxonomyService(db)
        report = service.get_content_health_report()
        elapsed = time.time() - t0

        print(f" Generated At     : {report.generated_at.isoformat()}")
        print(f" Total Exams      : {report.total_exams}")
        print(f" Total Subjects   : {report.total_subjects}")
        print(f" Total Topics     : {report.total_topics}")
        print(f" Total Questions  : {report.total_questions}")
        print(f" Total Materials  : {report.total_materials}")
        print(f" Issues Flagged   : {report.issue_count}")
        print(f" Execution Time   : {elapsed:.2f} seconds")
        print("=" * 60)

        if report.issues:
            print("\n---------------- CONTENT HEALTH ISSUES ----------------")
            for idx, issue in enumerate(report.issues[:20], start=1):
                print(f" [{idx}] [{issue.severity}] Entity: {issue.entity_id} | Type: {issue.type}")
                print(f"     Details: {issue.details}")
            if len(report.issues) > 20:
                print(f" ... and {len(report.issues) - 20} more issues.")
            print("-----------------------------------------------------")
        else:
            print("\n[SUCCESS] 0 taxonomy integrity or content health issues found!")

    finally:
        db.close()


if __name__ == "__main__":
    main()
