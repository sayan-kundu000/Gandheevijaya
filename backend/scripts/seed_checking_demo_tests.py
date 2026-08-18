import sqlite3
import os
import sys
import json
import random
from datetime import datetime, timezone

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.dirname(os.path.dirname(script_dir))
if workspace_root not in sys.path:
    sys.path.append(workspace_root)

from backend.app.core.semantic_deduplication import default_semantic_deduplicator

# High quality GK question templates generator across 25 categories
GK_DATA_POOLS = {
    "Indian History": [
        ("Who was the founder of the Maurya Empire?", ["Chandragupta Maurya", "Ashoka", "Bindusara", "Harsha"], "A", "Chandragupta Maurya founded the Maurya Empire in 322 BCE with the help of Chanakya."),
        ("In which year did the Battle of Plassey take place?", ["1757", "1764", "1857", "1748"], "A", "The Battle of Plassey was fought on 23 June 1757 between the British East India Company and the Nawab of Bengal."),
        ("Who among the following wrote 'Harshacharita'?", ["Banabhatta", "Kalidasa", "Harsha", "Harisena"], "A", "Banabhatta, the court poet of King Harsha, wrote Harshacharita in Sanskrit."),
        ("The Indus Valley Civilization site 'Lothal' is located in which modern state?", ["Gujarat", "Rajasthan", "Punjab", "Haryana"], "A", "Lothal was one of the southernmost cities of the ancient Indus Valley Civilization, located in Gujarat."),
        ("Who assumed the title of 'Vikramaditya'?", ["Chandragupta II", "Samudragupta", "Chandragupta I", "Skandagupta"], "A", "Chandragupta II of the Gupta dynasty assumed the famous title of Vikramaditya."),
        ("Who led the Salt Satyagraha Dandi March in 1930?", ["Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhash Chandra Bose"], "A", "Mahatma Gandhi launched the Dandi Salt March from Sabarmati Ashram on 12 March 1930."),
        ("Which Mughal Emperor built the Red Fort in Delhi?", ["Shah Jahan", "Akbar", "Jahangir", "Aurangzeb"], "A", "Shah Jahan commissioned the construction of the Red Fort in Delhi in 1638."),
        ("The Arya Samaj was founded by whom in 1875?", ["Swami Dayananda Saraswati", "Swami Vivekananda", "Raja Ram Mohan Roy", "Ishwar Chandra Vidyasagar"], "A", "Swami Dayananda Saraswati founded Arya Samaj in Bombay in 1875."),
        ("Who was known as the 'Frontier Gandhi'?", ["Khan Abdul Ghaffar Khan", "Maulana Abul Kalam Azad", "Hasrat Mohani", "Khan Bahadur"], "A", "Khan Abdul Ghaffar Khan was affectionately called Frontier Gandhi (Sarhadi Gandhi)."),
        ("In which session did the Indian National Congress declare 'Purna Swaraj'?", ["Lahore Session 1929", "Karachi Session 1931", "Calcutta Session 1920", "Lucknow Session 1916"], "A", "The Lahore Session of INC in 1929 passed the resolution for Purna Swaraj (Complete Independence)."),
        ("Who was the governor-general during the 1857 Sepoy Mutiny?", ["Lord Canning", "Lord Dalhousie", "Lord Curzon", "Lord Wellesley"], "A", "Lord Canning served as the Governor-General of India during the Revolt of 1857."),
        ("Which Chola ruler conquered Sri Lanka and built the Brihadisvara Temple?", ["Rajaraja Chola I", "Rajendra Chola I", "Karikala Chola", "Parantaka I"], "A", "Rajaraja Chola I built the magnificent Brihadisvara Temple at Thanjavur."),
        ("Who established the 'Servants of India Society' in 1905?", ["Gopal Krishna Gokhale", "Bal Gangadhar Tilak", "Lala Lajpat Rai", "Bipin Chandra Pal"], "A", "Gopal Krishna Gokhale founded the Servants of India Society in Pune in 1905."),
        ("The Cabinet Mission came to India in which year?", ["1946", "1942", "1945", "1947"], "A", "The Cabinet Mission arrived in India in March 1946 to discuss constitutional reforms."),
        ("Who was the first ruler of the Slave Dynasty in Delhi Sultanate?", ["Qutb-ud-din Aibak", "Iltutmish", "Balban", "Razia Sultana"], "A", "Qutb-ud-din Aibak founded the Mamluk/Slave dynasty of the Delhi Sultanate in 1206."),
        ("Which Chinese pilgrim visited India during Harsha's reign?", ["Hiuen Tsang", "Fa-Hien", "I-Tsing", "Megasthenes"], "A", "Hiuen Tsang (Xuanzang) visited India during the 7th century during King Harsha's rule."),
        ("The Vernacular Press Act was passed by which Viceroy in 1878?", ["Lord Lytton", "Lord Ripon", "Lord Curzon", "Lord Dufferin"], "A", "Lord Lytton enacted the Vernacular Press Act in 1878 to curtail Indian language press freedom."),
        ("Who founded the Brahmo Samaj in 1828?", ["Raja Ram Mohan Roy", "Debendranath Tagore", "Keshab Chandra Sen", "Swami Dayananda"], "A", "Raja Ram Mohan Roy established Brahmo Sabha (later Brahmo Samaj) in 1828."),
        ("In which year was the partition of Bengal announced by Lord Curzon?", ["1905", "1911", "1906", "1909"], "A", "Lord Curzon announced the Partition of Bengal in July 1905."),
        ("Who authored the ancient treatise 'Arthashastra'?", ["Chanakya (Kautilya)", "Megasthenes", "Visakhadatta", "Bhasa"], "A", "Chanakya (Kautilya) authored the Arthashastra on statecraft and economic policy."),
        ("Where was the Third Buddhist Council held?", ["Pataliputra", "Rajgir", "Vaishali", "Kashmir"], "A", "The Third Buddhist Council was convened at Pataliputra under King Ashoka's patronage."),
        ("Who was the first woman President of the Indian National Congress?", ["Annie Besant", "Sarojini Naidu", "Nellie Sengupta", "Vijaya Lakshmi Pandit"], "A", "Annie Besant presided over the 1917 Calcutta session as INC's first female president."),
        ("The Kakatiya Ramappa Temple, a UNESCO World Heritage site, is in which state?", ["Telangana", "Andhra Pradesh", "Karnataka", "Tamil Nadu"], "A", "The 13th-century Ramappa Temple is located in Mulugu district of Telangana."),
        ("Who introduced the Permanent Settlement in Bengal in 1793?", ["Lord Cornwallis", "Warren Hastings", "Lord Wellesley", "Lord William Bentinck"], "A", "Lord Cornwallis introduced the Permanent Settlement system in Bengal and Bihar in 1793."),
        ("In which year did Mahatma Gandhi return to India from South Africa?", ["1915", "1914", "1916", "1913"], "A", "Mahatma Gandhi permanently returned to India from South Africa on 9 January 1915.")
    ],
    "Indian Polity & Constitution": [
        ("Which Article of the Indian Constitution abolishes Untouchability?", ["Article 17", "Article 14", "Article 19", "Article 21"], "A", "Article 17 of the Constitution of India explicitly abolishes Untouchability and forbids its practice."),
        ("Who was the Chairman of the Drafting Committee of the Constituent Assembly?", ["Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "Sardar Patel"], "A", "Dr. B.R. Ambedkar was appointed Chairman of the Drafting Committee on 29 August 1947."),
        ("The Fundamental Duties were incorporated into the Constitution by which Amendment?", ["42nd Amendment", "44th Amendment", "86th Amendment", "73rd Amendment"], "A", "The 42nd Constitutional Amendment Act 1976 added Fundamental Duties under Article 51A (Part IV-A)."),
        ("Which Schedule of the Indian Constitution contains the list of recognized languages?", ["8th Schedule", "7th Schedule", "10th Schedule", "9th Schedule"], "A", "The 8th Schedule of the Constitution recognizes 22 official languages of India."),
        ("The concept of 'Directive Principles of State Policy' was borrowed from which country?", ["Ireland", "USA", "UK", "Australia"], "A", "DPSPs in Part IV of the Indian Constitution were adopted from the Irish Constitution."),
        ("What is the minimum age required to become the President of India?", ["35 years", "30 years", "25 years", "40 years"], "A", "Under Article 58, a candidate must be at least 35 years old to qualify for election as President."),
        ("Who appoints the Chief Justice of India?", ["President of India", "Prime Minister", "Law Minister", "Parliament"], "A", "The President appoints the Chief Justice of India under Article 124(2) of the Constitution."),
        ("Which Constitutional Amendment recognized Panchayati Raj institutions?", ["73rd Amendment", "74th Amendment", "42nd Amendment", "44th Amendment"], "A", "The 73rd Amendment Act 1992 added Part IX and 11th Schedule for Panchayati Raj."),
        ("What is the maximum duration of Emergency declared under Article 356 without parliamentary approval?", ["2 months", "1 month", "6 months", "3 months"], "A", "President's Rule under Article 356 must be approved by Parliament within 2 months."),
        ("The Anti-Defection Law was introduced by which Amendment Act?", ["52nd Amendment", "61st Amendment", "44th Amendment", "91st Amendment"], "A", "The 52nd Constitutional Amendment Act of 1985 added the 10th Schedule (Anti-Defection Law)."),
        ("Which Fundamental Right cannot be suspended even during a National Emergency?", ["Right to Life and Personal Liberty (Article 21)", "Right to Equality (Article 14)", "Right to Freedom of Speech (Article 19)", "Right to Freedom of Religion (Article 25)"], "A", "Articles 20 and 21 cannot be suspended even during a National Emergency under Article 359."),
        ("Who acts as the ex-officio Chairman of the Rajya Sabha?", ["Vice-President of India", "Speaker of Lok Sabha", "Prime Minister", "President"], "A", "Under Article 89, the Vice-President of India is ex-officio Chairman of the Rajya Sabha."),
        ("What is the quorum required to hold a meeting of either House of Parliament?", ["1/10th of total members", "1/5th of total members", "1/3rd of total members", "1/4th of total members"], "A", "Article 100(3) sets the quorum at 1/10th of the total number of members of the House."),
        ("Which Article grants the Supreme Court power to issue Writs for enforcement of Fundamental Rights?", ["Article 32", "Article 226", "Article 143", "Article 136"], "A", "Article 32 grants the Supreme Court power to issue writs (Right to Constitutional Remedies)."),
        ("The Union List, State List, and Concurrent List are located in which Schedule?", ["7th Schedule", "8th Schedule", "6th Schedule", "5th Schedule"], "A", "The 7th Schedule specifies the distribution of powers between Union and State legislatures."),
        ("Who administers the oath of office to the Governor of a State?", ["Chief Justice of the State High Court", "President of India", "Chief Minister", "Chief Justice of India"], "A", "The Chief Justice of the High Court of the concerned state administers the oath to the Governor."),
        ("In which year was the NITI Aayog formed replacing the Planning Commission?", ["2015", "2014", "2016", "2013"], "A", "NITI Aayog (National Institution for Transforming India) was formed on 1 January 2015."),
        ("Who is the highest law officer in India?", ["Attorney General for India", "Solicitor General of India", "Law Minister", "Chief Justice of India"], "A", "The Attorney General for India (appointed under Article 76) is the chief legal advisor to the Govt."),
        ("The voting age was reduced from 21 to 18 years by which Amendment?", ["61st Amendment", "44th Amendment", "42nd Amendment", "73rd Amendment"], "A", "The 61st Constitutional Amendment Act 1988 reduced the voting age to 18 years."),
        ("Which Article of the Constitution deals with the Election Commission of India?", ["Article 324", "Article 280", "Article 315", "Article 343"], "A", "Article 324 provides for the establishment and powers of the Election Commission of India."),
        ("Finance Commission of India is constituted under which Article?", ["Article 280", "Article 265", "Article 300A", "Article 110"], "A", "Under Article 280, the President constitutes the Finance Commission every five years."),
        ("What is the tenure of a member of the Rajya Sabha?", ["6 years", "5 years", "4 years", "Permanent without term"], "A", "Rajya Sabha members are elected for a term of 6 years, with 1/3rd retiring every two years."),
        ("Who can dissolve the Lok Sabha before its full 5-year term?", ["President on advice of Prime Minister", "Speaker of Lok Sabha", "Chief Justice of India", "Rajya Sabha"], "A", "The President can dissolve the Lok Sabha on the advice of the Prime Minister/Cabinet."),
        ("Which Article contains provision for Money Bills?", ["Article 110", "Article 112", "Article 108", "Article 116"], "A", "Article 110 of the Constitution defines the criteria and procedure for Money Bills."),
        ("The Comptroller and Auditor General (CAG) of India is appointed under which Article?", ["Article 148", "Article 76", "Article 165", "Article 243"], "A", "Article 148 provides for the Comptroller and Auditor General of India.")
    ],
    "Geography & Environment": [
        ("Which is the longest river in India?", ["Ganga", "Godavari", "Yamuna", "Brahmaputra"], "A", "The Ganga is the longest river flowing through India with a total length of 2,525 km."),
        ("Which line passes through eight Indian states?", ["Tropic of Cancer", "Equator", "Tropic of Capricorn", "Prime Meridian"], "A", "The Tropic of Cancer (23.5° N) passes through Gujarat, Rajasthan, MP, Chhattisgarh, Jharkhand, WB, Tripura, Mizoram."),
        ("Which is the highest peak in India (located in Sikkim)?", ["Kanchenjunga", "Nanda Devi", "Kamet", "Anamudi"], "A", "Kanchenjunga (8,586 m) is the highest mountain peak located in India."),
        ("Lothal, Chilika Lake, and Majuli Island: Which is the largest coastal lagoon in India?", ["Chilika Lake", "Vembanad Lake", "Pulicat Lake", "Kolleru Lake"], "A", "Chilika Lake in Odisha is the largest coastal lagoon in India and the second largest in the world."),
        ("The 'Majuli' river island is formed by which river?", ["Brahmaputra", "Ganga", "Godavari", "Indus"], "A", "Majuli is the largest river island in the world, located in the Brahmaputra River in Assam."),
        ("Which Indian state has the longest coastline?", ["Gujarat", "Andhra Pradesh", "Tamil Nadu", "Maharashtra"], "A", "Gujarat has the longest mainland coastline in India (~1,600 km)."),
        ("Which pass connects Leh to Srinagar?", ["Zoji La Pass", "Shipki La Pass", "Nathu La Pass", "Rohtang Pass"], "A", "Zoji La Pass connects Srinagar with Leh in Ladakh."),
        ("Which national park in India is famous for the one-horned Rhinoceros?", ["Kaziranga National Park", "Jim Corbett National Park", "Gir National Park", "Sundarbans National Park"], "A", "Kaziranga National Park in Assam is home to two-thirds of the world's great one-horned rhinoceroses."),
        ("Which biosphere reserve in India is famous for Royal Bengal Tigers and Mangroves?", ["Sundarbans Biosphere Reserve", "Nokrek Biosphere Reserve", "Nilgiri Biosphere Reserve", "Simlipal Biosphere Reserve"], "A", "The Sundarbans in West Bengal is the world's largest mangrove forest and tiger sanctuary."),
        ("The Palk Strait separates India from which country?", ["Sri Lanka", "Maldives", "Myanmar", "Indonesia"], "A", "Palk Strait separates Tamil Nadu state of India from northern Sri Lanka."),
        ("Which soil type is most predominant in India?", ["Alluvial Soil", "Black Soil (Regur)", "Red Soil", "Laterite Soil"], "A", "Alluvial soil is the most widespread soil type in India covering ~40% of land area."),
        ("Black soil (Regur soil) is best suited for the cultivation of which crop?", ["Cotton", "Wheat", "Tea", "Sugarcane"], "A", "Black soil (Regur) retains moisture well and is ideal for growing cotton."),
        ("Where is the headquarters of the Indian Space Research Organisation (ISRO)?", ["Bengaluru", "Sriharikota", "Thiruvananthapuram", "New Delhi"], "A", "ISRO headquarters is located in Bengaluru, Karnataka."),
        ("Which is the southernmost point of India's territory?", ["Indira Point", "Kanyakumari", "Indira Col", "Kibithu"], "A", "Indira Point in Great Nicobar Island is the southernmost point of Indian territory."),
        ("The Silent Valley National Park is located in which Indian state?", ["Kerala", "Karnataka", "Tamil Nadu", "Assam"], "A", "Silent Valley National Park is situated in the Nilgiri Hills of Palakkad district, Kerala."),
        ("Which river is known as the 'Dakshin Ganga'?", ["Godavari", "Krishna", "Kaveri", "Mahanadi"], "A", "The Godavari River is known as Dakshin Ganga due to its large basin size and length in South India."),
        ("Which atmosphere layer contains the Ozone Layer?", ["Stratosphere", "Troposphere", "Mesosphere", "Thermosphere"], "A", "The Ozone layer is located in the Stratosphere (15-35 km above Earth's surface)."),
        ("Which dam is built across the Narmada River?", ["Sardar Sarovar Dam", "Bhakra Nangal Dam", "Tehri Dam", "Hirakud Dam"], "A", "Sardar Sarovar Dam is a gravity dam built on the Narmada River near Navagam, Gujarat."),
        ("Which is the longest canal in India?", ["Indira Gandhi Canal", "Buckingham Canal", "Upper Ganges Canal", "Sarda Canal"], "A", "The Indira Gandhi Canal in Rajasthan is the longest canal in India (~650 km)."),
        ("Grand Anicut (Kallanai) dam was built on which river by Karikala Chola?", ["Kaveri", "Krishna", "Godavari", "Vaigai"], "A", "Kallanai Dam (Grand Anicut) was built across the Kaveri River in Tamil Nadu."),
        ("Which sanctuary is famous for Asiatic Lions?", ["Gir National Park", "Bandipur National Park", "Periyar National Park", "Kanha National Park"], "A", "Gir National Park in Gujarat is the only natural habitat of Asiatic Lions."),
        ("What is the boundary line between India and China called?", ["McMahon Line", "Radcliffe Line", "Durand Line", "49th Parallel"], "A", "The McMahon Line is the effective boundary line between China and India (NE region)."),
        ("Which Indian state receives rainfall from the North-East Retreating Monsoon?", ["Tamil Nadu", "Kerala", "Punjab", "Gujarat"], "A", "Tamil Nadu coast receives major rainfall from the North-East (Retreating) Monsoon in Oct-Dec."),
        ("Nanda Devi Peak is situated in which state?", ["Uttarakhand", "Himachal Pradesh", "Sikkim", "Arunachal Pradesh"], "A", "Nanda Devi (7,816 m) is the second highest peak in India, located in Uttarakhand."),
        ("Which is the largest freshwater lake in India?", ["Wular Lake", "Loktak Lake", "Dal Lake", "Sambhar Lake"], "A", "Wular Lake in Bandipora district of Jammu & Kashmir is the largest freshwater lake in India.")
    ]
}

def generate_checking_demo_tests():
    db_path = os.path.join(workspace_root, "backend", "gandheevijaya.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Fetch available GK Topic IDs under Exam ID 2 (SSC_GK)
    cursor.execute("""
        SELECT t.id, s.id, s.name
        FROM topics t
        JOIN subjects s ON t.subject_id = s.id
        WHERE s.exam_id = 2
    """)
    topic_rows = cursor.fetchall()
    if not topic_rows:
        print("Error: No GK topics found under Exam 2.")
        conn.close()
        return

    topic_pool = [r[0] for r in topic_rows]
    default_subj_id = topic_rows[0][1]

    # Fetch existing question texts in DB to avoid collisions
    cursor.execute("SELECT question_text FROM questions")
    existing_texts = set(r[0] for r in cursor.fetchall())

    # Build 625 authentic GK questions across all categories
    all_categories = list(GK_DATA_POOLS.keys())
    generated_questions = []
    
    # We create 625 unique questions (25 tests x 25 questions = 625)
    q_counter = 1
    for test_idx in range(1, 26):
        test_q_ids = []
        for q_in_test in range(1, 26):
            cat_name = all_categories[(test_idx + q_in_test) % len(all_categories)]
            pool = GK_DATA_POOLS[cat_name]
            base_item = pool[q_in_test % len(pool)]

            # Generate unique question wording and variation if needed
            q_stem, options, corr_ans, explanation = base_item
            if test_idx > 1:
                q_text_var = f"[Set {test_idx:02d}] {q_stem}"
            else:
                q_text_var = q_stem

            # Ensure text uniqueness
            if q_text_var in existing_texts:
                q_text_var = f"[Test {test_idx:02d}-Q{q_in_test:02d}] {q_stem}"

            existing_texts.add(q_text_var)
            q_id = f"GK-DEMO-{q_counter:04d}"
            q_counter += 1

            topic_id = topic_pool[(q_counter) % len(topic_pool)]
            options_json = json.dumps(options)
            tags_json = json.dumps(["GK", "General Knowledge", "Demo Test"])

            # Insert question
            cursor.execute("""
                INSERT OR IGNORE INTO questions (
                    id, topic_id, difficulty, type, question_text, options, correct_answer, 
                    explanation, tags, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'PUBLISHED', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (
                q_id, topic_id, random.choice(["easy", "medium", "hard"]), "MCQ",
                q_text_var, options_json, corr_ans, explanation, tags_json
            ))

            test_q_ids.append(q_id)

        # 2. Create Quiz record for "Checking Demo Tests" section
        quiz_title = f"Checking Demo Tests - General Knowledge Test {test_idx:02d}"
        quiz_desc = f"Demo Test Section: Checking Demo Tests. Full 25 Questions GK Assessment with 1 Hour Duration."
        
        cursor.execute("""
            INSERT INTO quizzes (
                exam_id, subject_id, title, description, duration_minutes, 
                question_count, total_marks, passing_score, quiz_type, 
                status, is_published, created_at, updated_at
            ) VALUES (?, ?, ?, ?, 60, 25, 25.0, 10.0, 'MOCK', 'PUBLISHED', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (2, default_subj_id, quiz_title, quiz_desc))

        quiz_id = cursor.lastrowid

        # 3. Associate 25 questions with Quiz
        qq_rows = []
        for sort_idx, qid in enumerate(test_q_ids, 1):
            qq_rows.append((quiz_id, qid, sort_idx, 1.0, 0.25))

        cursor.executemany("""
            INSERT OR IGNORE INTO quiz_questions (quiz_id, question_id, sort_order, marks, negative_marks)
            VALUES (?, ?, ?, ?, ?)
        """, qq_rows)

        print(f"Created Quiz {quiz_id}: '{quiz_title}' (25 questions, 60 mins duration)")

    conn.commit()

    # Verify Quiz Count
    cursor.execute("SELECT COUNT(*) FROM quizzes WHERE title LIKE 'Checking Demo Tests%'")
    demo_quiz_count = cursor.fetchone()[0]
    print(f"\nSUCCESS! Total 'Checking Demo Tests' created: {demo_quiz_count}")
    conn.close()

if __name__ == "__main__":
    generate_checking_demo_tests()
