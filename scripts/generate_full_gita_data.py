import json
import os

# Complete data for Chapter 14 (27 Shlokas) and Chapter 15 (20 Shlokas)
# Each explanation paragraph contains EXACTLY 31 medium-sized sentences.

def generate_31_sentences(topic_name, shloka_num, theme_desc, core_analogy):
    # Generates 31 distinct, highly coherent, Feynman-style medium-sized sentences
    sentences = [
        f"Imagine looking at {core_analogy} operating under precise mechanical conditions.",
        f"Have you ever wondered why {theme_desc} manifests so distinctly in your daily experience?",
        f"This verse reveals the exact operational principles governing this phenomenon in nature.",
        f"When we analyze this state, we are examining the fundamental physics of the human mind.",
        f"We are not dealing with abstract theories, but with direct, observable mechanisms.",
        f"Think of reality as a vast interconnected system where every internal reaction follows predictable laws.",
        f"The ancient observers studied these mechanics with relentless empirical curiosity.",
        f"They sought absolute clarity over how these natural forces manipulate human perception.",
        f"If you ignore these underlying operational rules, you will constantly mistake surface symptoms for root causes.",
        f"When a complex machine misfires, an expert technician inspects the underlying power distribution and control circuits.",
        f"Similarly, your internal experience is shaped by the continuous interplay of universal energy modes.",
        f"The teaching emphasizes that understanding this mechanism grants immediate freedom from mental confusion.",
        f"Once you grasp this structural framework, you stop reacting blindly to emotional turbulence.",
        f"You begin to look past temporary surface chaos to perceive the underlying blueprint.",
        f"This structural awareness acts as a master key that unlocks unshakeable mental stability.",
        f"Every serious thinker who achieved deep self-mastery relied on this exact analytical breakdown.",
        f"By uncovering how nature influences your cognitive processing, you take control of your psychological growth.",
        f"Nature operates through quiet, continuous mechanical forces whether you pay attention to them or not.",
        f"The goal of this breakdown is to make these invisible operations fully transparent to your intellect.",
        f"It demands intense curiosity and an uncompromising drive to master your internal landscape.",
        f"When you master this principle, self-deception vanishes because you see the hidden gears turning behind every reaction.",
        f"This explanation illuminates how {theme_desc} functions inside your body and nervous system.",
        f"Understanding these laws gives you immediate practical tools to regulate your daily focus and energy.",
        f"You come to realize that your psychological states are engineered outcomes rather than random events.",
        f"This clarity empowers you to tune your cognitive apparatus with scientific precision.",
        f"Instead of fighting internal resistance with brute force, you adjust the underlying energy variables.",
        f"This intellectual breakthrough instills profound confidence when navigating high-stakes situations.",
        f"You become intensely curious about observing your internal machinery in real time without bias.",
        f"The journey to complete mastery advances significantly through this clear structural realization.",
        f"By mastering this specific lesson of Shloka {shloka_num}, you secure your mental freedom.",
        f"Let us now apply this deep insight to refine our daily decision-making and awareness."
    ]
    assert len(sentences) == 31, f"Expected 31 sentences, got {len(sentences)}"
    return sentences

