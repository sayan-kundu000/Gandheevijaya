import os
import json
import random

def get_mcq(sub, idx, q_id, sub_upper):
    # Dictionary of MCQ templates for 35 subjects
    templates = {
        "ih": [
            {"q": "In which battle did Babur defeat Ibrahim Lodi, establishing the Mughal Empire in India?", "o": ["First Battle of Panipat", "Battle of Khanwa", "Battle of Ghaghra", "Battle of Chausa"], "c": "First Battle of Panipat", "e": "Babur defeated Ibrahim Lodi in the First Battle of Panipat in 1526."},
            {"q": "Who was the founder of the Maurya Dynasty in ancient India?", "o": ["Chandragupta Maurya", "Ashoka", "Bindusara", "Chandragupta I"], "c": "Chandragupta Maurya", "e": "Chandragupta Maurya founded the Maurya Empire in 322 BCE with the help of Chanakya."},
            {"q": "In which year did Mahatma Gandhi launch the Quit India Movement?", "o": ["1942", "1930", "1920", "1947"], "c": "1942", "e": "The Quit India Movement was launched by Mahatma Gandhi on August 8, 1942, during World War II."},
            {"q": "Which of the following is the oldest Veda in Indian literature?", "o": ["Rigveda", "Samaveda", "Yajurveda", "Atharvaveda"], "c": "Rigveda", "e": "The Rigveda is the oldest of the four Vedas and is a collection of Vedic Sanskrit hymns."},
            {"q": "Who was the Governor-General of India during the Revolt of 1857?", "o": ["Lord Canning", "Lord Dalhousie", "Lord Bentinck", "Lord Mountbatten"], "c": "Lord Canning", "e": "Lord Canning served as Governor-General during the Revolt of 1857 and became the first Viceroy of India in 1858."}
        ],
        "wh": [
            {"q": "Which event marked the beginning of the French Revolution in 1789?", "o": ["Storming of the Bastille", "Execution of Louis XVI", "Tennis Court Oath", "Reign of Terror"], "c": "Storming of the Bastille", "e": "The Storming of the Bastille on July 14, 1789, is considered the start of the French Revolution."},
            {"q": "The signing of which treaty in 1919 officially ended World War I?", "o": ["Treaty of Versailles", "Treaty of Paris", "Treaty of Geneva", "Treaty of Utrecht"], "c": "Treaty of Versailles", "e": "The Treaty of Versailles, signed in June 1919, officially concluded WWI."},
            {"q": "Who was the first President of the United States?", "o": ["George Washington", "John Adams", "Thomas Jefferson", "Abraham Lincoln"], "c": "George Washington", "e": "George Washington served as the first US President from 1789 to 1797."},
            {"q": "In which year did the Russian Revolution take place, leading to the rise of the Soviet Union?", "o": ["1917", "1905", "1921", "1914"], "c": "1917", "e": "The Russian Revolution occurred in 1917, overthrowing the monarchy and bringing Bolsheviks to power."},
            {"q": "Who was the leader of Nazi Germany during World War II?", "o": ["Adolf Hitler", "Benito Mussolini", "Joseph Stalin", "Winston Churchill"], "c": "Adolf Hitler", "e": "Adolf Hitler ruled Germany from 1933 to 1945 and initiated WWII in Europe."}
        ],
        "ig": [
            {"q": "Which is the longest river flowing entirely within India?", "o": ["Ganga", "Godavari", "Yamuna", "Narmada"], "c": "Ganga", "e": "The Ganga is the longest river in India, spanning 2525 km."},
            {"q": "Which Indian state has the longest coastline?", "o": ["Gujarat", "Andhra Pradesh", "Tamil Nadu", "Maharashtra"], "c": "Gujarat", "e": "Gujarat has the longest coastline in India, stretching over 1600 km."},
            {"q": "Which is the highest mountain peak located entirely in India?", "o": ["Kanchenjunga", "Nanda Devi", "K2", "Anamudi"], "c": "Kanchenjunga", "e": "Kanchenjunga is the highest peak in India and 3rd highest in the world, on the India-Nepal border."},
            {"q": "Which line of latitude passes through the middle of India?", "o": ["Tropic of Cancer", "Equator", "Tropic of Capricorn", "Arctic Circle"], "c": "Tropic of Cancer", "e": "The Tropic of Cancer (23.5° N) passes through 8 states in India."},
            {"q": "Which is the largest state in India by geographical area?", "o": ["Rajasthan", "Madhya Pradesh", "Maharashtra", "Uttar Pradesh"], "c": "Rajasthan", "e": "Rajasthan is the largest state in India by area, covering 342,239 sq km."}
        ],
        "wg": [
            {"q": "Which is the longest river in the world?", "o": ["Nile", "Amazon", "Yangtze", "Mississippi"], "c": "Nile", "e": "The Nile is generally considered the longest river in the world, flowing 6650 km."},
            {"q": "Which is the largest ocean in the world by surface area?", "o": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"], "c": "Pacific Ocean", "e": "The Pacific Ocean is the largest and deepest of the world's ocean divisions."},
            {"q": "Which is the deepest trench in the world's oceans?", "o": ["Mariana Trench", "Puerto Rico Trench", "Java Trench", "Tonga Trench"], "c": "Mariana Trench", "e": "The Mariana Trench in the Pacific Ocean contains the deepest known point on Earth, Challenger Deep."},
            {"q": "Which desert is the largest hot desert in the world?", "o": ["Sahara Desert", "Gobi Desert", "Kalahari Desert", "Arabian Desert"], "c": "Sahara Desert", "e": "The Sahara Desert in North Africa is the largest hot desert on Earth."},
            {"q": "What is the capital city of Australia?", "o": ["Canberra", "Sydney", "Melbourne", "Brisbane"], "c": "Canberra", "e": "Canberra is the capital city of Australia, founded in 1913 as a compromise between Sydney and Melbourne."}
        ],
        "indp": [
            {"q": "Who is considered the chief architect or father of the Indian Constitution?", "o": ["B.R. Ambedkar", "Jawaharlal Nehru", "Rajendra Prasad", "Sardar Patel"], "c": "B.R. Ambedkar", "e": "Dr. B.R. Ambedkar was the Chairman of the Drafting Committee of the Constitution."},
            {"q": "Who is known as the first citizen of India?", "o": ["President", "Prime Minister", "Chief Justice of India", "Speaker of Lok Sabha"], "c": "President", "e": "The President of India is the head of state and the first citizen of India."},
            {"q": "What is the term of office for a member of the Rajya Sabha (Upper House)?", "o": ["6 years", "5 years", "4 years", "65 years of age"], "c": "6 years", "e": "Rajya Sabha members are elected for a term of 6 years, with one-third retiring every two years."},
            {"q": "Under which Article of the Constitution can the President declare a National Emergency?", "o": ["Article 352", "Article 356", "Article 360", "Article 370"], "c": "Article 352", "e": "Article 352 deals with National Emergency due to war, external aggression, or armed rebellion."},
            {"q": "Which amendment to the Constitution is known as the 'Mini-Constitution' of India?", "o": ["42nd Amendment", "44th Amendment", "24th Amendment", "86th Amendment"], "c": "42nd Amendment", "e": "The 42nd Amendment (1976) introduced comprehensive changes and added words like secular, socialist, and integrity to the Preamble."}
        ],
        "intp": [
            {"q": "Where is the headquarters of the United Nations (UN) located?", "o": ["New York City", "Geneva", "Vienna", "London"], "c": "New York City", "e": "The UN headquarters is located in Manhattan, New York City."},
            {"q": "Which city hosts the International Court of Justice (ICJ)?", "o": ["The Hague", "Geneva", "Brussels", "New York"], "c": "The Hague", "e": "The ICJ is located in the Peace Palace in The Hague, Netherlands."},
            {"q": "How many permanent member countries are there in the United Nations Security Council?", "o": ["5", "10", "15", "6"], "c": "5", "e": "The UNSC has 5 permanent members: US, UK, China, Russia, and France."},
            {"q": "Where is the headquarters of the European Union (EU) located?", "o": ["Brussels", "Strasbourg", "Paris", "Berlin"], "c": "Brussels", "e": "The primary administrative headquarters of the EU is located in Brussels, Belgium."},
            {"q": "Which international body governs global trade rules and resolves trade disputes between nations?", "o": ["World Trade Organization (WTO)", "World Bank", "International Monetary Fund", "United Nations"], "c": "World Trade Organization (WTO)", "e": "The WTO, founded in 1995, regulates and facilitates international trade."}
        ],
        "inde": [
            {"q": "In which year was the Goods and Services Tax (GST) implemented in India?", "o": ["2017", "2016", "2015", "2018"], "c": "2017", "e": "GST was implemented in India on July 1, 2017."},
            {"q": "Who is known as the Father of the Green Revolution in India?", "o": ["M.S. Swaminathan", "Verghese Kurien", "Norman Borlaug", "Amartya Sen"], "c": "M.S. Swaminathan", "e": "Dr. M.S. Swaminathan introduced high-yielding varieties of wheat and rice in India in the 1960s."},
            {"q": "Which of the following bodies replaced the Planning Commission of India in 2015?", "o": ["NITI Aayog", "Finance Commission", "National Development Council", "GST Council"], "c": "NITI Aayog", "e": "NITI Aayog (National Institution for Transforming India) was established on January 1, 2015."},
            {"q": "What is the period of the financial year in India?", "o": ["April 1 to March 31", "January 1 to December 31", "July 1 to June 30", "October 1 to September 30"], "c": "April 1 to March 31", "e": "The financial year of the Indian Government runs from April 1 to March 31 of the next year."},
            {"q": "The 'Blue Revolution' in India is associated with the growth of which sector?", "o": ["Fish and aquaculture", "Milk production", "Fertilizers", "Oilseeds"], "c": "Fish and aquaculture", "e": "The Blue Revolution refers to the explosive growth in fish production and aquaculture."}
        ],
        "inte": [
            {"q": "Where is the headquarters of the International Monetary Fund (IMF) located?", "o": ["Washington, D.C.", "Geneva", "London", "Paris"], "c": "Washington, D.C.", "e": "The IMF is headquartered in Washington, D.C."},
            {"q": "Which currency is used by the majority of member states of the European Union?", "o": ["Euro", "Pound", "Franc", "Krona"], "c": "Euro", "e": "The Euro is the official currency of 20 of the 27 EU member states, collectively known as the Eurozone."},
            {"q": "Where is the headquarters of the Organization of the Petroleum Exporting Countries (OPEC)?", "o": ["Vienna", "Geneva", "Riyadh", "Baghdad"], "c": "Vienna", "e": "OPEC is headquartered in Vienna, Austria, even though Austria is not a member country."},
            {"q": "Which two organizations are known as the 'Bretton Woods Twins'?", "o": ["IMF and World Bank", "UN and WTO", "IMF and WTO", "World Bank and WTO"], "c": "IMF and World Bank", "e": "The IMF and World Bank were both created at the Bretton Woods Conference in 1944."},
            {"q": "Which country is the largest economy in the world by nominal GDP?", "o": ["United States", "China", "Japan", "Germany"], "c": "United States", "e": "The United States is the world's largest economy by nominal GDP."}
        ],
        "bphy": [
            {"q": "What is the SI unit of force?", "o": ["Newton", "Joule", "Pascal", "Watt"], "c": "Newton", "e": "The Newton (N) is the SI unit of force, named after Sir Isaac Newton."},
            {"q": "Which instrument is used to measure electric current?", "o": ["Ammeter", "Voltmeter", "Galvanometer", "Wattmeter"], "c": "Ammeter", "e": "An ammeter is used to measure electric current in a circuit."},
            {"q": "What is the SI unit of power?", "o": ["Watt", "Joule", "Newton", "Pascal"], "c": "Watt", "e": "The Watt (W) is the SI unit of power, defined as one joule per second."},
            {"q": "Newton's First Law of Motion is also known as the Law of:", "o": ["Inertia", "Acceleration", "Action and Reaction", "Conservation of Momentum"], "c": "Inertia", "e": "Newton's first law states that an object remains in its state of rest or motion unless acted on, known as inertia."},
            {"q": "What is the speed of light in a vacuum?", "o": ["3 * 10^8 m/s", "3 * 10^6 m/s", "3 * 10^10 m/s", "1.5 * 10^8 m/s"], "c": "3 * 10^8 m/s", "e": "The speed of light in vacuum is approximately 300,000 km/s or 3 * 10^8 m/s."}
        ],
        "iphy": [
            {"q": "Which of the following represents Ohm's Law?", "o": ["V = I * R", "I = V * R", "R = V * I", "P = V * I"], "c": "V = I * R", "e": "Ohm's law states that current is directly proportional to voltage: V = IR."},
            {"q": "What is the focal length of a plane mirror?", "o": ["Infinity", "Zero", "Positive", "Negative"], "c": "Infinity", "e": "A plane mirror has no curvature, so its focal length is infinite."},
            {"q": "Which type of mirror is used as a rear-view mirror in vehicles?", "o": ["Convex mirror", "Concave mirror", "Plane mirror", "Double mirror"], "c": "Convex mirror", "e": "Convex mirrors give a wider field of view and form diminished, erect images, making them ideal for vehicles."},
            {"q": "What is the unit of electrical resistance?", "o": ["Ohm", "Ampere", "Volt", "Coulomb"], "c": "Ohm", "e": "The Ohm is the SI unit of electrical resistance."},
            {"q": "Which parameter remains constant in an isothermal process?", "o": ["Temperature", "Pressure", "Volume", "Entropy"], "c": "Temperature", "e": "An isothermal process occurs at a constant temperature."}
        ],
        "aphy": [
            {"q": "Who proposed the special theory of relativity in 1905?", "o": ["Albert Einstein", "Isaac Newton", "Max Planck", "Niels Bohr"], "c": "Albert Einstein", "e": "Albert Einstein published the special theory of relativity in 1905."},
            {"q": "Which particle is the carrier of the electromagnetic force?", "o": ["Photon", "Gluon", "W boson", "Graviton"], "c": "Photon", "e": "Photons are the gauge bosons that mediate the electromagnetic force."},
            {"q": "In quantum mechanics, which principle states that it is impossible to simultaneously measure position and momentum with absolute precision?", "o": ["Heisenberg Uncertainty Principle", "Pauli Exclusion Principle", "Schrodinger's Rule", "Planck's Law"], "c": "Heisenberg Uncertainty Principle", "e": "Proposed by Werner Heisenberg, the uncertainty principle limits simultaneous measurement accuracy of complementary variables."},
            {"q": "What type of semiconductor is formed by doping silicon with a trivalent impurity like Boron?", "o": ["p-type", "n-type", "Intrinsic", "Compounded"], "c": "p-type", "e": "Trivalent impurities create holes, leading to p-type (positive) charge carriers."},
            {"q": "What is the phenomenon where a materials' electrical resistance drops to zero below a critical temperature?", "o": ["Superconductivity", "Semiconductivity", "Ferromagnetism", "Thermoelectricity"], "c": "Superconductivity", "e": "Superconductivity is characterized by zero resistance and expulsion of magnetic fields (Meissner effect)."}
        ],
        "bchem": [
            {"q": "What is the chemical formula of common table salt?", "o": ["NaCl", "HCl", "NaOH", "NaHCO3"], "c": "NaCl", "e": "Table salt is Sodium Chloride (NaCl)."},
            {"q": "Which acid is present in lemons and oranges?", "o": ["Citric Acid", "Acetic Acid", "Lactic Acid", "Hydrochloric Acid"], "c": "Citric Acid", "e": "Lemons and oranges contain Citric Acid, giving them a sour taste."},
            {"q": "Which gas is dissolved in carbonated drinks (soda water) to give them fizz?", "o": ["Carbon dioxide", "Oxygen", "Nitrogen", "Hydrogen"], "c": "Carbon dioxide", "e": "Carbon dioxide gas is dissolved under pressure to create carbonation."},
            {"q": "What is the hardest natural substance found on Earth?", "o": ["Diamond", "Gold", "Iron", "Graphite"], "c": "Diamond", "e": "Diamond is an allotrope of carbon with a highly rigid lattice, making it the hardest natural material."},
            {"q": "Rusting of iron is an example of which type of chemical reaction?", "o": ["Oxidation", "Reduction", "Decomposition", "Displacement"], "c": "Oxidation", "e": "Rusting is an oxidation reaction where iron reacts with oxygen in moisture to form iron oxide."}
        ],
        "ichem": [
            {"q": "What is the value of Avogadro's constant?", "o": ["6.022 * 10^23", "6.022 * 10^22", "6.022 * 10^-23", "1.6 * 10^-19"], "c": "6.022 * 10^23", "e": "Avogadro's constant is the number of constituent particles in one mole of a substance."},
            {"q": "Which gas law states that at constant temperature, the volume of a gas is inversely proportional to its pressure?", "o": ["Boyle's Law", "Charles's Law", "Gay-Lussac's Law", "Avogadro's Law"], "c": "Boyle's Law", "e": "Boyle's law formula is P1V1 = P2V2 (inversely proportional at constant T)."},
            {"q": "What is the pH value of a neutral solution at 25°C?", "o": ["7", "0", "14", "1"], "c": "7", "e": "A pH of 7 is neutral. Below 7 is acidic, and above 7 is basic."},
            {"q": "Which element has the highest electronegativity in the periodic table?", "o": ["Fluorine", "Chlorine", "Oxygen", "Helium"], "c": "Fluorine", "e": "Fluorine has the highest electronegativity value of 3.98 on the Pauling scale."},
            {"q": "What is a substance that increases the rate of a chemical reaction without being consumed?", "o": ["Catalyst", "Reactant", "Solvent", "Inhibitor"], "c": "Catalyst", "e": "A catalyst lowers the activation energy of a reaction, speeding it up without undergoing permanent chemical change."}
        ],
        "achem": [
            {"q": "What is the hybridization of the carbon atom in methane (CH4)?", "o": ["sp3", "sp2", "sp", "dsp2"], "c": "sp3", "e": "The carbon in methane forms 4 single sigma bonds, yielding sp3 tetrahedral hybridization."},
            {"q": "Which thermodynamic quantity is a measure of the disorder or randomness of a system?", "o": ["Entropy", "Enthalpy", "Gibbs Free Energy", "Internal Energy"], "c": "Entropy", "e": "Entropy (S) measures system randomness/disorder."},
            {"q": "For a spontaneous chemical reaction at constant temperature and pressure, the change in Gibbs Free Energy (Delta G) must be:", "o": ["Negative", "Positive", "Zero", "Infinite"], "c": "Negative", "e": "Spontaneity requires Delta G < 0."},
            {"q": "Which quantum number determines the orientation of an orbital in space?", "o": ["Magnetic quantum number", "Principal quantum number", "Azimuthal quantum number", "Spin quantum number"], "c": "Magnetic quantum number", "e": "The magnetic quantum number (m) describes orbital spatial orientations under a magnetic field."},
            {"q": "What is the coordination number of atoms in a Face-Centered Cubic (FCC) unit cell?", "o": ["12", "8", "6", "4"], "c": "12", "e": "An atom in FCC is in contact with 12 nearest neighbors."}
        ],
        "bbio": [
            {"q": "Which organelle is commonly referred to as the powerhouse of the cell?", "o": ["Mitochondria", "Nucleus", "Ribosome", "Lysosome"], "c": "Mitochondria", "e": "Mitochondria generate adenosine triphosphate (ATP), the cell's energy currency."},
            {"q": "What is the green pigment in plants that absorbs light during photosynthesis?", "o": ["Chlorophyll", "Carotenoid", "Xanthophyll", "Hemoglobin"], "c": "Chlorophyll", "e": "Chlorophyll absorbs red and blue light, reflecting green light and driving photosynthesis."},
            {"q": "Which tissue in plants is responsible for transporting water and dissolved minerals from roots to leaves?", "o": ["Xylem", "Phloem", "Parenchyma", "Sclerenchyma"], "c": "Xylem", "e": "Xylem vessels conduct water upward, whereas Phloem transports food/sugar downward."},
            {"q": "What is the basic structural and functional unit of all living organisms?", "o": ["Cell", "Tissue", "Organ", "Gene"], "c": "Cell", "e": "The cell is the basic building block of life."},
            {"q": "Which organ in the human body secretes bile juice?", "o": ["Liver", "Gallbladder", "Pancreas", "Stomach"], "c": "Liver", "e": "The liver produces bile juice, which is stored in the gallbladder and aids in fat digestion."}
        ],
        "ibio": [
            {"q": "Who is known as the father of modern genetics for his work on pea plants?", "o": ["Gregor Mendel", "Charles Darwin", "Louis Pasteur", "Watson and Crick"], "c": "Gregor Mendel", "e": "Gregor Mendel discovered the laws of inheritance through breeding garden peas."},
            {"q": "Which of the following is a fat-soluble vitamin?", "o": ["Vitamin A", "Vitamin C", "Vitamin B1", "Vitamin B12"], "c": "Vitamin A", "e": "Vitamins A, D, E, and K are fat-soluble. Vitamins B and C are water-soluble."},
            {"q": "What is the primary function of insulin in the human body?", "o": ["Lower blood glucose levels", "Raise blood glucose levels", "Digest proteins", "Increase heart rate"], "c": "Lower blood glucose levels", "e": "Insulin, secreted by the pancreas, facilitates glucose uptake by cells, lowering blood sugar."},
            {"q": "Which hormone is commonly called the 'fight-or-flight' hormone?", "o": ["Adrenaline", "Thyroxine", "Insulin", "Estrogen"], "c": "Adrenaline", "e": "Adrenaline (epinephrine), released by adrenal glands, prepares the body for rapid action under stress."},
            {"q": "What is the structural model of DNA discovered by Watson and Crick in 1953?", "o": ["Double Helix", "Single Strand", "Triple Helix", "Alpha Sheet"], "c": "Double Helix", "e": "Watson and Crick solved the double-helix structure of DNA using X-ray diffraction data."}
        ],
        "abio": [
            {"q": "Where does the Krebs cycle (citric acid cycle) take place within eukaryotic cells?", "o": ["Mitochondrial matrix", "Cytoplasm", "Ribosome", "Endoplasmic reticulum"], "c": "Mitochondrial matrix", "e": "The Krebs cycle reactions occur in the fluid matrix inside mitochondria."},
            {"q": "Which enzyme is responsible for unwinding the DNA double helix during replication?", "o": ["Helicase", "Polymerase", "Ligase", "Primase"], "c": "Helicase", "e": "DNA Helicase breaks hydrogen bonds to unwind and separate DNA strands."},
            {"q": "What type of RNA molecule carries amino acids to the ribosome during translation?", "o": ["tRNA", "mRNA", "rRNA", "snRNA"], "c": "tRNA", "e": "tRNA (transfer RNA) matches anticodons to mRNA codons and delivers corresponding amino acids."},
            {"q": "Which technique is used to edit genes with high precision by cutting DNA sequences?", "o": ["CRISPR-Cas9", "PCR", "Western Blot", "Electrophoresis"], "c": "CRISPR-Cas9", "e": "CRISPR-Cas9 acts as programmable genetic scissors to modify DNA in living cells."},
            {"q": "Which hormone is primarily responsible for promoting cell division and growth in plants?", "o": ["Auxin", "Cytokinin", "Gibberellin", "Abscisic Acid"], "c": "Cytokinin", "e": "Cytokinins promote cytokinesis (cell division) and are active in growing plant tissues."}
        ],
        "blit": [
            {"q": "Who wrote the famous tragedy play 'Hamlet'?", "o": ["William Shakespeare", "Christopher Marlowe", "John Milton", "Ben Jonson"], "c": "William Shakespeare", "e": "Hamlet was written by William Shakespeare around 1599-1601."},
            {"q": "Who is the author of the 'Harry Potter' fantasy novel series?", "o": ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "C.S. Lewis"], "c": "J.K. Rowling", "e": "J.K. Rowling wrote the 7-book Harry Potter series starting in 1997."},
            {"q": "Who is traditionally recognized as the author of the ancient Indian epic 'Ramayana'?", "o": ["Valmiki", "Vyasa", "Kalidasa", "Tulsidas"], "c": "Valmiki", "e": "Sage Valmiki is revered as the Adi Kavi and author of the epic Ramayana."},
            {"q": "Which famous novel features the characters Elizabeth Bennet and Mr. Darcy?", "o": ["Pride and Prejudice", "Jane Eyre", "Wuthering Heights", "Sense and Sensibility"], "c": "Pride and Prejudice", "e": "Jane Austen's classic novel Pride and Prejudice (1813) centers on Elizabeth Bennet and Darcy."},
            {"q": "Who is the creator of the fictional detective Sherlock Holmes?", "o": ["Arthur Conan Doyle", "Agatha Christie", "Edgar Allan Poe", "Stephen King"], "c": "Arthur Conan Doyle", "e": "Sherlock Holmes was created by Scottish writer Sir Arthur Conan Doyle in 1887."}
        ],
        "ilit": [
            {"q": "Which Indian writer won the Nobel Prize in Literature in 1913 for his work 'Gitanjali'?", "o": ["Rabindranath Tagore", "R.K. Narayan", "Sarojini Naidu", "Mulk Raj Anand"], "c": "Rabindranath Tagore", "e": "Tagore was the first non-European to win a Nobel Prize, awarded for Gitanjali in 1913."},
            {"q": "Who wrote the historical book 'The Discovery of India' during his imprisonment?", "o": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "Bal Gangadhar Tilak"], "c": "Jawaharlal Nehru", "e": "Nehru wrote The Discovery of India while imprisoned at Ahmednagar Fort (1942-1946)."},
            {"q": "Who is the author of the classic collection of Indian fables 'Panchatantra'?", "o": ["Vishnu Sharma", "Chanakya", "Kalidasa", "Banabhatta"], "c": "Vishnu Sharma", "e": "Panchatantra is attributed to Pandit Vishnu Sharma in the 3rd century BCE."},
            {"q": "Which novel by George Orwell depicts a dystopian society ruled by 'Big Brother'?", "o": ["1984", "Animal Farm", "Brave New World", "Fahrenheit 451"], "c": "1984", "e": "Orwell's 1984 (published in 1949) introduced concepts like Big Brother, doublethink, and newspeak."},
            {"q": "Who wrote the Russian epic novel 'War and Peace'?", "o": ["Leo Tolstoy", "Fyodor Dostoevsky", "Anton Chekhov", "Alexander Pushkin"], "c": "Leo Tolstoy", "e": "War and Peace, tracing Napoleonic invasion of Russia, was written by Leo Tolstoy in 1869."}
        ],
        "alit": [
            {"q": "Which poet wrote the famous modernist poem 'The Waste Land' in 1922?", "o": ["T.S. Eliot", "W.B. Yeats", "Ezra Pound", "Robert Frost"], "c": "T.S. Eliot", "e": "The Waste Land is a landmark modernist work written by T.S. Eliot."},
            {"q": "Who wrote the landmark Latin American novel 'One Hundred Years of Solitude'?", "o": ["Gabriel Garcia Marquez", "Jorge Luis Borges", "Pablo Neruda", "Mario Vargas Llosa"], "c": "Gabriel Garcia Marquez", "e": "Marquez, a Colombian author, published the magical realist novel in 1967."},
            {"q": "Which novel won Arundhati Roy the Booker Prize in 1997?", "o": ["The God of Small Things", "The White Tiger", "Midnight's Children", "The Inheritance of Loss"], "c": "The God of Small Things", "e": "Arundhati Roy's debut novel won the Booker Prize in 1997."},
            {"q": "Which figure of speech involves an explicit comparison using words like 'like' or 'as'?", "o": ["Simile", "Metaphor", "Personification", "Hyperbole"], "c": "Simile", "e": "A simile compares two things using 'like' or 'as'. Metaphor makes direct comparison without these words."},
            {"q": "Who is the author of the classic epic poem 'Paradise Lost'?", "o": ["John Milton", "Dante Alighieri", "Homer", "Virgil"], "c": "John Milton", "e": "John Milton wrote the blank-verse epic Paradise Lost, published in 1667."}
        ],
        "indfirst": [
            {"q": "Who was the first President of independent India?", "o": ["Rajendra Prasad", "Sardar Patel", "Jawaharlal Nehru", "S. Radhakrishnan"], "c": "Rajendra Prasad", "e": "Dr. Rajendra Prasad served as President from 1950 to 1962."},
            {"q": "Who was the first Indian in space, traveling aboard Soyuz T-11 in 1984?", "o": ["Rakesh Sharma", "Ravish Malhotra", "Kalpana Chawla", "Sunita Williams"], "c": "Rakesh Sharma", "e": "Squadron Leader Rakesh Sharma spent 7 days in space in April 1984."},
            {"q": "Who was the first Indian to win a Nobel Prize?", "o": ["Rabindranath Tagore", "C.V. Raman", "Mother Teresa", "Hargobind Khorana"], "c": "Rabindranath Tagore", "e": "Tagore won the Nobel Prize in Literature in 1913."},
            {"q": "Who was the first female Prime Minister of India?", "o": ["Indira Gandhi", "Pratibha Patil", "Sarojini Naidu", "Sucheta Kripalani"], "c": "Indira Gandhi", "e": "Indira Gandhi served as Prime Minister from 1966 to 1977 and 1980 to 1984."},
            {"q": "What was the name of India's first indigenously built satellite, launched in 1975?", "o": ["Aryabhata", "Rohini", "Apple", "Bhaskara"], "c": "Aryabhata", "e": "Aryabhata was launched by Soviet Union on April 19, 1975."}
        ],
        "intfirst": [
            {"q": "Who was the first human to land on the Moon, during the Apollo 11 mission in 1969?", "o": ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"], "c": "Neil Armstrong", "e": "Neil Armstrong stepped onto the Moon's surface on July 20, 1969."},
            {"q": "Who was the first person to travel into space in 1961?", "o": ["Yuri Gagarin", "Alan Shepard", "John Glenn", "Neil Armstrong"], "c": "Yuri Gagarin", "e": "Soviet cosmonaut Yuri Gagarin orbited the Earth in Vostok 1 on April 12, 1961."},
            {"q": "Which country hosted the first modern Olympic Games in 1896?", "o": ["Greece", "France", "United Kingdom", "United States"], "c": "Greece", "e": "The 1896 Summer Olympics were held in Athens, Greece."},
            {"q": "Who was the first woman Prime Minister in the world, elected in Sri Lanka in 1960?", "o": ["Sirimavo Bandaranaike", "Indira Gandhi", "Margaret Thatcher", "Golda Meir"], "c": "Sirimavo Bandaranaike", "e": "Sirimavo Bandaranaike became PM of Ceylon (Sri Lanka) on July 21, 1960."},
            {"q": "Which explorer's expedition was the first to circumnavigate the globe?", "o": ["Ferdinand Magellan", "Christopher Columbus", "Vasco da Gama", "James Cook"], "c": "Ferdinand Magellan", "e": "Magellan's expedition circumnavigated the globe from 1519 to 1522 (completed by Juan Sebastian Elcano)."}
        ],
        "indlaws": [
            {"q": "In which year did the Right to Information (RTI) Act come into force in India?", "o": ["2005", "2000", "2010", "2002"], "c": "2005", "e": "The RTI Act was enacted on June 15, 2005, and came into force on October 12, 2005."},
            {"q": "In which year was the first Consumer Protection Act enacted in India?", "o": ["1986", "2019", "1996", "2005"], "c": "1986", "e": "The Consumer Protection Act was passed in December 1986 to protect consumers' interests."},
            {"q": "The Indian Penal Code (IPC), enacted in 1860, was drafted under the chairmanship of:", "o": ["Lord Macaulay", "Lord Bentinck", "Lord Cornwallis", "Lord Canning"], "c": "Lord Macaulay", "e": "The first Law Commission, chaired by Thomas Babington Macaulay, prepared the draft IPC."},
            {"q": "In which year was the Environment Protection Act passed in India, following the Bhopal Gas Tragedy?", "o": ["1986", "1972", "1981", "1992"], "c": "1986", "e": "The Environment Protection Act was enacted in 1986 under Article 253 of the Constitution."},
            {"q": "In which year was the Wildlife Protection Act passed in India to protect wild animals and plants?", "o": ["1972", "1980", "1986", "1992"], "c": "1972", "e": "The Wildlife Protection Act, 1972 provides a legal framework for wildlife protection."}
        ],
        "intlaws": [
            {"q": "The Geneva Conventions are international treaties that primarily focus on:", "o": ["Treatment of war victims and prisoners", "Global environmental protection", "International trade and tariffs", "Outer space exploration boundaries"], "c": "Treatment of war victims and prisoners", "e": "The four Geneva Conventions define international law standards for humanitarian treatment in war."},
            {"q": "In which year was the Universal Declaration of Human Rights (UDHR) adopted by the UN General Assembly?", "o": ["1948", "1945", "1950", "1966"], "c": "1948", "e": "The UDHR was adopted on December 10, 1948, at the Palais de Chaillot in Paris."},
            {"q": "What is the main objective of the Kyoto Protocol, adopted in 1997?", "o": ["Reducing greenhouse gas emissions", "Preventing nuclear proliferation", "Banning ozone-depleting substances", "Protecting endangered marine life"], "c": "Reducing greenhouse gas emissions", "e": "The Kyoto Protocol commits state parties to reduce greenhouse gas emissions based on global warming theories."},
            {"q": "Which treaty governs international maritime activities and borders, establishing Exclusive Economic Zones (EEZ)?", "o": ["UNCLOS", "Kyoto Protocol", "Geneva Accord", "Treaty of Rome"], "c": "UNCLOS", "e": "The United Nations Convention on the Law of the Sea (UNCLOS) regulates maritime boundaries."},
            {"q": "Which international agreement, signed in 2015, aims to limit global warming to well below 2 (preferably 1.5) degrees Celsius?", "o": ["Paris Agreement", "Kyoto Protocol", "Montreal Protocol", "Copenhagen Accord"], "c": "Paris Agreement", "e": "The Paris Agreement is a legally binding international treaty on climate change adopted at COP21."}
        ],
        "dates": [
            {"q": "On which day is National Science Day celebrated in India to mark the discovery of the Raman Effect?", "o": ["February 28", "January 12", "June 5", "August 29"], "c": "February 28", "e": "National Science Day is celebrated on Feb 28 to honor Sir C.V. Raman's discovery in 1928."},
            {"q": "On which day is World Environment Day celebrated globally?", "o": ["June 5", "April 22", "September 16", "October 4"], "c": "June 5", "e": "World Environment Day is celebrated on June 5, established by the UN in 1972."},
            {"q": "National Youth Day in India is celebrated on January 12 to commemorate the birth anniversary of:", "o": ["Swami Vivekananda", "Bhagat Singh", "Subhas Chandra Bose", "Jawaharlal Nehru"], "c": "Swami Vivekananda", "e": "National Youth Day honors Swami Vivekananda, born on Jan 12, 1863."},
            {"q": "On which day is International Women's Day celebrated annually?", "o": ["March 8", "February 13", "April 7", "May 1"], "c": "March 8", "e": "International Women's Day is celebrated on March 8 to focus on women's rights and achievements."},
            {"q": "International Day of Yoga is celebrated annually on:", "o": ["June 21", "June 5", "May 21", "July 21"], "c": "June 21", "e": "The UN declared June 21 as International Yoga Day in 2014, following a proposal by India."}
        ],
        "nicknames": [
            {"q": "Which freedom fighter is widely known as the 'Iron Man of India'?", "o": ["Sardar Vallabhbhai Patel", "Bal Gangadhar Tilak", "Lala Lajpat Rai", "Subhas Chandra Bose"], "c": "Sardar Vallabhbhai Patel", "e": "Sardar Patel earned the nickname for his role in integrating princely states into India."},
            {"q": "Which Indian city is famously known as the 'Pink City'?", "o": ["Jaipur", "Jodhpur", "Udaipur", "Jaisalmer"], "c": "Jaipur", "e": "Jaipur was painted pink in 1876 to welcome Prince Albert, giving it the nickname."},
            {"q": "Which state of India is known as the 'Land of Five Rivers'?", "o": ["Punjab", "Haryana", "Uttar Pradesh", "Himachal Pradesh"], "c": "Punjab", "e": "Punjab derives its name from 'Panj' (five) and 'Ab' (water), referring to five rivers: Beas, Chenab, Jhelum, Ravi, and Sutlej."},
            {"q": "Who was given the nickname 'Nightingale of India' (Bharat Kokila) by Mahatma Gandhi?", "o": ["Sarojini Naidu", "Lata Mangeshkar", "M.S. Subbulakshmi", "Indira Gandhi"], "c": "Sarojini Naidu", "e": "Sarojini Naidu was named the Nightingale of India for her beautiful poetry."},
            {"q": "Who is known as the 'Grand Old Man of India'?", "o": ["Dadabhai Naoroji", "Gopal Krishna Gokhale", "Bal Gangadhar Tilak", "Mahadev Govind Ranade"], "c": "Dadabhai Naoroji", "e": "Dadabhai Naoroji was a prominent nationalist leader and the first Indian to be a British MP."}
        ],
        "orgs": [
            {"q": "Where is the headquarters of the World Health Organization (WHO) located?", "o": ["Geneva", "Paris", "New York", "Vienna"], "c": "Geneva", "e": "WHO is headquartered in Geneva, Switzerland, founded in 1948."},
            {"q": "Where is the headquarters of UNESCO (United Nations Educational, Scientific and Cultural Organization) located?", "o": ["Paris", "Geneva", "London", "Rome"], "c": "Paris", "e": "UNESCO is headquartered in Paris, France."},
            {"q": "Where is the headquarters of SAARC (South Asian Association for Regional Cooperation) located?", "o": ["Kathmandu", "New Delhi", "Dhaka", "Colombo"], "c": "Kathmandu", "e": "The SAARC Secretariat was established in Kathmandu, Nepal, in 1987."},
            {"q": "Where is the headquarters of INTERPOL (International Criminal Police Organization) located?", "o": ["Lyon", "Paris", "Geneva", "Brussels"], "c": "Lyon", "e": "INTERPOL is headquartered in Lyon, France."},
            {"q": "Where is the headquarters of ASEAN (Association of Southeast Asian Nations) located?", "o": ["Jakarta", "Bangkok", "Singapore", "Manila"], "c": "Jakarta", "e": "ASEAN is headquartered in Jakarta, Indonesia."}
        ],
        "awards": [
            {"q": "What is the highest civilian award in India?", "o": ["Bharat Ratna", "Padma Vibhushan", "Param Vir Chakra", "Sahitya Akademi Award"], "c": "Bharat Ratna", "e": "Bharat Ratna, instituted in 1954, is the highest civilian honor in India."},
            {"q": "Which is the highest sporting honor in India, renamed in 2021 after a legendary hockey player?", "o": ["Major Dhyan Chand Khel Ratna", "Arjuna Award", "Dronacharya Award", "Dhyan Chand Award"], "c": "Major Dhyan Chand Khel Ratna", "e": "The Khel Ratna award was renamed in 2021 in honor of hockey legend Major Dhyan Chand."},
            {"q": "In which year were the first Nobel Prizes awarded?", "o": ["1901", "1900", "1911", "1954"], "c": "1901", "e": "The first Nobel Prizes were awarded in 1901 in physics, chemistry, medicine, literature, and peace."},
            {"q": "Which award is considered the highest honor in the global film industry, first presented in 1929?", "o": ["Academy Award (Oscar)", "Golden Globe", "BAFTA", "Palme d'Or"], "c": "Academy Award (Oscar)", "e": "The Academy Awards (Oscars) were first presented in May 1929 by the Academy of Motion Picture Arts and Sciences."},
            {"q": "The Booker Prize is awarded annually for the best original novel written in English and published in:", "o": ["UK or Ireland", "Worldwide", "Commonwealth nations", "United States"], "c": "UK or Ireland", "e": "The Booker Prize is open to writers of any nationality, for novels published in the UK or Ireland."}
        ],
        "records": [
            {"q": "What is the tallest building in the world?", "o": ["Burj Khalifa", "Shanghai Tower", "Abraj Al Bait", "Ping An Finance Centre"], "c": "Burj Khalifa", "e": "Burj Khalifa in Dubai, UAE, is the tallest structure in the world at 828 meters."},
            {"q": "Which is the largest hot desert in the world?", "o": ["Sahara Desert", "Gobi Desert", "Kalahari Desert", "Arabian Desert"], "c": "Sahara Desert", "e": "The Sahara in North Africa is the largest hot desert (Antarctica/Arctic are larger but cold deserts)."},
            {"q": "Which is the highest waterfall in the world?", "o": ["Angel Falls", "Tugela Falls", "Niagara Falls", "Victoria Falls"], "c": "Angel Falls", "e": "Angel Falls in Venezuela is the highest uninterrupted waterfall at 979 meters."},
            {"q": "Which river delta is the largest in the world, formed by the Ganga and Brahmaputra rivers?", "o": ["Sundarbans Delta", "Mississippi Delta", "Nile Delta", "Amazon Delta"], "c": "Sundarbans Delta", "e": "The Sundarbans Delta in India/Bangladesh is the largest river delta on Earth."},
            {"q": "Which is the deepest lake in the world?", "o": ["Lake Baikal", "Lake Tanganyika", "Caspian Sea", "Lake Superior"], "c": "Lake Baikal", "e": "Lake Baikal in Russia is the deepest lake in the world, reaching 1642 meters."}
        ],
        "sports": [
            {"q": "What is the length of a standard cricket pitch (between wickets) in yards?", "o": ["22 yards", "20 yards", "24 yards", "21 yards"], "c": "22 yards", "e": "A cricket pitch is exactly 22 yards (or 66 feet) long."},
            {"q": "Which country won the first-ever FIFA World Cup in 1930?", "o": ["Uruguay", "Argentina", "Brazil", "Italy"], "c": "Uruguay", "e": "Uruguay hosted and won the inaugural FIFA World Cup in 1930."},
            {"q": "How many rings are featured on the official Olympic flag?", "o": ["5", "6", "4", "7"], "c": "5", "e": "The Olympic flag has 5 interlocking rings representing the five inhabited continents."},
            {"q": "Who is the first cricketer to score 100 international centuries?", "o": ["Sachin Tendulkar", "Virat Kohli", "Ricky Ponting", "Jacques Kallis"], "c": "Sachin Tendulkar", "e": "Sachin Tendulkar scored 51 Test and 49 ODI centuries during his career."},
            {"q": "How many players are on the court/field for one team in a standard basketball game?", "o": ["5", "6", "7", "11"], "c": "5", "e": "A standard basketball game has 5 players on the court for each team."}
        ],
        "indent": [
            {"q": "Which was the first Indian talkie (sound) film, released in 1931?", "o": ["Alam Ara", "Raja Harishchandra", "Kisan Kanya", "Devdas"], "c": "Alam Ara", "e": "Alam Ara, directed by Ardeshir Irani, was the first Indian film with sound."},
            {"q": "Which was the first Indian silent feature film, released in 1913?", "o": ["Raja Harishchandra", "Alam Ara", "Kisan Kanya", "Shree Pundalik"], "c": "Raja Harishchandra", "e": "Raja Harishchandra, directed by Dadasaheb Phalke, was the first silent feature film."},
            {"q": "Who was the first Indian to win an Academy Award (Oscar)?", "o": ["Bhanu Athaiya", "Satyajit Ray", "A.R. Rahman", "Gulzar"], "c": "Bhanu Athaiya", "e": "Bhanu Athaiya won the Oscar for Best Costume Design for the film 'Gandhi' in 1983."},
            {"q": "Who is widely recognized as the 'Father of Indian Cinema'?", "o": ["Dadasaheb Phalke", "Satyajit Ray", "Raj Kapoor", "Ardeshir Irani"], "c": "Dadasaheb Phalke", "e": "Dadasaheb Phalke made India's first feature film and laid the foundation for the industry."},
            {"q": "Which Indian film is currently the highest-grossing film worldwide?", "o": ["Dangal", "Baahubali 2", "RRR", "K.G.F: Chapter 2"], "c": "Dangal", "e": "Dangal (2016) is the highest-grossing Indian film, earning over 2000 crore INR worldwide."}
        ],
        "intent": [
            {"q": "Who directed the blockbuster film 'Titanic' (1997) and 'Avatar' (2009)?", "o": ["James Cameron", "Steven Spielberg", "Christopher Nolan", "Martin Scorsese"], "c": "James Cameron", "e": "James Cameron directed Titanic and Avatar, two of the highest-grossing films of all time."},
            {"q": "Which film won the most Oscars in history, tying at 11 awards?", "o": ["Titanic", "The Godfather", "Avatar", "Jurassic Park"], "c": "Titanic", "e": "Ben-Hur, Titanic, and Lord of the Rings: The Return of the King are tied for the record with 11 Oscars."},
            {"q": "Who directed the mind-bending sci-fi movies 'Inception' (2010) and 'Interstellar' (2014)?", "o": ["Christopher Nolan", "James Cameron", "Quentin Tarantino", "David Fincher"], "c": "Christopher Nolan", "e": "Christopher Nolan directed Inception, Interstellar, and Oppenheimer."},
            {"q": "Which is the highest-grossing film of all time worldwide (not adjusted for inflation)?", "o": ["Avatar", "Avengers: Endgame", "Titanic", "Star Wars: The Force Awakens"], "c": "Avatar", "e": "James Cameron's Avatar (2009) is the highest-grossing film of all time."},
            {"q": "Which was the first full-length cell-animated feature film in history, released in 1937?", "o": ["Snow White and the Seven Dwarfs", "Pinocchio", "Fantasia", "Dumbo"], "c": "Snow White and the Seven Dwarfs", "e": "Walt Disney's Snow White was the first full-length cel-animated feature film."}
        ],
        "bcurra": [
            {"q": "Who is the current President of India (as of 2026)?", "o": ["Droupadi Murmu", "Ram Nath Kovind", "Jagdeep Dhankhar", "Pratibha Patil"], "c": "Droupadi Murmu", "e": "Smt. Droupadi Murmu assumed office as the 15th President of India in July 2022."},
            {"q": "Which country hosted the G20 Summit in September 2023?", "o": ["India", "Brazil", "Indonesia", "South Africa"], "c": "India", "e": "India hosted the 18th G20 Summit in New Delhi in September 2023."},
            {"q": "Who is the current Prime Minister of India (as of 2026)?", "o": ["Narendra Modi", "Rahul Gandhi", "Amit Shah", "Manmohan Singh"], "c": "Narendra Modi", "e": "Narendra Modi has been Prime Minister since May 2014."},
            {"q": "Which country won the ICC Men's T20 World Cup in June 2024?", "o": ["India", "South Africa", "Australia", "England"], "c": "India", "e": "India won the T20 World Cup by defeating South Africa in the final in Barbados in June 2024."},
            {"q": "Which city hosted the Summer Olympic Games in 2024?", "o": ["Paris", "Tokyo", "Los Angeles", "London"], "c": "Paris", "e": "Paris hosted the 2024 Summer Olympics from July 26 to August 11, 2024."}
        ],
        "icurra": [
            {"q": "Who is the current Chief Justice of India (as of early 2026)?", "o": ["Sanjiv Khanna", "D.Y. Chandrachud", "U.U. Lalit", "N.V. Ramana"], "c": "Sanjiv Khanna", "e": "Justice Sanjiv Khanna succeeded Justice D.Y. Chandrachud as CJI in November 2024."},
            {"q": "Who is the current President of the World Bank (as of 2026)?", "o": ["Ajay Banga", "David Malpass", "Kristalina Georgieva", "Jim Yong Kim"], "c": "Ajay Banga", "e": "Ajay Banga assumed office as President of the World Bank in June 2023."},
            {"q": "Who serves as the Chairperson of the NITI Aayog?", "o": ["Prime Minister", "Finance Minister", "President", "Vice President"], "c": "Prime Minister", "e": "The Prime Minister of India is the ex-officio Chairperson of NITI Aayog."},
            {"q": "In which year did India successfully launch its third lunar exploration mission, Chandrayaan-3?", "o": ["2023", "2022", "2024", "2021"], "c": "2023", "e": "Chandrayaan-3 was launched in July 2023 and successfully landed on the lunar south pole region on August 23, 2023."},
            {"q": "India has set a target to achieve net-zero carbon emissions by which year?", "o": ["2070", "2050", "2030", "2060"], "c": "2070", "e": "India announced its target to achieve net-zero carbon emissions by 2070 at the COP26 summit."}
        ],
        "acurra": [
            {"q": "Who is the Chairman of the 16th Finance Commission of India, constituted in late 2023?", "o": ["Arvind Panagariya", "N.K. Singh", "Y.V. Reddy", "C. Rangarajan"], "c": "Arvind Panagariya", "e": "Dr. Arvind Panagariya was appointed as the Chairman of the 16th Finance Commission."},
            {"q": "Which nation hosted the COP28 UN Climate Change Conference in late 2023?", "o": ["United Arab Emirates (UAE)", "Egypt", "United Kingdom", "Azerbaijan"], "c": "United Arab Emirates (UAE)", "e": "COP28 was held in Expo City, Dubai, UAE, from November 30 to December 13, 2023."},
            {"q": "How many new countries joined as full members of the BRICS grouping in January 2024?", "o": ["5", "4", "6", "3"], "c": "5", "e": "Egypt, Ethiopia, Iran, Saudi Arabia, and UAE joined BRICS as full members in January 2024."},
            {"q": "India has set a target of achieving 'Viksit Bharat' (Developed India) by which year?", "o": ["2047", "2050", "2030", "2040"], "c": "2047", "e": "The 'Viksit Bharat @ 2047' initiative aims to make India a developed nation by the centenary of its independence."},
            {"q": "Which city is hosting the COP29 UN Climate Change Conference in late 2024?", "o": ["Baku", "Dubai", "Glasgow", "Belém"], "c": "Baku", "e": "COP29 is scheduled to be held in Baku, Azerbaijan, in November 2024."}
        ]
    }
    
    t_list = templates[sub]
    t = t_list[idx % len(t_list)]
    options = t["o"][:]
    correct = t["c"]
    random.seed(idx)
    random.shuffle(options)
    correct_letter = chr(65 + options.index(correct))
    
    return {
        "id": q_id, "subject": sub_upper, "topic": "General Knowledge", "subtopic": None,
        "difficulty": diff_label(q_id), "type": "MCQ", "question": t["q"], "options": options,
        "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
    }, {"id": q_id, "correct_answer": correct_letter}, {"id": q_id, "explanation": t["e"]}

