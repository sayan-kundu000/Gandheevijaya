import sqlite3
import os
import sys
import time

def deduplicate_database(db_path):
    print(f"\n=========================================")
    print(f"Deduplicating Database: {db_path}")
    print(f"=========================================")
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return

    t0 = time.time()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # Inspect questions table
    cursor.execute("PRAGMA table_info(questions)")
    cols = [col[1] for col in cursor.fetchall()]
    if not cols:
        print(f"No questions table found in {db_path}.")
        conn.close()
        return

    text_col = 'question_text' if 'question_text' in cols else 'question'

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_before = cursor.fetchone()[0]

    # Find canonical IDs (MIN(id)) for each question_text
    cursor.execute(f"SELECT MIN(id), {text_col} FROM questions GROUP BY {text_col}")
    canon_rows = cursor.fetchall()
    canon_map = {text: canon_id for canon_id, text in canon_rows}
    canon_id_set = set(canon_map.values())

    print(f"Total question rows before: {total_before}")
    print(f"Unique question texts (canonical rows): {len(canon_map)}")

    cursor.execute(f"SELECT id, {text_col} FROM questions")
    all_rows = cursor.fetchall()
    id_to_canon = {}
    for qid, qtext in all_rows:
        c_id = canon_map[qtext]
        if qid != c_id:
            id_to_canon[qid] = c_id

    print(f"Non-canonical IDs to re-map & remove: {len(id_to_canon)}")

    tables = [t[0] for t in cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

    # 1. Update quiz_questions table if present
    if 'quiz_questions' in tables:
        cursor.execute("SELECT quiz_id, question_id, sort_order, marks, negative_marks FROM quiz_questions")
        qq_rows = cursor.fetchall()

        remapped_qq = 0
        dropped_qq = 0
        existing_qq_pairs = set()
        new_qq_rows = []

        for quiz_id, q_id, sort_order, marks, neg_marks in qq_rows:
            target_q_id = id_to_canon.get(q_id, q_id)
            if (quiz_id, target_q_id) in existing_qq_pairs:
                dropped_qq += 1
            else:
                existing_qq_pairs.add((quiz_id, target_q_id))
                if target_q_id != q_id:
                    remapped_qq += 1
                new_qq_rows.append((quiz_id, target_q_id, sort_order, marks, neg_marks))

        print(f"quiz_questions: {remapped_qq} remapped, {dropped_qq} duplicates dropped, {len(new_qq_rows)} final rows.")

        cursor.execute("DELETE FROM quiz_questions")
        cursor.executemany(
            "INSERT OR IGNORE INTO quiz_questions (quiz_id, question_id, sort_order, marks, negative_marks) VALUES (?, ?, ?, ?, ?)",
            new_qq_rows
        )

    # 2. Update attempt_answers table if present
    if 'attempt_answers' in tables:
        cursor.execute("SELECT id, question_id FROM attempt_answers")
        aa_rows = cursor.fetchall()
        remapped_aa = 0
        for aa_id, q_id in aa_rows:
            if q_id in id_to_canon:
                canon_q_id = id_to_canon[q_id]
                cursor.execute("UPDATE attempt_answers SET question_id = ? WHERE id = ?", (canon_q_id, aa_id))
                remapped_aa += 1
        print(f"attempt_answers: {remapped_aa} rows remapped.")

    # 3. Delete non-canonical questions
    print("Deleting duplicate question rows from questions table...")
    cursor.execute("CREATE TEMP TABLE temp_canon_ids (id TEXT PRIMARY KEY)")
    cursor.executemany("INSERT INTO temp_canon_ids VALUES (?)", [(cid,) for cid in canon_id_set])
    cursor.execute("DELETE FROM questions WHERE id NOT IN (SELECT id FROM temp_canon_ids)")
    cursor.execute("DROP TABLE temp_canon_ids")

    # 4. Create unique index
    idx_name = f"uq_questions_{text_col}"
    cursor.execute(f"CREATE UNIQUE INDEX IF NOT EXISTS {idx_name} ON questions({text_col})")
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_after = cursor.fetchone()[0]
    print(f"Deduplication COMPLETE! Total question rows after: {total_after} (Removed {total_before - total_after} duplicate rows)")

    print("Reclaiming disk space (VACUUM)...")
    cursor.execute("VACUUM")
    conn.close()

    print(f"Completed DB deduplication in {time.time() - t0:.2f}s")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(os.path.dirname(script_dir))
    backend_db = os.path.join(workspace_root, "backend", "gandheevijaya.db")
    scripts_db = os.path.join(workspace_root, "scripts", "gate_questions.db")

    if os.path.exists(backend_db):
        deduplicate_database(backend_db)
    if os.path.exists(scripts_db):
        deduplicate_database(scripts_db)
