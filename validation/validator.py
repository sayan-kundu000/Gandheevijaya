import json
import re
import difflib
from database.db_manager import DBManager

class QuestionValidator:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def validate(self, q_data):
        """Runs the validation pipeline. Returns (is_valid, reason, score)."""
        # 1. Structural Checks
        is_structure_ok, struct_reason = self._check_structure(q_data)
        if not is_structure_ok:
            return False, f"STRUCTURAL_ERROR: {struct_reason}", 0.0

        # 2. C Code Syntax check (if representation includes 'code')
        if q_data.get("representation") and "code" in q_data["representation"]:
            is_code_ok, code_reason = self._check_c_code_integrity(q_data["question"])
            if not is_code_ok:
                return False, f"CODE_ERROR: {code_reason}", 0.0

        # 3. Originality Check (Lexical similarity)
        is_original, similarity_reason, similarity_score = self._check_originality(q_data)
        if not is_original:
            return False, f"COPY_RISK: {similarity_reason}", similarity_score

        # 4. Difficulty & Quality Calibration
        quality_score = self._calculate_quality_score(q_data, similarity_score)
        
        # Rejection rules
        if quality_score < 85:
            return False, "LOW_QUALITY: Overall quality score below passing threshold (85).", quality_score
            
        return True, "Passed all quality controls.", quality_score

    def _check_structure(self, q_data):
        """Verifies the basic required fields, answer formats and options."""
        required_fields = ["id", "subject", "concept", "difficulty", "type", "question", "correct_answer", "explanation"]
        for field in required_fields:
            if not q_data.get(field):
                return False, f"Missing required field: {field}"

        q_type = q_data["type"].lower()
        
        # MCQ Specific checks
        if q_type == "mcq":
            if not q_data.get("options") or len(q_data["options"]) != 4:
                return False, "MCQ must have exactly 4 options."
            if q_data["correct_answer"] not in ["A", "B", "C", "D"]:
                return False, f"MCQ correct answer must be 'A', 'B', 'C', or 'D'. Got '{q_data['correct_answer']}'"
                
        # MSQ Specific checks
        elif q_type == "msq":
            if not q_data.get("options") or len(q_data["options"]) != 4:
                return False, "MSQ must have exactly 4 options."
            # Correct answer should be a JSON array or list containing subset of A,B,C,D
            ans = q_data["correct_answer"]
            if isinstance(ans, str):
                try:
                    ans = json.loads(ans)
                except json.JSONDecodeError:
                    return False, f"MSQ correct answer must be a valid JSON array. Got '{ans}'"
            if not isinstance(ans, list) or len(ans) == 0:
                return False, "MSQ correct answer must be a list containing at least one option."
            for a in ans:
                if a not in ["A", "B", "C", "D"]:
                    return False, f"MSQ option '{a}' is invalid. Must be A, B, C, or D."
                    
        # NAT Specific checks
        elif q_type == "nat":
            if q_data.get("options"):
                return False, "NAT must not have options."
            ans_str = str(q_data["correct_answer"]).strip()
            # Try to convert to float
            try:
                float(ans_str)
            except ValueError:
                return False, f"NAT correct answer must be a valid number. Got '{ans_str}'"
                
        else:
            return False, f"Unknown question type: {q_type}"
            
        return True, ""

    def _check_c_code_integrity(self, question_text):
        """Performs simple static analysis checks on C code blocks to ensure brace balance and basic formatting."""
        code_blocks = re.findall(r'```c(.*?)```', question_text, re.DOTALL)
        if not code_blocks:
            return True, "" # No code blocks, but 'code' representation was declared. Acceptable.

        for block in code_blocks:
            # Check basic braces balance
            open_braces = block.count('{')
            close_braces = block.count('}')
            if open_braces != close_braces:
                return False, f"Unbalanced curly braces in C code block. Opened {open_braces}, Closed {close_braces}"
                
            open_parens = block.count('(')
            close_parens = block.count(')')
            if open_parens != close_parens:
                return False, f"Unbalanced parentheses in C code block. Opened {open_parens}, Closed {close_parens}"
                
            # Check for main function basic structure
            if "main" in block and "{" not in block:
                return False, "main function declared but brace not opened."

        return True, ""

    def _check_originality(self, q_data):
        """Checks Jaccard lexical similarity against the database of existing questions."""
        q_text = q_data["question"].strip().lower()
        
        conn = self.db_manager._get_connection()
        cursor = conn.cursor()
        # Only check similarity against already VALIDATED questions to avoid draft/rejection collision
        cursor.execute("SELECT id, question FROM questions WHERE id != ? AND validation_status = 'VALIDATED'", (q_data["id"],))
        rows = cursor.fetchall()
        conn.close()

        ignore_words = {
            "int", "char", "float", "double", "void", "static", "struct", "main", "return", 
            "include", "stdio", "h", "printf", "sizeof", "if", "else", "for", "while", "do", 
            "const", "unsigned", "signed", "what", "will", "the", "output", "following", "program", 
            "consider", "code", "block", "value", "printed", "function", "statements", "about", 
            "correct", "which", "are", "statement", "declared", "declaration", "evaluate", 
            "evaluates", "to", "after", "completes", "shown", "below", "option", "correct_answer",
            "given", "relevant", "principle", "step", "reasoning", "calculation", "derivation"
        }
        
        # Filter out stop words, digits, and short variables (length <= 2)
        words_new = {
            w for w in re.findall(r'\w+', q_text) 
            if w not in ignore_words and not w.isdigit() and len(w) > 2
        }
        
        if not words_new:
            return True, "", 1.0
            
        max_sim = 0.0
        match_id = None
        
        # Clean new text for sequence matching
        clean_new = q_text
        for word in ignore_words:
            clean_new = re.sub(r'\b' + word + r'\b', '', clean_new)
        # Remove numbers and short words
        clean_new = re.sub(r'\b\w{1,2}\b', '', clean_new)
        clean_new = re.sub(r'\b\d+\b', '', clean_new)
        # Remove non-alphanumeric characters and collapse spaces
        clean_new = re.sub(r'[^\w\s]', '', clean_new)
        clean_new = re.sub(r'\s+', ' ', clean_new).strip()
        
        for row in rows:
            exist_id = row["id"]
            exist_text = row["question"].strip().lower()
            
            words_exist = {
                w for w in re.findall(r'\w+', exist_text) 
                if w not in ignore_words and not w.isdigit() and len(w) > 2
            }
            
            if not words_exist:
                continue
                
            # Jaccard Similarity
            intersection = set(words_new).intersection(words_exist)
            union = set(words_new).union(words_exist)
            sim = len(intersection) / len(union)
            
            # SequenceMatcher for sub-phrase matching on stripped texts
            clean_exist = exist_text
            for word in ignore_words:
                clean_exist = re.sub(r'\b' + word + r'\b', '', clean_exist)
            clean_exist = re.sub(r'\b\w{1,2}\b', '', clean_exist)
            clean_exist = re.sub(r'\b\d+\b', '', clean_exist)
            clean_exist = re.sub(r'[^\w\s]', '', clean_exist)
            clean_exist = re.sub(r'\s+', ' ', clean_exist).strip()
                
            seq_sim = difflib.SequenceMatcher(None, clean_new, clean_exist).ratio()
            sim = max(sim, seq_sim)
            
            # Incorporate Data Science TF-IDF + Char N-Gram semantic similarity
            from backend.app.core.semantic_deduplication import default_semantic_deduplicator
            ds_sem_sim = default_semantic_deduplicator.get_semantic_similarity(q_text, exist_text)
            sim = max(sim, ds_sem_sim)

            if sim > max_sim:
                max_sim = sim
                match_id = exist_id

        originality_score = 1.0 - max_sim
        
        # Max lexical similarity is 50% (meaning at least 50% originality on non-boilerplate content)
        if max_sim > 0.50:
            return False, f"Lexical similarity with {match_id} is {max_sim:.2f} (exceeds threshold 0.50).", originality_score
            
        return True, "", originality_score

    def _calculate_quality_score(self, q_data, originality_score):
        """Calculates a composite quality score from 0-100."""
        # Baseline score starts at 90
        score = 90.0
        
        # Adjust based on originality (originality_score is from 0.0 to 1.0)
        # We want originality_score to be high (e.g., > 0.60, meaning similarity < 0.40)
        if originality_score < 0.70:
            score -= (0.70 - originality_score) * 30.0 # penalty for near similarity
            
        # Code block evaluation
        q_text = q_data["question"]
        if "```c" in q_text:
            score += 2.0  # code questions have higher depth
            
        # Explanations quality: must contain Given, Principle, and step-by-step
        explanation = q_data["explanation"].lower()
        if "given:" in explanation or "given" in explanation:
            score += 1.0
        else:
            score -= 3.0
            
        if "principle" in explanation or "rule" in explanation:
            score += 1.0
        else:
            score -= 3.0
            
        if "step" in explanation or "reasoning" in explanation:
            score += 1.0
        else:
            score -= 3.0
            
        # Cap score between 0 and 100
        return max(0.0, min(100.0, score))