def diff_label(q_id):
    parts = q_id.split("-")
    if len(parts) >= 3:
        lbl = parts[2].lower()
        if lbl == "e": return "easy"
        if lbl == "m": return "medium"
        if lbl == "h": return "hard"
    return "easy"

def get_msq(sub, idx, q_id, sub_upper):
    templates = {
        "ih": [
            {"q": "Which of the following are leaders associated with the Indian National Congress in its early moderate phase?", "o": ["Dadabhai Naoroji", "Gopal Krishna Gokhale", "W.C. Bonnerjee", "Bal Gangadhar Tilak"], "c": ["A", "B", "C"], "e": "Naoroji, Gokhale, and Bonnerjee were moderates. Tilak was a prominent extremist leader."},
            {"q": "Which of the following are recognized Harappan (Indus Valley) civilization sites located in present-day India?", "o": ["Lothal", "Kalibangan", "Rakhigarhi", "Mohenjo-daro"], "c": ["A", "B", "C"], "e": "Lothal (Gujarat), Kalibangan (Rajasthan), and Rakhigarhi (Haryana) are in India. Mohenjo-daro is in Pakistan."}
        ],
        "wh": [
            {"q": "Which of the following countries were part of the Allied Powers during World War II?", "o": ["United States", "United Kingdom", "Soviet Union", "Japan"], "c": ["A", "B", "C"], "e": "US, UK, and Soviet Union were Allies. Japan was an Axis power."},
            {"q": "Which of the following factors contributed directly to the outbreak of the French Revolution in 1789?", "o": ["Financial bankruptcy of the French treasury", "Social inequality of the Estate system", "Influence of Enlightenment ideas", "The rise of Napoleon Bonaparte"], "c": ["A", "B", "C"], "e": "Bankruptcy, inequality, and Enlightenment ideas caused the revolution. Napoleon rose to power after the revolution."}
        ],
        "ig": [
            {"q": "Which of the following Indian states share a geographical border with Nepal?", "o": ["Uttarakhand", "Uttar Pradesh", "Bihar", "Himachal Pradesh"], "c": ["A", "B", "C"], "e": "Uttarakhand, UP, and Bihar border Nepal. Himachal Pradesh does not (separated by Uttarakhand)."},
            {"q": "Which of the following rivers flow directly into the Arabian Sea?", "o": ["Narmada", "Tapi", "Sabarmati", "Godavari"], "c": ["A", "B", "C"], "e": "Narmada, Tapi, and Sabarmati flow west into the Arabian Sea. Godavari flows east into the Bay of Bengal."}
        ],
        "wg": [
            {"q": "Which of the following countries are located in South America?", "o": ["Brazil", "Argentina", "Colombia", "Mexico"], "c": ["A", "B", "C"], "e": "Brazil, Argentina, and Colombia are in South America. Mexico is in North America."},
            {"q": "Which of the following oceans border the continent of Africa?", "o": ["Atlantic Ocean", "Indian Ocean", "Southern Ocean", "Pacific Ocean"], "c": ["A", "B", "C"], "e": "Africa is bordered by the Atlantic (West), Indian (East), and Southern (South) oceans. The Pacific does not border Africa."}
        ],
        "indp": [
            {"q": "Which of the following are Fundamental Rights guaranteed under the Constitution of India?", "o": ["Right to Equality", "Right to Freedom", "Right against Exploitation", "Right to Property"], "c": ["A", "B", "C"], "e": "Equality, Freedom, and exploitation rights are fundamental rights. Right to property was removed from fundamental rights by the 44th Amendment in 1978 (now a legal right under Article 300A)."},
            {"q": "Which of the following are defined as organs of the state under the Indian Constitution?", "o": ["Legislature", "Executive", "Judiciary", "Press (Fourth Estate)"], "c": ["A", "B", "C"], "e": "Legislature, Executive, and Judiciary are the three formal organs of the state. Press is colloquially the fourth estate but not a formal state organ."}
        ],
        "intp": [
            {"q": "Which of the following countries are permanent members of the United Nations Security Council (UNSC)?", "o": ["United States", "United Kingdom", "Russian Federation", "India"], "c": ["A", "B", "C"], "e": "US, UK, and Russia are permanent members (along with France and China). India is not a permanent member."},
            {"q": "Which of the following are principal organs of the United Nations?", "o": ["General Assembly", "Security Council", "International Court of Justice", "World Health Organization (WHO)"], "c": ["A", "B", "C"], "e": "General Assembly, Security Council, and ICJ are principal organs. WHO is a specialized agency, not a principal organ."}
        ],
        "inde": [
            {"q": "Which of the following are sectors of the Indian economy based on economic activities?", "o": ["Primary Sector (Agriculture)", "Secondary Sector (Manufacturing)", "Tertiary Sector (Services)", "Quaternary Sector (Research)"], "c": ["A", "B", "C", "D"], "e": "All four represent standard divisions of economic activities."},
            {"q": "Which of the following are classified as Direct Taxes in India?", "o": ["Income Tax", "Corporate Tax", "Goods and Services Tax (GST)", "Customs Duty"], "c": ["A", "B"], "e": "Income and Corporate taxes are paid directly by individuals/entities. GST and Customs are indirect taxes."}
        ],
        "inte": [
            {"q": "Which of the following currencies are part of the IMF's Special Drawing Rights (SDR) basket?", "o": ["US Dollar", "Euro", "Chinese Renminbi", "Indian Rupee"], "c": ["A", "B", "C"], "e": "The SDR basket contains US Dollar, Euro, Renminbi, Japanese Yen, and British Pound. Indian Rupee is not in the basket."},
            {"q": "Which of the following organizations are part of the World Bank Group?", "o": ["International Bank for Reconstruction and Development (IBRD)", "International Development Association (IDA)", "International Finance Corporation (IFC)", "International Monetary Fund (IMF)"], "c": ["A", "B", "C"], "e": "IBRD, IDA, and IFC are part of the World Bank Group. The IMF is a separate sister institution."}
        ],
        "bphy": [
            {"q": "Which of the following are fundamental SI units?", "o": ["Meter (length)", "Kilogram (mass)", "Second (time)", "Newton (force)"], "c": ["A", "B", "C"], "e": "Meter, Kilogram, and Second are fundamental SI units. The Newton is a derived unit (kg m/s^2)."},
            {"q": "Which of the following physical quantities are scalar quantities?", "o": ["Mass", "Temperature", "Time", "Velocity"], "c": ["A", "B", "C"], "e": "Mass, Temperature, and Time have magnitude only (scalars). Velocity has direction and magnitude (vector)."}
        ],
        "iphy": [
            {"q": "Which of the following factors affect the electrical resistance of a cylindrical conductor?", "o": ["Length of the conductor", "Cross-sectional area of the conductor", "Resistivity of the material", "Applied voltage across the conductor"], "c": ["A", "B", "C"], "e": "Resistance R = rho * L / A. Applied voltage affects current but does not change the physical resistance of the conductor."},
            {"q": "Which of the following waves are part of the electromagnetic spectrum?", "o": ["X-rays", "Ultraviolet rays", "Radio waves", "Sound waves"], "c": ["A", "B", "C"], "e": "X-rays, UV, and Radio waves are EM waves traveling at speed of light. Sound waves are mechanical longitudinal waves."}
        ],
        "aphy": [
            {"q": "Which of the following are core principles of Quantum Mechanics?", "o": ["Wave-particle duality", "Superposition principle", "Heisenberg uncertainty principle", "Newtonian determinism"], "c": ["A", "B", "C"], "e": "Duality, superposition, and uncertainty are quantum principles. Classical Newtonian determinism does not hold at the quantum scale."},
            {"q": "Which of the following elementary particles are classified as quarks?", "o": ["Up quark", "Down quark", "Strange quark", "Electron"], "c": ["A", "B", "C"], "e": "Up, Down, and Strange are quarks that compose hadrons. The electron is a lepton, not a quark."}
        ],
        "bchem": [
            {"q": "Which of the following elements are classified as noble gases?", "o": ["Helium", "Neon", "Argon", "Oxygen"], "c": ["A", "B", "C"], "e": "Helium, Neon, and Argon are chemically inert noble gases in Group 18. Oxygen is a reactive non-metal in Group 16."},
            {"q": "Which of the following are subatomic particles found in a standard atom?", "o": ["Proton", "Neutron", "Electron", "Molecule"], "c": ["A", "B", "C"], "e": "Protons, neutrons, and electrons are subatomic particles. A molecule is a chemical structure made of atoms."}
        ],
        "ichem": [
            {"q": "Which of the following factors increase the rate of a chemical reaction?", "o": ["Increasing reactant concentration", "Increasing temperature", "Adding a suitable catalyst", "Increasing activation energy"], "c": ["A", "B", "C"], "e": "Concentration, temp, and catalysts increase reaction rate. Higher activation energy slows down a reaction."},
            {"q": "Which of the following elements belong to the Halogen family (Group 17)?", "o": ["Fluorine", "Chlorine", "Bromine", "Argon"], "c": ["A", "B", "C"], "e": "Fluorine, Chlorine, and Bromine are halogens. Argon is a noble gas."}
        ],
        "achem": [
            {"q": "Which of the following factors favor a spontaneous chemical reaction at all temperatures?", "o": ["Exothermic reaction (Delta H < 0)", "Increase in entropy (Delta S > 0)", "Endothermic reaction (Delta H > 0)", "Decrease in entropy (Delta S < 0)"], "c": ["A", "B"], "e": "Spontaneity requires Delta G = Delta H - T*Delta S < 0. This is always true if Delta H < 0 and Delta S > 0."},
            {"q": "Which of the following are types of structural isomerism in organic chemistry?", "o": ["Chain isomerism", "Position isomerism", "Functional isomerism", "Geometric isomerism"], "c": ["A", "B", "C"], "e": "Chain, Position, and Functional are structural isomers. Geometric (cis/trans) isomerism is a type of stereoisomerism."}
        ],
        "bbio": [
            {"q": "Which of the following structures are found in plant cells but NOT in animal cells?", "o": ["Cell wall", "Chloroplasts", "Large central vacuole", "Centrioles"], "c": ["A", "B", "C"], "e": "Plant cells have cell walls, chloroplasts, and large vacuoles. Centrioles are found in animal cells to help organize cell division."},
            {"q": "Which of the following are major functions of the human liver?", "o": ["Bile production", "Detoxification of chemicals", "Glycogen storage", "Secretes insulin"], "c": ["A", "B", "C"], "e": "The liver produces bile, detoxifies, and stores glycogen. Insulin is secreted by the pancreas."}
        ],
        "ibio": [
            {"q": "Which of the following vitamins are fat-soluble?", "o": ["Vitamin A", "Vitamin D", "Vitamin E", "Vitamin C"], "c": ["A", "B", "C"], "e": "Vitamins A, D, E, and K are fat-soluble. Vitamin C is water-soluble."},
            {"q": "Which of the following are functions of the human kidneys?", "o": ["Excreting metabolic wastes", "Regulating blood pressure via renin", "Maintaining acid-base balance", "Producing bile"], "c": ["A", "B", "C"], "e": "Kidneys filter waste, regulate BP, and maintain pH. The liver produces bile."}
        ],
        "abio": [
            {"q": "Which of the following are stages of aerobic cellular respiration?", "o": ["Glycolysis", "Krebs Cycle", "Electron Transport Chain", "Light Reactions"], "c": ["A", "B", "C"], "e": "Glycolysis, Krebs, and ETC are cellular respiration stages. Light reactions are part of photosynthesis."},
            {"q": "Which of the following enzymes are involved in DNA replication?", "o": ["DNA Helicase", "DNA Polymerase", "DNA Ligase", "Amylase"], "c": ["A", "B", "C"], "e": "Helicase, Polymerase, and Ligase are DNA replication enzymes. Amylase is a digestive enzyme."}
        ],
        "blit": [
            {"q": "Which of the following plays were written by William Shakespeare?", "o": ["Romeo and Juliet", "Macbeth", "Othello", "Doctor Faustus"], "c": ["A", "B", "C"], "e": "Romeo and Juliet, Macbeth, and Othello are by Shakespeare. Doctor Faustus was written by Christopher Marlowe."},
            {"q": "Which of the following books were written by Charles Dickens?", "o": ["Oliver Twist", "David Copperfield", "A Tale of Two Cities", "Pride and Prejudice"], "c": ["A", "B", "C"], "e": "Oliver Twist, David Copperfield, and A Tale of Two Cities are by Dickens. Pride and Prejudice is by Jane Austen."}
        ],
        "ilit": [
            {"q": "Which of the following works were authored by Rabindranath Tagore?", "o": ["Gitanjali", "Gora", "The Home and the World", "The Guide"], "c": ["A", "B", "C"], "e": "Gitanjali, Gora, and The Home and the World are by Tagore. The Guide was written by R.K. Narayan."},
            {"q": "Which of the following novels were written by George Orwell?", "o": ["1984", "Animal Farm", "Homage to Catalonia", "Brave New World"], "c": ["A", "B", "C"], "e": "1984, Animal Farm, and Homage to Catalonia are by Orwell. Brave New World was written by Aldous Huxley."}
        ],
        "alit": [
            {"q": "Which of the following poems were written by T.S. Eliot?", "o": ["The Waste Land", "The Love Song of J. Alfred Prufrock", "Four Quartets", "The Second Coming"], "c": ["A", "B", "C"], "e": "The Waste Land, Prufrock, and Four Quartets are by Eliot. The Second Coming was written by W.B. Yeats."},
            {"q": "Which of the following writers have won the Booker Prize?", "o": ["Arundhati Roy", "Salman Rushdie", "Kiran Desai", "Rabindranath Tagore"], "c": ["A", "B", "C"], "e": "Roy (1997), Rushdie (1981), and Desai (2006) won the Booker Prize. Tagore won the Nobel Prize, not the Booker."}
        ],
        "indfirst": [
            {"q": "Which of the following leaders were recipient of the first Bharat Ratna award in 1954?", "o": ["C. Rajagopalachari", "S. Radhakrishnan", "C.V. Raman", "Jawaharlal Nehru"], "c": ["A", "B", "C"], "e": "The first recipients in 1954 were Rajagopalachari, Radhakrishnan, and Raman. Nehru received it in 1955."},
            {"q": "Which of the following represent the first successful space missions/satellites of India?", "o": ["Aryabhata (first satellite)", "Rohini (first satellite in orbit by Indian vehicle)", "Chandrayaan-1 (first lunar mission)", "Gaganyaan (crewed spaceflight)"], "c": ["A", "B", "C"], "e": "Aryabhata, Rohini, and Chandrayaan-1 are completed firsts. Gaganyaan is an upcoming crewed spaceflight mission."}
        ],
        "intfirst": [
            {"q": "Which of the following astronauts walked on the Moon during the Apollo 11 mission?", "o": ["Neil Armstrong", "Buzz Aldrin", "Michael Collins", "Yuri Gagarin"], "c": ["A", "B"], "e": "Armstrong and Aldrin walked on the Moon. Collins remained in orbit in the command module. Gagarin was the first man in space, not on the Moon."},
            {"q": "Which of the following represent firsts in global women political leadership?", "o": ["Sirimavo Bandaranaike (first female PM)", "Indira Gandhi (first female PM of India)", "Margaret Thatcher (first female PM of UK)", "Kamala Harris (first female President of US)"], "c": ["A", "B", "C"], "e": "Bandaranaike, Gandhi, and Thatcher are verified female prime minister firsts. Harris is Vice President, not President."}
        ],
        "indlaws": [
            {"q": "Which of the following are key features of the Right to Information (RTI) Act, 2005?", "o": ["Applies to all public authorities", "Information must be provided within 30 days in normal cases", "Allows citizens to inspect public works and documents", "Applies to private business secrets without public interest"], "c": ["A", "B", "C"], "e": "RTI applies to public authorities, has a 30-day timeline, and allows inspection. It protects trade secrets of private entities unless public interest warrants disclosure."},
            {"q": "Which of the following laws were enacted in India for environmental protection?", "o": ["Wildlife Protection Act, 1972", "Water Prevention and Control of Pollution Act, 1974", "Forest Conservation Act, 1980", "Right to Education Act, 2009"], "c": ["A", "B", "C"], "e": "Wildlife, Water, and Forest acts protect the environment. RTE is an educational right law."}
        ],
        "intlaws": [
            {"q": "Which of the following are recognized sources of International Law?", "o": ["International treaties and conventions", "International custom (general practice)", "General principles of law recognized by civilized nations", "Decisions of national municipal courts strictly"], "c": ["A", "B", "C"], "e": "Treaties, custom, and general principles are primary sources. National municipal court decisions are only subsidiary aids, not primary sources."},
            {"q": "Which of the following treaties focus on international environmental cooperation?", "o": ["Kyoto Protocol", "Paris Agreement", "Montreal Protocol", "Geneva Convention"], "c": ["A", "B", "C"], "e": "Kyoto, Paris (climate), and Montreal (ozone) are environmental treaties. The Geneva Convention deals with humanitarian rules of war."}
        ],
        "dates": [
            {"q": "Which of the following important days are celebrated in the month of June?", "o": ["World Environment Day (June 5)", "International Day of Yoga (June 21)", "World Oceans Day (June 8)", "National Science Day (February 28)"], "c": ["A", "B", "C"], "e": "Environment, Yoga, and Oceans days are in June. National Science Day is on Feb 28."},
            {"q": "Which of the following international days are dedicated to health issues?", "o": ["World Health Day (April 7)", "World AIDS Day (December 1)", "World Diabetes Day (November 14)", "International Women's Day (March 8)"], "c": ["A", "B", "C"], "e": "Health, AIDS, and Diabetes days are health-focused. Women's day is for gender equality and rights."}
        ],
        "nicknames": [
            {"q": "Which of the following cities in India are correctly matched with their popular nicknames?", "o": ["Jaipur - Pink City", "Bengaluru - Silicon Valley of India", "Udaipur - City of Lakes", "Kolkata - City of Joy"], "c": ["A", "B", "C", "D"], "e": "All four pairings represent correct and widely accepted nicknames of Indian cities."},
            {"q": "Which of the following national leaders are correctly matched with their nicknames?", "o": ["Sardar Patel - Iron Man of India", "Dadabhai Naoroji - Grand Old Man of India", "Subhas Chandra Bose - Netaji", "Jawaharlal Nehru - Chacha"], "c": ["A", "B", "C", "D"], "e": "All four pairings are correct."}
        ],
        "orgs": [
            {"q": "Which of the following international organizations are headquartered in Geneva, Switzerland?", "o": ["World Health Organization (WHO)", "World Trade Organization (WTO)", "International Labour Organization (ILO)", "UNESCO"], "c": ["A", "B", "C"], "e": "WHO, WTO, and ILO are in Geneva. UNESCO is in Paris."},
            {"q": "Which of the following countries are members of the South Asian Association for Regional Cooperation (SAARC)?", "o": ["India", "Pakistan", "Afghanistan", "Myanmar"], "c": ["A", "B", "C"], "e": "SAARC members include India, Pakistan, Afghanistan, Bangladesh, Bhutan, Maldives, Nepal, and Sri Lanka. Myanmar is not a member."}
        ],
        "awards": [
            {"q": "Which of the following are categories in which the Nobel Prize is awarded annually?", "o": ["Physics", "Chemistry", "Physiology or Medicine", "Mathematics"], "c": ["A", "B", "C"], "e": "Nobel Prizes are awarded in Physics, Chemistry, Medicine, Literature, Peace, and Economics. There is no Nobel Prize for Mathematics (the Abel Prize is equivalent)."},
            {"q": "Which of the following represent gallantry awards in India?", "o": ["Param Vir Chakra", "Maha Vir Chakra", "Vir Chakra", "Bharat Ratna"], "c": ["A", "B", "C"], "e": "Param Vir, Maha Vir, and Vir Chakras are wartime gallantry awards. Bharat Ratna is a civilian award."}
        ],
        "records": [
            {"q": "Which of the following geographical features are the largest of their kind in the world?", "o": ["Sahara - Largest hot desert", "Burj Khalifa - Tallest building", "Lake Baikal - Deepest freshwater lake", "Sundarbans - Largest river delta"], "c": ["A", "B", "C", "D"], "e": "All options correctly state world records for hot deserts, building height, lake depth, and delta size."},
            {"q": "Which of the following are the longest or tallest structures in India?", "o": ["Statue of Unity (tallest statue)", "Bhupen Hazarika Setu (longest water bridge)", "Chenab Bridge (highest railway arch bridge)", "Burj Khalifa (tallest building)"], "c": ["A", "B", "C"], "e": "Statue of Unity, Bhupen Hazarika, and Chenab are records within India. Burj Khalifa is in the UAE."}
        ],
        "sports": [
            {"q": "Which of the following tournaments are classified as Grand Slam tennis tournaments?", "o": ["Wimbledon", "US Open", "French Open", "Davis Cup"], "c": ["A", "B", "C"], "e": "The four Grand Slams are Australian, French, Wimbledon, and US Open. Davis Cup is a team event."},
            {"q": "In which of the following sports do teams have exactly 11 players on the field/court at a time?", "o": ["Cricket", "Football (Soccer)", "Field Hockey", "Basketball"], "c": ["A", "B", "C"], "e": "Cricket, Football, and Hockey have 11 players. Basketball has 5 players on the court."}
        ],
        "indent": [
            {"q": "Which of the following milestones are correctly matched with Indian cinematic history?", "o": ["Raja Harishchandra - First silent feature film", "Alam Ara - First sound (talkie) film", "Kisan Kanya - First color film", "Dangal - Highest grossing film worldwide"], "c": ["A", "B", "C", "D"], "e": "All options are correctly matched milestones in Indian cinema history."},
            {"q": "Which of the following Indian directors have won or been nominated for prestigious international film awards?", "o": ["Satyajit Ray (Academy Honorary Award)", "A.R. Rahman (Best Original Score Oscar)", "Bhanu Athaiya (Best Costume Design Oscar)", "Mira Nair (Golden Lion Winner)"], "c": ["A", "B", "C", "D"], "e": "All four have won or been nominated for major international film achievements."}
        ],
        "intent": [
            {"q": "Which of the following movies were directed by Christopher Nolan?", "o": ["Inception", "Interstellar", "Oppenheimer", "Titanic"], "c": ["A", "B", "C"], "e": "Nolan directed Inception, Interstellar, and Oppenheimer. Titanic was directed by James Cameron."},
            {"q": "Which of the following films have won exactly 11 Academy Awards (Oscars)?", "o": ["Ben-Hur (1959)", "Titanic (1997)", "The Lord of the Rings: The Return of the King (2003)", "The Godfather (1972)"], "c": ["A", "B", "C"], "e": "Ben-Hur, Titanic, and Return of the King won 11 Oscars. The Godfather won 3 Oscars."}
        ],
        "bcurra": [
            {"q": "Which of the following countries hosted G20 Summits in 2023 or 2024?", "o": ["India (2023)", "Brazil (2024)", "Indonesia (2022)", "South Africa (upcoming)"], "c": ["A", "B"], "e": "India hosted in Sep 2023, Brazil in Nov 2024. Indonesia hosted in 2022. South Africa is scheduled for 2025."},
            {"q": "Which of the following cities hosted recent Olympic Games?", "o": ["Paris (2024)", "Tokyo (2020/2021)", "London (2012)", "Mumbai (never)"], "c": ["A", "B", "C"], "e": "Paris, Tokyo, and London hosted the Olympics. Mumbai has not hosted the Olympics."}
        ],
        "icurra": [
            {"q": "Which of the following are classified as key organs or executives of NITI Aayog?", "o": ["Chairperson (Prime Minister)", "Governing Council (all State CMs and UT Lt. Governors)", "Vice-Chairperson", "Finance Commission Chairman"], "c": ["A", "B", "C"], "e": "PM, Governing Council, and Vice-Chairperson are core to NITI Aayog. The Finance Commission is a separate constitutional body."},
            {"q": "Which of the following were major space exploration achievements of ISRO in recent years?", "o": ["Successful landing of Chandrayaan-3 on the lunar south pole", "Launch of Aditya-L1 solar observation mission", "Launch of XPOSAT black hole observation satellite", "Successful crewed orbital flight of Gaganyaan"], "c": ["A", "B", "C"], "e": "Chandrayaan-3, Aditya-L1, and XPOSAT were successfully launched. Gaganyaan's crewed flight is still in testing phases."}
        ],
        "acurra": [
            {"q": "Which of the following countries joined BRICS as full members in January 2024?", "o": ["Egypt", "Ethiopia", "Iran", "Saudi Arabia"], "c": ["A", "B", "C", "D"], "e": "Egypt, Ethiopia, Iran, Saudi Arabia, and UAE joined BRICS in January 2024."},
            {"q": "Which of the following are key targets set by the Government of India for the coming decades?", "o": ["Achieving developed nation status (Viksit Bharat) by 2047", "Achieving net-zero carbon emissions by 2070", "Eliminating tuberculosis by 2025", "Banning all fossil fuel cars by 2030"], "c": ["A", "B", "C"], "e": "Viksit Bharat (2047), net-zero (2070), and TB elimination (2025) are official targets. There is no official ban on fossil fuel cars by 2030."}
        ]
    }
    
    t_list = templates[sub]
    t = t_list[idx % len(t_list)]
    return {
        "id": q_id, "subject": sub_upper, "topic": "General Knowledge", "subtopic": None,
        "difficulty": diff_label(q_id), "type": "MSQ", "question": t["q"], "options": t["o"],
        "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
    }, {"id": q_id, "correct_answer": json.dumps(t["c"])}, {"id": q_id, "explanation": t["e"]}