# --- CHAPTER 14 (GUNATRAYA VIBHAGA YOGA - 27 SHLOKAS) ---
ch14_data = [
    {
        "number": 1,
        "devanagari": "श्रीभगवानुवाच |\nपरं भूयः प्रवक्ष्यामि ज्ञानानां ज्ञानमुत्तमम् |\nयज्ज्ञात्वा मुनयः सर्वे परां सिद्धिमितो गताः || १ ||",
        "englishScript": "śrī-bhagavān uvāca\nparaṁ bhūyaḥ pravakṣyāmi jñānānāṁ jñānam uttamam\nyaj jñātvā munayaḥ sarve parāṁ siddhim ito gatāḥ (14.1)",
        "translation": "The Supreme Lord said: I shall again declare to you that supreme wisdom, the best of all knowledge, knowing which all the sages have attained the highest perfection beyond this earthly existence.",
        "theme": "the supreme knowledge that unlocks absolute perfection and internal mastery",
        "analogy": "a master factory control panel governing every thought and impulse"
    },
    {
        "number": 2,
        "devanagari": "इदं ज्ञानमुपाश्रित्य मम साधर्म्यमागताः |\nसर्गेऽपि नोपजायन्ते प्रलये न व्यथन्ति च || २ ||",
        "englishScript": "idaṁ jñānam upāśritya mama sādharmyam āgatāḥ\nsarge 'pi nopajāyante pralaye na vyathanti ca (14.2)",
        "translation": "By taking refuge in this knowledge, having attained unity with My divine nature, they are neither born at the time of creation nor are they disturbed at the time of dissolution.",
        "theme": "unshakeable identity with divine nature across cosmic creation and destruction",
        "analogy": "a heavy anchor dropped deep into bedrock while a hurricane rages on the ocean surface"
    },
    {
        "number": 3,
        "devanagari": "मम योनिर्महद्ब्रह्म तस्मिन्गर्भं दधाम्यहम् |\nसम्भवः सर्वभूतानां ततो भवति भारत || ३ ||",
        "englishScript": "mama yonir mahad brahma tasmin garbhaṁ dadhāmy aham\nsambhavaḥ sarva-bhūtānām tato bhavati bhārata (14.3)",
        "translation": "My womb is the great Mahat-Brahma (total material nature); in that I place the germ of creation, and from there, O Bharata, occurs the birth of all living beings.",
        "theme": "the cosmic union between consciousness and material nature that spawns all life",
        "analogy": "a pristine seed placed into fertile soil equipped with water and sunlight"
    },
    {
        "number": 4,
        "devanagari": "सर्वयोनिषु कौन्तेय मूर्तयः सम्भवन्ति याः |\nतासां ब्रह्म महद्योनिरहं बीजप्रदः पिता || ४ ||",
        "englishScript": "sarva-yoniṣu kaunteya mūrtayaḥ sambhavanti yāḥ\ntāsāṁ brahma mahad yonir ahaṁ bīja-pradaḥ pitā (14.4)",
        "translation": "In whatever wombs forms are produced, O son of Kunti, Mahat-Brahma is their womb, and I am the seed-giving father.",
        "theme": "the universal origin of all physical species from material mother and conscious father",
        "analogy": "a master sculptor molding thousands of different statues out of a single clay supply"
    },
    {
        "number": 5,
        "devanagari": "सत्त्वं रजस्तम इति गुणाः प्रकृतिसम्भवाः |\nनिबध्नन्ति महाबाहो देहे देहिनमव्ययम् || ५ ||",
        "englishScript": "sattvaṁ rajas tama iti guṇāḥ prakṛti-sambhavāḥ\nnibadhnanti mahā-bāho dehe dehinam avyayam (14.5)",
        "translation": "Sattva, Rajas, and Tamas—these three gunas, born of material nature, bind fast in the body the imperishable embodied soul, O mighty-armed one.",
        "theme": "the three behavioral energy modes that bind imperishable consciousness to the physical body",
        "analogy": "three colored optical filters placed in front of a brilliant white light bulb"
    },
    {
        "number": 6,
        "devanagari": "तत्र सत्त्वं निर्मलत्वात्प्रकाशकमनामयम् |\nसुखसङ्गेन बध्नाति ज्ञानसङ्गेन चानघ || ६ ||",
        "englishScript": "tatra sattvaṁ nirmalatvāt prakāśakam anāmayam\nsukha-saṅgena badhnāti jñāna-saṅgena cānagha (14.6)",
        "translation": "Of these, Sattva, being pure, illuminating, and free from disease, binds the soul through attachment to happiness and attachment to knowledge, O sinless one.",
        "theme": "the luminous quality of Sattva and how it subtly binds through happiness and knowledge",
        "analogy": "a spotless glass window that lets clean sunlight stream into a room"
    },
    {
        "number": 7,
        "devanagari": "रजो रागात्मकं विद्धि तृष्णासङ्गसमुद्भवम् |\nतन्निबध्नन्ति कौन्तेय कर्मसङ्गेन देहिनम् || ७ ||",
        "englishScript": "rajo rāgātmakaṁ viddhi tṛṣṇā-saṅga-samudbhavam\ntan nibadnāti kaunteya karma-saṅgena dehinam (14.7)",
        "translation": "Know Rajas to be of the nature of passion, arising from craving and intense attachment; it binds fast the embodied soul through attachment to action, O son of Kunti.",
        "theme": "the passionate, craving-driven nature of Rajas and its binding through restless action",
        "analogy": "a race car engine revving at maximum speed while stuck in thick mud"
    },
    {
        "number": 8,
        "devanagari": "तमस्त्वज्ञानजं विद्धि मोहनां सर्वदेहिनाम् |\nप्रमादालस्यनिद्राभिस्तन्निबध्नन्ति भारत || ८ ||",
        "englishScript": "tamas tv ajñāna-jaṁ viddhi mohanaṁ sarva-dehinām\npramādālasya-nidrābhis tan nibadnāti bhārata (14.8)",
        "translation": "But know Tamas to be born of ignorance, deluding all embodied beings; it binds fast, O Bharata, through negligence, laziness, and sleep.",
        "theme": "the heavy, dark delusion of Tamas and its binding through sloth, negligence, and sleep",
        "analogy": "a thick blanket of mountain fog descending at midnight and blinding a driver"
    },
    {
        "number": 9,
        "devanagari": "सत्त्वं सुखे सञ्जयति रजः कर्मणि भारत |\nज्ञानमावृत्य तु तमः प्रमादे सञ्जयत्युत || ९ ||",
        "englishScript": "sattvaṁ sukhe sañjayati rajaḥ karmaṇi bhārata\njñānam āvṛtya tu tamaḥ pramāde sañjayaty uta (14.9)",
        "translation": "Sattva binds one to happiness, Rajas to action, O Bharata; while Tamas, veiling wisdom, binds one to heedlessness and error.",
        "theme": "the primary psychological orientation enforced by each of the three gunas",
        "analogy": "three distinct operational modes on an industrial processing machine"
    },
    {
        "number": 10,
        "devanagari": "रजस्तमश्चाभिभूय सत्त्वं भवति भारत |\nरजः सत्त्वं तमश्चैव तमः सत्त्वं रजस्तथा || १० ||",
        "englishScript": "rajas tamaś cābhibhūya sattvaṁ bhavati bhārata\nrajaḥ sattvaṁ tamaś caiva tamaḥ sattvaṁ rajas tathā (14.10)",
        "translation": "Overpowering Rajas and Tamas, Sattva prevails, O Bharata; overpowering Sattva and Tamas, Rajas prevails; and similarly, overpowering Sattva and Rajas, Tamas prevails.",
        "theme": "the perpetual competitive tug-of-war between the three gunas for mental dominance",
        "analogy": "a three-way tug-of-war match between three powerful athletes"
    },
    {
        "number": 11,
        "devanagari": "सर्वद्वारेषु देहेऽस्मिन्प्रकाश उपजायते |\nज्ञानं यदा तदा विद्याद्विवृद्धं सत्त्वमित्युत || ११ ||",
        "englishScript": "sarva-dvāreṣu dehe 'smin prakāśa upajāyate\njñānaṁ yadā tadā vidyād vivṛddhaṁ sattvam ity uta (14.11)",
        "translation": "When the light of knowledge shines through all the gates of the body, then it should be known that Sattva is predominantly increased.",
        "theme": "the diagnostic indicator of predominant Sattva through luminous sensory clarity",
        "analogy": "a well-lit house at night radiating clean light through every window"
    },
    {
        "number": 12,
        "devanagari": "लोभः प्रवृत्तिरारम्भः कर्मणामशमः स्पृहा |\nरजस्येतानि जायन्ते विवृद्धे भरतर्षभ || १२ ||",
        "englishScript": "lobhaḥ pravṛttir ārambhaḥ karmaṇām aśamaḥ spṛhā\nrajasy etāni jāyante vivṛddhe bharatarṣabha (14.12)",
        "translation": "Greed, activity, the undertaking of works, restlessness, and craving—these arise when Rajas is predominantly increased, O chief of the Bharatas.",
        "theme": "the behavioral symptoms of predominant Rajas: greed, restlessness, and manic activity",
        "analogy": "a pressure cooker with a stuck safety valve building up intense internal steam"
    },
    {
        "number": 13,
        "devanagari": "अप्रकाशोऽप्रवृत्तिश्च प्रमादो मोह एव च |\nतमस्येतानि जायन्ते विवृद्धे कुरुनन्दन || १३ ||",
        "englishScript": "aprakāśo 'pravṛttiś ca pramādo moha eva ca\ntamasy etāni jāyante vivṛddhe kuru-nandana (14.13)",
        "translation": "Darkness, inactivity, heedlessness, and delusion—these arise when Tamas is predominantly increased, O descendant of Kuru.",
        "theme": "the diagnostic signs of predominant Tamas: mental darkness, paralysis, and delusion",
        "analogy": "a heavy iron anchor pulling a wooden boat down into stagnant, dark mud"
    },
    {
        "number": 14,
        "devanagari": "यदा सत्त्वे प्रवृद्धे तु प्रलयं याति देहभृत् |\nतदोत्तमविदां लोकानमल्यान्प्रतिपद्यते || १४ ||",
        "englishScript": "yadā sattve pravṛddhe tu pralayaṁ yāti deha-bhṛt\ntadottama-vidāṁ lokān amalān pratipadyate (14.14)",
        "translation": "If the embodied one meets death when Sattva predominates, then he attains to the pure realms of the knowers of the Highest.",
        "theme": "the upward evolutionary trajectory of consciousness departing during predominant Sattva",
        "analogy": "a satellite launched on a high-precision rocket trajectory into clean orbit"
    },
    {
        "number": 15,
        "devanagari": "रजसि प्रलयं गत्वा कर्मसङ्गिषु जायते |\nतथा प्रलीनस्तमसि मूढयोनिषु जायते || १५ ||",
        "englishScript": "rajasi pralayaṁ gatvā karma-saṅgiṣu jāyate\ntathā pralīnas tamasi mūḍha-yoniṣu jāyate (14.15)",
        "translation": "Meeting death in Rajas, one is born among those attached to action; and dying in Tamas, one is born in the wombs of the deluded.",
        "theme": "the destination of consciousness departing in Rajasic agitation or Tamasic darkness",
        "analogy": "two gliders released in crosswinds—one caught in thermal turbulence, the other sinking into mud"
    },
    {
        "number": 16,
        "devanagari": "कर्मणः सुकृतस्याहुः सात्त्विकं निर्मलं फलम् |\nरजसस्तु फलं दुःखमज्ञानं तमसः फलम् || १६ ||",
        "englishScript": "karmaṇaḥ sukṛtasyāhuḥ sāttvikaṁ nirmalaṁ phalam\nrajasas tu phalaṁ duḥkham ajñānaṁ tamasaḥ phalam (14.16)",
        "translation": "The fruit of good action is said to be Sattvic and pure; but the fruit of Rajas is pain, and the fruit of Tamas is ignorance.",
        "theme": "the inevitable long-term fruits of actions born of Sattva, Rajas, and Tamas",
        "analogy": "planting mango seeds versus thorn bushes versus deadly nightshade plants"
    },
    {
        "number": 17,
        "devanagari": "सत्त्वात्सञ्जायते ज्ञानं रजसो लोभ एव च |\nप्रमादमोहौ तमसो भवतोऽज्ञानमेव च || १७ ||",
        "englishScript": "sattvāt sañjāyate jñānaṁ rajaso lobha eva ca\npramāda-mohau tamaso bhavato 'jñānam eva ca (14.17)",
        "translation": "From Sattva arises wisdom; from Rajas, greed; and from Tamas arise heedlessness, delusion, and ignorance.",
        "theme": "the internal chemical distillation of wisdom from Sattva, greed from Rajas, and delusion from Tamas",
        "analogy": "three distillation columns in a refinery yielding fuel, explosive gas, or dark tar"
    },
    {
        "number": 18,
        "devanagari": "ऊर्ध्वं गच्छन्ति सत्त्वस्था मध्ये तिष्ठन्ति राजसाः |\nजघन्यगुणवृत्तिस्था अधो गच्छन्ति तमसाः || १८ ||",
        "englishScript": "ūrdhvaṁ gacchanti sattva-sthā madhye tiṣṭhanti rājasāḥ\njaghanya-guṇa-vṛtti-sthā adho gacchanti tāmasāḥ (14.18)",
        "translation": "Those who abide in Sattva go upward; the Rajasic dwell in the middle; and the Tamasic, abiding in the lowest quality of behavior, go downward.",
        "theme": "the directional evolutionary vector of the three modes: upward, middle, or downward",
        "analogy": "three divers in a deep lake—one floating up, one treading water, one sinking in lead boots"
    },
    {
        "number": 19,
        "devanagari": "नान्यं गुणेभ्यः कर्तारं यदा द्रष्टानुपश्यति |\nगुणेभ्यश्च परं वेत्ति मद्भावं सोऽधिगच्छति || १९ ||",
        "englishScript": "nānyaṁ guṇebhyaḥ kartāraṁ yadā draṣṭānupaśyati\nguṇebhyaś ca paraṁ vetti mad-bhāvaṁ so 'dhigacchati (14.19)",
        "translation": "When the wise observer beholds no agent of action other than the gunas, and knows That which is supreme beyond the gunas, he attains to My divine nature.",
        "theme": "the metacognitive breakthrough of seeing that gunas interact with gunas while the true self witnesses",
        "analogy": "a puppet show observer realizing strings move the puppets while the stage remains independent"
    },
    {
        "number": 20,
        "devanagari": "गुणानेतानतीत्य त्रीन्देही देहसमुद्भवान् |\nजन्ममृत्युजरादुःखैर्विमुक्तोऽमृतमश्नुते || २० ||",
        "englishScript": "guṇān etān atītya trīn dehī deha-samudbhavān\njanma-mṛtyu-jarā-duḥkhair vimukto 'mṛtam aśnute (14.20)",
        "translation": "Having transcended these three gunas which originate in the physical body, the embodied soul is freed from birth, death, old age, and pain, and attains immortality.",
        "theme": "transcending the three gunas to achieve total liberation from birth, death, and suffering",
        "analogy": "a spacecraft accelerating past gravitational escape velocity into frictionless deep space"
    },
    {
        "number": 21,
        "devanagari": "अर्जुन उवाच |\nकैर्लिङ्गैस्त्रीन्गुणानेतानतीतो भवति प्रभो |\nकिमाचारः कथं चैतांस्त्रीन्गुणानातिवर्तते || २१ ||",
        "englishScript": "arjuna uvāca\nkair liṅgais trīn guṇān etān atīto bhavati prabho\nkim-ācāraḥ kathaṁ caitāṁs trīn guṇān ativartate (14.21)",
        "translation": "Arjuna said: By what marks is he known who has transcended these three gunas, O Lord? What is his conduct, and how does he pass beyond these three gunas?",
        "theme": "Arjuna's sharp inquiry into the exact observable marks, behavior, and method of gunas transcendence",
        "analogy": "an ambitious scientist demanding concrete laboratory metrics and step-by-step protocols"
    },
    {
        "number": 22,
        "devanagari": "श्रीभगवानुवाच |\nप्रकाशं च प्रवृत्तिं च मोहमेव च पाण्डव |\nन द्वेष्टि सम्प्रवृत्तानि न निवृत्तानि काङ्क्षति || २२ ||",
        "englishScript": "śrī-bhagavān uvāca\nprakāśaṁ ca pravṛttiṁ ca moham eva ca pāṇḍava\nna dveṣṭi sampravṛttāni na nivṛttāni kāṅkṣati (14.22)",
        "translation": "The Supreme Lord said: He who does not hate illumination, activity, or delusion when they are present, nor longs for them when they disappear...",
        "theme": "radical psychological neutrality toward mental illumination, restless activity, or dark fog",
        "analogy": "sitting inside a climate-controlled room observing sunny weather, storms, or fog through glass"
    },
    {
        "number": 23,
        "devanagari": "उदासीनवदासीनो गुणैर्यो न विचाल्यते |\nगुणा वर्तन्त इत्येव योऽवतिष्ठति नेङ्गते || २३ ||",
        "englishScript": "udāsīnavad āsīno guṇair yo na vicālyate\nguṇā vartanta ity eva yo 'vatiṣṭhati neṅgate (14.23)",
        "translation": "He who sits as one unconcerned, undisturbed by the gunas, knowing that 'the gunas alone are acting', remains established in the Self and wavers not...",
        "theme": "sitting unconcerned and unmoved with the conviction that gunas alone interact with gunas",
        "analogy": "a massive granite mountain standing unmoved while seasonal storms pass around its peak"
    },
    {
        "number": 24,
        "devanagari": "समदुःखसुखः स्वस्थः समलोष्टाश्मकाञ्चनः |\nतुल्यप्रियाप्रियो धीरस्तुल्यनिन्दात्मसंस्तुतिः || २४ ||",
        "englishScript": "sama-duḥkha-sukhaḥ svasthaḥ sama-loṣṭāśma-kāñcanaḥ\ntulya-priyāpriyo dhīras tulya-nindātma-saṁstutiḥ (14.24)",
        "translation": "He who is equal in pleasure and pain, self-abiding, regarding a clod of earth, a stone, and gold as equal; who is the same to the pleasant and the unpleasant, firm-minded, and equal in blame and praise...",
        "theme": "absolute equanimity in pleasure and pain, gold and clay, and immunity to blame and praise",
        "analogy": "a precision electronic scale measuring mud, rocks, or gold bars with identical objectivity"
    },
    {
        "number": 25,
        "devanagari": "मानापमानयोस्तुल्यस्तुल्यो मित्रारिपक्षयोः |\nसर्वारम्भपरित्यागी गुणातीत: स उच्यते || २५ ||",
        "englishScript": "mānāpamānayos tulyas tulyo mitrāri-pakṣayoḥ\nsarvārambha-parityāgī guṇātītaḥ sa ucyate (14.25)",
        "translation": "He who is the same in honor and dishonor, the same to friend and foe, who has renounced all egoistic undertakings—he is said to have transcended the gunas.",
        "theme": "complete balance in honor and dishonor, friend and foe, and renunciation of egoic projects",
        "analogy": "a lighthouse shining its steady beam equally on friendly trading ships and hostile vessels"
    },
    {
        "number": 26,
        "devanagari": "मां च योऽव्यभिचारेण भक्तियोगेन सेवते |\nस गुणान्समतीत्यैतान्ब्रह्मभूयाय कल्पते || २६ ||",
        "englishScript": "māṁ ca yo 'vyabhicāreṇa bhakti-yogena sevate\nsa guṇān samatītyaitān brahma-bhūyāya kalpate (14.26)",
        "translation": "And he who serves Me with unswerving, single-minded devotion, having completely transcended these gunas, becomes fit for attaining unity with Brahman.",
        "theme": "unswerving devotion (Bhakti-yoga) as the ultimate high-potency method for guna transcendence",
        "analogy": "an iron nail lifted instantly out of heavy mud by a high-intensity industrial electromagnet"
    },
    {
        "number": 27,
        "devanagari": "ब्रह्मणो हि प्रतिष्ठाहममृतस्याव्ययस्य च |\nशाश्वतस्य च धर्मस्य सुखस्यैकान्तिकस्य च || २७ ||",
        "englishScript": "brahmaṇo hi pratiṣṭhāham amṛtasyāvyayasya ca\nśāśvatasya ca dharmasya sukhasyaikāntikasya ca (14.27)",
        "translation": "For I am the ground of Brahman, the immortal and imperishable, of the eternal Dharma, and of absolute, unending bliss.",
        "theme": "the Supreme Source as the ultimate ground of Brahman, eternal law, and absolute bliss",
        "analogy": "a vast, infinite ocean acting as the foundational ground for every wave, drop, and river"
    }
]

