-- Database schema for GATE Question Generation Engine

-- Table to store syllabus concepts
CREATE TABLE IF NOT EXISTS syllabus_concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_code TEXT NOT NULL,
    chapter_name TEXT NOT NULL,
    topic_name TEXT NOT NULL,
    concept_name TEXT NOT NULL
);

-- Table to store abstract RAG patterns
CREATE TABLE IF NOT EXISTS abstract_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT,
    concept TEXT NOT NULL,
    archetype TEXT NOT NULL,
    reasoning_type TEXT NOT NULL,
    required_knowledge TEXT,
    reasoning_steps INTEGER,
    pattern_text TEXT NOT NULL
);

-- Table to store final and validated questions
CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    chapter TEXT NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT,
    concept TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    type TEXT NOT NULL,
    question TEXT NOT NULL UNIQUE,
    options TEXT, -- JSON array of strings: ["A", "B", "C", "D"] (empty for NAT)
    correct_answer TEXT NOT NULL, -- "A", "B", "C", "D" or JSON array for MSQ or value/range for NAT
    explanation TEXT NOT NULL,
    reasoning_type TEXT, -- JSON array of reasoning tags
    archetype TEXT,
    representation TEXT, -- JSON array of representation formats (e.g. ["code", "table"])
    estimated_reasoning_steps INTEGER,
    originality_score REAL,
    quality_score REAL,
    validation_status TEXT DEFAULT 'DRAFT', -- DRAFT, VALIDATED, REJECTED
    generation_timestamp TEXT NOT NULL
);

-- Table to store logs of rejected questions for iterative improvement
CREATE TABLE IF NOT EXISTS rejection_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT,
    subject TEXT,
    difficulty TEXT,
    type TEXT,
    reason TEXT NOT NULL, -- COPY_RISK, AMBIGUITY, ANSWER_ERROR, etc.
    feedback_comment TEXT,
    timestamp TEXT NOT NULL
);

-- Table to store persistent question counts (Ledger)
CREATE TABLE IF NOT EXISTS generation_ledger (
    difficulty TEXT NOT NULL,
    type TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    PRIMARY KEY (difficulty, type)
);

-- Initialize generation ledger targets with 0 count
INSERT OR IGNORE INTO generation_ledger (difficulty, type, count) VALUES
('easy', 'mcq', 0),
('easy', 'msq', 0),
('easy', 'nat', 0),
('medium', 'mcq', 0),
('medium', 'msq', 0),
('medium', 'nat', 0),
('hard', 'mcq', 0),
('hard', 'msq', 0),
('hard', 'nat', 0);
