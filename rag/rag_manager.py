import os
import json
from database.db_manager import DBManager

class RAGManager:
    def __init__(self, db_manager: DBManager, patterns_path=None):
        self.db_manager = db_manager
        if patterns_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            patterns_path = os.path.join(current_dir, "patterns.json")
        self.patterns_path = patterns_path

    def preload_patterns(self):
        """Loads patterns from patterns.json and inserts them into the database if the database is empty."""
        conn = self.db_manager._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM abstract_patterns")
        count = cursor.fetchone()[0]
        conn.close()

        if count == 0:
            print("Preloading abstract patterns into the database...")
            with open(self.patterns_path, 'r') as f:
                patterns = json.load(f)
            
            for p in patterns:
                self.db_manager.insert_abstract_pattern(
                    subject=p["subject"],
                    topic=p["topic"],
                    subtopic=p.get("subtopic"),
                    concept=p["concept"],
                    archetype=p["archetype"],
                    reasoning_type=",".join(p["reasoning_type"]),
                    required_knowledge=p.get("required_knowledge"),
                    reasoning_steps=p.get("reasoning_steps"),
                    pattern_text=p["pattern_text"]
                )
            print(f"Preloaded {len(patterns)} patterns.")
        else:
            print(f"Patterns table already has {count} entries. Skipping preloading.")

    def preload_syllabus(self, syllabus_path=None):
        """Preloads syllabus concepts from syllabus.json into the syllabus_concepts table."""
        if syllabus_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            syllabus_path = os.path.join(os.path.dirname(current_dir), "config", "syllabus.json")
            
        conn = self.db_manager._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM syllabus_concepts")
        count = cursor.fetchone()[0]
        conn.close()

        if count == 0:
            print("Preloading syllabus concepts into the database...")
            with open(syllabus_path, 'r') as f:
                syllabus = json.load(f)
            
            for sub_code, sub_data in syllabus["subjects"].items():
                for chap_name, topics in sub_data["chapters"].items():
                    for topic in topics:
                        # For simplicity, we treat the topic as both the topic and the concept in the database
                        self.db_manager.insert_syllabus_concept(
                            subject_code=sub_code,
                            chapter_name=chap_name,
                            topic_name=topic,
                            concept_name=topic
                        )
            print("Preloaded syllabus concepts.")
        else:
            print("Syllabus concepts table already initialized. Skipping.")

    def retrieve_patterns(self, subject, concept=None):
        """Retrieves patterns for a given subject, optionally filtered by concept."""
        if concept:
            return self.db_manager.get_patterns_for_concept(subject, concept)
        else:
            return self.db_manager.get_random_pattern_for_subject(subject)
