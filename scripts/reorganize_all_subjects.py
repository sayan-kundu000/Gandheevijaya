import os
import shutil
import json
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def write_simple_pdf(filepath, title, text_content):
    """Generates a fast single-pass canvas PDF file without the complex layout engine."""
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(54, 750, title)
    c.setLineWidth(0.5)
    c.line(54, 740, 558, 740)
    
    c.setFont("Helvetica", 10)
    y = 715
    for line in text_content.split('\n'):
        # Simple wrap at 85 chars
        words = line.split(' ')
        current_line = ""
        for word in words:
            if len(current_line) + len(word) < 85:
                current_line += word + " "
            else:
                c.drawString(54, y, current_line.strip())
                y -= 15
                current_line = word + " "
                if y < 50:
                    c.showPage()
                    y = 750
                    c.setFont("Helvetica", 10)
        if current_line:
            c.drawString(54, y, current_line.strip())
            y -= 15
            if y < 50:
                c.showPage()
                y = 750
                c.setFont("Helvetica", 10)
    c.save()

def main():
    import random
    base_dir = "datasets"
    print("Clearing datasets directory...")
    if os.path.exists(base_dir):
        temp_dir = base_dir + "_old_" + str(random.randint(1000, 9999))
        try:
            os.rename(base_dir, temp_dir)
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception as e:
            try:
                shutil.rmtree(base_dir, ignore_errors=True)
            except Exception as e2:
                pass
    os.makedirs(base_dir, exist_ok=True)
    
    # Create directories for subjects (PDS, DSA, ALGO, OS, DB, COA, DL, CN, TOC, CD, LA, CALC, DM, PROB, MA, QA, VA, VR, LR, SA, AA, AR, MR)
    subjects = ["PDS", "DSA", "ALGO", "OS", "DB", "COA", "DL", "CN", "TOC", "CD", "LA", "CALC", "DM", "PROB", "MA", "QA", "VA", "VR", "LR", "SA", "AA", "AR", "MR"]
    sub_folders = {
        "PDS": "cprog", 
        "DSA": "dsa", 
        "ALGO": "algo", 
        "OS": "os", 
        "DB": "dbms", 
        "COA": "coa", 
        "DL": "digitallogic",
        "CN": "cn",
        "TOC": "toc",
        "CD": "cd",
        "LA": "la",
        "CALC": "calc",
        "DM": "dm",
        "PROB": "probstat",
        "MA": "ma",
        "QA": "qa",
        "VA": "va",
        "VR": "vr",
        "LR": "lr",
        "SA": "sa",
        "AA": "aa",
        "AR": "ar",
        "MR": "mr"
    }
    difficulties = ["easy", "medium", "hard"]
    diff_folders = {"easy": "ej", "medium": "mj", "hard": "hj"}
    
    for sub in subjects:
        sub_f = sub_folders[sub]
        for diff in difficulties:
            diff_f = diff_folders[diff]
            os.makedirs(os.path.join(base_dir, sub_f, diff_f, "quesj"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, sub_f, diff_f, "ansj"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, sub_f, diff_f, "solnj"), exist_ok=True)
            
    print("Connecting to database...")
    db_path = "gate_questions.db"
    if not os.path.exists(db_path):
        print("Database not found! Run final_dataset_generator.py first.")
        return
        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions WHERE validation_status = 'VALIDATED'")
    questions = cursor.fetchall()
    conn.close()
    
    print(f"Loaded {len(questions)} validated questions. Splitting...")
    
    # Process questions in groups
    for sub in subjects:
        sub_f = sub_folders[sub]
        sub_qs = [q for q in questions if q["subject"] == sub]
        print(f"Processing subject: {sub} ({len(sub_qs)} questions)")
        
        for diff in difficulties:
            diff_f = diff_folders[diff]
            diff_qs = [q for q in sub_qs if q["difficulty"].lower() == diff]
            
            mcqs = [q for q in diff_qs if q["type"].lower() == "mcq"]
            msqs = [q for q in diff_qs if q["type"].lower() == "msq"]
            nats = [q for q in diff_qs if q["type"].lower() == "nat"]
            
            print(f"  Difficulty: {diff.upper()} ({diff_f}) -> MCQs: {len(mcqs)}, MSQs: {len(msqs)}, NATs: {len(nats)}")
            
            # Split into 25 files
            for i in range(25):
                group_num = i + 1
                q_file_name = f"{sub_f}{group_num:02d}{diff_f[0]}q.json"
                a_file_name = f"{sub_f}{group_num:02d}{diff_f[0]}a.json"
                s_file_name = f"{sub_f}{group_num:02d}{diff_f[0]}s.json"
                
                slice_mcq = mcqs[i*25 : (i+1)*25]
                slice_msq = msqs[i*25 : (i+1)*25]
                slice_nat = nats[i*25 : (i+1)*25]
                
                group_qs = slice_mcq + slice_msq + slice_nat
                
                questions_list = []
                answers_list = []
                solutions_list = []
                
                for q in group_qs:
                    q_dict = dict(q)
                    q_id = q_dict["id"]
                    options = json.loads(q_dict["options"]) if q_dict["options"] else []
                    reasoning_type = json.loads(q_dict["reasoning_type"]) if q_dict["reasoning_type"] else []
                    representation = json.loads(q_dict["representation"]) if q_dict["representation"] else []
                    
                    q_obj = {
                        "id": q_id,
                        "subject": q_dict["subject"],
                        "topic": q_dict.get("topic", ""),
                        "subtopic": q_dict.get("subtopic", ""),
                        "difficulty": q_dict["difficulty"],
                        "type": q_dict["type"].upper(),
                        "question": q_dict["question"],
                        "options": options,
                        "answer_id": q_id,
                        "pattern_type": q_dict.get("archetype", ""),
                        "reasoning_type": reasoning_type,
                        "representation": representation
                    }
                    questions_list.append(q_obj)
                    
                    answers_list.append({"id": q_id, "correct_answer": q_dict["correct_answer"]})
                    solutions_list.append({"id": q_id, "explanation": q_dict["explanation"]})
                    
                # Write files
                with open(os.path.join(base_dir, sub_f, diff_f, "quesj", q_file_name), 'w', encoding='utf-8') as f:
                    json.dump(questions_list, f, indent=2)
                with open(os.path.join(base_dir, sub_f, diff_f, "ansj", a_file_name), 'w', encoding='utf-8') as f:
                    json.dump(answers_list, f, indent=2)
                with open(os.path.join(base_dir, sub_f, diff_f, "solnj", s_file_name), 'w', encoding='utf-8') as f:
                    json.dump(solutions_list, f, indent=2)
                    
            print(f"  Successfully wrote 25 group files for {sub_f}/{diff_f}.")
            
    print("\nDataset organization completed successfully.")

if __name__ == "__main__":
    main()
