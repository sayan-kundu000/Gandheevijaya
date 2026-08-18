import sqlite3
import os
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(script_dir))
if workspace_root not in sys.path:
    sys.path.append(workspace_root)

from backend.app.core.semantic_deduplication import default_semantic_deduplicator

def run_semantic_deduplication(db_path: str, similarity_threshold: float = 0.50):
    print(f"\n=========================================")
    print(f"Running Fast Data Science Semantic Deduplication: {db_path}")
    print(f"=========================================")
    if not os.path.exists(db_path):
        print(f"Database path not found: {db_path}")
        return

    t0 = time.time()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF;")

    cursor.execute("PRAGMA table_info(questions)")
    cols = [col[1] for col in cursor.fetchall()]
    if not cols:
        print("No questions table found.")
        conn.close()
        return

    text_col = 'question_text' if 'question_text' in cols else 'question'
    topic_col = 'topic_id' if 'topic_id' in cols else ('topic' if 'topic' in cols else None)

    query = f"SELECT id, {text_col}, {topic_col if topic_col else '1'} FROM questions"
    cursor.execute(query)
    all_questions = cursor.fetchall()
    print(f"Total questions loaded: {len(all_questions)}")

    grouped = {}
    for q_id, q_text, t_val in all_questions:
        t_key = str(t_val)
        if t_key not in grouped:
            grouped[t_key] = []
        grouped[t_key].append((q_id, q_text))

    ids_to_remove = set()
    for t_key, q_list in grouped.items():
        chosen = []
        for q_id, q_text in q_list:
            tokens = set(default_semantic_deduplicator.get_word_tokens(q_text))
            if not tokens:
                chosen.append((q_id, q_text, tokens))
                continue

            is_dup = False
            for chosen_id, chosen_text, chosen_tokens in chosen:
                # Fast pre-filter: require token overlap > 30% before full TF-IDF computation
                overlap = len(tokens.intersection(chosen_tokens)) / max(len(tokens), 1)
                if overlap < 0.25:
                    continue

                score = default_semantic_deduplicator.get_semantic_similarity(q_text, chosen_text)
                if score >= similarity_threshold:
                    is_dup = True
                    ids_to_remove.add(q_id)
                    break

            if not is_dup:
                chosen.append((q_id, q_text, tokens))

    print(f"Identified {len(ids_to_remove)} semantically duplicate questions (threshold >= {similarity_threshold}).")

    if ids_to_remove:
        print("Removing semantically duplicate questions from DB...")
        cursor.execute("CREATE TEMP TABLE temp_sem_ids (id TEXT PRIMARY KEY)")
        cursor.executemany("INSERT INTO temp_sem_ids VALUES (?)", [(qid,) for qid in ids_to_remove])
        cursor.execute("DELETE FROM questions WHERE id IN (SELECT id FROM temp_sem_ids)")
        cursor.execute("DROP TABLE temp_sem_ids")
        conn.commit()

    cursor.execute("SELECT COUNT(*) FROM questions")
    total_after = cursor.fetchone()[0]
    print(f"Data Science Semantic Deduplication COMPLETE! Remaining questions: {total_after} (Removed {len(ids_to_remove)})")

    print("Optimizing DB (VACUUM)...")
    cursor.execute("VACUUM")
    conn.close()

    print(f"Completed in {time.time() - t0:.2f}s")

if __name__ == "__main__":
    backend_db = os.path.join(workspace_root, "backend", "gandheevijaya.db")
    scripts_db = os.path.join(workspace_root, "scripts", "gate_questions.db")

    if os.path.exists(backend_db):
        run_semantic_deduplication(backend_db)
    if os.path.exists(scripts_db):
        run_semantic_deduplication(scripts_db)
