import json
import os
import re

ch14_shlokas_data = [
    {
        "number": 1,
        "devanagari": "श्रीभगवानुवाच |\nपरं भूयः प्रवक्ष्यामि ज्ञानानां ज्ञानमुत्तमम् |\nयज्ज्ञात्वा मुनयः सर्वे परां सिद्धिमितो गताः || १ ||",
        "englishScript": "śrī-bhagavān uvāca\nparaṁ bhūyaḥ pravakṣyāmi jñānānāṁ jñānam uttamam\nyaj jñātvā munayaḥ sarve parāṁ siddhim ito gatāḥ (14.1)",
        "translation": "The Supreme Lord said: I shall again declare to you that supreme wisdom, the best of all knowledge, knowing which all the sages have attained the highest perfection beyond this earthly existence.",
        "sentences": [
            "Imagine standing in front of a giant factory control panel that governs every single thought, feeling, impulse, and action inside your human machine.",
            "Have you ever wondered why your mind suddenly feels crystal clear on some mornings, completely hyperactive on afternoons, and hopelessly heavy or sluggish by nightfall?",
            "This chapter opens the master manual to the fundamental physics of inner experience.",
            "When we talk about Jnana, we are not talking about storing dry facts inside a filing cabinet in your brain.",
            "We are talking about Uttama Jnana, the ultimate operational insight that reveals the hidden mechanisms driving all human behavior.",
            "Think of reality as a vast ocean where every wave looks unique, yet every wave is made of the identical underlying water molecules.",
            "The ancient sages, known as Munis, were not passive dreamers sitting under trees; they were relentless empirical researchers studying the nature of consciousness.",
            "They sought Parama Siddhi, which means absolute mastery over the internal machinery of existence.",
            "If you do not understand the underlying software running your mind, you will constantly mistake external circumstances for the cause of your mood.",
            "When an engine sputters, a master mechanic does not beat the engine with a stick; they look inside at the fuel ratio, spark plugs, and air intake.",
            "Similarly, your internal experience is governed by precise, predictable operational laws of Prakriti, which is material nature.",
            "The Lord begins by emphasizing that this supreme knowledge is not a matter of dogmatic belief, but of direct structural observation.",
            "Once you grasp this foundational framework, you stop blaming the outside world for your internal chaos.",
            "You begin to look past the surface noise of life to see the deep structural blueprint operating underneath.",
            "This awareness acts as an invisible key that unlocks total freedom from emotional volatility.",
            "Every single thinker who achieved true inner liberation throughout history relied on this exact structural breakdown.",
            "By uncovering how nature manipulates your perception, you move from being a helpless passenger to becoming the conscious driver of your destiny.",
            "Nature operates through quiet, continuous mechanical forces that function whether you notice them or not.",
            "The purpose of this teaching is to make the invisible visible, giving you direct access to the control switches of your own mind.",
            "It requires intense curiosity and a refusal to settle for surface-level explanations of why you act the way you act.",
            "When you master this principle, confusion evaporates because you finally see the hidden gears turning behind every thought.",
            "This opening declaration sets the stage for a complete breakdown of the three universal energies that construct your daily reality.",
            "Understanding these operational laws gives you immediate clarity on why mental clarity fluctuates from hour to hour.",
            "You begin to realize that your mental states are engineered outcomes rather than random accidents.",
            "This knowledge allows you to approach self-improvement with the precision of an engineer tuning a high-performance engine.",
            "Instead of fighting your emotions with brute force, you learn to adjust the underlying variables that create those emotions.",
            "This intellectual breakthrough grants you unshakeable confidence in navigating high-pressure situations.",
            "You become intensely curious about observing your internal machinery in real time without judgment.",
            "The journey to self-mastery begins with this single, powerful shift in perspective.",
            "By mastering this supreme wisdom, you unlock the door to absolute psychological freedom.",
            "Let us now dive deep into the specific mechanisms that govern these internal states."
        ]
    },
    {
        "number": 2,
        "devanagari": "इदं ज्ञानमुपाश्रित्य मम साधर्म्यमागताः |\nसर्गेऽपि नोपजायन्ते प्रलये न व्यथन्ति च || २ ||",
        "englishScript": "idaṁ jñānam upāśritya mama sādharmyam āgatāḥ\nsarge 'pi nopajāyante pralaye na vyathanti ca (14.2)",
        "translation": "By taking refuge in this knowledge, having attained unity with My divine nature, they are neither born at the time of creation nor are they disturbed at the time of dissolution.",
        "sentences": [
            "Consider a heavy anchor dropped deep into the solid bedrock of the ocean floor while a violent hurricane rages across the surface.",
            "The surface water might crash into giant chaotic waves, but the anchor remains completely motionless down in the stillness of the abyss.",
            "This shloka introduces the profound concept of Sadharmyam, which means attaining identity with the unshakeable, non-material essence of existence.",
            "When an individual shelters within this deep structural realization, they no longer get swept away by the endless cycles of birth and destruction happening around them.",
            "The word Sarga represents the cycle of creation, expansion, and high-energy manifestation.",
            "Conversely, Pralaya represents dissolution, collapse, breakdown, and quiet withdrawal.",
            "Most human beings live on an intense emotional roller coaster because their internal state is completely tied to external cycles of growth and decay.",
            "When things expand, they feel extreme excitement; when things collapse, they suffer devastating agony and mental breakdown.",
            "But when you anchor yourself in the timeless awareness of Adhyatma, the rise and fall of external events loses its power to disrupt your core.",
            "Think of a movie screen showing a raging fire followed by a torrential downpour; the screen itself never burns, nor does it ever get wet.",
            "The observer who understands this principle sees that the physical universe is an ongoing dynamic play of temporary forms.",
            "This level of mastery prevents you from panicking when projects fail, structures collapse, or life undergoes violent disruption.",
            "It grants an unyielding psychological immunity against the chaos of environmental instability.",
            "You stop identifying as a fragile, perishable vessel caught in a storm, recognizing yourself instead as the vast space in which the storm occurs.",
            "This transformation does not make you cold or indifferent; rather, it gives you absolute stability to act effectively while others panic.",
            "Imagine watching a high-stakes drama while knowing with one hundred percent certainty that it is merely a projected illusion.",
            "You remain fully engaged in the moment, yet completely free from terror or devastation.",
            "The mind that reaches Sadharmyam remains untouched during cosmic expansion and unfazed during cosmic collapse.",
            "This state of unshakeable poise is the ultimate goal of all serious inquiry into the nature of reality.",
            "By mastering this perspective, you gain the power to stand firm regardless of how wildly the world oscillates around you.",
            "External cycles of success and failure lose their ability to define your intrinsic self-worth.",
            "You develop a calm, objective attitude toward macro-level economic and environmental shifts.",
            "This equanimity acts as a protective shield for your emotional and mental health.",
            "You begin to observe life's ups and downs with the detachment of an expert scientist monitoring laboratory data.",
            "This level of mental clarity enables optimal decision-making under conditions of extreme uncertainty.",
            "You no longer waste vital energy agonizing over uncontrollable external disruptions.",
            "Your attention stays focused on executing your immediate duties with calm precision.",
            "This stability becomes an inspiration to those struggling around you in chaotic environments.",
            "By anchoring your awareness in eternal reality, you transcend the paralyzing fear of change.",
            "This is the true meaning of attaining unity with divine nature.",
            "Now let us examine how material creation itself comes into existence."
        ]
    }
]

print("Script template ready")
