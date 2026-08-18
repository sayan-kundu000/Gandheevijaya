import argparse
import sys
import os
import json
import csv
from datetime import datetime

# Adjust Python path to resolve imports properly from workspace root
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if workspace_root not in sys.path:
    sys.path.append(workspace_root)

from database.db_manager import DBManager
from rag.rag_manager import RAGManager
from generation.generator import QuestionGenerator
from validation.validator import QuestionValidator

def init_env(db_path="gate_questions.db"):
    db_manager = DBManager(db_path=db_path)
    rag_manager = RAGManager(db_manager=db_manager)
    
    # Preload configurations
    rag_manager.preload_syllabus()
    rag_manager.preload_patterns()
    
    return db_manager, rag_manager

def run_pilot(db_manager, rag_manager, limit=9):
    """Generates a balanced sample pilot batch of questions for C programming."""
    print("\n=== RUNNING PILOT GENERATION BATCH ===")
    generator = QuestionGenerator(db_manager=db_manager)
    validator = QuestionValidator(db_manager=db_manager)
    
    # We want a balanced matrix: Easy/Medium/Hard x MCQ/MSQ/NAT
    difficulties = ["easy", "medium", "hard"]
    types = ["mcq", "msq", "nat"]
    
    generated_count = 0
    passed_count = 0
    rejected_count = 0
    
    # Locate all C Programming patterns
    c_patterns = rag_manager.retrieve_patterns(subject="PDS")
    if not c_patterns:
        # Fallback if specific filtering by concept is empty
        c_patterns = [rag_manager.db_manager.get_random_pattern_for_subject("PDS")]
        
    print(f"Starting pilot generation. Target: {limit} balanced questions.")
    
    # Loop over difficulty and type matrix
    for diff in difficulties:
        for q_type in types:
            if passed_count >= limit:
                break
                
            print(f"\nGenerating: {diff.upper()} - {q_type.upper()}")
            
            # Select pattern randomly from PDS (Programming and Data Structures)
            pattern = rag_manager.db_manager.get_random_pattern_for_subject("PDS")
            if not pattern:
                print("Error: No abstract patterns found in DB. Run --init-db first.")
                return
                
            concept = pattern["concept"]
            
            # Generate Question
            draft_q = generator.generate_question(
                subject="PDS",
                concept=concept,
                difficulty=diff,
                q_type=q_type,
                pattern=pattern
            )
            generated_count += 1
            
            # Validate Question
            is_valid, reason, score = validator.validate(draft_q)
            draft_q["quality_score"] = score
            
            if is_valid:
                draft_q["validation_status"] = "VALIDATED"
                db_manager.store_question(draft_q)
                passed_count += 1
                print(f"-> SUCCESS: Generated {draft_q['id']} (Quality Score: {score:.1f}/100)")
            else:
                draft_q["validation_status"] = "REJECTED"
                db_manager.store_question(draft_q) # Store in DB as draft/rejected for logs
                db_manager.log_rejection(
                    question_id=draft_q["id"],
                    subject="PDS",
                    difficulty=diff,
                    q_type=q_type,
                    reason=reason.split(":")[0],
                    feedback_comment=reason
                )
                rejected_count += 1
                print(f"-> REJECTED: {reason}")
                
                # Retry generation once for pilot stability
                print("Retrying generation with a different pattern...")
                alt_pattern = rag_manager.db_manager.get_random_pattern_for_subject("PDS")
                retry_q = generator.generate_question(
                    subject="PDS",
                    concept=alt_pattern["concept"],
                    difficulty=diff,
                    q_type=q_type,
                    pattern=alt_pattern
                )
                is_valid, reason, score = validator.validate(retry_q)
                retry_q["quality_score"] = score
                if is_valid:
                    retry_q["validation_status"] = "VALIDATED"
                    db_manager.store_question(retry_q)
                    passed_count += 1
                    print(f"-> SUCCESS (RETRY): Generated {retry_q['id']} (Quality Score: {score:.1f}/100)")
                else:
                    print(f"-> RETRY FAILED: {reason}")

    print("\n=== PILOT GENERATION AUDIT REPORT ===")
    print(f"Total Attempted: {generated_count}")
    print(f"Total Validated & Stored: {passed_count}")
    print(f"Total Rejected: {rejected_count}")
    print("=====================================")