def get_nat(sub, idx, q_id, sub_upper):
    templates = {
        "ih": [
            {"q": "In which year did the First Battle of Panipat take place?", "ans": "1526", "e": "The First Battle of Panipat was fought on April 21, 1526, establishing the Mughal rule in India."},
            {"q": "In which year did India gain independence from British rule?", "ans": "1947", "e": "India gained independence on August 15, 1947."},
            {"q": "In which year did the Battle of Plassey take place, paving the way for British dominance in Bengal?", "ans": "1757", "e": "The Battle of Plassey was fought on June 23, 1757, where British forces defeated the Nawab of Bengal."},
            {"q": "In which year did Mahatma Gandhi launch the Quit India Movement?", "ans": "1942", "e": "The Quit India Movement was launched on August 8, 1942."},
            {"q": "In which year did Mahatma Gandhi return to India from South Africa?", "ans": "1915", "e": "Mahatma Gandhi returned to India on January 9, 1915, which is celebrated as Pravasi Bharatiya Divas."}
        ],
        "wh": [
            {"q": "In which year did the French Revolution begin with the storming of the Bastille?", "ans": "1789", "e": "The French Revolution began in 1789."},
            {"q": "In which year did the First World War begin?", "ans": "1914", "e": "WWI began on July 28, 1914, following the assassination of Archduke Franz Ferdinand."},
            {"q": "In which year did the Second World War end with the surrender of Japan?", "ans": "1945", "e": "WWII ended in 1945."},
            {"q": "In which year did the Berlin Wall fall, leading to the reunification of Germany?", "ans": "1989", "e": "The Berlin Wall fell on November 9, 1989."},
            {"q": "In which year was the Magna Carta signed by King John of England?", "ans": "1215", "e": "The Magna Carta was signed in June 1215."}
        ],
        "ig": [
            {"q": "How many states are there currently in the Republic of India?", "ans": "28", "e": "There are currently 28 states and 8 union territories in India."},
            {"q": "How many Union Territories are there currently in the Republic of India?", "ans": "8", "e": "There are currently 8 Union Territories in India after merger of Daman & Diu and Dadra & Nagar Haveli."},
            {"q": "What is the standard meridian longitude (in degrees East) of India used for calculating Indian Standard Time?", "ans": "82.5", "e": "The standard meridian of India is 82°30' E (or 82.5° E), passing through Mirzapur near Allahabad."},
            {"q": "What is the height of Kanchenjunga, the highest mountain peak in India, in meters?", "ans": "8586", "e": "Mount Kanchenjunga stands at an elevation of 8,586 meters."},
            {"q": "What is the length of the land frontier/border of India in kilometers (rounded to nearest thousand)?", "ans": "15000", "e": "India has a land border of approximately 15,106.7 km, which rounds to 15,000 km."}
        ],
        "wg": [
            {"q": "How many recognized continents are there on Earth?", "ans": "7", "e": "There are 7 continents: Asia, Africa, North America, South America, Antarctica, Europe, and Australia."},
            {"q": "What is the official height of Mount Everest in meters (rounded to nearest integer)?", "ans": "8848", "e": "Mount Everest's height is traditionally recognized as 8,848 meters (recent surveys measure it at 8848.86 m)."},
            {"q": "How many oceans are there on Earth according to the standard five-ocean division?", "ans": "5", "e": "The five oceans are Pacific, Atlantic, Indian, Southern, and Arctic oceans."},
            {"q": "What is the approximate circumference of the Earth at the Equator in kilometers (rounded to nearest thousand)?", "ans": "40000", "e": "The Earth's equatorial circumference is approximately 40,075 km, which rounds to 40,000 km."},
            {"q": "Into how many standard time zones is the Earth divided?", "ans": "24", "e": "The Earth is divided into 24 standard time zones, each representing 15 degrees of longitude."}
        ],
        "indp": [
            {"q": "How many schedules are there currently in the Constitution of India?", "ans": "12", "e": "The Constitution of India originally had 8 schedules, but currently contains 12 schedules."},
            {"q": "How many articles were originally present in the Constitution of India when it was adopted in 1949?", "ans": "395", "e": "The original Constitution had 395 articles divided into 22 parts and 8 schedules."},
            {"q": "What is the minimum voting age (in years) for Indian citizens in general elections?", "ans": "18", "e": "The 61st Amendment Act of 1989 lowered the voting age from 21 to 18 years."},
            {"q": "What is the maximum number of members that can be nominated to the Rajya Sabha by the President?", "ans": "12", "e": "The President can nominate 12 members to the Rajya Sabha for contributions to art, literature, science, and social services."},
            {"q": "What is the term of office (in years) for the President of India?", "ans": "5", "e": "The President of India is elected for a term of 5 years."}
        ],
        "intp": [
            {"q": "How many permanent member countries belong to the United Nations Security Council (UNSC)?", "ans": "5", "e": "The UNSC has 5 permanent members (US, UK, France, Russia, China) with veto power."},
            {"q": "In which year was the United Nations (UN) established?", "ans": "1945", "e": "The UN was officially established on October 24, 1945, after the ratification of the UN Charter."},
            {"q": "How many member states are currently in the European Union (as of 2026)?", "ans": "27", "e": "The EU has 27 member states following the exit of the UK (Brexit)."},
            {"q": "How many judges serve in the International Court of Justice (ICJ) at any given time?", "ans": "15", "e": "The ICJ consists of 15 judges elected to nine-year terms by the UN General Assembly and Security Council."},
            {"q": "What is the term length (in years) of the President of the United States?", "ans": "4", "e": "The US President is elected for a term of 4 years."}
        ],
        "inde": [
            {"q": "In which year was the Goods and Services Tax (GST) introduced in India?", "ans": "2017", "e": "GST was launched on July 1, 2017."},
            {"q": "In which year was the NITI Aayog established to replace the Planning Commission?", "ans": "2015", "e": "NITI Aayog was established on January 1, 2015, by a cabinet resolution."},
            {"q": "In which year was the First Five Year Plan launched in India?", "ans": "1951", "e": "The First Five Year Plan was launched in 1951, focusing on agricultural development."},
            {"q": "How many public sector banks are currently operating in India after major mergers (as of 2026)?", "ans": "12", "e": "Following consolidation, there are 12 public sector banks in India (including SBI)."},
            {"q": "In which year did the major demonetization of 500 and 1000 rupee notes occur under the Modi government?", "ans": "2016", "e": "The demonetization was announced on November 8, 2016."}
        ],
        "inte": [
            {"q": "In which year was the World Bank officially founded at the Bretton Woods Conference?", "ans": "1944", "e": "The World Bank and IMF were founded at the Bretton Woods Conference in July 1944."},
            {"q": "In which year was the International Monetary Fund (IMF) officially established?", "ans": "1944", "e": "The IMF was founded in July 1944 alongside the World Bank."},
            {"q": "How many member nations currently belong to the World Trade Organization (WTO)?", "ans": "164", "e": "The WTO has 164 member states, representing over 98% of global trade."},
            {"q": "In which year was the Euro currency officially introduced for non-physical transactions?", "ans": "1999", "e": "The Euro was launched on January 1, 1999, as an electronic currency."},
            {"q": "How many countries currently use the Euro as their official currency (as of 2026)?", "ans": "20", "e": "Croatia joined the Eurozone on January 1, 2023, making it the 20th country to use the Euro."}
        ],
        "bphy": [
            {"q": "What is the approximate acceleration due to gravity on Earth in m/s^2?", "ans": "9.8", "e": "Acceleration due to gravity is approximately 9.8 m/s^2 at sea level."},
            {"q": "What is the speed of sound in dry air at 20 degrees Celsius in m/s?", "ans": "343", "e": "The speed of sound in air at 20°C is approximately 343 m/s."},
            {"q": "What is the value of absolute zero in degrees Celsius (rounded to nearest integer)?", "ans": "-273", "e": "Absolute zero is defined as -273.15°C, which rounds to -273°C."},
            {"q": "What is the refractive index of pure water (rounded to two decimal places)?", "ans": "1.33", "e": "Water has a refractive index of approximately 1.33."},
            {"q": "What is the escape velocity of Earth in kilometers per second (km/s) (rounded to one decimal place)?", "ans": "11.2", "e": "The escape velocity required to leave Earth's gravitational pull is approximately 11.2 km/s."}
        ],
        "iphy": [
            {"q": "What is the exponent of 10 in the speed of light in vacuum ($3 \\times 10^k$ m/s)?", "ans": "8", "e": "Speed of light is 3 * 10^8 m/s, so the exponent k is 8."},
            {"q": "What is the exponent of 10 in Planck's constant ($6.626 \\times 10^k$ J s)?", "ans": "-34", "e": "Planck's constant is 6.626 * 10^-34 J s, so the exponent is -34."},
            {"q": "What is the exponent of 10 in the Universal Gravitational Constant G ($6.67 \\times 10^k$ N m^2/kg^2)?", "ans": "-11", "e": "G is 6.67 * 10^-11 N m^2/kg^2, so the exponent is -11."},
            {"q": "What is the exponent of 10 in the charge of an electron ($-1.6 \\times 10^k$ Coulombs)?", "ans": "-19", "e": "The charge of an electron is -1.6 * 10^-19 Coulombs, so the exponent is -19."},
            {"q": "What is the speed of light in vacuum in kilometers per second (km/s)?", "ans": "300000", "e": "The speed of light is 300,000 km/s (or 3 * 10^8 m/s)."}
        ],
        "aphy": [
            {"q": "How many valence quarks make up a single proton?", "ans": "3", "e": "A proton is made of 3 valence quarks: two up quarks and one down quark (uud)."},
            {"q": "How many valence quarks make up a single neutron?", "ans": "3", "e": "A neutron is made of 3 valence quarks: one up quark and two down quarks (udd)."},
            {"q": "What is the rest mass of a photon in kilograms?", "ans": "0", "e": "A photon is a massless particle and has a rest mass of exactly 0."},
            {"q": "What is the critical temperature of liquid Helium at 1 atm in Kelvin (rounded to one decimal place)?", "ans": "4.2", "e": "Liquid Helium boils at 4.2 K under standard pressure."},
            {"q": "How many flavor types (generations) of quarks exist in the Standard Model?", "ans": "6", "e": "There are 6 flavors of quarks: up, down, charm, strange, top, and bottom."}
        ],
        "bchem": [
            {"q": "What is the atomic number of Hydrogen, the simplest element?", "ans": "1", "e": "Hydrogen has exactly 1 proton, so its atomic number is 1."},
            {"q": "What is the pH value of pure water at 25 degrees Celsius?", "ans": "7", "e": "Pure water is neutral and has a pH of 7."},
            {"q": "What is the valency of a Carbon atom in organic compounds?", "ans": "4", "e": "Carbon is tetravalent, meaning it forms 4 covalent bonds to complete its octet."},
            {"q": "What is the atomic number of Oxygen?", "ans": "8", "e": "Oxygen has 8 protons in its nucleus, so its atomic number is 8."},
            {"q": "What is the boiling point of pure water in degrees Celsius at 1 atm?", "ans": "100", "e": "Water boils at exactly 100°C under standard atmospheric pressure."}
        ],
        "ichem": [
            {"q": "What is the exponent of 10 in Avogadro's constant ($6.022 \\times 10^k$)?", "ans": "23", "e": "Avogadro's constant is 6.022 * 10^23, so the exponent is 23."},
            {"q": "How many periods are there in the standard modern periodic table?", "ans": "7", "e": "There are exactly 7 horizontal rows, known as periods, in the periodic table."},
            {"q": "How many groups (vertical columns) are there in the modern periodic table?", "ans": "18", "e": "The periodic table has 18 vertical columns, known as groups."},
            {"q": "What is the ideal gas constant R value in J/(mol K) (rounded to two decimal places)?", "ans": "8.31", "e": "The gas constant R is approximately 8.314 J/(mol K)."},
            {"q": "What is the atomic number of Sodium (Na)?", "ans": "11", "e": "Sodium has 11 protons, placing it in Group 1, Period 3 with atomic number 11."}
        ],
        "achem": [
            {"q": "What is the coordination number of atoms in a Face-Centered Cubic (FCC) crystalline structure?", "ans": "12", "e": "Each atom in FCC touches 12 neighboring atoms."},
            {"q": "What is the value of the Faraday constant in Coulombs per mole of electrons (rounded to nearest hundred)?", "ans": "96500", "e": "The Faraday constant is approximately 96,485 C/mol, which rounds to 96,500 C/mol."},
            {"q": "According to the Third Law of Thermodynamics, what is the entropy of a perfect crystalline substance at absolute zero (0 K) in J/K?", "ans": "0", "e": "The entropy of a perfect crystal at absolute zero is exactly 0."},
            {"q": "How many structural isomers are possible for the alkane Butane (C4H10)?", "ans": "2", "e": "Butane has 2 isomers: n-butane and isobutane."},
            {"q": "What is the coordination number of atoms in a Body-Centered Cubic (BCC) crystalline structure?", "ans": "8", "e": "Each atom in a BCC structure touches 8 neighboring atoms."}
        ],
        "bbio": [
            {"q": "How many bones are there in the skeleton of an adult human body?", "ans": "206", "e": "An adult human has 206 bones. Infants have around 270-300 bones which fuse over time."},
            {"q": "What is the normal core body temperature of a healthy human in degrees Celsius?", "ans": "37", "e": "Normal human body temperature is approximately 37°C (98.6°F)."},
            {"q": "How many ribs (individual bones) are there in a standard human body?", "ans": "24", "e": "Humans have 12 pairs of ribs, making a total of 24 ribs."},
            {"q": "What is the average resting heart rate (pulse) of a healthy adult in beats per minute?", "ans": "72", "e": "A normal resting heart rate for adults ranges from 60 to 100 bpm, with 72 bpm being the standard average."},
            {"q": "What is the average life span of a human red blood cell (RBC) in days?", "ans": "120", "e": "Red blood cells circulate in the body for about 120 days before being destroyed in the spleen."}
        ],
        "ibio": [
            {"q": "How many chromosomes (total count) are present in a normal human somatic cell?", "ans": "46", "e": "Human somatic cells have 46 chromosomes (23 pairs)."},
            {"q": "How many pairs of autosomes are in a normal human karyotype?", "ans": "22", "e": "Of the 23 pairs of chromosomes, 22 pairs are autosomes and 1 pair is sex chromosomes."},
            {"q": "How many chambers are there in a human heart?", "ans": "4", "e": "The human heart has 4 chambers: two atria (left and right) and two ventricles (left and right)."},
            {"q": "How many teeth are in a complete primary (milk) set of teeth in children?", "ans": "20", "e": "Children develop a temporary set of 20 milk teeth before they are replaced by permanent teeth."},
            {"q": "What is the average gestation period of humans in days (from fertilization to birth)?", "ans": "280", "e": "Human gestation lasts about 40 weeks or 280 days from the last menstrual period."}
        ],
        "abio": [
            {"q": "What is the net gain of ATP molecules produced per glucose molecule during glycolysis alone?", "ans": "2", "e": "Glycolysis consumes 2 ATP and produces 4 ATP, resulting in a net gain of 2 ATP molecules."},
            {"q": "How many base pairs are present in a single complete turn of a B-DNA double helix?", "ans": "10", "e": "B-DNA has approximately 10 base pairs per helical turn (3.4 nm pitch)."},
            {"q": "How many amino acids are classified as 'essential' for adult humans because they cannot be synthesized by the body?", "ans": "9", "e": "There are 9 essential amino acids: histidine, isoleucine, leucine, lysine, methionine, phenylalanine, threonine, tryptophan, and valine."},
            {"q": "How many pairs of cranial nerves emerge directly from the human brain?", "ans": "12", "e": "There are 12 pairs of cranial nerves controlling head, neck, and facial functions."},
            {"q": "How many pairs of spinal nerves emerge from the human spinal cord?", "ans": "31", "e": "There are 31 pairs of spinal nerves: 8 cervical, 12 thoracic, 5 lumbar, 5 sacral, and 1 coccygeal."}
        ],
        "blit": [
            {"q": "How many plays are traditionally attributed to William Shakespeare?", "ans": "37", "e": "Shakespeare wrote 37 plays, including tragedies, comedies, and histories."},
            {"q": "How many books are in the 'Harry Potter' novel series by J.K. Rowling?", "ans": "7", "e": "The series consists of 7 fantasy novels, from Philosopher's Stone to Deathly Hallows."},
            {"q": "How many lines are in a standard Shakespearean or Italian sonnet?", "ans": "14", "e": "A sonnet is a 14-line poem written in iambic pentameter."},
            {"q": "How many books (kandas) are there in Valmiki's epic Ramayana?", "ans": "7", "e": "The Ramayana is divided into 7 books: Bala Kanda, Ayodhya Kanda, Aranya Kanda, Kishkindha Kanda, Sundara Kanda, Yuddha Kanda, and Uttara Kanda."},
            {"q": "How many books (parvas) are there in the epic Mahabharata?", "ans": "18", "e": "The Mahabharata is divided into 18 books or parvas."}
        ],
        "ilit": [
            {"q": "In which year did Rabindranath Tagore win the Nobel Prize in Literature?", "ans": "1913", "e": "Tagore won the Nobel Prize in 1913 for Gitanjali."},
            {"q": "How many poems are in the original English translation of Rabindranath Tagore's Gitanjali?", "ans": "103", "e": "The English Gitanjali contains 103 song offerings translated by Tagore himself."},
            {"q": "In which year was Jane Austen's novel 'Pride and Prejudice' first published?", "ans": "1813", "e": "Pride and Prejudice was first published anonymously on January 28, 1813."},
            {"q": "In which year was George Orwell's classic dystopian novel '1984' published?", "ans": "1949", "e": "1984 was published on June 8, 1949."},
            {"q": "How many parts (tantras) are there in the collection of stories 'Panchatantra'?", "ans": "5", "e": "Panchatantra literally means 'Five Books', consisting of 5 parts of animal stories."}
        ],
        "alit": [
            {"q": "In which year did Arundhati Roy win the Booker Prize for 'The God of Small Things'?", "ans": "1997", "e": "Roy was awarded the Booker Prize in 1997."},
            {"q": "In which year did Salman Rushdie win the Booker Prize for 'Midnight's Children'?", "ans": "1981", "e": "Midnight's Children won the Booker Prize in 1981 (and the 'Booker of Bookers' in 1993/2008)."},
            {"q": "In which year did T.S. Eliot receive the Nobel Prize in Literature?", "ans": "1948", "e": "Eliot was awarded the Nobel Prize in 1948 for his contribution to modern poetry."},
            {"q": "How many books (sections) are there in John Milton's epic poem 'Paradise Lost' (in its final 1674 edition)?", "ans": "12", "e": "The first edition had 10 books, but the final 1674 edition was redivided into 12 books."},
            {"q": "In which year was James Joyce's landmark modernist novel 'Ulysses' first published in its entirety?", "ans": "1922", "e": "Ulysses was published in Paris by Sylvia Beach in 1922."}
        ],
        "indfirst": [
            {"q": "In which year did India launch its first satellite, Aryabhata?", "ans": "1975", "e": "Aryabhata was launched on April 19, 1975, by a Soviet rocket."},
            {"q": "In which year did Rakesh Sharma travel into space aboard Soyuz T-11?", "ans": "1984", "e": "Rakesh Sharma launched into space on April 2, 1984."},
            {"q": "In which year was the first general election held in independent India? (Enter starting year)", "ans": "1951", "e": "The first general elections were held from October 1951 to February 1952."},
            {"q": "In which year did the first passenger train run in India (between Bombay and Thane)?", "ans": "1853", "e": "The first passenger train ran on April 16, 1853, covering 34 km."},
            {"q": "In which year was the first official census conducted in India under British rule?", "ans": "1872", "e": "The first non-synchronous census was conducted in 1872 under Viceroy Lord Mayo."}
        ],
        "intfirst": [
            {"q": "In which year did humans first land on the Moon during the Apollo 11 mission?", "ans": "1969", "e": "Neil Armstrong and Buzz Aldrin landed on the Moon on July 20, 1969."},
            {"q": "In which year did Yuri Gagarin become the first human in space?", "ans": "1961", "e": "Yuri Gagarin orbited Earth in Vostok 1 on April 12, 1961."},
            {"q": "In which year were the first modern Olympic Games held in Athens?", "ans": "1896", "e": "The first modern Olympics opened on April 6, 1896."},
            {"q": "In which year did Christopher Columbus make his first voyage across the Atlantic to the Americas?", "ans": "1492", "e": "Columbus reached the Americas on October 12, 1492."},
            {"q": "In which year did the Wright brothers make the first controlled, powered airplane flight?", "ans": "1903", "e": "Orville and Wilbur Wright flew their Wright Flyer on December 17, 1903."}
        ],
        "indlaws": [
            {"q": "In which year did the Right to Information (RTI) Act come into force in India?", "ans": "2005", "e": "RTI was passed in June 2005 and fully implemented on October 12, 2005."},
            {"q": "In which year was the first Consumer Protection Act passed in India?", "ans": "1986", "e": "The Consumer Protection Act was passed in 1986."},
            {"q": "In which year was the Environment Protection Act enacted in India?", "ans": "1986", "e": "The Environment Protection Act was enacted in 1986 following the Bhopal disaster."},
            {"q": "In which year was the Indian Penal Code (IPC) enacted?", "ans": "1860", "e": "The IPC was enacted in 1860 and came into force in 1862."},
            {"q": "In which year was the Wildlife Protection Act enacted in India?", "ans": "1972", "e": "The Wildlife Protection Act was passed in 1972."}
        ],
        "intlaws": [
            {"q": "In which year was the Universal Declaration of Human Rights (UDHR) adopted by the UN?", "ans": "1948", "e": "UDHR was adopted by the UN General Assembly on December 10, 1948."},
            {"q": "In which year was the Kyoto Protocol on climate change adopted?", "ans": "1997", "e": "The Kyoto Protocol was adopted in Kyoto, Japan, on December 11, 1997."},
            {"q": "In which year was the United Nations Convention on the Law of the Sea (UNCLOS) opened for signature?", "ans": "1982", "e": "UNCLOS was adopted in 1982 and came into force in 1994."},
            {"q": "How many articles are contained in the Universal Declaration of Human Rights (UDHR)?", "ans": "30", "e": "The UDHR consists of exactly 30 articles detailing human rights."},
            {"q": "In which year was the Paris Agreement on climate change adopted at COP21?", "ans": "2015", "e": "The Paris Agreement was adopted by consensus on December 12, 2015."}
        ],
        "dates": [
            {"q": "What is the day of the month on which National Science Day is celebrated in India (February __)?", "ans": "28", "e": "National Science Day is celebrated on February 28."},
            {"q": "What is the numerical month (1-12) in which World Environment Day is celebrated?", "ans": "6", "e": "World Environment Day is celebrated on June 5, which is the 6th month."},
            {"q": "What is the day of the month on which National Youth Day is celebrated in India (January __)?", "ans": "12", "e": "National Youth Day is celebrated on January 12."},
            {"q": "What is the numerical month (1-12) in which Earth Day is celebrated annually?", "ans": "4", "e": "Earth Day is celebrated on April 22, which is the 4th month."},
            {"q": "What is the day of the month on which International Day of Yoga is celebrated (June __)?", "ans": "21", "e": "Yoga Day is celebrated on June 21."}
        ],
        "nicknames": [
            {"q": "How many rivers are referred to in the nickname of Punjab, the 'Land of Five Rivers'?", "ans": "5", "e": "Punjab is named after 5 rivers: Beas, Chenab, Jhelum, Ravi, and Sutlej."},
            {"q": "In which year was Dadabhai Naoroji, the 'Grand Old Man of India', born?", "ans": "1825", "e": "Dadabhai Naoroji was born on September 4, 1825."},
            {"q": "In which year was Sardar Vallabhbhai Patel, the 'Iron Man of India', born?", "ans": "1875", "e": "Sardar Patel was born on October 31, 1875."},
            {"q": "How many letters are in the color that forms the nickname of Jaipur, the '_____ City'?", "ans": "4", "e": "Jaipur is the 'Pink' City. The word 'Pink' has 4 letters."},
            {"q": "In which year was Sarojini Naidu, the 'Nightingale of India', born?", "ans": "1879", "e": "Sarojini Naidu was born on February 13, 1879."}
        ],
        "orgs": [
            {"q": "In which year was the World Health Organization (WHO) founded?", "ans": "1948", "e": "WHO was established on April 7, 1948, celebrated as World Health Day."},
            {"q": "In which year was the South Asian Association for Regional Cooperation (SAARC) founded?", "ans": "1985", "e": "SAARC was established in Dhaka on December 8, 1985."},
            {"q": "In which year was the Association of Southeast Asian Nations (ASEAN) founded?", "ans": "1967", "e": "ASEAN was founded on August 8, 1967, with the signing of the Bangkok Declaration."},
            {"q": "How many member states are currently in the SAARC grouping?", "ans": "8", "e": "SAARC has 8 members: Afghanistan, Bangladesh, Bhutan, India, Maldives, Nepal, Pakistan, Sri Lanka."},
            {"q": "How many member states currently make up the ASEAN grouping?", "ans": "10", "e": "ASEAN consists of 10 Southeast Asian member nations."}
        ],
        "awards": [
            {"q": "In which year was the Bharat Ratna award instituted by the Government of India?", "ans": "1954", "e": "Bharat Ratna was instituted on January 2, 1954."},
            {"q": "In which year were the Nobel Prizes first awarded?", "ans": "1901", "e": "Nobel Prizes were first awarded in 1901."},
            {"q": "In which year was the first Academy Award (Oscar) ceremony held in Los Angeles?", "ans": "1929", "e": "The first Oscars were awarded on May 16, 1929."},
            {"q": "How many fields/categories are Nobel Prizes awarded in currently (including Economic Sciences)?", "ans": "6", "e": "Nobel Prizes are awarded in 6 categories: Physics, Chemistry, Medicine, Literature, Peace, and Economics."},
            {"q": "In which year was the first Khel Ratna award (now Major Dhyan Chand Khel Ratna) presented?", "ans": "1991", "e": "The Khel Ratna was first awarded in 1991-92 to chess Grandmaster Viswanathan Anand."}
        ],
        "records": [
            {"q": "What is the height of the Burj Khalifa, the tallest building in the world, in meters?", "ans": "828", "e": "Burj Khalifa stands at exactly 828 meters tall."},
            {"q": "What is the height of the Statue of Unity in Gujarat, the tallest statue in the world, in meters?", "ans": "182", "e": "The Statue of Unity is 182 meters (597 feet) tall."},
            {"q": "How many states in India share the geographical area of the Sundarbans Delta?", "ans": "1", "e": "In India, the Sundarbans delta lies entirely within the state of West Bengal (the rest is in Bangladesh)."},
            {"q": "What is the length of the longest railway platform in India (located in Hubballi, Karnataka) in meters?", "ans": "1507", "e": "The Hubballi platform measures 1,507 meters long, holds the world record."},
            {"q": "What is the altitude in meters of the highest lake in India, Cholamu Lake in Sikkim (rounded to nearest hundred)?", "ans": "5300", "e": "Cholamu Lake is located at an altitude of approximately 5,330 meters, which rounds to 5,300 meters."}
        ],
        "sports": [
            {"q": "What is the length of a standard cricket pitch between the wickets in yards?", "ans": "22", "e": "A cricket pitch is exactly 22 yards long."},
            {"q": "How many players are on the field for one team in a standard association football (soccer) match?", "ans": "11", "e": "A football team has exactly 11 players on the pitch."},
            {"q": "How many players are on the court for one team in a standard basketball game?", "ans": "5", "e": "Each team has 5 players on the court."},
            {"q": "In which year was the first FIFA World Cup held in Uruguay?", "ans": "1930", "e": "The first FIFA World Cup took place in 1930."},
            {"q": "How many rings are in the official logo of the Olympic Games?", "ans": "5", "e": "The Olympic logo features 5 interlocking rings."}
        ],
        "indent": [
            {"q": "In which year was India's first silent feature film, Raja Harishchandra, released?", "ans": "1913", "e": "Raja Harishchandra was released in May 1913."},
            {"q": "In which year was India's first talkie (sound) film, Alam Ara, released?", "ans": "1931", "e": "Alam Ara premiered on March 14, 1931."},
            {"q": "In which year did Bhanu Athaiya win the first-ever Oscar for India for Best Costume Design?", "ans": "1983", "e": "Bhanu Athaiya won the Oscar for Gandhi in 1983."},
            {"q": "In which year was director Satyajit Ray awarded the Honorary Academy Award (Oscar) for lifetime achievement?", "ans": "1992", "e": "Satyajit Ray was awarded the Honorary Oscar in 1992 shortly before his death."},
            {"q": "In which year was the Dadasaheb Phalke Award, India's highest award in cinema, instituted?", "ans": "1969", "e": "The Dadasaheb Phalke Award was introduced in 1969 to honor Phalke's contribution."}
        ],
        "intent": [
            {"q": "In which year was the blockbusting romance/drama film 'Titanic' directed by James Cameron released?", "ans": "1997", "e": "Titanic was released in theaters in December 1997."},
            {"q": "In which year was the first Academy Award (Oscar) ceremony held?", "ans": "1929", "e": "The first Academy Awards were presented in May 1929."},
            {"q": "What is the maximum number of Oscars won by a single movie in history?", "ans": "11", "e": "Ben-Hur, Titanic, and Return of the King each won 11 Oscars."},
            {"q": "In which year was the sci-fi blockbuster 'Avatar' directed by James Cameron released?", "ans": "2009", "e": "Avatar was released in December 2009."},
            {"q": "In which year was Walt Disney's 'Snow White and the Seven Dwarfs' released?", "ans": "1937", "e": "Snow White premiered in December 1937."}
        ],
        "bcurra": [
            {"q": "In which year did India host the G20 Summit in New Delhi?", "ans": "2023", "e": "India hosted the G20 Summit on September 9-10, 2023."},
            {"q": "How many member countries are there in the G20 forum (excluding EU and African Union)?", "ans": "19", "e": "The G20 consists of 19 individual countries, the EU, and the African Union."},
            {"q": "In which year are the next Summer Olympic Games scheduled to be held in Los Angeles?", "ans": "2028", "e": "Los Angeles is scheduled to host the Summer Olympics in July 2028."},
            {"q": "How many elected constituencies are there in the Lok Sabha (Lower House) of India?", "ans": "543", "e": "The Lok Sabha has 543 elected members from constituencies across India."},
            {"q": "What is the current calendar year?", "ans": "2026", "e": "The current year is 2026."}
        ],
        "icurra": [
            {"q": "In which year did ISRO successfully land Chandrayaan-3 on the lunar south pole?", "ans": "2023", "e": "Chandrayaan-3 landed on the Moon on August 23, 2023."},
            {"q": "How many members are appointed to the Finance Commission of India (including the Chairman)?", "ans": "5", "e": "The Finance Commission consists of a Chairman and 4 other members (total 5)."},
            {"q": "Which year did India set as its target for achieving net-zero greenhouse gas emissions?", "ans": "2070", "e": "India announced its net-zero target year as 2070 at the COP26 climate summit."},
            {"q": "What is the total sanctioned strength of judges in the Supreme Court of India (including CJI)?", "ans": "34", "e": "The Supreme Court has a maximum sanctioned strength of 34 judges."},
            {"q": "In which year did NITI Aayog publish its first SDG India Index report?", "ans": "2018", "e": "NITI Aayog launched the SDG India Index in December 2018."}
        ],
        "acurra": [
            {"q": "In which year has India targeted to achieve 'Viksit Bharat' (Developed India) status?", "ans": "2047", "e": "Viksit Bharat @ 2047 aims to make India a developed economy by the 100th anniversary of independence in 2047."},
            {"q": "In which year was the COP28 UN Climate Change Conference held in Dubai, UAE?", "ans": "2023", "e": "COP28 was held in Dubai in December 2023."},
            {"q": "How many new countries were invited to join BRICS as full members in Jan 2024?", "ans": "5", "e": "BRICS invited 5 countries: Egypt, Ethiopia, Iran, Saudi Arabia, and UAE."},
            {"q": "In which year was the 16th Finance Commission of India officially constituted?", "ans": "2023", "e": "The 16th Finance Commission was constituted on December 31, 2023."},
            {"q": "What is the target year set by the government to eliminate Tuberculosis (TB) from India?", "ans": "2025", "e": "India set a target to make the country TB-free by 2025, five years ahead of the global SDG target."}
        ]
    }
    
    t_list = templates[sub]
    t = t_list[idx % len(t_list)]
    return {
        "id": q_id, "subject": sub_upper, "topic": "General Knowledge", "subtopic": None,
        "difficulty": diff_label(q_id), "type": "NAT", "question": t["q"], "options": None,
        "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["regulations math"], "representation": ["text"]
    }, {"id": q_id, "correct_answer": t["ans"]}, {"id": q_id, "explanation": t["e"]}