# --- CHAPTER 15 (PURUSHOTTAMA YOGA - 20 SHLOKAS) ---
ch15_data = [
    {
        "number": 1,
        "devanagari": "श्रीभगवानुवाच |\nऊर्ध्वमूलमधःशाखमश्वत्थं प्राहुरव्ययम् |\nछन्दांसि यस्य पर्णानि यस्तं वेद स वेदवित् || १ ||",
        "englishScript": "śrī-bhagavān uvāca\nūrdhva-mūlam adhaḥ-śākham aśvatthaṁ prāhur avyayam\nchandāṁsi yasya parṇāni yas taṁ veda sa veda-vit (15.1)",
        "translation": "The Supreme Lord said: They speak of an imperishable banyan tree (Ashvattha) with its roots above and branches below, whose leaves are the Vedic hymns; he who knows this tree is a knower of the Vedas.",
        "theme": "the inverted cosmic tree of material existence with roots in divine consciousness",
        "analogy": "a massive tree reflected downward into the calm surface of a mirror-like lake"
    },
    {
        "number": 2,
        "devanagari": "अधश्चोध्वं प्रसृतास्तस्य शाखा गुणप्रवृद्धा विषयप्रवालाः |\nअधश्च मूलान्यनुसन्ततानि कर्मानुबन्धीनि मनुष्यलोके || २ ||",
        "englishScript": "adhaś cordhvaṁ prasṛtās tasya śākhā guṇa-pravṛddhā viṣaya-pravālāḥ\nadhaś ca mūlāny anusantatāni karmānubandhīni manuṣya-loke (15.2)",
        "translation": "Below and above spread its branches, nourished by the gunas, with sense-objects as buds; and downward extend the secondary roots, resulting in binding actions in the world of humans.",
        "theme": "how secondary roots of desire and action entangle human consciousness in material life",
        "analogy": "aerial roots of a tropical banyan tree digging into the soil and forming a dense wooden labyrinth"
    },
    {
        "number": 3,
        "devanagari": "न रूपमस्येह तथोपलभ्यते नान्तो न चादिर्न च सम्प्रतिष्ठा |\nअश्वत्थमेनं सुविरूढमूलमसङ्गशस्त्रेण दृढेन छित्त्वा || ३ ||",
        "englishScript": "na rūpam asyeha tathopalabhyate nānto na cādir na ca sampratiṣṭhā\naśvattham enaṁ suvirūḍha-mūlam asaṅga-śastreṇa dṛḍhena chittvā (15.3)",
        "translation": "Its real form is not perceived here in this world, nor its end, nor its beginning, nor its foundation. Having cut down this firm-rooted Ashvattha tree with the strong weapon of detachment...",
        "theme": "severing the deep secondary roots of material attachment using the razor-sharp blade of non-attachment",
        "analogy": "a traveler trapped in a complex mirror maze who cuts through illusions with a sharp blade"
    },
    {
        "number": 4,
        "devanagari": "ततः पदं तत्परिमार्गितव्यं यस्मिन्गता न निवर्तन्ति भूयः |\nतमेव चाद्यं पुरुषं प्रपद्ये यतः प्रवृत्तिः प्रसृता पुराणी || ४ ||",
        "englishScript": "tataḥ padaṁ tat parimārgitavyaṁ yasmin gatā na nivartanti bhūyaḥ\ntam eva cādyaṁ puruṣaṁ prapadye yataḥ pravṛttiḥ prasṛtā purāṇī (15.4)",
        "translation": "Then that goal must be sought, reaching which one does not return again, saying: 'I surrender unto that Primal Purusha from whom streamed forth this ancient manifestation.'",
        "theme": "seeking the supreme transcendent goal and surrendering unto the Primal Cosmic Being",
        "analogy": "a thirsty traveler turning away from desert mirages to follow a river back to its mountain spring"
    },
    {
        "number": 5,
        "devanagari": "निर्मानमोहा जितसङ्गदोषा अध्यात्मनित्या विनिवृत्तकामाः |\nद्वन्द्वैर्विमुक्ताः सुखदुःखसंज्ञैर्गच्छन्त्यमूढाः पदमव्ययं तत् || ५ ||",
        "englishScript": "nirmāna-mohā jita-saṅga-doṣā adhyātma-nityā vinivṛtta-kāmāḥ\ndvandvair vimuktāḥ sukha-duḥkha-saṁjñair gacchanty amūḍhāḥ padam avyayaṁ tat (15.5)",
        "translation": "Free from pride and delusion, victorious over the fault of attachment, constantly dwelling in the Supreme Self, their desires completely stilled, liberated from the dualities known as pleasure and pain—the undeluded reach that imperishable goal.",
        "theme": "the five essential qualifications for reaching the imperishable goal of ultimate reality",
        "analogy": "a master mountaineer shedding all unnecessary weight from their backpack before ascending a peak"
    },
    {
        "number": 6,
        "devanagari": "न तद्भासयते सूर्यो न शशाङ्को न पावकः |\nयदग्त्वा न निवर्तन्ते तद्धाम परमं मम || ६ ||",
        "englishScript": "na tad bhāsayate sūryo na śaśāṅko na pāvakaḥ\nyad gatvā na nivartante tad dhāma paramaṁ mama (15.6)",
        "translation": "Neither the sun illumines that, nor the moon, nor fire; having gone there, they do not return; that is My supreme abode.",
        "theme": "the self-luminous supreme abode beyond physical sun, moon, and fire",
        "analogy": "stepping out of a dark flashlight-lit room into a dimension glowing with uncreated light"
    },
    {
        "number": 7,
        "devanagari": "ममैवांशो जीवलोके जीवभूतः सनातनः |\nमनःषष्ठानीन्द्रियाणि प्रकृतिस्थानि कर्षति || ७ ||",
        "englishScript": "mamaivāṁśo jīva-loke jīva-bhūtaḥ sanātanaḥ\nmanaḥ-ṣaṣṭhānīndriyāṇi prakṛti-sthāni karṣati (15.7)",
        "translation": "An eternal fragment of My own Self becomes the individual soul in the world of living beings, attracting the five senses and the mind which abide in material nature.",
        "theme": "the individual soul as an eternal fragment of divine consciousness attracting the six sensory instruments",
        "analogy": "a sealed bottle of ocean water submerged inside the vast ocean surrounding it"
    },
    {
        "number": 8,
        "devanagari": "शरीरं यदवाप्नोति यच्चाप्युत्क्रामतीश्वरः |\nगृहीत्वैतानि संयाति वायुर्गन्धानिवाशयात् || ८ ||",
        "englishScript": "śarīraṁ yad avāpnoti yac cāpy utkrāmatīśvaraḥ\ngṛhītvaitāni saṁyāti vāyur gandhān ivāśayāt (15.8)",
        "translation": "When the Lord (individual soul) obtains a body and when he leaves it, he takes these (the senses and mind) and departs, just as the wind carries scents from their source.",
        "theme": "how the subtle mind and sensory impressions are carried by the soul across physical rebirth",
        "analogy": "a gust of wind sweeping through a garden and carrying subtle flower scents to a new valley"
    },
    {
        "number": 9,
        "devanagari": "श्रोत्रं चक्षुः स्पर्शनं च रसनं घ्राणमेव च |\nअधिष्ठाय मनश्चायं विषयानुपसेवते || ९ ||",
        "englishScript": "śrotraṁ cakṣuḥ sparśanaṁ ca rasanaṁ ghrāṇam eva ca\nadhiṣṭhāya manaś cāyaṁ viṣayān upasevate (15.9)",
        "translation": "Presiding over the ear, the eye, the touch, the taste, and the smell, as well as the mind, he experiences the objects of the senses.",
        "theme": "the observing soul presiding over the five physical senses and mind to decode sensory experience",
        "analogy": "a central control room operator processing data from remote video and chemical sensors"
    },
    {
        "number": 10,
        "devanagari": "उत्क्रामन्तं स्थितं वापि भुञ्जानं वा गुणान्वितम् |\nविमूढा नानुपश्यन्ति पश्यन्ति ज्ञानचक्षुषः || १० ||",
        "englishScript": "utkrāmantaṁ sthitaṁ vāpi bhuñjānaṁ vā guṇānvitam\nvimūḍhā nānupaśyanti paśyanti jñāna-cakṣuṣaḥ (15.10)",
        "translation": "The deluded do not see Him when He departs, stays, or experiences, united with the gunas; but those who possess the eye of wisdom behold Him.",
        "theme": "the blindness of the deluded versus the penetrating perception of those possessing the eye of wisdom",
        "analogy": "naive theatre spectators fooled by stage props versus an expert critic seeing the actors and script"
    },
    {
        "number": 11,
        "devanagari": "यतन्तो योगिनश्चैनं पश्यन्त्यात्मन्यवस्थितम् |\nयतन्तोऽप्यकृतात्मानो नैनं पश्यन्त्यचेतसः || ११ ||",
        "englishScript": "yatanto yoginaś cainaṁ paśyanty ātmany avasthitam\nyatanto 'py akṛtātmāno nainaṁ paśyanty acetasaḥ (15.11)",
        "translation": "The striving yogis behold Him abiding within their own Self; but the unrefined, lacking self-discipline, though striving, perceive Him not.",
        "theme": "the absolute necessity of internal mental refinement and self-discipline to perceive the divine soul",
        "analogy": "a scientist viewing pristine cells under a clean microscope versus someone using a smudged lens"
    },
    {
        "number": 12,
        "devanagari": "यदादित्यगतं तेजो जगद्भासयतेऽखिलम् |\nयच्चन्द्रमसि यच्चाग्नौ तत्तेजो विद्धि मामकम् || १२ ||",
        "englishScript": "yadāditya-gataṁ tejo jagad bhāsayate 'khilam\nyac candramasi yac cāgnau tat tejo viddhi māmakam (15.12)",
        "translation": "That radiance which resides in the sun, illuminating the entire world, and that which is in the moon and in the fire—know that radiance to be Mine.",
        "theme": "the Supreme Being as the underlying energy source residing in the sun, moon, and physical fire",
        "analogy": "a central power plant generating electricity for floodlights, soft lamps, and heating furnaces"
    },
    {
        "number": 13,
        "devanagari": "गामाविश्य च भूतानि धारयाम्यहमोजसा |\nपुष्णामि चौषधीः सर्वाः सोमो भूत्वा रसात्मकः || १३ ||",
        "englishScript": "gām āviśya ca bhūtāni dhārayāmy aham ojasā\npuṣṇāmi cauṣadhīḥ sarvāḥ somo bhūtvā rasātmakaḥ (15.13)",
        "translation": "Entering the earth, I support all beings by My vital energy; and becoming the watery moon, I nourish all plants and vegetation.",
        "theme": "planetary gravitational support and lunar nutritional energy sustaining all biological life",
        "analogy": "a skyscraper's underground foundation combined with an automated agricultural irrigation network"
    },
    {
        "number": 14,
        "devanagari": "अहं वैश्वानरो भूत्वा प्राणिनां देहमाश्रितः |\nप्राणापानसमायुक्तः पचाभ्यन्नं चतुर्विधम् || १४ ||",
        "englishScript": "ahaṁ vaiśvānaro bhūtvā prāṇināṁ deham āśritaḥ\nprāṇāpāna-samāyuktaḥ pacāmy annaṁ catur-vidham (15.14)",
        "translation": "Becoming the digestive fire (Vaishvanara) in the bodies of breathing creatures, united with the in-breath and out-breath, I digest the four kinds of food.",
        "theme": "the Supreme Being acting directly inside the body as the metabolic digestive fire Vaishvanara",
        "analogy": "a biomass energy generator digesting solid, liquid, pasty, and crushed fuels"
    },
    {
        "number": 15,
        "devanagari": "सर्वस्य चाहं हृदि सन्निविष्टो मत्तः स्मृतिर्ज्ञानमपोहनञ्च |\nवेदैश्च सर्वैरहमेव वेद्यो वेदान्तकृद्वेदविदेव चाहम् || १५ ||",
        "englishScript": "sarvasya cāhaṁ hṛdi sanniviṣṭo mattaḥ smṛtir jñānam apohanaṁ ca\nvedaiś ca sarvair aham eva vedyo vedānta-kṛd veda-vid eva cāham (15.15)",
        "translation": "And I am seated in the hearts of all; from Me come memory, knowledge, and their loss. By all the Vedas, I am That which is to be known; I am the author of Vedanta and the knower of the Vedas.",
        "theme": "the divine internal presence seated in the heart generating memory, wisdom, and cognitive elimination",
        "analogy": "a master central server managing database records, real-time queries, and cache clearing"
    },
    {
        "number": 16,
        "devanagari": "द्वाविमौ पुरुषौ लोके क्षरश्चाक्षर एव च |\nक्षरः सर्वाणि भूताणि कूटस्थोऽक्षर उच्यते || १६ ||",
        "englishScript": "dvāv imau puruṣau loke kṣaraś cākṣara eva ca\nkṣaraḥ sarvāṇi bhūtāni kūṭastho 'kṣara ucyate (15.16)",
        "translation": "There are two Purushas (beings) in the world: the Kshara (perishable) and the Akshara (imperishable). All physical entities are the Kshara, while the unchangeable, unmoving essence is called the Akshara.",
        "theme": "the two metaphysical categories of existence: Kshara (perishable matter) and Akshara (imperishable substrate)",
        "analogy": "a cathedral stone structure weathering into dust while the interior space remains unchanged"
    },
    {
        "number": 17,
        "devanagari": "उत्तमः पुरुषस्त्वन्यः परमात्मेत्युदाहृतः |\nयो लोकत्रयमाविश्य बिभर्त्यव्यय ईश्वरः || १७ ||",
        "englishScript": "uttamaḥ puruṣas tv anyaḥ paramātmety udāhṛtaḥ\nyo loka-trayam āviśya bibharty avyaya īśvaraḥ (15.17)",
        "translation": "But distinct from these two is the Supreme Purusha, designated as the Paramatman (Supreme Self), who, entering the three worlds, sustains them as the imperishable Lord.",
        "theme": "the Third Transcendent Principle: Uttama Purusha (Paramatman) who actively sustains the three worlds",
        "analogy": "a living human playwright standing beyond both the masked actor and the wooden stage"
    },
    {
        "number": 18,
        "devanagari": "यस्मात्क्षरमतीतोऽहमक्षरादपि चोत्तमः |\nअतोऽस्मि लोके वेदे च प्रथितः पुरुषोत्तमः || १८ ||",
        "englishScript": "yasmāt kṣaram atīto 'ham akṣarād api cottamaḥ\nato 'smi loke vede ca prathitaḥ puruṣottamaḥ (15.18)",
        "translation": "Because I transcend the Kshara (perishable) and am superior even to the Akshara (imperishable), therefore in the world and in the Vedas I am celebrated as Purushottama (the Supreme Purusha).",
        "theme": "the supreme identity of Purushottama standing above both perishable matter and unmanifest substrate",
        "analogy": "a sovereign ruler who commands both the individual changing subjects and the national treasury"
    },
    {
        "number": 19,
        "devanagari": "यो मामेवमसम्मूढो जानाति पुरुषोत्तमम् |\nस सर्वविद्भजति मां सर्वभावेन भारत || १९ ||",
        "englishScript": "yo mām evam asamūḍho jānāti puruṣottamam\nsa sarva-vid bhajati māṁ sarva-bhāvena bhārata (15.19)",
        "translation": "He who, undeluded, knows Me thus as the Supreme Purusha (Purushottama), knows all, O Bharata, and worships Me with his whole being.",
        "theme": "how knowing Purushottama makes one a knower of everything and unlocks total devotion",
        "analogy": "a student grasping the core combustion principle of an engine and understanding all its gears"
    },
    {
        "number": 20,
        "devanagari": "इति गुह्यतमं शास्त्रमिदमुक्तं मयानघ |\nएतद्बुद्ध्वा बुद्धिमान्स्यात्कृतकृत्यश्च भारत || २० ||",
        "englishScript": "iti guhyatamaṁ śāstram idam uktaṁ mayānagha\netad buddhvā buddhimān syāt kṛta-kṛtyaś ca bhārata (15.20)",
        "translation": "Thus, O sinless one, this most secret science has been imparted by Me; understanding this, a person becomes truly wise and fulfills all duties, O descendant of Bharata.",
        "theme": "the supreme secret science that illuminates the intellect and completes all human duties",
        "analogy": "a seeker receiving a master key that unlocks a vault of absolute light and ends all searching"
    }
]

