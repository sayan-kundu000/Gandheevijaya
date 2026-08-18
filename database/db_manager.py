import sqlite3
import json
import os
from datetime import datetime

class DBManager:
    def __init__(self, db_path="gate_questions.db", schema_path=None):
        self.db_path = db_path
        if schema_path is None:
            # Locate schema.sql relative to db_manager.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            schema_path = os.path.join(current_dir, "schema.sql")
        
        self.schema_path = schema_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initializes the database using schema.sql if tables do not exist."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(self.schema_path, 'r') as f:
            schema_sql = f.read()
            
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()

    def insert_syllabus_concept(self, subject_code, chapter_name, topic_name, concept_name):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO syllabus_concepts (subject_code, chapter_name, topic_name, concept_name)
            VALUES (?, ?, ?, ?)
        """, (subject_code, chapter_name, topic_name, concept_name))
        conn.commit()
        conn.close()

    def insert_abstract_pattern(self, subject, topic, subtopic, concept, archetype, reasoning_type, required_knowledge, reasoning_steps, pattern_text):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO abstract_patterns (subject, topic, subtopic, concept, archetype, reasoning_type, required_knowledge, reasoning_steps, pattern_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (subject, topic, subtopic, concept, archetype, reasoning_type, required_knowledge, reasoning_steps, pattern_text))
        conn.commit()
        conn.close()

    def get_patterns_for_concept(self, subject, concept):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM abstract_patterns 
            WHERE subject = ? AND concept = ?
        """, (subject, concept))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    def get_random_pattern_for_subject(self, subject):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM abstract_patterns 
            WHERE subject = ?
            ORDER BY RANDOM() LIMIT 1
        """, (subject,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def store_question(self, q_data):
        """Stores a generated question. If validation_status is 'VALIDATED', updates the ledger count."""
        is_dup, dup_id = self.check_duplicate(q_data["question"])
        if is_dup:
            print(f"Skipping duplicate question text (matches existing question ID {dup_id}).")
            return False

        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Convert list/dict fields to JSON strings
        options_str = json.dumps(q_data.get("options")) if q_data.get("options") else None
        reasoning_type_str = json.dumps(q_data.get("reasoning_type")) if q_data.get("reasoning_type") else None
        representation_str = json.dumps(q_data.get("representation")) if q_data.get("representation") else None
        
        # Insert/replace question
        cursor.execute("""
            INSERT OR IGNORE INTO questions (
                id, subject, chapter, topic, subtopic, concept, difficulty, type, 
                question, options, correct_answer, explanation, reasoning_type, 
                archetype, representation, estimated_reasoning_steps, 
                originality_score, quality_score, validation_status, generation_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q_data["id"],
            q_data["subject"],
            q_data["chapter"],
            q_data["topic"],
            q_data.get("subtopic"),
            q_data["concept"],
            q_data["difficulty"].lower(),
            q_data["type"].lower(),
            q_data["question"],
            options_str,
            str(q_data["correct_answer"]),
            q_data["explanation"],
            reasoning_type_str,
            q_data.get("archetype"),
            representation_str,
            q_data.get("estimated_reasoning_steps"),
            q_data.get("originality_score"),
            q_data.get("quality_score"),
            q_data.get("validation_status", "DRAFT"),
            q_data.get("generation_timestamp", datetime.now().isoformat())
        ))
        
        # If validated, update ledger
        if q_data.get("validation_status") == "VALIDATED":
            diff = q_data["difficulty"].lower()
            q_type = q_data["type"].lower()
            cursor.execute("""
                INSERT INTO generation_ledger (difficulty, type, count)
                VALUES (?, ?, 1)
                ON CONFLICT(difficulty, type) DO UPDATE SET count = count + 1
            """, (diff, q_type))
            
        conn.commit()
        conn.close()

    def log_rejection(self, question_id, subject, difficulty, q_type, reason, feedback_comment=""):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO rejection_logs (question_id, subject, difficulty, type, reason, feedback_comment, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            question_id, 
            subject, 
            difficulty.lower() if difficulty else None, 
            q_type.lower() if q_type else None, 
            reason, 
            feedback_comment, 
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    def get_ledger(self):
        """Returns a dict of current validated counts by difficulty and type."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT difficulty, type, count FROM generation_ledger")
        rows = cursor.fetchall()
        conn.close()
        
        ledger = {
            "easy": {"mcq": 0, "msq": 0, "nat": 0},
            "medium": {"mcq": 0, "msq": 0, "nat": 0},
            "hard": {"mcq": 0, "msq": 0, "nat": 0}
        }
        for row in rows:
            diff = row["difficulty"].lower()
            q_type = row["type"].lower()
            ledger[diff][q_type] = row["count"]
        return ledger

    def get_total_validated_count(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(count) FROM generation_ledger")
        res = cursor.fetchone()[0]
        conn.close()
        return res if res else 0

    def get_questions(self, subject=None, difficulty=None, q_type=None, status="VALIDATED"):
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM questions WHERE validation_status = ?"
        params = [status]
        
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        if difficulty:
            query += " AND difficulty = ?"
            params.append(difficulty.lower())
        if q_type:
            query += " AND type = ?"
            params.append(q_type.lower())
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        questions = []
        for row in rows:
            q = dict(row)
            q["options"] = json.loads(q["options"]) if q["options"] else None
            q["reasoning_type"] = json.loads(q["reasoning_type"]) if q["reasoning_type"] else None
            q["representation"] = json.loads(q["representation"]) if q["representation"] else None
            questions.append(q)
        return questions

    def get_question_by_id(self, q_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions WHERE id = ?", (q_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            q = dict(row)
            q["options"] = json.loads(q["options"]) if q["options"] else None
            q["reasoning_type"] = json.loads(q["reasoning_type"]) if q["reasoning_type"] else None
            q["representation"] = json.loads(q["representation"]) if q["representation"] else None
            return q
        return None

    def check_duplicate(self, text_to_check, threshold=0.85):
        """Simple exact and lexical check against existing questions. 
        Returns True, similar_question_id if match exceeds threshold, else False, None."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, question FROM questions")
        rows = cursor.fetchall()
        conn.close()
        
        for row in rows:
            q_id = row["id"]
            q_text = row["question"]
            if text_to_check.strip() == q_text.strip():
                return True, q_id
        return False, None
