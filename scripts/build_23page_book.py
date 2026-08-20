import os
import sys

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Custom canvas to implement two-pass page numbering (Page X of Y) and running headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Don't draw running header/footer on cover page (Page 1)
        if self._pageNumber > 1:
            # Header
            self.drawString(54, 750, "GANDHEEVIJAYA — MASTER ARCHITECTURE & SYSTEM GUIDE")
            self.drawRightString(558, 750, "Made by Sayan Kundu")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Footer
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 40, page_text)
            self.drawString(54, 40, "Made by Sayan Kundu | Comprehensive Technical & Mindset Textbook Guide")
            self.line(54, 52, 558, 52)
            
        self.restoreState()

def create_23page_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Premium Paragraph Styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=15
    )

    cover_subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=25
    )

    author_style = ParagraphStyle(
        'AuthorStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2B6CB0"),
        alignment=1,
        spaceAfter=30
    )

    page_heading_style = ParagraphStyle(
        'PageHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=0,
        spaceAfter=10
    )

    sub_heading_style = ParagraphStyle(
        'SubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BookBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=10
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#1A202C"),
        backColor=colors.HexColor("#EDF2F7"),
        borderColor=colors.HexColor("#CBD5E0"),
        borderWidth=0.5,
        borderPadding=10,
        spaceBefore=8,
        spaceAfter=10
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 1.0 * inch))
    story.append(Paragraph("THE ULTIMATE SYSTEM ARCHITECTURE", cover_subtitle_style))
    story.append(Paragraph("GANDHEEVIJAYA", cover_title_style))
    story.append(Paragraph("A Master Class in Multi-Exam Assessment, Modular Monolith Engineering, Relational Data Hydraulics & Cognitive Mindset Architecture", cover_subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#3182CE"), spaceBefore=10, spaceAfter=20))
    story.append(Paragraph("Made by Sayan Kundu", author_style))
    story.append(Spacer(1, 0.4 * inch))

    overview_box = (
        "<b>EXECUTIVE BLUEPRINT OVERVIEW:</b><br/>"
        "Welcome to the master architectural textbook of <b>Gandheevijaya</b>. Designed and engineered by <b>Sayan Kundu</b>, "
        "this platform is a high-precision, production-grade assessment and cognitive resilience engine. Built as a decoupled modular "
        "monolith, it seamlessly integrates a FastAPI asynchronous Python backend, a PostgreSQL relational schema, a React 18 frontend, "
        "and a secular Bhagavad Gita student mindset portal. This 23-page detailed textbook guide deconstructs every mechanical layer of the system "
        "from first principles to absolute mastery, providing total transparency into its design, algorithms, security, and deployment."
    )
    story.append(Paragraph(overview_box, callout_style))
    story.append(Spacer(1, 0.3 * inch))

    # Cover Summary Table
    cover_table_data = [
        ["System Component", "Core Technology", "Operational Role", "Architectural Invariant"],
        ["Backend Service", "FastAPI / Uvicorn", "ASGI Async Event Loop", "Non-blocking I/O execution"],
        ["Relational Storage", "PostgreSQL / SQLAlchemy 2.x", "ACID Compliance & Pooling", "Strict foreign-key integrity"],
        ["Auth & Security", "JWT / Argon2 Hashing", "Stateless Token Rotation", "Zero cleartext secret leaks"],
        ["Frontend UI", "React 18 / Vite / Tailwind", "Virtual DOM & State Management", "Zero-scroll click deck reader"],
        ["Mindset Engine", "Secular Gita Portal", "23 Modules & 18 Chapters", "Working memory stress reset"],
        ["Infrastructure", "Render Cloud / Docker", "Automated Blueprint CI/CD", "Zero-downtime web service"]
    ]
    cover_table = Table(cover_table_data, colWidths=[1.5*inch, 1.7*inch, 1.8*inch, 2.0*inch])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F7FAFC")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#EDF2F7")]),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # Helper function to generate standardized 1-page textbook chapters
    def add_chapter(page_num, title, subtitle, main_text, feynman_analogy, technical_deepdive):
        story.append(Paragraph(f"<b>PAGE {page_num} — CHAPTER {page_num - 1}</b>", ParagraphStyle('PageNumHeader', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#718096"), spaceAfter=2)))
        story.append(Paragraph(title, page_heading_style))
        story.append(Paragraph(f"<i>{subtitle}</i>", ParagraphStyle('SubHeadingItalic', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor("#4A5568"), spaceAfter=10)))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=2, spaceAfter=10))

        story.append(Paragraph("<b>1. First-Principles Concept & Overview</b>", sub_heading_style))
        story.append(Paragraph(main_text, body_style))

        story.append(Paragraph("<b>2. The Relatable Mechanical Analogy</b>", sub_heading_style))
        story.append(Paragraph(feynman_analogy, callout_style))

        story.append(Paragraph("<b>3. Deep-Dive Technical Mechanics & System Invariants</b>", sub_heading_style))
        story.append(Paragraph(technical_deepdive, body_style))
        story.append(PageBreak())

    # =========================================================================
    # PAGES 2 TO 23: 22 DEEP TECHNICAL & PHILOSOPHICAL CHAPTERS
    # =========================================================================

    add_chapter(
        2,
        "The Grand Synthesis (System Purpose & Core Vision)",
        "Deconstructing multi-exam assessment, cognitive evaluation, and secular mindset integration.",
        "Imagine trying to build a master assessment platform capable of evaluating thousands of candidates across diverse competitive domains such as engineering, civil services, and banking. Most legacy software treats exam testing as simple text displays and superficial grade counting. Gandheevijaya, conceived and created by Sayan Kundu, re-engineers this paradigm from the ground up. It operates as an integrated dual engine: a high-throughput multi-exam testing platform paired with a secular cognitive resilience portal based on rational philosophy. By decoupling exam delivery from evaluation logic, the system guarantees zero data corruption, sub-millisecond scoring precision, and unshakeable operational reliability.",
        "<b>Feynman Analogy:</b> Imagine a grand central train terminal handling thousands of high-speed passenger trains arriving simultaneously on multiple tracks. If station managers attempt to direct trains by shouting across platforms, chaos ensues. Instead, the terminal uses an automated, electric signaling box where every track switch moves in perfect synchronization. Gandheevijaya is that automated electric signaling box—routing user authentication, question ingestion, quiz generation, and analytics without a single collision.",
        "The system architecture enforces strict separation of concerns through a modular monolith design pattern. The backend leverages asynchronous request handling (`ASGI`), relational table normalization (`PostgreSQL`), and strict input validation schemas (`Pydantic v2`). The frontend consumes these APIs via single-page application (`SPA`) client-side routing (`React Router v6`), ensuring that user state remains perfectly preserved across transitions without full browser page reloads."
    )

    add_chapter(
        3,
        "The Modular Monolith (Architectural Layering)",
        "Isolating domain logic, API routers, service layers, and data repositories for zero coupling.",
        "When building complex enterprise software, developers often face a dilemma: build a messy monolithic blob where everything depends on everything else, or prematurely split into dozens of microservices that introduce network latency and distributed failure modes. Sayan Kundu chose the elegant middle path: the <b>Modular Monolith</b>. In Gandheevijaya, all core domains—Authentication, Content Lifecycle, Assessment Engine, Performance Intelligence, and Mindset Portal—reside in a single unified codebase, but are strictly isolated into distinct architectural layers.",
        "<b>Feynman Analogy:</b> Think of a modern container ship carrying hundreds of sealed steel cargo boxes. Even if heavy ocean waves crash against the hull, water cannot leak from one box into another. If a fruit container develops an issue, it does not affect the machinery container next to it. Similarly, in Gandheevijaya, if the analytics service undergoes a heavy query calculation, the authentication service remains completely untouched and responsive.",
        "The backend enforces a clean 4-tier layer pattern: <b>1. API Routers</b> (handling HTTP request deserialization and CORS middleware), <b>2. Service Layer</b> (encapsulating domain rules and transaction boundaries), <b>3. Repository Layer</b> (abstracting SQLAlchemy 2.x queries), and <b>4. Database Models</b> (defining relational schemas). This strict flow guarantees that API controllers never execute raw SQL statements, maintaining total testability and code isolation."
    )

    add_chapter(
        4,
        "The Gateway Engine (FastAPI, Uvicorn & Asynchronous I/O)",
        "How non-blocking event loops process thousands of concurrent API requests without thread locking.",
        "Traditional web servers operate like old telephone switchboards: for every incoming phone call, a dedicated operator (a OS thread) is locked until the call finishes. If 1,000 calls arrive at once, the server runs out of operators and crashes. Gandheevijaya solves this bottleneck by employing <b>FastAPI</b> powered by the <b>Uvicorn ASGI server</b>. Operating on an asynchronous event loop (`asyncio`), Uvicorn handles thousands of concurrent HTTP requests on a single CPU thread without ever blocking execution during database I/O.",
        "<b>Feynman Analogy:</b> Imagine a master waiter in a busy restaurant. An inefficient waiter takes an order from Table 1, walks into the kitchen, stands still waiting for the chef to cook the steak, and only returns to Table 2 after Table 1 is served. A master waiter takes Table 1's order, hands it to the kitchen instantly, immediately takes orders from Tables 2, 3, and 4, and delivers food the microsecond it is ready. Uvicorn is that master waiter.",
        "When a student submits a test attempt via `POST /api/v1/attempts/{id}/submit`, FastAPI receives the payload, hands the database write operation to the async engine, and instantly returns to process incoming heartbeats from other users. The underlying event loop uses OS-level non-blocking primitives (`epoll` on Linux, `IOCP` on Windows), allowing the system to achieve ultra-low latency (`< 15ms`) under heavy concurrent load."
    )

    add_chapter(
        5,
        "The Relational Vault (PostgreSQL & SQLAlchemy 2.x Schema)",
        "Engineering foreign key constraints, indexes, connection pooling, and ACID database integrity.",
        "At the core of Gandheevijaya lies its relational data vault, structured in <b>PostgreSQL</b> and managed via <b>SQLAlchemy 2.x ORM</b>. Data integrity is the non-negotiable foundation of any serious assessment platform. If a student's answer score or quiz submission is lost due to a database glitch, the system fails. Sayan Kundu designed a normalized database schema comprising 16 interconnected tables, enforcing strict foreign key constraints, cascade rules, and unique index constraints to prevent data duplication.",
        "<b>Feynman Analogy:</b> Picture a bank vault containing thousands of safety deposit boxes. Each box has two distinct locks: one key held by the customer (Primary Key) and one key held by the bank manager (Foreign Key). You cannot place a deposit box in the vault unless the customer account already exists in the master ledger. This ensures no orphan boxes can ever exist.",
        "The database layer implements advanced connection pooling parameters (`pool_size=10`, `max_overflow=20`, `pool_pre_ping=True`, `pool_recycle=1800`). The `pool_pre_ping` mechanism sends a lightweight `SELECT 1` ping before handing a connection to a request, automatically pruning stale or dropped database sockets. To ensure smooth local development, the configuration dynamically falls back to an isolated SQLite file (`gandheevijaya.db`) if PostgreSQL environment variables are absent."
    )

    add_chapter(
        6,
        "The Guard at the Gate (JWT Authentication & Security)",
        "Argon2 password hashing, stateless JSON Web Tokens, refresh token rotation, and RBAC.",
        "Security in Gandheevijaya is engineered with defense-in-depth principles. User authentication relies on stateless **JSON Web Tokens (JWT)** signed with cryptographic algorithms (`HS256`). Passwords are never stored in plain text or using weak legacy hashes like MD5 or SHA1; instead, they are hashed using **Argon2id** (via `passlib`), providing maximum resistance against GPU-accelerated brute-force attacks and rainbow table lookups.",
        "<b>Feynman Analogy:</b> Imagine an exclusive airport lounge that issues biometric digital wristbands. When you check in at the counter with your passport (login credentials), the agent verifies your identity and hands you a sealed wristband containing an encrypted expiration timestamp. Every time you enter a room, the door scanner checks your wristband instantly without calling the front desk. When the wristband expires, you present your long-term renewal card (Refresh Token) to get a fresh wristband.",
        "The authentication workflow uses a dual-token strategy: a short-lived Access Token (valid for 60 minutes) for API request authorization and a long-lived Refresh Token (valid for 7 days) stored in secure database tables (`refresh_tokens`). Role-Based Access Control (**RBAC**) middleware inspects token claims on protected endpoints, enforcing strict permission boundaries between standard `STUDENT` users and `ADMIN` managers."
    )

    add_chapter(
        7,
        "The Pipeline (Content Ingestion & Data Hydraulics)",
        "Extracting, transforming, validating, and loading massive question datasets with zero downtime.",
        "Populating an assessment engine with tens of thousands of complex exam questions requires a robust **ETL (Extract, Transform, Load)** pipeline. Gandheevijaya features automated ingestion scripts (`import_questions.py`, `mass_generator.py`, `final_dataset_generator.py`) capable of parsing raw JSON question banks, validating schema payloads against strict Pydantic structures, and performing idempotent database insertions.",
        "<b>Feynman Analogy:</b> Think of a massive municipal water purification plant. Raw river water (unfiltered raw JSON data) flows into large settling basins. High-powered mesh filters trap mud and debris (schema validation catching missing fields or broken formatting). Chemicals adjust pH balance (normalizing subject and category slugs), and finally, pure clean water is pumped into the city reservoir (PostgreSQL database).",
        "The ETL engine tracks every import batch inside an audit table (`import_audits`). If a JSON payload contains malformed syntax, invalid option arrays, or duplicate question identifiers, the pipeline captures the exact line error, logs it into `import_errors`, rolls back the current atomic transaction, and continues processing valid items—ensuring that ingestion never halts completely due to a single bad data entry."
    )

    add_chapter(
        8,
        "Unmasking Duplicates (Semantic Hashing & Fingerprinting)",
        "Preventing duplicate questions across exam pools using canonical string hashing and SHA-256 fingerprinting.",
        "When aggregating content from multiple academic contributors, duplicate questions inevitably enter the system. Storing identical questions dilutes assessment accuracy and wastes storage. Sayan Kundu implemented a **Semantic Deduplication Engine** (`semantic_deduplication.py`) that generates unique cryptographic fingerprints for every incoming question payload before database insertion.",
        "<b>Feynman Analogy:</b> Imagine a police forensic lab comparing fingerprints collected from different locations. Even if a suspect changes their clothes, wear a hat, or alters their voice (variations in whitespace, punctuation, or option ordering), their physical fingerprint remains identical. The forensic scanner detects the exact match instantly.",
        "The deduplication algorithm strips away formatting noise: it converts question text to lowercase, removes Markdown code fences, strips punctuation, sorts option arrays deterministically, and hashes the normalized string using `SHA-256`. The resulting hash is stored in a indexed database column (`source_fingerprint`). Any attempt to insert a question yielding an existing fingerprint is intercepted immediately with an idempotent skip log."
    )

    add_chapter(
        9,
        "The Assessment Arena (Quiz Engine & State Machines)",
        "Managing timed attempts, question randomization, auto-expiry, and state machine transitions.",
        "The core user experience during testing is governed by the **Assessment Engine**. A quiz attempt is not a static webpage; it is a live state machine moving through strict operational phases: `CREATED` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `SUBMITTED` or `EXPIRED`. The engine enforces precise time limits, preventing students from submitting answers after the allocated duration has elapsed.",
        "<b>Feynman Analogy:</b> Picture a grand master chess tournament. When a player's clock starts, every move is recorded on a official score sheet. If the player attempts to make a move after their clock flag drops (time expired), the arbiter stops the game instantly and locks the board state. No further moves can be made, and the score at the moment of expiry is recorded permanently.",
        "When a student calls `POST /api/v1/quizzes/{id}/start`, the backend creates an attempt record (`attempts`), generates a randomized sequence of question options for that specific user (preventing side-by-side cheating), and sets an explicit `expires_at` timestamp. Server-side middleware constantly checks `expires_at` during response submissions (`POST /responses`), auto-submitting the test if the time boundary is crossed."
    )

    add_chapter(
        10,
        "The Master Scorekeeper (Golden Scoring Engine & Negative Marking)",
        "Algorithmic precision for MCQ, MSQ, and NAT questions with strict fractional penalty enforcement.",
        "Competitive exam scoring demands absolute mathematical precision. Gandheevijaya supports three distinct question archetypes, each governed by specific evaluation rules: **1. Multiple Choice Questions (MCQ)**, **2. Multiple Select Questions (MSQ)**, and **3. Numerical Answer Type (NAT)**. The scoring service (`scoring_service.py`) calculates raw marks, negative penalties, and final scaled percentages with zero rounding distortion.",
        "<b>Feynman Analogy:</b> Imagine an ultra-sensitive gold bullion scale used by mint masters. When weighing a gold coin, the scale does not guess or round up to the nearest gram; it measures down to the exact microgram. If the coin has even a minor scratch or impurity, the scale factors it into the valuation instantly and impartially.",
        "The scoring matrix operates as follows: For **MCQ**, a correct answer awards full marks (e.g., +1.0 or +2.0), while an incorrect selection deducts negative penalty marks (e.g., -0.33 or -0.66). For **MSQ**, ALL correct options must be selected with ZERO wrong options; partial credit is strictly prohibited to mirror official exam standards. For **NAT**, numerical inputs are evaluated against exact floating-point tolerances (`abs(user_input - correct_value) <= tolerance`)."
    )

    add_chapter(
        11,
        "Anti-Tampering & Security Seals (Score & State Protection)",
        "Preventing client-side payload tampering, IDOR vulnerabilities, and concurrent response race conditions.",
        "In high-stakes online testing, dishonest users may attempt to manipulate client-side JavaScript payloads, alter submitted scores, or intercept network traffic to submit answers for other students (**Insecure Direct Object Reference - IDOR**). Gandheevijaya integrates comprehensive security controls to neutralize these attack vectors completely.",
        "<b>Feynman Analogy:</b> Think of a high-security armored transport truck carrying confidential documents between bank branches. The rear doors are sealed with tamper-evident steel bolts, each stamped with a unique serial number (`X-Request-ID` correlation header). If anyone attempts to force open the door or swap packages in transit, the seal breaks, alerting the central command tower instantly.",
        "Security invariants enforced by the system include: **1. Server-Side Score Calculation**: The frontend NEVER calculates or sends scores; it only submits raw answer selections. The backend evaluates scores against database ground truth. **2. User Ownership Locking**: Every route verifies that `attempt.user_id == current_user.id`. **3. Optimistic Locking**: Prevents race conditions during rapid concurrent click submissions."
    )

    add_chapter(
        12,
        "The Mindset Engine (Bhagavad Gita Student Portal)",
        "Synthesizing ancient rational philosophy with modern cognitive science for student anxiety resilience.",
        "Engineering excellence extends beyond technical code into human psychology. Sayan Kundu realized that even the best-prepared candidates often fail due to acute performance anxiety, panic attacks, and overthinking during high-stakes exams. To solve this human bottleneck, Gandheevijaya incorporates a dedicated **Bhagavad Gita Student Mindset Portal**—a secular, realist synthesis of the 18 chapters and 23 student-focused modules.",
        "<b>Feynman Analogy:</b> Imagine a world-class fighter jet equipped with powerful jet engines, advanced radar, and titanium wings. However, if the pilot inside experiences severe dizziness or vertigo during a high-speed maneuver, the plane cannot fulfill its mission. The Gita Student Portal acts as the pilot's internal gyroscope—restoring instant balance, orientation, and focus under intense pressure.",
        "The portal reframes ancient philosophical texts into actionable cognitive tools. It strips away religious dogma, presenting the Gita as a secular operating system for decision-making under uncertainty. It teaches students 14 core competencies, including **Anxiety Management**, **Result Detachment (Tyaga)**, **Process Orientation**, **Metacognition**, and **Emotional Equanimity (Sthitaprajna)**."
    )

    add_chapter(
        13,
        "Cognitive Mechanics (Working Memory & Stress Resets)",
        "Managing prefrontal cortex load, vagus nerve breathing, and present execution flow state.",
        "Why do students experience sudden mental blanking during exams? Cognitive science proves that human **Working Memory** operates like a short-term RAM buffer with strictly limited capacity (holding roughly 4 to 7 items). When a student panics about exam ranks or failure consequences, catastrophic negative thoughts flood the working memory buffer. This leaves zero RAM available for solving the actual equation, causing immediate processing failure.",
        "<b>Feynman Analogy:</b> Think of a computer trying to run a complex 3D simulation game while 50 background virus programs are consuming 99% of CPU RAM. The game stutters, freezes, and eventually crashes. You do not need a faster computer; you simply need to kill the background virus processes. Outcome anxiety is that background virus process.",
        "The Mindset Portal teaches practical physical hacks to clear the RAM buffer instantly: **1. Vagus Nerve Reset**: Slow, controlled belly exhales stimulate the parasympathetic nervous system, lowering heart rate and signaling safety to the brain. **2. Tyaga Protocol**: Releasing attachment to future test scores frees up 100% of working memory bandwidth for present microsecond problem-solving."
    )

    add_chapter(
        14,
        "The User Experience (React 18, Vite & Component Architecture)",
        "Building a high-performance, modular UI with virtual DOM efficiency and component reuse.",
        "The frontend of Gandheevijaya is crafted with **React 18** and bundled using **Vite**. The UI is built as a modular hierarchy of reusable UI components (`Card`, `Badge`, `Button`, `AppShell`), ensuring uniform visual aesthetics, zero layout shifts, and instantaneous user interactions.",
        "<b>Feynman Analogy:</b> Imagine an advanced aircraft cockpit dashboard where every instrument dial, toggle switch, and multi-function display is modularly mounted on a standardized bus. If you flip a toggle switch on the left panel, only that specific indicator light updates instantly without causing the main navigation screen to flicker or reset.",
        "React 18's **Virtual DOM** diffing engine ensures that when a user selects an answer option in a quiz or switches between Gita slides, only the specific modified DOM nodes are re-rendered in the browser. Vite's Native ES Modules (`ESM`) dev server delivers lightning-fast Instant Module Replacement (`HMR`), compiling changes in milliseconds during development."
    )

    add_chapter(
        15,
        "Flow Control & Routing (React Router & SPA State Management)",
        "Managing client-side route transitions, persistent local storage, and zero-page-reload navigation.",
        "Navigating between different sections of a large web application—such as switching from the Admin Dashboard to a Live Quiz Attempt or the Gita Portal—should feel instantaneous. Traditional multi-page websites force the browser to discard the current page, request a new HTML document from the server, and rebuild the page from scratch. Gandheevijaya utilizes **React Router v6** to deliver a seamless **Single Page Application (SPA)** experience.",
        "<b>Feynman Analogy:</b> Picture a high-speed monorail train running on a single continuous track inside a futuristic dome. When passengers move from the terminal building to the observation deck, the train doesn't dismantle itself and rebuild at the destination; it glides smoothly along the track while passengers remain comfortably seated inside.",
        "Client-side routing intercepts URL changes (e.g., `/gita`, `/quizzes`, `/dashboard`) entirely within JavaScript. Application state—such as active quiz timer counts, user preferences, and active slide indexes—is synchronized with `localStorage`, ensuring that even if a student accidentally refreshes their browser during an exam, their session resumes seamlessly without data loss."
    )

    add_chapter(
        16,
        "The Visual Lens (Tailwind CSS, Glassmorphism & Aesthetics)",
        "Crafting a dark-mode UI with harmonious color palettes, micro-animations, and responsive design.",
        "Visual design directly influences cognitive fatigue and user engagement. Sayan Kundu designed Gandheevijaya with a custom visual system built on **Tailwind CSS**. Moving away from generic browser defaults, the platform employs a curated dark-mode theme utilizing deep slate blues, glowing amber accents, rich emerald highlights, and subtle glassmorphic translucent panels.",
        "<b>Feynman Analogy:</b> Think of a luxury high-end observatory telescope room. The room lighting is dimmed to a deep soft indigo so that your eyes adapt perfectly to night vision. The control dials glow softly in warm amber and emerald colors, allowing astronomers to work for ten consecutive hours without eye strain or headache.",
        "Tailwind CSS utility classes enable precise layout control with zero CSS bundle bloat. Interactivity is enhanced with subtle CSS micro-animations (`hover:scale-105`, `transition-all duration-200`, `animate-in fade-in`), providing instant visual feedback when buttons are clicked or tabs are selected. Responsive flex and grid utility layouts guarantee flawless rendering across desktop monitors, laptops, and mobile screens."
    )

    add_chapter(
        17,
        "Performance Analytics (Student Dashboards & Progress Diagnostics)",
        "Translating raw assessment responses into actionable cognitive quadrant profiles and accuracy trends.",
        "Taking mock exams is useless unless the student receives clear, actionable feedback on their performance. The Analytics module in Gandheevijaya (`analytics_service.py`, `PerformanceQuadrant`) processes historical test attempts to generate comprehensive diagnostic profiles for every student.",
        "<b>Feynman Analogy:</b> Imagine a sports physician using a high-tech motion capture suit to analyze a sprinter's stride. The suit doesn't just tell the runner 'you were fast' or 'you were slow'; it measures exact ground impact force, knee flexion angle, and torso tilt. It pinpoints precisely which muscle group is fatiguing on the final 50 meters.",
        "The analytics engine evaluates performance across multiple dimensions: **1. Overall Accuracy Percentage**, **2. Category Breakdown** (GATE CS, SSC CGL, SBI PO), **3. Topic-Level Strengths & Weaknesses**, and **4. Speed vs. Accuracy Trade-off Ratio**. Students are categorized into four performance quadrants (e.g., *High Speed / High Accuracy = Master*, *Low Speed / High Accuracy = Perfectionist*, *High Speed / Low Accuracy = Rushed*, *Low Speed / Low Accuracy = Novice*), guiding their study focus."
    )

    add_chapter(
        18,
        "The Intelligence Layer (Item Analysis & Distractor Diagnostics)",
        "Evaluating question quality, discrimination index, and distractor effectiveness using psychometrics.",
        "How do test designers know if an exam question is fair, well-calibrated, or flawed? Gandheevijaya incorporates an **Item Analysis Engine** (`intelligence_service.py`) rooted in classical test theory and psychometrics. It continuously evaluates question quality based on student performance data.",
        "<b>Feynman Analogy:</b> Think of a master lock manufacturer testing new key designs. They don't just check if the key opens the lock once; they test it against 10,000 lock picks, master keys, and tension wrenches. If a key lock opens when bumped accidentally by a paperclip, the lock design is defective and must be recalled.",
        "The intelligence engine computes two key psychometric metrics for every question: **1. Difficulty Index (p-value)**: The proportion of candidates answering correctly. **2. Discrimination Index (d-index)**: The ability of the question to distinguish between high-performing top 27% candidates and lower-performing bottom 27% candidates. Distractor options that receive zero selections are flagged for revision."
    )

    add_chapter(
        19,
        "The Command Center (Admin Suite, Audit Logs & Content Management)",
        "Empowering administrators with real-time platform overview, user management, and system monitoring.",
        "Managing an enterprise educational ecosystem requires powerful administrative oversight. The **Admin Suite** (`admin_service.py`, `AdminDashboardPage.tsx`) provides authorized personnel with a comprehensive management console for user roles, exam taxonomies, question pools, and security audit trails.",
        "<b>Feynman Analogy:</b> Picture the main control tower at a major international airport. Air traffic controllers sit in front of panoramic radar screens tracking every inbound and outbound aircraft, monitoring runway clear statuses, weather fronts, and fuel levels across the entire airspace from one central desk.",
        "Key capabilities of the Admin Suite include: **1. Real-Time System Metrics**: Total registered users, active quiz attempts, total ingested questions, and server uptime health. **2. User Management**: Searching, role upgrading, password resets, and account suspension. **3. Content Lifecycle Control**: Transitioning questions from `DRAFT` $\rightarrow$ `REVIEW` $\rightarrow$ `VALIDATED` $\rightarrow$ `ARCHIVED`. **4. Security Audit Logs**: Inspecting login IP records and failed authentication attempts."
    )

    add_chapter(
        20,
        "The Quality Shield (Automated Pytest & Vitest Suites)",
        "Ensuring complete system reliability through automated unit, integration, and security testing.",
        "How can Sayan Kundu guarantee that a modification in the database schema or scoring calculation doesn't break user authentication or test submissions? The answer lies in **Rigorous Automated Testing**. Gandheevijaya maintains an extensive automated test suite built with **Pytest** for the backend and **Vitest** for the frontend.",
        "<b>Feynman Analogy:</b> Imagine an automobile factory where every newly manufactured car is driven onto a automated test track before leaving the building. Mechanical rollers test high-speed braking, water cannons test door seals against leaks, and robotic arms shake the chassis to verify bolt torque. Only cars that pass every single test track milestone are cleared for delivery.",
        "The backend test suite contains **82 comprehensive automated test modules**, covering: **1. Golden Scoring Matrix Tests**, **2. Anti-Tampering & IDOR Security Tests**, **3. JWT Authentication & Token Rotation Tests**, **4. Concurrency & Race Condition Lock Tests**, and **5. Database ETL Idempotency Tests**. All 82 tests execute in under 30 seconds with a 100% pass rate."
    )

    add_chapter(
        21,
        "The Cloud Launchpad (Render Deployment, Docker & Environment Safety)",
        "Deploying web services, static sites, and PostgreSQL databases cleanly in production cloud environments.",
        "Bringing a local development environment into production requires careful cloud deployment configuration. Gandheevijaya is engineered for seamless deployment on **Render**, leveraging containerized web services, static site CDNs, and managed PostgreSQL databases.",
        "<b>Feynman Analogy:</b> Think of a satellite launch vehicle standing on the launch pad at Kennedy Space Center. Before the main engine ignites, automated pre-flight computers execute hundreds of sensor checks—checking liquid oxygen pressure, electrical bus voltage, and guidance computer alignment. If any single sensor reads abnormal, launch is paused automatically.",
        "To ensure zero deployment friction, Sayan Kundu implemented automatic environment validators in `config.py`: **1. Production Safety Guards**: Enforces secure cookies (`COOKIE_SECURE=True`) and rejects weak default JWT secrets in production. **2. Database URL Normalizer**: Automatically transforms Render's default `postgres://` URLs into `postgresql+psycopg://` for SQLAlchemy 2.x compatibility. **3. Runtime Migration**: Runs `alembic upgrade head` cleanly during Uvicorn container startup."
    )

    add_chapter(
        22,
        "The Infrastructure Blueprint (Render YAML & CI/CD Pipelines)",
        "Automating cloud infrastructure setup, CORS origins, dynamic port binding, and continuous deployment.",
        "Modern cloud engineering favors **Infrastructure as Code (IaC)** over manual point-and-click dashboard setups. Sayan Kundu authored a standardized **Render Blueprint** specification file ([`render.yaml`](file:///c:/Users/DELL/Downloads/Gandheevijaya/render.yaml)) that defines the complete cloud ecosystem for Gandheevijaya in version-controlled declarative code.",
        "<b>Feynman Analogy:</b> Imagine an architect providing a master blueprint to a team of robotic builders. Instead of telling the builders step-by-step 'brick by brick', the architect feeds the 3D CAD blueprint into the central computer. The robotic builders scan the blueprint and erect the entire skyscraper, plumbing, electrical wiring, and windows automatically without human error.",
        "The [`render.yaml`](file:///c:/Users/DELL/Downloads/Gandheevijaya/render.yaml) specification automates: **1. Backend Service (`gandheevijaya-backend`)**: Python environment, build commands, Uvicorn start commands, health check endpoints, and CORS environment variables. **2. Frontend Static Site (`gandheevijaya-frontend`)**: Node build pipelines, dist publish directories, SPA rewrite rules (`/* -> /index.html`), and API base URL bindings."
    )

    # =========================================================================
    # PAGE 23: THE SUPREME MASTERY (FINAL SYNTHESIS & BRANDING)
    # =========================================================================
    story.append(Paragraph("<b>PAGE 23 — CHAPTER 22</b>", ParagraphStyle('PageNumHeader23', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor("#718096"), spaceAfter=2)))
    story.append(Paragraph("The Supreme Mastery (Final Synthesis & Future Horizons)", page_heading_style))
    story.append(Paragraph("<i>Synthesizing engineering excellence, cognitive resilience, and the relentless pursuit of truth.</i>", ParagraphStyle('SubHeadingItalic23', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, textColor=colors.HexColor("#4A5568"), spaceAfter=10)))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=2, spaceAfter=10))

    story.append(Paragraph("<b>1. The Ultimate Synthesis</b>", sub_heading_style))
    story.append(Paragraph(
        "We have journeyed through every layer of the <b>Gandheevijaya</b> platform—from ASGI event loops and relational PostgreSQL schemas to psychometric item analysis and the secular Bhagavad Gita mindset portal. "
        "What emerges is not merely a collection of python scripts and React components, but a unified, living ecosystem engineered for absolute excellence. "
        "By grounding technical design in first principles and combining it with cognitive stress resilience, Gandheevijaya provides students with an unshakeable platform for academic and intellectual growth.",
        body_style
    ))

    story.append(Paragraph("<b>2. Core System Invariants & Key Takeaways</b>", sub_heading_style))
    synthesis_box = (
        "<b>SUMMARY OF CORE SYSTEM INVARIANTS:</b><br/>"
        "• <b>Decoupled Architecture:</b> Modular monolith design ensures total testability, security, and scalability.<br/>"
        "• <b>Zero-Hallucination Ingestion:</b> Deduplication engine with SHA-256 fingerprinting guarantees clean data pools.<br/>"
        "• <b>Mathematical Precision:</b> Golden scoring matrix handles MCQ, MSQ, and NAT questions with zero rounding errors.<br/>"
        "• <b>Cognitive Resilience:</b> Gita Mindset Portal arms candidates with Tyaga (result detachment) and vagus nerve stress resets.<br/>"
        "• <b>Cloud Readiness:</b> Production safety validators and `render.yaml` infrastructure-as-code enable 1-click deployments."
    )
    story.append(Paragraph(synthesis_box, callout_style))

    story.append(Paragraph("<b>3. Final Words & Platform Dedication</b>", sub_heading_style))
    story.append(Paragraph(
        "True mastery in engineering and life comes from an unshakeable desire to uncover every hidden layer of a domain. "
        "Approach learning with intense curiosity, treat every mistake as high-value diagnostic data, and execute your daily work with deep present focus. "
        "Gandheevijaya stands as a testament to what is possible when engineering rigor meets profound human purpose.",
        body_style
    ))
    story.append(Spacer(1, 0.3 * inch))

    # Prominent Final Author Branding Box
    author_box = Table([
        [Paragraph("<font size=14 color='#1A365D'><b>GANDHEEVIJAYA PLATFORM</b></font><br/><br/>"
                   "<font size=12 color='#2B6CB0'><b>Made by Sayan Kundu</b></font><br/><br/>"
                   "<font size=9 color='#4A5568'>Multi-Exam Preparation • Quiz Assessment • Solution Review • Mindset Portal<br/>"
                   "Engineered with Python 3.12, FastAPI, PostgreSQL, React 18, Vite & Tailwind CSS</font>", ParagraphStyle('AuthBox', parent=styles['Normal'], alignment=1))]
    ], colWidths=[doc.width])
    author_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BORDER', (0,0), (-1,-1), 1.5, colors.HexColor("#2B6CB0")),
        ('PADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(author_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated 23-page PDF textbook at: {output_path}")

if __name__ == "__main__":
    output_pdf = os.path.join(r"c:\Users\DELL\Downloads\Gandheevijaya", "gandheevijaya_master_textbook_23pages.pdf")
    create_23page_pdf(output_pdf)