def display_status(db_manager):
    """Displays the ledger counts and metrics."""
    ledger = db_manager.get_ledger()
    print("\n==============================================")
    print("      GATE CS 2027 LEDGER STATUS REPORT")
    print("==============================================")
    print("Difficulty |  MCQ  |  MSQ  |  NAT  |  Total")
    print("-----------|-------|-------|-------|-------")
    for diff in ["easy", "medium", "hard"]:
        mcq = ledger[diff]["mcq"]
        msq = ledger[diff]["msq"]
        nat = ledger[diff]["nat"]
        tot = mcq + msq + nat
        print(f"{diff.capitalize():10} | {mcq:5} | {msq:5} | {nat:5} | {tot:5}")
    print("-----------|-------|-------|-------|-------")
    total_mcq = sum(ledger[d]["mcq"] for d in ledger)
    total_msq = sum(ledger[d]["msq"] for d in ledger)
    total_nat = sum(ledger[d]["nat"] for d in ledger)
    grand_total = total_mcq + total_msq + total_nat
    print(f"{'Total':10} | {total_mcq:5} | {total_msq:5} | {total_nat:5} | {grand_total:5}")
    print(f"TARGET     |  1875 |  1875 |  1875 |  5625")
    print("==============================================")
    
    # Print rejection stats
    conn = db_manager._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT reason, COUNT(*) as c FROM rejection_logs GROUP BY reason")
    rejections = cursor.fetchall()
    cursor.execute("SELECT AVG(quality_score) FROM questions WHERE validation_status = 'VALIDATED'")
    avg_quality = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(originality_score) FROM questions WHERE validation_status = 'VALIDATED'")
    avg_originality = cursor.fetchone()[0]
    conn.close()
    
    print("\n--- Quality Control Metrics ---")
    print(f"Average Quality Score (Validated): {avg_quality:.2f}/100" if avg_quality else "Average Quality Score: N/A")
    print(f"Average Originality Score (Validated): {avg_originality * 100:.1f}%" if avg_originality else "Average Originality: N/A")
    
    if rejections:
        print("\n--- Rejection Log Summary ---")
        for r in rejections:
            print(f"- {r['reason']}: {r['c']} times")
    else:
        print("\nRejection Logs: Empty (no rejections logged).")
    print("==============================================")

