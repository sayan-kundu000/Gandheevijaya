import sys

part1_path = "frontend/src/data/gita/part1.ts"
with open(part1_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add imports if not present
imports_to_add = """import gunatraya27Shlokas from "./bhagavad_gita_ch14_gunatraya_27_shlokas.json";
import purushottama20Shlokas from "./bhagavad_gita_ch15_purushottama_20_shlokas.json";
"""

if "gunatraya27Shlokas" not in content:
    content = imports_to_add + content

# 2. Add ch16Data and ch17Data definitions before GITA_PART_1_FULL_TEXT
data_definitions = """
const ch16Data: ChapterDetailContent = {
  chapterId: 16,
  title: "Chapter 14: Gunatraya Vibhaga Yoga — The Three Modes of Behaviour",
  subtitle: "Sattva, Rajas, and Tamas as a framework for clarity, ambition, inertia, and habits.",
  confidenceScore: 99.8,
  shlokasData: gunatraya27Shlokas as any,
  paragraphs: (gunatraya27Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),
  keyPhilosophicalConcepts: [
    {
      concept: "Triguna Mechanics (Sattva, Rajas, Tamas)",
      sanskritTerm: "त्रिगुण",
      explanation: "Material nature operates entirely through three fundamental energy modes: Sattva (clarity, harmony, illumination), Rajas (passion, frantic motion, craving), and Tamas (inertia, heaviness, delusion)."
    },
    {
      concept: "Mechanism of Binding (Guna-Bandhana)",
      sanskritTerm: "गुणबन्धन",
      explanation: "Consciousness becomes bound when it misidentifies with the dominant Guna operating inside the body-mind complex."
    },
    {
      concept: "Dynamic Interplay and Competition (Guna-Vrittam)",
      sanskritTerm: "गुणवृत्त",
      explanation: "The three Gunas are in perpetual competition for dominance over mood, cognitive capacity, sensory perception, and choice."
    },
    {
      concept: "Trajectory of Reincarnation (Gati-Bheda)",
      sanskritTerm: "गतिभेद",
      explanation: "The predominant Guna active at death dictates evolutionary trajectory: Sattva leads upward, Rajas stays middle, Tamas goes downward."
    },
    {
      concept: "Transcendence (Trigunatita)",
      sanskritTerm: "गुणातीत",
      explanation: "Becoming Trigunatita means observing all mental states neutrally with the realization that 'gunas alone are interacting with gunas'."
    }
  ],
  studentTakeaways: [
    {
      title: "Diagnose Your Mental State in Real Time",
      actionableAdvice: "Treat emotions and energy levels as objective indicators of Guna shifts rather than your permanent identity."
    },
    {
      title: "Actively Engineer Your Environment",
      actionableAdvice: "Intentionally design your daily routine to maximize Sattva while systematically draining Rajas and Tamas."
    },
    {
      title: "Practice Radical Non-Reactivity to Mental Weather",
      actionableAdvice: "Observe all internal states like weather passing through a sky, knowing you are the vast untouched sky."
    },
    {
      title: "Beware Golden Handcuffs of Intellectual Pride",
      actionableAdvice: "Notice when mental clarity turns into subtle arrogance or attachment to comfort."
    },
    {
      title: "Leverage Unswerving Focus for Fast Transcendence",
      actionableAdvice: "Anchor daily efforts in single-minded devotion (Bhakti-yoga) to your highest purpose for ultimate escape velocity."
    }
  ],
  advancedSkillsMastery: {
    criticalThinking: {
      title: "Critical Thinking Mastery",
      description: "Deconstructing Multi-Variable Causality and Eliminating Cognitive Bias through Guna dissection.",
      techniques: [
        "Analyze complex systems by isolating Tamasic inertia, Rajasic opportunistic greed, and Sattvic systemic harmony.",
        "Recognize how Rajas over-estimates rewards while Tamas perceives solvable challenges as impossible."
      ]
    },
    metacognition: {
      title: "Metacognition Mastery",
      description: "Internal Observer Protocol and Watching the Watcher (Sakshi-Bhava).",
      techniques: [
        "Execute real-time labeling: 'This is a Rajasic surge' or 'This is a Tamasic wave of avoidance'.",
        "Establish primary identity in the silent, immovable witness consciousness beyond mental weather."
      ]
    },
    deception: {
      title: "Deception & Anti-Deception Mastery",
      description: "Detecting Manipulation through Guna-Profiling and Immunity to Social Engineering.",
      techniques: [
        "Identify bad actors using Rajasic artificial urgency or Tamasic confusion and weaponized incompetence.",
        "Build total immunity to public praise (Samstuti) or blame (Ninda) by recognizing them as Guna manipulations."
      ]
    }
  }
};

const ch17Data: ChapterDetailContent = {
  chapterId: 17,
  title: "Chapter 15: Purushottama Yoga — Identity Beyond Circumstances",
  subtitle: "Identity, ego, values, desires, roots, and what remains when external labels disappear.",
  confidenceScore: 99.8,
  shlokasData: purushottama20Shlokas as any,
  paragraphs: (purushottama20Shlokas as any[]).map(s => s.paragraphText || s.fullExplanation),
  keyPhilosophicalConcepts: [
    {
      concept: "The Inverted Cosmic Tree (Ashvattha-Rupa)",
      sanskritTerm: "अश्वत्थ",
      explanation: "Material existence is structured as an inverted banyan tree with ultimate roots above in divine consciousness and branches spreading downward into sensory experience."
    },
    {
      concept: "The Weapon of Detachment (Asanga-Shastra)",
      sanskritTerm: "असङ्गशस्त्र",
      explanation: "Secondary roots of material attachment are severed at the base using the razor-sharp, unbreakable weapon of non-attachment."
    },
    {
      concept: "The Microscopic Divine Spark (Jivatma-Amsha)",
      sanskritTerm: "ममैवांश",
      explanation: "The individual soul is an eternal fragment of the Supreme Divine Source operating a six-part mental and sensory suit."
    },
    {
      concept: "The Three-Tier Metaphysical Triad (Kshara, Akshara, Purushottama)",
      sanskritTerm: "पुरुषोत्तम",
      explanation: "Reality is classified into Kshara (perishable matter), Akshara (imperishable substrate), and Purushottama (the Supreme Transcendent Being)."
    },
    {
      concept: "The Internal Divine Presence (Antaryami-Tattva)",
      sanskritTerm: "वैश्वानर",
      explanation: "The Supreme Being is seated in the heart of all entities as the metabolic fire Vaishvanara and the source of memory, wisdom, and elimination."
    }
  ],
  studentTakeaways: [
    {
      title: "Cut Through Secondary Roots of Distraction",
      actionableAdvice: "Use the sharp blade of conscious detachment (Asanga) to immediately cut away toxic habits rather than negotiating with them."
    },
    {
      title: "Stop Identifying as Biological Hardware",
      actionableAdvice: "Remind yourself daily that you are an eternal fragment of divine consciousness operating a temporary mental suit."
    },
    {
      title: "Honor Internal Metabolic and Cognitive Engines",
      actionableAdvice: "Recognize that your digestive system is a divine furnace (Vaishvanara) and cognitive faculties are powered by the heart's divine presence."
    },
    {
      title: "Develop the Eye of Wisdom (Jnana-Chakshu)",
      actionableAdvice: "Train your intellect to perceive the immortal observing spirit operating inside yourself and every person you encounter."
    },
    {
      title: "Anchor Yourself in the Unshakeable (Purushottama)",
      actionableAdvice: "When physical circumstances undergo violent change, step back and anchor your identity in Purushottama."
    }
  ],
  advancedSkillsMastery: {
    criticalThinking: {
      title: "Critical Thinking Mastery",
      description: "Root-Cause Inversion Analysis and Ontological Categorization Matrix.",
      techniques: [
        "Trace surface leaves and secondary branches up to the primary foundational assumptions driving a complex system.",
        "Categorize inputs into Kshara (perishable decay), Akshara (stable constraints), and Purushottama (sustaining intent)."
      ]
    },
    metacognition: {
      title: "Metacognition Mastery",
      description: "Central Operator Attentional Protocol and Cognitive Function Tracking.",
      techniques: [
        "Observe sensory inputs from the 'central operator room' of pure witness awareness without absorbing emotional turbulence.",
        "Track how memory, synthesis, and elimination occur automatically without personal ego strain."
      ]
    },
    deception: {
      title: "Deception & Anti-Deception Mastery",
      description: "Deconstructing Illusion through Asanga-Shastra and Kshara-Akshara Auditing.",
      techniques: [
        "Slice through false narratives by refusing to engage with illusory premises and demanding first-principles truth.",
        "Audit offerings to verify whether they rest on shifting Kshara sands or Purushottama foundational truth."
      ]
    }
  }
};
"""

if "const ch16Data" not in content:
    idx_map = content.find("export const GITA_PART_1_FULL_TEXT")
    content = content[:idx_map] + data_definitions + "\n" + content[idx_map:]

# 3. Add 16: ch16Data, and 17: ch17Data, to GITA_PART_1_FULL_TEXT map
if "16: ch16Data" not in content:
    idx_15 = content.find("15: ch15Data,")
    if idx_15 != -1:
        insert_pos = idx_15 + len("15: ch15Data,")
        content = content[:insert_pos] + "\n  16: ch16Data,\n  17: ch17Data," + content[insert_pos:]

with open(part1_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated part1.ts successfully!")
