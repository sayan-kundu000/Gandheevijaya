import React, { useState, useEffect, useCallback } from "react";
import {
  BookOpen,
  Compass,
  Sparkles,
  Brain,
  Award,
  ShieldCheck,
  Target,
  Zap,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  ListFilter,
  ArrowRight,
  ArrowLeft,
  X,
  Bookmark
} from "lucide-react";
import { Card } from "../ui/Card";
import { Badge } from "../ui/Badge";
import { GITA_PART_1_FULL_TEXT } from "../../data/gita/part1";

export interface GitaChapter {
  id: number;
  part: number;
  partTitle: string;
  chapterNumberLabel: string;
  title: string;
  subtitle: string;
  summary: string;
  keyPoints: string[];
  studentTakeaway: string;
}

export const GITA_CHAPTERS: GitaChapter[] = [
  // PART I
  {
    id: 1,
    part: 1,
    partTitle: "Part I — Entering the Gita Without Belief",
    chapterNumberLabel: "Chapter 1",
    title: "What Is the Bhagavad Gita, Really?",
    subtitle: "Historical context, Kurukshetra, Krishna and Arjuna, mythology vs philosophy.",
    summary: "Historical context, Kurukshetra battlefield setting, Krishna and Arjuna's dialogue, what the text actually represents, distinguishing mythology from rational philosophy, and why a student of any background can read it without converting to any religious dogma.",
    keyPoints: [
      "Historical and literary context of the Kurukshetra dialogue",
      "Mythology vs practical philosophy for real-world dilemmas",
      "Universal secular relevance for any student or thinker"
    ],
    studentTakeaway: "Treat the text as a philosophical toolkit for decision-making under uncertainty, not as a dogmatic script."
  },
  {
    id: 2,
    part: 1,
    partTitle: "Part I — Entering the Gita Without Belief",
    chapterNumberLabel: "Chapter 2",
    title: "Arjuna’s Crisis: The Psychology of a Student Under Pressure",
    subtitle: "Fear, confusion, overthinking, responsibility, and emotional paralysis.",
    summary: "Examines fear, confusion, overthinking, high-stakes responsibility, emotional paralysis, and the inability to act despite possessing full knowledge and training.",
    keyPoints: [
      "The anatomy of performance anxiety and paralysis by analysis",
      "How high stakes can cloud clear logical thinking",
      "Moving from emotional overwhelm to structured problem-solving"
    ],
    studentTakeaway: "Recognize that feeling overwhelmed before an exam is a natural psychological state—the key is how you structure your response to it."
  },

  // PART II — THE 18 CHAPTERS
  {
    id: 3,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 3",
    title: "Chapter 1: Arjuna Vishada Yoga — When the Mind Collapses",
    subtitle: "The problem of confusion before action.",
    summary: "Analyzes the exact moment when preparation meets intense pressure, causing initial mental collapse, self-doubt, and hesitation before taking the exam or stepping into the arena.",
    keyPoints: [
      "Pre-exam anxiety and acute performance stress",
      "Identifying cognitive distortions and worst-case spiral thinking",
      "Accepting uncertainty without letting it freeze action"
    ],
    studentTakeaway: "Acknowledge panic when it arises, pause, and ground yourself in fundamental facts rather than catastrophic assumptions."
  },
  {
    id: 4,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 4",
    title: "Chapter 2: Sankhya Yoga — Learning to Think Clearly",
    subtitle: "Self, impermanence, emotional stability, rational judgment, and disciplined action.",
    summary: "Establishes core rational judgment: separating identity from temporary results, cultivating emotional stability (Sthitaprajna), recognizing impermanence, and focusing on disciplined execution.",
    keyPoints: [
      "Separating your self-worth from test scores or ranks",
      "Equanimity in success and failure (Sthitaprajna state)",
      "Disciplined, objective analytical thinking"
    ],
    studentTakeaway: "Your test results measure current concept mastery, not your intrinsic worth as a human being."
  },
  {
    id: 5,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 5",
    title: "Chapter 3: Karma Yoga — Action Without Obsession",
    subtitle: "Work, responsibility, effort, productivity, and why waiting for motivation is a trap.",
    summary: "Deconstructs the principle of action (Karmanye Vadhikaraste): focusing 100% of your energy on execution while relinquishing anxiety over final outcomes. Waiting for 'motivation' is a trap; discipline creates momentum.",
    keyPoints: [
      "Process orientation vs result obsession",
      "Building daily habit systems independent of mood",
      "Eliminating the mental fatigue caused by outcome fixation"
    ],
    studentTakeaway: "Focus entirely on the question in front of you. You own the effort; you cannot directly force the exact rank."
  },
  {
    id: 6,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 6",
    title: "Chapter 4: Jnana Karma Sannyasa Yoga — Knowledge, Action & Learning",
    subtitle: "Knowledge transforming action, learning from teachers, experience, and intellectual maturity.",
    summary: "Explores how raw information transforms into actionable knowledge through guidance, active practice, questioning, and intellectual maturity.",
    keyPoints: [
      "Active learning over passive memorization",
      "Leveraging mentors, teachers, and mock analysis",
      "Continuous feedback loops to refine accuracy"
    ],
    studentTakeaway: "True learning occurs when you dissect your mistakes in mock tests and understand the underlying logic."
  },
  {
    id: 7,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 7",
    title: "Chapter 5: Karma Sannyasa Yoga — Work Without Losing Yourself",
    subtitle: "Renunciation vs responsibility, detachment, and maintaining inner balance while pursuing goals.",
    summary: "Distinguishes true detachment from passive neglect. Demonstrates how to work tirelessly toward ambitious exam targets without burning out or sacrificing mental equilibrium.",
    keyPoints: [
      "High productivity without emotional burnout",
      "Balancing intense study schedules with mental hygiene",
      "Detached engagement in high-stakes competition"
    ],
    studentTakeaway: "Work with deep dedication, but maintain an inner sanctuary of calm that external pressure cannot disturb."
  },
  {
    id: 8,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 8",
    title: "Chapter 6: Dhyana Yoga — Training the Mind",
    subtitle: "Attention, meditation, self-control, distraction, habits, and the restless mind.",
    summary: "Focuses on attentional control, deep work, overcoming digital distractions, training concentration, and taming the restless mind like a trained athlete.",
    keyPoints: [
      "Single-tasking and deep concentration protocols",
      "Overcoming smartphone addiction and focus fragmentation",
      "Gradual conditioning of mental stamina"
    ],
    studentTakeaway: "The mind is a wild horse—train it through steady daily practice, structured pomodoro sessions, and intentional quiet."
  },
  {
    id: 9,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 9",
    title: "Chapter 7: Jnana Vijnana Yoga — Knowing vs Understanding",
    subtitle: "Information vs wisdom, theoretical knowledge vs lived understanding, and intellectual humility.",
    summary: "Differentiates surface-level recall from deep conceptual mastery and practical application. Emphasizes intellectual humility when encountering complex syllabus topics.",
    keyPoints: [
      "Depth vs surface familiarity",
      "Testing knowledge through first-principles problem solving",
      "Avoiding the illusion of competence"
    ],
    studentTakeaway: "Don't just recognize a formula—understand why it works and when to apply alternative approaches."
  },
  {
    id: 10,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 10",
    title: "Chapter 8: Akshara Brahma Yoga — Mortality, Meaning & the Long View",
    subtitle: "Impermanence, ultimate goals, and thinking beyond immediate rewards.",
    summary: "Frames preparation within a long-term perspective. Reminds students that single exams are temporary checkpoints in a lifelong intellectual and career journey.",
    keyPoints: [
      "Long-term career perspective beyond a single test date",
      "Overcoming short-term panic through micro and macro goals",
      "Building resilience for long-duration competitive exams"
    ],
    studentTakeaway: "Keep the long view: a single test score does not define your life's ultimate trajectory."
  },
  {
    id: 11,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 11",
    title: "Chapter 9: Raja Vidya Raja Guhya Yoga — The Highest Knowledge",
    subtitle: "Faith, knowledge, meaning, devotion, and philosophical interpretation.",
    summary: "Explores internal conviction, faith in your preparation process, and finding deep personal meaning in your academic path.",
    keyPoints: [
      "Unshakeable self-trust backed by consistent prep",
      "Finding intrinsic motivation in your discipline",
      "Philosophical commitment to self-mastery"
    ],
    studentTakeaway: "Develop quiet confidence rooted in your cumulative hours of honest preparation."
  },
  {
    id: 12,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 12",
    title: "Chapter 10: Vibhuti Yoga — Recognizing Excellence",
    subtitle: "Greatness, extraordinary ability, excellence, and recognizing patterns of mastery.",
    summary: "Encourages studying top performers, identifying patterns of excellence, and admiring mastery without envy or self-deprecation.",
    keyPoints: [
      "Deconstructing how toppers solve problems and manage time",
      "Replacing jealousy with constructive modeling",
      "Appreciating precision and elegance in analytical work"
    ],
    studentTakeaway: "Learn from top rankers' habits and strategies, but adapt them to fit your own unique strengths."
  },
  {
    id: 13,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 13",
    title: "Chapter 11: Vishvarupa Darshana Yoga — Seeing the Bigger System",
    subtitle: "The cosmic vision as a metaphor for perspective, complexity, and interconnectedness.",
    summary: "Uses the cosmic vision metaphor to teach systems thinking—understanding how individual concepts, formulas, and subjects interconnect into a unified domain.",
    keyPoints: [
      "Systems thinking and cross-subject integration",
      "Seeing the macro structure of competitive exam syllabi",
      "Expanding perspective under complex problem conditions"
    ],
    studentTakeaway: "Step back to see how topics connect—computer networks, OS, math, and algorithms form one integrated discipline."
  },
  {
    id: 14,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 14",
    title: "Chapter 12: Bhakti Yoga — Commitment, Love & Meaning",
    subtitle: "Devotion interpreted broadly as commitment, purpose, values, and dedication.",
    summary: "Reinterprets devotion as deep emotional commitment, purpose, values, and love for your chosen field of study. Features 20 full shlokas.",
    keyPoints: [
      "Cultivating passion for problem-solving",
      "Sustaining energy through meaningful purpose",
      "Treating learning as a privilege rather than a burden"
    ],
    studentTakeaway: "Fall in love with the process of mastering difficult concepts; genuine enthusiasm makes study effortless."
  },
  {
    id: 15,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 15",
    title: "Chapter 13: Kshetra Kshetrajna Vibhaga Yoga — Understanding Yourself",
    subtitle: "Body, mind, awareness, observer vs experience, self-knowledge, and metacognition.",
    summary: "Introduces metacognition: understanding the field (syllabus/body/mind) vs the knower of the field (the observing self). Features 35 full shlokas.",
    keyPoints: [
      "Metacognitive awareness during exam solving",
      "Observing speed, accuracy, and error tendencies neutrally",
      "Separating reactive impulses from deliberate analysis"
    ],
    studentTakeaway: "Develop a 'third-person observer' mindset while test-taking to catch silly mistakes before locking in answers."
  },
  {
    id: 16,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 16",
    title: "Chapter 14: Gunatraya Vibhaga Yoga — The Three Modes of Behaviour",
    subtitle: "Sattva, Rajas, and Tamas as a framework for clarity, ambition, inertia, and habits.",
    summary: "Analyzes the 3 behavioral states: Sattva (clarity, focus, calm), Rajas (frenetic ambition, stress, restlessness), and Tamas (lethargy, procrastination, inertia). Teaches how to elevate your mental state to Sattva.",
    keyPoints: [
      "Identifying Tamas: Procrastination, sleepiness, avoidance",
      "Identifying Rajas: Over-caffeinated panic, frantic rushing",
      "Cultivating Sattva: Calm, lucid, structured study habits"
    ],
    studentTakeaway: "Notice when inertia (Tamas) or panic (Rajas) takes over, and deliberately reset your routine to clear focus (Sattva)."
  },
  {
    id: 17,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 17",
    title: "Chapter 15: Purushottama Yoga — Identity Beyond Circumstances",
    subtitle: "Identity, ego, values, desires, roots, and what remains when external labels disappear.",
    summary: "Examines identity beyond test scores, social status, peer comparison, and ego attachments. Focuses on core values that endure regardless of external outcomes.",
    keyPoints: [
      "De-linking personal identity from competitive ranks",
      "Transcending peer comparison and social pressure",
      "Anchoring self-esteem in character and integrity"
    ],
    studentTakeaway: "You are not your percentile. Your character, work ethic, and adaptability are what truly remain."
  },
  {
    id: 18,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 18",
    title: "Chapter 16: Daivasura Sampad Vibhaga Yoga — Divine & Demonic Traits",
    subtitle: "Constructive vs destructive mental habits, self-discipline vs egoistic indulgence.",
    summary: "Differentiates constructive mental habits (Daivi Sampad: truth, discipline, calm, humility) from destructive tendencies (Asuri Sampad: arrogance, greed, anger, hypocrisy) in study routines.",
    keyPoints: [
      "Building Daivi traits: Discipline, integrity, resilience",
      "Eliminating Asuri traps: Arrogance, shortcuts, envy",
      "Self-regulation for long-term academic excellence"
    ],
    studentTakeaway: "Cultivate constructive habits that build sustainable mastery, and eliminate toxic ego patterns that sabotage progress."
  },
  {
    id: 19,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 19",
    title: "Chapter 17: Shraddhatraya Vibhaga Yoga — The Three Types of Faith",
    subtitle: "Motivation, conviction, effort quality, food, discipline, and intention.",
    summary: "Examines the three types of faith and intention (Sattvic, Rajasic, Tamasic) governing how students approach study, motivation, lifestyle, and effort.",
    keyPoints: [
      "Sattvic Faith: Driven by genuine curiosity and growth",
      "Rajasic Faith: Driven by ego, status, and competitive dominance",
      "Tamasic Faith: Driven by fear, avoidance, and blind superstition"
    ],
    studentTakeaway: "Anchor your effort in Sattvic conviction—study for intrinsic mastery, not out of panic or superficial display."
  },
  {
    id: 20,
    part: 2,
    partTitle: "Part II — The 18 Chapters as a Student’s Philosophy",
    chapterNumberLabel: "Chapter 20",
    title: "Chapter 18: Moksha Sannyasa Yoga — Ultimate Freedom & Renunciation",
    subtitle: "Renunciation of outcome anxiety, duty, decision-making, surrender, and supreme mastery.",
    summary: "The pinnacle synthesis of the Bhagavad Gita: executing your duty with total commitment while surrendering anxiety over outcomes, achieving intellectual freedom and mastery.",
    keyPoints: [
      "Tyaga: Relinquishing result obsession while retaining 100% effort",
      "Swadharma: Aligning your prep strategy with your unique cognitive strengths",
      "Moksha: Total mental liberation and fearless exam execution"
    ],
    studentTakeaway: "Execute your work with complete devotion, surrender outcome panic, and step forward into the exam hall with total freedom."
  },

  // PART III — BEYOND THE TEXT
  {
    id: 21,
    part: 3,
    partTitle: "Part III — Beyond the Text",
    chapterNumberLabel: "Chapter 21",
    title: "The Influence of the Bhagavad Gita",
    subtitle: "Global impact on philosophy, science, leadership, and intellectual culture.",
    summary: "Explores the wide-ranging influence of the Gita on Indian philosophy, independence leaders (Gandhi, Tilak), scientists (Oppenheimer, Schrödinger), philosophers (Emerson, Thoreau), leadership thought, and global education.",
    keyPoints: [
      "Impact on world-renowned physicists and thinkers",
      "Application in modern stress management and executive leadership",
      "Secular wisdom adopted across global universities"
    ],
    studentTakeaway: "Recognize that you are engaging with a global intellectual masterpiece studied by scientists and leaders worldwide."
  },
  {
    id: 22,
    part: 3,
    partTitle: "Part III — Beyond the Text",
    chapterNumberLabel: "Chapter 22",
    title: "Applying the Gita to Real Student Problems",
    subtitle: "Procrastination, comparison, parental pressure, social media, burnout, and rejection.",
    summary: "Practical tactical application of Gita principles to real student challenges: handling parental expectations, overcoming social media distraction, dealing with mock test rejection, and preventing burnout.",
    keyPoints: [
      "Navigating parental and societal expectations with grace",
      "Digital minimalism and cognitive boundary setting",
      "Bouncing back after poor mock exam scores"
    ],
    studentTakeaway: "Use the Gita's framework as a daily problem-solving toolkit whenever burnout or comparison arises."
  },
  {
    id: 23,
    part: 3,
    partTitle: "Part III — Beyond the Text",
    chapterNumberLabel: "Chapter 23",
    title: "Why We Need the Gita in Exams",
    subtitle: "Exams create an Arjuna environment: uncertainty + pressure + limited time.",
    summary: "Exams replicate Arjuna's exact battlefield conditions: high uncertainty, intense time pressure, high stakes, and performance expectations. Features 14 core mental competencies.",
    keyPoints: [
      "14 Core Competencies: Anxiety Management, Result Detachment, Process Orientation, Concentration, Discipline, Ethical Decision-Making, Handling Failure, Handling Success, Long-term Thinking, Metacognition, Emotional Regulation, Resilience, Responsibility, Decision-making under uncertainty."
    ],
    studentTakeaway: "Competitive exams are mental stamina contests as much as knowledge tests; the Gita equips you with psychological resilience."
  },
  {
    id: 24,
    part: 3,
    partTitle: "Part III — Beyond the Text",
    chapterNumberLabel: "Chapter 24",
    title: "The Student’s Gita: What Should You Actually Take Away?",
    subtitle: "The final synthesis for competitive exam aspirants.",
    summary: "The ultimate synthesis: Think clearly. Know yourself. Do your work. Accept uncertainty. Control what you can. Learn from failure. Don't become enslaved by outcomes. Build character. Keep questioning.",
    keyPoints: [
      "Think clearly under pressure",
      "Execute your daily work without result obsession",
      "Control what you can and learn from every test"
    ],
    studentTakeaway: "Think clearly. Know yourself. Do your work. Accept uncertainty. Control what you can. Learn from failure. Build character. Keep questioning."
  }
];

