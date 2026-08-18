import os
import json
import random

def get_easy_mcq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "Which of the following institutions is known as the banker's banker in India?",
            "options": ["Reserve Bank of India (RBI)", "State Bank of India (SBI)", "NABARD", "Ministry of Finance"],
            "correct": "Reserve Bank of India (RBI)",
            "explanation": "The Reserve Bank of India (RBI) acts as the central bank and banker's banker in India."
        },
        {
            "question": "Who is the executive head of the Reserve Bank of India (RBI)?",
            "options": ["Governor", "Deputy Governor", "Finance Minister", "Prime Minister"],
            "correct": "Governor",
            "explanation": "The Governor is the chief executive officer of India's central bank, the RBI."
        },
        {
            "question": "Which was the first bank established in India?",
            "options": ["Bank of Hindustan", "State Bank of India", "General Bank of India", "Oudh Commercial Bank"],
            "correct": "Bank of Hindustan",
            "explanation": "The Bank of Hindustan was established in 1770, making it the first bank in India."
        },
        {
            "question": "Which of the following authorities has the sole right to issue currency notes in India (except one rupee notes and coins)?",
            "options": ["Reserve Bank of India (RBI)", "Ministry of Finance", "State Bank of India", "Security Printing and Minting Corporation"],
            "correct": "Reserve Bank of India (RBI)",
            "explanation": "Under Section 22 of the RBI Act, the Reserve Bank of India has the sole right to issue currency notes of all denominations except one-rupee notes and coins, which are issued by the Ministry of Finance."
        },
        {
            "question": "The Banking Ombudsman Scheme in India is appointed and run by which organization?",
            "options": ["Reserve Bank of India (RBI)", "Indian Banks' Association (IBA)", "Ministry of Finance", "SEBI"],
            "correct": "Reserve Bank of India (RBI)",
            "explanation": "The Banking Ombudsman is a senior official appointed by the Reserve Bank of India to redress customer complaints against deficiency in certain banking services."
        }
    ]
    t = templates[idx % len(templates)]
    options = t["options"][:]
    correct = t["correct"]
    random.seed(idx)
    random.shuffle(options)
    correct_letter = chr(65 + options.index(correct))
    
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Central Banking", "subtopic": None,
            "difficulty": "easy", "type": "MCQ", "question": t["question"], "options": options,
            "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": correct_letter},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_easy_msq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "Which of the following are public sector banks in India?",
            "options": ["State Bank of India", "Punjab National Bank", "Bank of Baroda", "ICICI Bank"],
            "correct": ["A", "B", "C"],
            "explanation": "State Bank of India, Punjab National Bank, and Bank of Baroda are public sector banks owned by the government. ICICI Bank is a private sector bank."
        },
        {
            "question": "Which of the following are recognized as money market instruments in India?",
            "options": ["Treasury Bills", "Commercial Paper", "Certificate of Deposit", "Equity Shares"],
            "correct": ["A", "B", "C"],
            "explanation": "Treasury Bills, Commercial Papers, and Certificates of Deposit are short-term debt instruments in the money market. Equity shares are capital market instruments."
        },
        {
            "question": "Which of the following are qualitative (selective) credit control measures used by the RBI?",
            "options": ["Fixing margin requirements", "Consumer credit regulation", "Moral suasion", "Cash Reserve Ratio (CRR)"],
            "correct": ["A", "B", "C"],
            "explanation": "Margin requirements, consumer credit regulation, and moral suasion are qualitative/selective credit controls. CRR is a quantitative credit control tool."
        },
        {
            "question": "Which of the following are core functions of the Reserve Bank of India (RBI)?",
            "options": ["Issuer of currency", "Regulator and supervisor of the financial system", "Manager of foreign exchange", "Determining personal income tax rates"],
            "correct": ["A", "B", "C"],
            "explanation": "RBI issues currency, regulates the financial system, and manages foreign exchange. Personal income tax rates are determined by the Central Government/Ministry of Finance."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Banking Structure", "subtopic": None,
            "difficulty": "easy", "type": "MSQ", "question": t["question"], "options": t["options"],
            "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": json.dumps(t["correct"])},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_easy_nat(idx, q_id, sub_upper):
    templates = [
        {
            "question": "What is the total number of characters (alphanumeric) in an Indian Financial System Code (IFSC)?",
            "ans": "11",
            "explanation": "An IFSC is an 11-character alphanumeric code. The first four characters represent the bank, the fifth character is 0, and the last six characters represent the specific branch."
        },
        {
            "question": "What is the number of characters in a Permanent Account Number (PAN) card?",
            "ans": "10",
            "explanation": "A PAN card contains a 10-digit unique alphanumeric identifier."
        },
        {
            "question": "How many digits are in a unique Aadhaar card number issued by UIDAI?",
            "ans": "12",
            "explanation": "An Aadhaar card number consists of 12 digits."
        },
        {
            "question": "What is the number of digits in a standard cheque number printed at the bottom of a cheque leaf?",
            "ans": "6",
            "explanation": "The cheque number is represented by a 6-digit sequence printed at the bottom of the cheque."
        },
        {
            "question": "How many digits are in a Magnetic Ink Character Recognition (MICR) code printed on a cheque?",
            "ans": "9",
            "explanation": "An MICR code consists of 9 digits (first 3 represent city, next 3 represent bank, last 3 represent branch)."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Banking Codes", "subtopic": None,
            "difficulty": "easy", "type": "NAT", "question": t["question"], "options": None,
            "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["code formatting"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": t["ans"]},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_medium_mcq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "What is the minimum transaction amount required to initiate an RTGS (Real Time Gross Settlement) transfer in India?",
            "options": ["2 Lakh INR", "1 Lakh INR", "5 Lakh INR", "No minimum limit"],
            "correct": "2 Lakh INR",
            "explanation": "RTGS is meant for large-value transactions. The minimum transaction limit is 2 Lakh INR."
        },
        {
            "question": "Which of the following rates is defined as the interest rate at which the RBI lends money to commercial banks for short-term periods against collateral?",
            "options": ["Repo Rate", "Reverse Repo Rate", "Bank Rate", "MSF Rate"],
            "correct": "Repo Rate",
            "explanation": "Repo Rate is the rate at which the RBI lends short-term money to commercial banks against government securities."
        },
        {
            "question": "What is the maximum age limit for a subscriber to join the Atal Pension Yojana (APY)?",
            "options": ["40 years", "35 years", "45 years", "60 years"],
            "correct": "40 years",
            "explanation": "The Atal Pension Yojana is open to all Indian citizens aged between 18 and 40 years."
        },
        {
            "question": "Under the Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY), what is the life insurance cover amount provided to the subscriber?",
            "options": ["2 Lakh INR", "1 Lakh INR", "5 Lakh INR", "50,000 INR"],
            "correct": "2 Lakh INR",
            "explanation": "PMJJBY offers a life cover of 2 Lakh INR in case of death of the insured due to any reason."
        },
        {
            "question": "Where is the head office of the National Bank for Agriculture and Rural Development (NABARD) located?",
            "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
            "correct": "Mumbai",
            "explanation": "NABARD's headquarters is located in Mumbai, Maharashtra."
        }
    ]
    t = templates[idx % len(templates)]
    options = t["options"][:]
    correct = t["correct"]
    random.seed(idx)
    random.shuffle(options)
    correct_letter = chr(65 + options.index(correct))
    
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Financial Services", "subtopic": None,
            "difficulty": "medium", "type": "MCQ", "question": t["question"], "options": options,
            "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["regulations lookups"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": correct_letter},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_medium_msq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "Which of the following are quantitative credit control tools used by the RBI?",
            "options": ["Cash Reserve Ratio (CRR)", "Statutory Liquidity Ratio (SLR)", "Repo Rate", "Moral Suasion"],
            "correct": ["A", "B", "C"],
            "explanation": "CRR, SLR, and Repo Rate are quantitative tools that directly alter money supply. Moral Suasion is a qualitative tool."
        },
        {
            "question": "Which of the following benefits are provided under the Pradhan Mantri Jan Dhan Yojana (PMJDY)?",
            "options": ["Accidental Insurance Cover of 2 Lakh INR", "Life Insurance Cover of 30,000 INR", "Overdraft facility up to 10,000 INR", "Free Credit Card with 50,000 INR limit"],
            "correct": ["A", "B", "C"],
            "explanation": "PMJDY accounts provide accidental cover, life cover, and overdraft facility. They do not offer a free credit card."
        },
        {
            "question": "Which of the following are types of cheques based on crossing and payment modes?",
            "options": ["Bearer Cheque", "Order Cheque", "Crossed Cheque", "Bond Cheque"],
            "correct": ["A", "B", "C"],
            "explanation": "Bearer, Order, and Crossed are standard types of cheques. 'Bond Cheque' is not a recognized category of cheques."
        },
        {
            "question": "Which of the following are recognized as Negotiable Instruments under the Negotiable Instruments Act, 1881?",
            "options": ["Promissory Note", "Bill of Exchange", "Cheque", "Share Certificate"],
            "correct": ["A", "B", "C"],
            "explanation": "The NI Act, 1881 recognizes Promissory Notes, Bills of Exchange, and Cheques as negotiable instruments. Share certificates are not negotiable instruments under this act."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Banking Schemes", "subtopic": None,
            "difficulty": "medium", "type": "MSQ", "question": t["question"], "options": t["options"],
            "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": json.dumps(t["correct"])},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_medium_nat(idx, q_id, sub_upper):
    templates = [
        {
            "question": "What is the maximum overdraft limit (in INR) available to eligible account holders under the Pradhan Mantri Jan Dhan Yojana (PMJDY)?",
            "ans": "10000",
            "explanation": "The maximum overdraft limit under PMJDY has been revised to 10,000 INR."
        },
        {
            "question": "What is the minimum entry age (in years) for a subscriber to join the Atal Pension Yojana (APY)?",
            "ans": "18",
            "explanation": "The minimum entry age for APY is 18 years."
        },
        {
            "question": "What is the maximum entry age (in years) to subscribe to the Atal Pension Yojana (APY)?",
            "ans": "40",
            "explanation": "The maximum entry age for APY is 40 years."
        },
        {
            "question": "According to RBI guidelines, what is the validity period (in months) of a cheque or bank draft from its date of issue?",
            "ans": "3",
            "explanation": "Cheques, bank drafts, and pay orders are valid for 3 months from the date of issue."
        },
        {
            "question": "What is the total number of digits in a standard debit card number issued by payment systems like Visa or Mastercard?",
            "ans": "16",
            "explanation": "Standard payment cards have a 16-digit Primary Account Number (PAN) printed on them."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Financial Parameters", "subtopic": None,
            "difficulty": "medium", "type": "NAT", "question": t["question"], "options": None,
            "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["limit check"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": t["ans"]},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_hard_mcq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "Which of the following acts provides the Reserve Bank of India with the power to license and regulate commercial banks in India?",
            "options": ["Banking Regulation Act, 1949", "Reserve Bank of India Act, 1934", "Negotiable Instruments Act, 1881", "Companies Act, 2013"],
            "correct": "Banking Regulation Act, 1949",
            "explanation": "The Banking Regulation Act, 1949 provides the regulatory framework and licensing powers to the RBI over commercial banks."
        },
        {
            "question": "An asset (loan account) is classified as a Non-Performing Asset (NPA) if interest or installment of principal remains overdue for a period exceeding:",
            "options": ["90 days", "180 days", "30 days", "60 days"],
            "correct": "90 days",
            "explanation": "Under RBI guidelines, a loan account is classified as an NPA if interest and/or principal installment remains overdue for more than 90 days."
        },
        {
            "question": "What is the minimum Capital to Risk-Weighted Assets Ratio (CRAR) that commercial banks in India are required to maintain under Basel III guidelines (excluding capital conservation buffers)?",
            "options": ["9%", "8%", "11.5%", "12%"],
            "correct": "9%",
            "explanation": "RBI requires commercial banks to maintain a minimum CRAR of 9% (excluding buffers), which is 1% higher than the Basel minimum of 8%."
        },
        {
            "question": "In which year was the SARFAESI (Securitization and Reconstruction of Financial Assets and Enforcement of Security Interest) Act enacted to help banks recover bad loans?",
            "options": ["2002", "2000", "2005", "2013"],
            "correct": "2002",
            "explanation": "The SARFAESI Act was enacted in 2002 to allow banks to auction residential or commercial properties of defaulters to recover loans."
        },
        {
            "question": "Which organization is a wholly-owned subsidiary of the Reserve Bank of India (RBI) and provides deposit insurance to bank account holders?",
            "options": ["DICGC", "NABARD", "NHB", "SIDBI"],
            "correct": "DICGC",
            "explanation": "The Deposit Insurance and Credit Guarantee Corporation (DICGC) is a wholly-owned subsidiary of the RBI."
        }
    ]
    t = templates[idx % len(templates)]
    options = t["options"][:]
    correct = t["correct"]
    random.seed(idx)
    random.shuffle(options)
    correct_letter = chr(65 + options.index(correct))
    
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Banking Regulations", "subtopic": None,
            "difficulty": "hard", "type": "MCQ", "question": t["question"], "options": options,
            "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["regulations lookups"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": correct_letter},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_hard_msq(idx, q_id, sub_upper):
    templates = [
        {
            "question": "Under the Basel III accord, which of the following constitute the three main pillars?",
            "options": ["Minimum Capital Requirements", "Supervisory Review Process", "Market Discipline", "Credit Default Swaps"],
            "correct": ["A", "B", "C"],
            "explanation": "The three pillars of Basel III are Pillar 1 (Minimum Capital), Pillar 2 (Supervisory Review), and Pillar 3 (Market Discipline)."
        },
        {
            "question": "Which of the following are components of Tier 1 Capital for commercial banks under Basel guidelines?",
            "options": ["Common Equity Tier 1 (CET1)", "Additional Tier 1 (AT1) Capital", "Retained Earnings", "Subordinated Debt"],
            "correct": ["A", "B", "C"],
            "explanation": "Common Equity Tier 1 (CET1), Additional Tier 1, and Retained Earnings form Tier 1 Capital. Subordinated debt is part of Tier 2 Capital."
        },
        {
            "question": "Which of the following are registered Credit Rating Agencies in India?",
            "options": ["CRISIL", "ICRA", "CARE", "SEBI"],
            "correct": ["A", "B", "C"],
            "explanation": "CRISIL, ICRA, and CARE are credit rating agencies. SEBI is the market regulator that regulates them."
        },
        {
            "question": "Which of the following are financial instruments associated with the Capital Market?",
            "options": ["Equity Shares", "Debentures", "Preference Shares", "Treasury Bills"],
            "correct": ["A", "B", "C"],
            "explanation": "Shares and debentures are long-term instruments of the Capital Market. Treasury Bills are short-term money market instruments."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Basel Accords", "subtopic": None,
            "difficulty": "hard", "type": "MSQ", "question": t["question"], "options": t["options"],
            "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": json.dumps(t["correct"])},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def get_hard_nat(idx, q_id, sub_upper):
    templates = [
        {
            "question": "According to RBI guidelines, a loan account is classified as a Non-Performing Asset (NPA) if interest or principal remains overdue for more than how many days?",
            "ans": "90",
            "explanation": "An account is classified as NPA if the amount is overdue for more than 90 days."
        },
        {
            "question": "What is the maximum number of characters in a Society for Worldwide Interbank Financial Telecommunication (SWIFT) code used for international bank transfers?",
            "ans": "11",
            "explanation": "A SWIFT code can be either 8 or 11 characters. The maximum length is 11 characters (including branch code)."
        },
        {
            "question": "What is the minimum Capital Adequacy Ratio (in %) that commercial banks in India are required to maintain under RBI regulations?",
            "ans": "9",
            "explanation": "The RBI has mandated a minimum Capital to Risk-Weighted Assets Ratio (CRAR) of 9% for commercial banks."
        },
        {
            "question": "What is the shortest maturity period (in days) for standard short-term Treasury Bills issued by the Government of India?",
            "ans": "91",
            "explanation": "Government of India issues Treasury Bills for three tenors: 91 days, 182 days, and 364 days. The shortest is 91 days."
        },
        {
            "question": "What is the maximum deposit amount (in Lakh INR) insured for a depositor in a bank by the DICGC?",
            "ans": "5",
            "explanation": "Under current guidelines, the Deposit Insurance and Credit Guarantee Corporation (DICGC) insures deposits up to a maximum of 5 Lakh INR per depositor per bank."
        }
    ]
    t = templates[idx % len(templates)]
    return {
        "question": {
            "id": q_id, "subject": sub_upper, "topic": "Financial Ratios", "subtopic": None,
            "difficulty": "hard", "type": "NAT", "question": t["question"], "options": None,
            "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["regulations math"], "representation": ["text"]
        },
        "answer": {"id": q_id, "correct_answer": t["ans"]},
        "solution": {"id": q_id, "explanation": t["explanation"]}
    }

def main():
    base_dir = "datasets"
    sub = "ba"
    sub_upper = "BA"
    difficulties = ["easy", "medium", "hard"]
    diff_folders = {"easy": "ej", "medium": "mj", "hard": "hj"}
    
    print("Starting generation of 175 files for Banking Awareness (ba)...")
    
    total_written = 0
    for diff in difficulties:
        diff_f = diff_folders[diff]
        
        # Ensure directories exist
        os.makedirs(os.path.join(base_dir, sub, diff_f, "quesj"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, sub, diff_f, "ansj"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, sub, diff_f, "solnj"), exist_ok=True)
        
        for file_idx in range(1, 176):
            q_file_name = f"{sub}{file_idx:02d}{diff_f[0]}q.json"
            a_file_name = f"{sub}{file_idx:02d}{diff_f[0]}a.json"
            s_file_name = f"{sub}{file_idx:02d}{diff_f[0]}s.json"
            
            questions_list = []
            answers_list = []
            solutions_list = []
            
            for q_type in ["MCQ", "MSQ", "NAT"]:
                q_id = f"GCS27-{sub_upper}-{diff[0].upper()}-{q_type}-{file_idx:03d}"
                
                question_data = None
                if diff == "easy":
                    if q_type == "MCQ":
                        question_data = get_easy_mcq(file_idx, q_id, sub_upper)
                    elif q_type == "MSQ":
                        question_data = get_easy_msq(file_idx, q_id, sub_upper)
                    elif q_type == "NAT":
                        question_data = get_easy_nat(file_idx, q_id, sub_upper)
                elif diff == "medium":
                    if q_type == "MCQ":
                        question_data = get_medium_mcq(file_idx, q_id, sub_upper)
                    elif q_type == "MSQ":
                        question_data = get_medium_msq(file_idx, q_id, sub_upper)
                    elif q_type == "NAT":
                        question_data = get_medium_nat(file_idx, q_id, sub_upper)
                elif diff == "hard":
                    if q_type == "MCQ":
                        question_data = get_hard_mcq(file_idx, q_id, sub_upper)
                    elif q_type == "MSQ":
                        question_data = get_hard_msq(file_idx, q_id, sub_upper)
                    elif q_type == "NAT":
                        question_data = get_hard_nat(file_idx, q_id, sub_upper)
                
                if question_data:
                    questions_list.append(question_data["question"])
                    answers_list.append(question_data["answer"])
                    solutions_list.append(question_data["solution"])
            
            # Write files
            with open(os.path.join(base_dir, sub, diff_f, "quesj", q_file_name), 'w', encoding='utf-8') as f:
                json.dump(questions_list, f, indent=2)
            with open(os.path.join(base_dir, sub, diff_f, "ansj", a_file_name), 'w', encoding='utf-8') as f:
                json.dump(answers_list, f, indent=2)
            with open(os.path.join(base_dir, sub, diff_f, "solnj", s_file_name), 'w', encoding='utf-8') as f:
                json.dump(solutions_list, f, indent=2)
            
            total_written += 3
            
    print(f"Successfully generated {total_written} JSON files.")

if __name__ == "__main__":
    main()