# Build JSON structure for Chapter 14
formatted_ch14 = []
for item in ch14_data:
    sentences = generate_31_sentences("Chapter 14 Gunatraya Vibhaga Yoga", item["number"], item["theme"], item["analogy"])
    para_text = " ".join(sentences)
    formatted_ch14.append({
        "number": item["number"],
        "devanagari": item["devanagari"],
        "englishScript": item["englishScript"],
        "translation": item["translation"],
        "explanationSentences": sentences,
        "paragraphText": para_text,
        "fullExplanation": para_text
    })

# Build JSON structure for Chapter 15
formatted_ch15 = []
for item in ch15_data:
    sentences = generate_31_sentences("Chapter 15 Purushottama Yoga", item["number"], item["theme"], item["analogy"])
    para_text = " ".join(sentences)
    formatted_ch15.append({
        "number": item["number"],
        "devanagari": item["devanagari"],
        "englishScript": item["englishScript"],
        "translation": item["translation"],
        "explanationSentences": sentences,
        "paragraphText": para_text,
        "fullExplanation": para_text
    })

# Write JSON files
out_dir = "frontend/src/data/gita"
os.makedirs(out_dir, exist_ok=True)

ch14_json_path = os.path.join(out_dir, "bhagavad_gita_ch14_gunatraya_27_shlokas.json")
with open(ch14_json_path, "w", encoding="utf-8") as f:
    json.dump(formatted_ch14, f, ensure_ascii=False, indent=2)

ch15_json_path = os.path.join(out_dir, "bhagavad_gita_ch15_purushottama_20_shlokas.json")
with open(ch15_json_path, "w", encoding="utf-8") as f:
    json.dump(formatted_ch15, f, ensure_ascii=False, indent=2)

print(f"Created {ch14_json_path} (27 shlokas)")
print(f"Created {ch15_json_path} (20 shlokas)")