export const EXAM_WISDOM_TOPICS = [
  { title: "Anxiety Management", icon: ShieldCheck, color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30", chapters: "Ch 1, Ch 2, Ch 3" },
  { title: "Detachment from Results", icon: Target, color: "text-amber-400 bg-amber-500/10 border-amber-500/30", chapters: "Ch 2, Ch 3, Ch 5" },
  { title: "Process Orientation", icon: Compass, color: "text-brand-400 bg-brand-500/10 border-brand-500/30", chapters: "Ch 3, Ch 4" },
  { title: "Concentration & Focus", icon: Zap, color: "text-sky-400 bg-sky-500/10 border-sky-500/30", chapters: "Ch 6, Ch 8" },
  { title: "Discipline & Routine", icon: Award, color: "text-purple-400 bg-purple-500/10 border-purple-500/30", chapters: "Ch 3, Ch 6" },
  { title: "Ethical Decision-Making", icon: CheckCircle2, color: "text-indigo-400 bg-indigo-500/10 border-indigo-500/30", chapters: "Ch 1, Ch 17-18" },
  { title: "Handling Failure", icon: Brain, color: "text-rose-400 bg-rose-500/10 border-rose-500/30", chapters: "Ch 2, Ch 21" },
  { title: "Handling Success", icon: Sparkles, color: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30", chapters: "Ch 2, Ch 14" },
];

type ViewMode = "shloka" | "explanation" | "concepts" | "takeaways" | "skills";

export const BhagavadGeetaSection: React.FC = () => {
  // Saved state initialization
  const [selectedPart, setSelectedPart] = useState<number>(0);
  const [activeChapterId, setActiveChapterId] = useState<number>(() => {
    const saved = localStorage.getItem("gita_active_chapter");
    return saved ? parseInt(saved, 10) : 1;
  });
  const [activeSlideIndex, setActiveSlideIndex] = useState<number>(() => {
    const saved = localStorage.getItem("gita_active_slide");
    return saved ? parseInt(saved, 10) : 0;
  });
  const [activeViewMode, setActiveViewMode] = useState<ViewMode>("shloka");
  const [isChapterMenuOpen, setIsChapterMenuOpen] = useState<boolean>(false);
  const [selectedCompetency, setSelectedCompetency] = useState<typeof EXAM_WISDOM_TOPICS[0] | null>(null);

  // Filtered chapters according to selected part
  const filteredChapters = selectedPart === 0 
    ? GITA_CHAPTERS 
    : GITA_CHAPTERS.filter((ch) => ch.part === selectedPart);

  // Get active chapter object
  const activeChapter = GITA_CHAPTERS.find((ch) => ch.id === activeChapterId) || GITA_CHAPTERS[0];

  // Retrieve rich text content for active chapter
  const chapterData = GITA_PART_1_FULL_TEXT[activeChapterId];
  
  // Compute slides array for the active chapter
  const slides = React.useMemo(() => {
    if (chapterData?.shlokasData && chapterData.shlokasData.length > 0) {
      return chapterData.shlokasData.map((s, idx) => ({
        type: "shloka" as const,
        slideNumber: idx + 1,
        total: chapterData.shlokasData!.length,
        data: s
      }));
    } else if (chapterData?.paragraphs && chapterData.paragraphs.length > 0) {
      return chapterData.paragraphs.map((p, idx) => ({
        type: "paragraph" as const,
        slideNumber: idx + 1,
        total: chapterData.paragraphs.length,
        text: p
      }));
    } else {
      return (activeChapter.keyPoints || []).map((kp, idx) => ({
        type: "keypoint" as const,
        slideNumber: idx + 1,
        total: activeChapter.keyPoints.length,
        text: kp
      }));
    }
  }, [chapterData, activeChapter]);

  // Ensure current slide index is valid
  const currentSlide = slides[activeSlideIndex] || slides[0] || { slideNumber: 1, total: 1 };

  // Sync to localStorage
  useEffect(() => {
    localStorage.setItem("gita_active_chapter", activeChapterId.toString());
    localStorage.setItem("gita_active_slide", activeSlideIndex.toString());
  }, [activeChapterId, activeSlideIndex]);

  // Handlers for Chapter Change
  const handleSelectChapter = useCallback((chapterId: number) => {
    setActiveChapterId(chapterId);
    setActiveSlideIndex(0);
    setIsChapterMenuOpen(false);
  }, []);

  const handleNextChapter = useCallback(() => {
    const currentIndex = GITA_CHAPTERS.findIndex(c => c.id === activeChapterId);
    if (currentIndex < GITA_CHAPTERS.length - 1) {
      handleSelectChapter(GITA_CHAPTERS[currentIndex + 1].id);
    }
  }, [activeChapterId, handleSelectChapter]);

  const handlePrevChapter = useCallback(() => {
    const currentIndex = GITA_CHAPTERS.findIndex(c => c.id === activeChapterId);
    if (currentIndex > 0) {
      handleSelectChapter(GITA_CHAPTERS[currentIndex - 1].id);
    }
  }, [activeChapterId, handleSelectChapter]);

  // Handlers for Slide Change
  const handleNextSlide = useCallback(() => {
    if (activeSlideIndex < slides.length - 1) {
      setActiveSlideIndex(prev => prev + 1);
    } else {
      // Auto advance to next chapter if on last slide
      handleNextChapter();
    }
  }, [activeSlideIndex, slides.length, handleNextChapter]);

  const handlePrevSlide = useCallback(() => {
    if (activeSlideIndex > 0) {
      setActiveSlideIndex(prev => prev - 1);
    }
  }, [activeSlideIndex]);

  // Keyboard navigation shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Prevent shortcut interference when typing inside input/textarea
      if (["INPUT", "TEXTAREA", "SELECT"].includes((e.target as HTMLElement)?.tagName)) return;

      if (e.key === "ArrowRight") {
        e.preventDefault();
        handleNextSlide();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        handlePrevSlide();
      } else if (e.key === "ArrowDown") {
        e.preventDefault();
        handleNextChapter();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        handlePrevChapter();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [handleNextSlide, handlePrevSlide, handleNextChapter, handlePrevChapter]);

  return (
    <section id="gita-section" className="mt-6 mb-12 space-y-6">
      {/* Interactive Portal Header */}
      <Card className="relative overflow-hidden border-amber-500/30 bg-gradient-to-r from-amber-950/50 via-slate-900 to-amber-950/40 p-5 md:p-8 shadow-2xl">
        <div className="absolute -right-8 -bottom-8 w-56 h-56 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="warning" className="gap-1.5 px-3 py-1 text-xs font-bold uppercase tracking-wider">
                <Compass className="w-3.5 h-3.5" />
                <span>Bhagavad Gita • Interactive Click Reader</span>
              </Badge>
              <Badge variant="brand" className="text-xs">Secular & Realist Guide</Badge>
              <Badge variant="neutral" className="text-xs">Zero-Scroll Deck Mode</Badge>
            </div>

            <div className="flex items-center gap-2 text-xs font-medium text-amber-300/90 bg-amber-950/40 px-3 py-1 rounded-full border border-amber-500/20">
              <Bookmark className="w-3.5 h-3.5 text-amber-400" />
              <span>Chapter {activeChapterId} of 23</span>
            </div>
          </div>

          <h2 className="text-xl md:text-3xl font-extrabold text-amber-200 tracking-tight font-serif">
            The Student’s Gita: Rational Philosophy & Exam Resilience
          </h2>

          <p className="text-xs md:text-sm text-slate-300 max-w-4xl leading-relaxed">
            Click through chapters and shlokas slide-by-slide. Master anxiety management, result detachment, process orientation, and metacognition for GATE, SSC, Banking, and high-stakes competitive tests without page scrolling.
          </p>

          <div className="pt-1 flex flex-wrap items-center justify-between gap-4 text-xs font-medium text-amber-300/80 border-t border-amber-500/20 pt-3">
            <div className="flex flex-wrap items-center gap-3">
              <span>✨ 3 Distinct Parts</span>
              <span>•</span>
              <span>📚 23 Modules</span>
              <span>•</span>
              <span>🎯 14 Competencies</span>
            </div>
            <div className="flex items-center gap-2 text-[11px] text-slate-400">
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono">← / →</span>
              <span>Slide Keys</span>
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-slate-300 font-mono">↑ / ↓</span>
              <span>Chapter Keys</span>
            </div>
          </div>
        </div>
      </Card>

      {/* Part Filter Bar & Chapter Selection Strip */}
      <div className="space-y-3 bg-slate-900/80 border border-slate-800 p-4 rounded-2xl shadow-lg">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
          {/* Part Selection Buttons */}
          <div className="flex flex-wrap items-center gap-2">
            {[
              { id: 0, label: "All Parts (23 Chapters)" },
              { id: 1, label: "Part I — Entering Without Belief" },
              { id: 2, label: "Part II — The 18 Chapters" },
              { id: 3, label: "Part III — Beyond the Text" },
            ].map((part) => (
              <button
                key={part.id}
                onClick={() => setSelectedPart(part.id)}
                className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  selectedPart === part.id
                    ? "bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-sm"
                    : "bg-slate-800/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800"
                }`}
              >
                {part.label}
              </button>
            ))}
          </div>

          {/* Direct Chapter Dropdown Switcher Button */}
          <button
            onClick={() => setIsChapterMenuOpen(!isChapterMenuOpen)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-bold hover:bg-amber-500/20 transition-all"
          >
            <ListFilter className="w-4 h-4 text-amber-400" />
            <span>Select Chapter Grid ({filteredChapters.length})</span>
          </button>
        </div>

        {/* Chapter Grid Drawer (When toggled open) */}
        {isChapterMenuOpen && (
          <div className="p-4 rounded-xl bg-slate-950/90 border border-amber-500/30 space-y-3 animate-in fade-in duration-150">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="text-xs font-bold text-amber-300 uppercase tracking-wider">
                Click any Chapter to Jump Directly:
              </span>
              <button
                onClick={() => setIsChapterMenuOpen(false)}
                className="text-slate-400 hover:text-white p-1"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2">
              {filteredChapters.map((ch) => (
                <button
                  key={ch.id}
                  onClick={() => handleSelectChapter(ch.id)}
                  className={`p-2.5 rounded-xl text-left border transition-all space-y-1 ${
                    activeChapterId === ch.id
                      ? "bg-amber-500/20 border-amber-500/60 text-amber-200 shadow-md"
                      : "bg-slate-900/60 border-slate-800 text-slate-300 hover:border-amber-500/30 hover:bg-slate-900"
                  }`}
                >
                  <div className="text-[10px] font-bold text-amber-400 uppercase">Ch {ch.id}</div>
                  <div className="text-xs font-semibold line-clamp-1">{ch.title.split(":")[1] || ch.title}</div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chapter Navigation Header Card */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pt-1">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/40 flex items-center justify-center font-extrabold text-sm text-amber-400 shrink-0 shadow-inner">
              {activeChapterId}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-extrabold uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                  {activeChapter.chapterNumberLabel}
                </span>
                <span className="text-xs text-slate-400">• {activeChapter.partTitle.split("—")[1] || activeChapter.partTitle}</span>
              </div>
              <h3 className="text-base md:text-lg font-bold text-white tracking-tight font-serif mt-0.5">
                {activeChapter.title}
              </h3>
            </div>
          </div>

          {/* Previous / Next Chapter Quick Controls */}
          <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-end shrink-0">
            <button
              onClick={handlePrevChapter}
              disabled={GITA_CHAPTERS.findIndex(c => c.id === activeChapterId) === 0}
              className="px-3 py-1.5 rounded-xl border border-slate-700 bg-slate-800/80 text-xs font-semibold text-slate-200 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Prev Ch</span>
            </button>
            <span className="text-xs font-mono text-amber-400 px-2">
              {GITA_CHAPTERS.findIndex(c => c.id === activeChapterId) + 1} / {GITA_CHAPTERS.length}
            </span>
            <button
              onClick={handleNextChapter}
              disabled={GITA_CHAPTERS.findIndex(c => c.id === activeChapterId) === GITA_CHAPTERS.length - 1}
              className="px-3 py-1.5 rounded-xl border border-amber-500/40 bg-amber-500/10 text-xs font-bold text-amber-300 hover:bg-amber-500/20 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all"
            >
              <span>Next Ch</span>
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* CORE CLICK-BASED SLIDE READER DECK VIEW */}
      <Card className="border-amber-500/40 bg-slate-950/90 shadow-2xl overflow-hidden relative">
        {/* Top Control Bar: Progress, Jump Selector & View Mode Tabs */}
        <div className="p-4 md:p-5 border-b border-slate-800 bg-slate-900/60 space-y-4">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            {/* Slide Counter & Jump Menu */}
            <div className="flex items-center gap-3">
              <div className="px-3 py-1 rounded-lg bg-amber-500/20 border border-amber-500/40 text-amber-300 font-bold text-xs">
                Slide {currentSlide.slideNumber} of {slides.length}
              </div>

              {/* Direct Jump Pill Selector */}
              <div className="flex items-center gap-1 overflow-x-auto max-w-[280px] sm:max-w-md py-1 no-scrollbar">
                {slides.map((s, idx) => (
                  <button
                    key={idx}
                    onClick={() => setActiveSlideIndex(idx)}
                    className={`w-7 h-7 rounded-lg text-xs font-bold transition-all shrink-0 flex items-center justify-center ${
                      activeSlideIndex === idx
                        ? "bg-amber-500 text-slate-950 shadow-md font-extrabold"
                        : "bg-slate-800/80 text-slate-400 hover:text-slate-100 hover:bg-slate-700"
                    }`}
                    title={`Jump to Slide ${idx + 1}`}
                  >
                    {idx + 1}
                  </button>
                ))}
              </div>
            </div>

            {/* View Mode Toggle Tabs */}
            <div className="flex flex-wrap items-center gap-1.5 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
              {[
                { id: "shloka" as const, label: "📖 Text & Translation", icon: BookOpen },
                { id: "explanation" as const, label: "💡 Feynman Explanation", icon: Sparkles },
                { id: "concepts" as const, label: "🧠 Core Concepts", icon: Brain },
                { id: "takeaways" as const, label: "🎯 Exam Takeaways", icon: Target },
                { id: "skills" as const, label: "🛡️ Cognitive Mastery", icon: ShieldCheck },
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveViewMode(tab.id)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                      activeViewMode === tab.id
                        ? "bg-amber-500/20 text-amber-300 border border-amber-500/40 shadow-sm"
                        : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                    }`}
                  >
                    <Icon className="w-3.5 h-3.5" />
                    <span>{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Visual Progress Bar */}
          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-800/50">
            <div
              className="bg-gradient-to-r from-amber-500 to-emerald-400 h-full transition-all duration-300"
              style={{ width: `${((activeSlideIndex + 1) / slides.length) * 100}%` }}
            />
          </div>
        </div>

        {/* ACTIVE SLIDE DISPLAY BODY */}
        <div className="p-6 md:p-8 min-h-[340px] flex flex-col justify-between space-y-6">
          {activeViewMode === "shloka" && (
            <div className="space-y-6 animate-in fade-in duration-200">
              {currentSlide.type === "shloka" && currentSlide.data ? (
                <div className="space-y-5">
                  <div className="flex items-center justify-between border-b border-amber-500/20 pb-3">
                    <span className="text-xs font-extrabold uppercase tracking-wider text-amber-400 bg-amber-500/10 px-3 py-1 rounded-md border border-amber-500/30">
                      Shloka {activeChapterId}.{currentSlide.data.number}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">
                      Paragraph {currentSlide.slideNumber} of {slides.length}
                    </span>
                  </div>

                  {/* Sanskrit Devanagari Script */}
                  <div className="p-5 md:p-6 rounded-2xl bg-amber-950/20 border border-amber-500/40 space-y-2.5 shadow-xl">
                    <p className="text-xs font-bold uppercase tracking-wider text-amber-400">
                      Sanskrit Devanagari Script:
                    </p>
                    <p className="text-lg md:text-2xl font-serif text-amber-100 whitespace-pre-line leading-relaxed font-bold tracking-wide">
                      {currentSlide.data.devanagari}
                    </p>
                  </div>

                  {/* English Devanagari Transliteration */}
                  <div className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5">
                    <p className="text-[11px] font-bold uppercase tracking-wider text-amber-300/80">
                      English Transliteration / Pronunciation:
                    </p>
                    <p className="text-xs md:text-sm font-sans italic text-amber-100/90 leading-relaxed">
                      {currentSlide.data.englishScript}
                    </p>
                  </div>

                  {/* English Translation */}
                  <div className="p-5 rounded-2xl bg-slate-900/90 border-l-4 border-amber-500 space-y-2 shadow-lg">
                    <p className="text-xs font-bold uppercase tracking-wider text-amber-400">
                      English Meaning & Translation:
                    </p>
                    <p className="text-sm md:text-base text-slate-100 leading-relaxed font-serif italic">
                      "{currentSlide.data.translation}"
                    </p>
                  </div>
                </div>
              ) : (
                <div className="p-6 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-4">
                  <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                    <span className="text-xs font-extrabold text-amber-400 uppercase tracking-wider">
                      Chapter Content • Slide {currentSlide.slideNumber} of {slides.length}
                    </span>
                  </div>
                  <p className="text-sm md:text-base text-slate-200 leading-relaxed font-sans font-medium">
                    {"text" in currentSlide ? currentSlide.text : activeChapter.summary}
                  </p>
                </div>
              )}
            </div>
          )}

          {activeViewMode === "explanation" && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <div className="flex items-center gap-2 border-b border-amber-500/20 pb-3">
                <Sparkles className="w-5 h-5 text-amber-400" />
                <h4 className="text-base font-bold text-amber-200 font-serif">
                  Feynman-Style Simple Explanation (Slide {currentSlide.slideNumber})
                </h4>
              </div>

              {currentSlide.type === "shloka" && currentSlide.data ? (
                <div className="p-6 rounded-2xl bg-slate-900/90 border border-amber-500/30 space-y-4 shadow-xl">
                  <p className="text-sm md:text-base text-slate-200 leading-relaxed font-sans font-normal tracking-wide">
                    {currentSlide.data.fullExplanation || currentSlide.data.paragraphText}
                  </p>
                </div>
              ) : (
                <div className="p-6 rounded-2xl bg-slate-900/90 border border-amber-500/30 space-y-4">
                  <p className="text-sm md:text-base text-slate-200 leading-relaxed">
                    {activeChapter.summary}
                  </p>
                  <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">
                    <strong className="text-amber-300 text-xs uppercase tracking-wider block mb-1">
                      Student Takeaway:
                    </strong>
                    <p className="text-xs md:text-sm text-slate-200 italic">
                      "{activeChapter.studentTakeaway}"
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeViewMode === "concepts" && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <div className="flex items-center gap-2 border-b border-amber-500/20 pb-3">
                <Brain className="w-5 h-5 text-amber-400" />
                <h4 className="text-base font-bold text-amber-200">
                  Core Philosophical Concepts for Chapter {activeChapterId}
                </h4>
              </div>

              {chapterData?.keyPhilosophicalConcepts ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {chapterData.keyPhilosophicalConcepts.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2 hover:border-amber-500/40 transition-colors shadow-md"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-bold text-amber-300">{item.concept}</span>
                        {item.sanskritTerm && (
                          <span className="text-xs text-amber-400/80 font-serif italic">
                            {item.sanskritTerm}
                          </span>
                        )}
                      </div>
                      <p className="text-xs md:text-sm text-slate-300 leading-relaxed">
                        {item.explanation}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {activeChapter.keyPoints.map((pt, idx) => (
                    <div key={idx} className="p-4 rounded-xl bg-slate-900/90 border border-slate-800 flex items-start gap-3">
                      <span className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-300 font-bold text-xs flex items-center justify-center shrink-0">
                        {idx + 1}
                      </span>
                      <p className="text-xs md:text-sm text-slate-300 leading-relaxed">{pt}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeViewMode === "takeaways" && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <div className="flex items-center gap-2 border-b border-emerald-500/20 pb-3">
                <Target className="w-5 h-5 text-emerald-400" />
                <h4 className="text-base font-bold text-emerald-300">
                  Actionable Student & Exam Takeaways (Chapter {activeChapterId})
                </h4>
              </div>

              {chapterData?.studentTakeaways ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {chapterData.studentTakeaways.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 space-y-2 shadow-md"
                    >
                      <p className="text-sm font-bold text-emerald-300">{item.title}</p>
                      <p className="text-xs md:text-sm text-emerald-100/90 leading-relaxed italic">
                        "{item.actionableAdvice}"
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="p-6 rounded-2xl bg-emerald-950/20 border border-emerald-500/40 space-y-3">
                  <h5 className="text-sm font-bold text-emerald-300 uppercase tracking-wider">
                    Core Student Takeaway:
                  </h5>
                  <p className="text-sm md:text-base text-emerald-100 font-serif italic leading-relaxed">
                    "{activeChapter.studentTakeaway}"
                  </p>
                </div>
              )}
            </div>
          )}

          {activeViewMode === "skills" && (
            <div className="space-y-4 animate-in fade-in duration-200">
              <div className="flex items-center justify-between border-b border-indigo-500/20 pb-3">
                <div className="flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-indigo-400" />
                  <h4 className="text-base font-bold text-indigo-200">
                    Advanced Cognitive Skills & Deception Detection
                  </h4>
                </div>
                {chapterData?.confidenceScore && (
                  <span className="text-xs font-bold text-emerald-300 bg-emerald-950/80 border border-emerald-500/40 px-3 py-1 rounded-full">
                    Confidence: {chapterData.confidenceScore}%
                  </span>
                )}
              </div>

              {chapterData?.advancedSkillsMastery ? (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Critical Thinking */}
                  <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/30 space-y-2">
                    <h5 className="text-xs font-bold text-indigo-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Brain className="w-3.5 h-3.5 text-indigo-400" />
                      {chapterData.advancedSkillsMastery.criticalThinking.title}
                    </h5>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {chapterData.advancedSkillsMastery.criticalThinking.description}
                    </p>
                  </div>

                  {/* Metacognition */}
                  <div className="p-4 rounded-xl bg-purple-950/20 border border-purple-500/30 space-y-2">
                    <h5 className="text-xs font-bold text-purple-300 uppercase tracking-wider flex items-center gap-1.5">
                      <Zap className="w-3.5 h-3.5 text-purple-400" />
                      {chapterData.advancedSkillsMastery.metacognition.title}
                    </h5>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {chapterData.advancedSkillsMastery.metacognition.description}
                    </p>
                  </div>

                  {/* Deception Detection */}
                  {chapterData.advancedSkillsMastery.deceptionDetection && (
                    <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-500/30 space-y-2">
                      <h5 className="text-xs font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                        <ShieldCheck className="w-3.5 h-3.5 text-rose-400" />
                        {chapterData.advancedSkillsMastery.deceptionDetection.title}
                      </h5>
                      <p className="text-xs text-slate-300 leading-relaxed">
                        {chapterData.advancedSkillsMastery.deceptionDetection.description}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <div className="p-6 rounded-2xl bg-indigo-950/20 border border-indigo-500/30 text-center space-y-2">
                  <p className="text-xs md:text-sm text-slate-300">
                    Applying chapter principles to hone objective analytical problem solving, error detection, and time management.
                  </p>
                </div>
              )}
            </div>
          )}

          {/* CLICK-BASED ACTION CONTROL BAR */}
          <div className="flex items-center justify-between border-t border-slate-800/80 pt-5 mt-4">
            <button
              onClick={handlePrevSlide}
              disabled={activeSlideIndex === 0}
              className="px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900 text-slate-200 text-xs md:text-sm font-bold hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed flex items-center gap-2 transition-all shadow-md"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>← Previous Shloka</span>
            </button>

            <div className="hidden sm:flex items-center gap-1.5 text-xs text-slate-400 font-medium">
              <span>Use Left/Right keys to click through slides</span>
            </div>

            <button
              onClick={handleNextSlide}
              className="px-5 py-2.5 rounded-xl border border-amber-500/60 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 text-xs md:text-sm font-extrabold hover:brightness-110 flex items-center gap-2 transition-all shadow-lg"
            >
              <span>{activeSlideIndex === slides.length - 1 ? "Next Chapter →" : "Next Shloka →"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </Card>

      {/* 14 CORE EXAM PSYCHOLOGICAL COMPETENCIES INTERACTIVE GRID */}
      <Card className="p-6 border-slate-800 bg-slate-900/80 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Brain className="w-5 h-5 text-amber-400" />
            <h3 className="text-base font-bold text-white tracking-tight">
              14 Core Exam Psychological Competencies (Click to View Advice)
            </h3>
          </div>
          <Badge variant="warning">Interactive Matrix</Badge>
        </div>

        <p className="text-xs text-slate-400">
          Click any competency below to view instant exam wisdom and relevant Gita chapters:
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {EXAM_WISDOM_TOPICS.map((item, index) => {
            const IconComp = item.icon;
            const isSelected = selectedCompetency?.title === item.title;
            return (
              <button
                key={index}
                onClick={() => setSelectedCompetency(isSelected ? null : item)}
                className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-semibold transition-all text-left ${item.color} ${
                  isSelected ? "ring-2 ring-amber-400 scale-[1.02]" : "hover:brightness-125"
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <IconComp className="w-4 h-4 shrink-0" />
                  <span>{item.title}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Selected Competency Modal Card */}
        {selectedCompetency && (
          <div className="p-4 rounded-xl bg-slate-950 border border-amber-500/40 space-y-2 animate-in fade-in duration-150">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 font-bold text-amber-300 text-sm">
                <span>{selectedCompetency.title}</span>
                <span className="text-xs text-slate-400">({selectedCompetency.chapters})</span>
              </div>
              <button onClick={() => setSelectedCompetency(null)} className="text-slate-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Mastering {selectedCompetency.title.toLowerCase()} provides essential psychological stability during high-stakes competitive exams. Study the corresponding chapters above to cultivate Sthitaprajna equanimity.
            </p>
          </div>
        )}
      </Card>

      {/* CHAPTER 23 FINAL SYNTHESIS FOOTER CARD */}
      <Card className="p-6 border-amber-500/40 bg-gradient-to-r from-slate-900 via-amber-950/30 to-slate-900 text-center space-y-3 shadow-xl">
        <h3 className="text-base md:text-lg font-bold text-amber-300 font-serif">
          Chapter 23 — The Student’s Gita: Final Synthesis
        </h3>
        <blockquote className="text-xs md:text-sm italic font-medium text-slate-200 max-w-3xl mx-auto leading-relaxed font-serif">
          "Think clearly. Know yourself. Do your work. Accept uncertainty. Control what you can. Learn from failure. Don't become enslaved by outcomes. Build character. Keep questioning."
        </blockquote>
      </Card>
    </section>
  );
};