def export_data(db_manager, export_dir="datasets"):
    """Exports dataset to json, csv, and pdf files."""
    os.makedirs(export_dir, exist_ok=True)
    os.makedirs(os.path.join(export_dir, "final"), exist_ok=True)
    
    questions = db_manager.get_questions(status="VALIDATED")
    if not questions:
        # Fallback to drafts if no validated questions exist yet, to show system execution
        questions = db_manager.get_questions(status="DRAFT")
        if not questions:
            print("No questions in DB to export.")
            return

    # 1. Export questions.json
    with open(os.path.join(export_dir, "questions.json"), 'w') as f:
        json.dump(questions, f, indent=2)
        
    # 2. Export answers.json
    answers = [{"id": q["id"], "correct_answer": q["correct_answer"], "type": q["type"]} for q in questions]
    with open(os.path.join(export_dir, "answers.json"), 'w') as f:
        json.dump(answers, f, indent=2)

    # 3. Export metadata.json
    metadata = {
        "dataset_name": "GATE CS 2027 C Programming Question Bank",
        "version": "1.0.0",
        "total_questions": len(questions),
        "exported_timestamp": datetime.now().isoformat(),
        "distribution": {
            "easy": len([q for q in questions if q["difficulty"].lower() == "easy"]),
            "medium": len([q for q in questions if q["difficulty"].lower() == "medium"]),
            "hard": len([q for q in questions if q["difficulty"].lower() == "hard"]),
            "mcq": len([q for q in questions if q["type"].lower() == "mcq"]),
            "msq": len([q for q in questions if q["type"].lower() == "msq"]),
            "nat": len([q for q in questions if q["type"].lower() == "nat"]),
        }
    }
    with open(os.path.join(export_dir, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)

    # 4. Export questions.csv
    with open(os.path.join(export_dir, "questions.csv"), 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Subject", "Chapter", "Topic", "Concept", "Difficulty", "Type", "Question", "Options", "Correct Answer"])
        for q in questions:
            options_str = "|".join(q["options"]) if q["options"] else ""
            writer.writerow([
                q["id"], q["subject"], q["chapter"], q.get("topic", ""), q["concept"],
                q["difficulty"], q["type"], q["question"], options_str, q["correct_answer"]
            ])

    # 5. Export subject-wise folders for final delivery
    subject_dir = os.path.join(export_dir, "final", "Programming_Data_Structures")
    os.makedirs(subject_dir, exist_ok=True)
    with open(os.path.join(subject_dir, "c_programming_questions.json"), 'w') as f:
        json.dump(questions, f, indent=2)

    # 6. Export questions.md
    with open(os.path.join(export_dir, "questions.md"), 'w', encoding='utf-8') as f:
        f.write("# GATE CS 2027 C Programming Question Bank — Questions\n\n")
        for idx, q in enumerate(questions, 1):
            f.write(f"## Question {idx}: {q['id']} ({q['difficulty'].upper()} - {q['type'].upper()})\n\n")
            f.write(f"{q['question']}\n\n")
            if q["options"]:
                options = q["options"]
                for i, opt in enumerate(options):
                    letter = chr(65 + i)
                    f.write(f"**({letter})** {opt}\n\n")
            f.write("---\n\n")

    # 7. Export solutions.md
    with open(os.path.join(export_dir, "solutions.md"), 'w', encoding='utf-8') as f:
        f.write("# GATE CS 2027 C Programming Question Bank — Solutions\n\n")
        for idx, q in enumerate(questions, 1):
            f.write(f"## Solution {idx}: {q['id']} ({q['difficulty'].upper()} - {q['type'].upper()})\n\n")
            f.write(f"**Question:**\n\n{q['question']}\n\n")
            if q["options"]:
                options = q["options"]
                for i, opt in enumerate(options):
                    letter = chr(65 + i)
                    f.write(f"**({letter})** {opt}\n\n")
            f.write(f"**Correct Answer:** {q['correct_answer']}\n\n")
            f.write(f"**Explanation:**\n\n{q['explanation']}\n\n")
            f.write("---\n\n")

    # 8. Export coverage_report.json
    coverage = {
        "subject": "PDS",
        "total_questions": len(questions),
        "by_difficulty": {
            "easy": len([q for q in questions if q["difficulty"].lower() == "easy"]),
            "medium": len([q for q in questions if q["difficulty"].lower() == "medium"]),
            "hard": len([q for q in questions if q["difficulty"].lower() == "hard"]),
        },
        "by_type": {
            "mcq": len([q for q in questions if q["type"].lower() == "mcq"]),
            "msq": len([q for q in questions if q["type"].lower() == "msq"]),
            "nat": len([q for q in questions if q["type"].lower() == "nat"]),
        },
        "by_topic": {},
        "by_concept": {}
    }
    for q in questions:
        topic = q.get("topic", "Unknown")
        concept = q.get("concept", "Unknown")
        coverage["by_topic"][topic] = coverage["by_topic"].get(topic, 0) + 1
        coverage["by_concept"][concept] = coverage["by_concept"].get(concept, 0) + 1
        
    with open(os.path.join(export_dir, "coverage_report.json"), 'w') as f:
        json.dump(coverage, f, indent=2)

    # 9. Export quality_report.json
    quality_scores = [q.get("quality_score", 0.0) for q in questions if q.get("quality_score") is not None]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
    quality_report = {
        "total_evaluated": len(quality_scores),
        "average_quality_score": avg_quality,
        "max_quality_score": max(quality_scores) if quality_scores else 0.0,
        "min_quality_score": min(quality_scores) if quality_scores else 0.0,
        "distribution": {
            "90_100": len([s for s in quality_scores if s >= 90]),
            "85_89": len([s for s in quality_scores if 85 <= s < 90]),
            "below_85": len([s for s in quality_scores if s < 85]),
        }
    }
    with open(os.path.join(export_dir, "quality_report.json"), 'w') as f:
        json.dump(quality_report, f, indent=2)

    # 10. Export originality_report.json
    originality_scores = [q.get("originality_score", 0.0) for q in questions if q.get("originality_score") is not None]
    avg_originality = sum(originality_scores) / len(originality_scores) if originality_scores else 0.0
    originality_report = {
        "total_evaluated": len(originality_scores),
        "average_originality_score": avg_originality,
        "max_originality_score": max(originality_scores) if originality_scores else 0.0,
        "min_originality_score": min(originality_scores) if originality_scores else 0.0,
        "distribution": {
            "90_100": len([s for s in originality_scores if s >= 0.90]),
            "80_89": len([s for s in originality_scores if 0.80 <= s < 0.90]),
            "below_80": len([s for s in originality_scores if s < 0.80]),
        }
    }
    with open(os.path.join(export_dir, "originality_report.json"), 'w') as f:
        json.dump(originality_report, f, indent=2)

    # 11. Export generation_report.json
    conn = db_manager._get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM rejection_logs")
    rej_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM questions WHERE validation_status = 'REJECTED'")
    rejected_questions = cursor.fetchone()[0]
    conn.close()
    
    generation_report = {
        "total_generated": len(questions),
        "rejection_logs_count": rej_count,
        "rejected_questions_in_db": rejected_questions,
        "status": "COMPLETED",
        "timestamp": datetime.now().isoformat()
    }
    with open(os.path.join(export_dir, "generation_report.json"), 'w') as f:
        json.dump(generation_report, f, indent=2)
        
    print(f"Data exports completed successfully. Files saved in directory: {export_dir}")

    # 6. Export PDF
    try:
        from pdf.pdf_exporter import PDFExporter
        pdf_path = os.path.join(export_dir, "gate_c_programming_questions.pdf")
        exporter = PDFExporter(db_manager)
        exporter.export_pdf(pdf_path)
    except Exception as e:
        print(f"PDF generation failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="GATE CS 2027 Original Question Generation Engine")
    parser.add_argument("--init-db", action="store_true", help="Initialize the database structure and configurations")
    parser.add_argument("--run-pilot", action="store_true", help="Generate a small pilot batch of balanced questions")
    parser.add_argument("--status", action="store_true", help="Display current counts ledger and metrics")
    parser.add_argument("--export", action="store_true", help="Export validated questions to JSON, CSV, and PDF")
    parser.add_argument("--db", type=str, default="gate_questions.db", help="Path to SQLite database file")
    
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    db_manager, rag_manager = init_env(args.db)

    if args.init_db:
        print("Database successfully initialized.")
        sys.exit(0)

    if args.run_pilot:
        run_pilot(db_manager, rag_manager)
        
    if args.status:
        display_status(db_manager)

    if args.export:
        export_data(db_manager)

if __name__ == "__main__":
    main()
