import re

with open('scripts/build_ch18_part2.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Additions map for shlokas 51 to 78
additions = {
    63: [
        "It puts you in the driver's seat of your own consciousness, empowering you to live with deep purpose and total clarity."
    ],
    64: [
        "It provides an unshakeable foundation for navigating the uncertainties of human existence.",
        "Now let us open our hearts to absorb this supreme declaration in its full, majestic glory."
    ],
    65: [
        "This four-fold path guarantees that your mind remains calm, clear, and immensely powerful under all life circumstances.",
        "It establishes an unbreakable bridge between your daily activities and eternal supreme awareness."
    ],
    66: [
        "You step into the world as a radiant beacon of divine love, peace, and ultimate freedom."
    ],
    67: [
        "This careful filtering protects the sacred dignity of knowledge from being dragged down into futile arguments.",
        "It reminds us that genuine growth requires a willing heart, a humble mind, and a disciplined life."
    ],
    68: [
        "You become an active partner in spreading light, clarity, and peace throughout the human community.",
        "This sacred mission transforms your entire life into a glorious, continuous offering of divine service."
    ],
    69: [
        "You act as a living channel through which supreme wisdom reaches seeking hearts.",
        "This high calling elevates your daily focus far above mundane worries and petty concerns.",
        "It seals your life with the supreme blessing of eternal divine affection."
    ],
    70: [
        "This continuous intellectual sacrifice refines your cognitive faculties to their highest sharpest state.",
        "It turns your daily study room into a powerhouse of spiritual illumination and mental clarity."
    ],
    71: [
        "It proves that open-hearted sincerity is the ultimate currency in the spiritual realm.",
        "You don't need academic titles to touch the deepest truths of existence.",
        "Simply listening with faith and a clean heart opens the gates to eternal light."
    ],
    72: [
        "It challenges us to measure our learning by the real-world reduction of our daily anxiety and confusion.",
        "If our study does not shatter our delusions, we must pause and refine our attention.",
        "True education is not about accumulating information, but about eradicating internal ignorance.",
        "This relentless focus on practical outcome distinguishes authentic wisdom from hollow academic theory.",
        "It ensures that every moment spent in study yields concrete, life-transforming results."
    ],
    73: [
        "You no longer waste time complaining about circumstances or waiting for external permission.",
        "You take full ownership of your path, executing your duties with joyous, single-pointed dedication.",
        "This is the ultimate triumph of human consciousness aligned perfectly with divine truth."
    ],
    74: [
        "It reminds us that true wisdom is not a dry intellectual exercise, but a thrilling heart-expanding adventure.",
        "You feel an intense yearning to re-read and meditate on these words every single day.",
        "It elevates your emotional field, washing away mundane stress with waves of divine wonder.",
        "This hair-raising joy is the natural mark of touching authentic spiritual reality."
    ],
    75: [
        "You receive the pure, unadulterated essence of life guidance straight from the supreme source.",
        "This direct transmission eliminates all second-hand confusion and speculative human theories.",
        "It gives you total confidence to stand firm in truth, regardless of shifting societal opinions.",
        "By honoring this authentic lineage, you anchor your mind in timeless, unshakeable reality."
    ],
    76: [
        "Each time you bring these concepts back to mind, your inner peace deepens further.",
        "It forms an impenetrable shield against depression, fear, and emotional exhaustion.",
        "You develop a steady internal fountain of joy that never dries up.",
        "This continuous reflection turns your daily life into a ongoing festival of spiritual delight.",
        "It keeps your awareness firmly rooted in supreme truth from morning until night."
    ],
    77: [
        "It expands your mental horizon to embrace the entire cosmos as a single living reality.",
        "Your small personal grievances dissolve into complete insignificance before this cosmic grandeur.",
        "You feel deeply honored and privileged to exist inside this vast, beautiful universe.",
        "This grand perspective infuses your daily actions with immense dignity and quiet reverence.",
        "You move through the world with a sense of wonder that keeps your spirit perpetually young.",
        "It cures all existential loneliness by revealing your intimate connection with the cosmic whole.",
        "This visual awe seals your heart in unbroken joy and eternal gratitude."
    ],
    78: [
        "It provides an eternal blueprint for building a prosperous, ethical, and victorious human life.",
        "You step out into the world equipped with both supreme vision and relentless execution power.",
        "May this timeless wisdom guide your every step to absolute mastery and eternal freedom!"
    ]
}

# Let's inspect build_ch18_part2.py and insert sentences before the last sentence of each shloka block in additions
import eval_helper if False else None

# We can parse the file and update `shlokas_part2` dictionary directly in code!
print("Additions dictionary loaded.")