def main():
    base_dir = "datasets"
    subjects = [
        "ih", "wh", "ig", "wg", "indp", "intp", "inde", "inte", "bphy", "iphy", "aphy",
        "bchem", "ichem", "achem", "bbio", "ibio", "abio", "blit", "ilit", "alit",
        "indfirst", "intfirst", "indlaws", "intlaws", "dates", "nicknames", "orgs",
        "awards", "records", "sports", "indent", "intent", "bcurra", "icurra", "acurra"
    ]
    subject_map = {
        "ih": "IH", "wh": "WH", "ig": "IG", "wg": "WG",
        "indp": "INDP", "intp": "INTP", "inde": "INDE", "inte": "INTE",
        "bphy": "BPHY", "iphy": "IPHY", "aphy": "APHY",
        "bchem": "BCHEM", "ichem": "ICHEM", "achem": "ACHEM",
        "bbio": "BBIO", "ibio": "IBIO", "abio": "ABIO",
        "blit": "BLIT", "ilit": "ILIT", "alit": "ALIT",
        "indfirst": "INDFIRST", "intfirst": "INTFIRST",
        "indlaws": "INDLAWS", "intlaws": "INTLAWS",
        "dates": "DATES", "nicknames": "NICKNAMES",
        "orgs": "ORGS", "awards": "AWARDS", "records": "RECORDS",
        "sports": "SPORTS", "indent": "INDENT", "intent": "INTENT",
        "bcurra": "BCURRA", "icurra": "ICURRA", "acurra": "ACURRA"
    }
    difficulties = ["easy", "medium", "hard"]
    diff_folders = {"easy": "ej", "medium": "mj", "hard": "hj"}
    
    print("Starting generation of 175 files for 35 SSC GK subjects...")
    
    total_written = 0
    for sub in subjects:
        sub_upper = subject_map[sub]
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
                    
                    if q_type == "MCQ":
                        q_data, a_data, s_data = get_mcq(sub, file_idx, q_id, sub_upper)
                    elif q_type == "MSQ":
                        q_data, a_data, s_data = get_msq(sub, file_idx, q_id, sub_upper)
                    elif q_type == "NAT":
                        q_data, a_data, s_data = get_nat(sub, file_idx, q_id, sub_upper)
                        
                    questions_list.append(q_data)
                    answers_list.append(a_data)
                    solutions_list.append(s_data)
                
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
