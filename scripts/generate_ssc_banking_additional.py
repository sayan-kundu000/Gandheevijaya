import os
import json
import random

def generate_ma(diff, q_type, idx, q_id, sub_upper, primes):
    if diff == "easy":
        if q_type == "MCQ":
            val1 = random.randint(2, 10)
            val2 = random.randint(11, 20)
            question = f"If $\\tan \\theta = {val1}/{val2}$, and $\\theta$ is acute, what is the value of $\\sin^2 \\theta + \\cos^2 \\theta$?"
            options = ["1", "0", f"{val1}/{val2}", f"{val2}/{val1}"]
            correct = "1"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Using the fundamental trigonometric identity, $\\sin^2\\theta + \\cos^2\\theta = 1$ for any angle $\\theta$."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Trigonometry", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are standard trigonometric identities?"
            options = [
                "$\\sin^2 x + \\cos^2 x = 1$",
                "$1 + \\tan^2 x = \\sec^2 x$",
                "$1 + \\cot^2 x = \\csc^2 x$",
                "$\\sin(2x) = 2\\sin x \\cos x$"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All four are standard trigonometric identities."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Trigonometry", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(1, 10)
            val2 = random.randint(1, 10)
            ans = 2 * val2 - 3 * val1
            question = f"Find the value of $k$ if the point $({val1}, {val2})$ lies on the line $3x - 2y + k = 0$."
            explanation = f"Substitute the point into the equation: $3({val1}) - 2({val2}) + k = 0 \\implies {3*val1} - {2*val2} + k = 0 \\implies k = {ans}$."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Coordinate Geometry", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["algebra math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            h = random.randint(5, 50)
            question = f"The length of the shadow of a tower of height {h} meters is {h}\\sqrt{{3}} meters. The angle of elevation of the sun is:"
            options = ["30°", "45°", "60°", "90°"]
            correct = "30°"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"$\\tan \\theta = \\text{{height}} / \\text{{shadow}} = {h} / ({h}\\sqrt{{3}}) = 1/\\sqrt{{3}} \\implies \\theta = 30^\\circ$."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Trigonometry", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["numerical speed computation"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            val1 = random.randint(2, 6)
            val2 = random.randint(7, 12)
            question = f"Which of the following values satisfy the quadratic equation $x^2 - {val1+val2}x + {val1*val2} = 0$?"
            options = [f"x = {val1}", f"x = {val2}", f"x = -{val1}", f"x = -{val2}"]
            correct = ["A", "B"]
            explanation = f"The quadratic equation factors into $(x - {val1})(x - {val2}) = 0$, so the roots are {val1} and {val2}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Algebra", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["algebra expansion"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(5, 15)
            val2 = random.randint(2, 10)
            ans = val1*val1 - 2*val2
            question = f"If $a + b = {val1}$ and $ab = {val2}$, find the value of $a^2 + b^2$."
            explanation = f"$a^2 + b^2 = (a+b)^2 - 2ab = {val1}^2 - 2({val2}) = {val1*val1} - {2*val2} = {ans}$."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Algebra", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["algebra math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            val1 = random.randint(3, 10)
            ans = val1**3 - 3*val1
            question = f"If $x + 1/x = {val1}$, then find the value of $x^3 + 1/x^3$."
            options = [str(ans), str(val1**3 + 3*val1), str(val1**3), str(val1**2)]
            correct = str(ans)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"$x^3 + 1/x^3 = (x+1/x)^3 - 3(x+1/x) = {val1}^3 - 3({val1}) = {val1**3} - {3*val1} = {ans}$."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Algebra", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["algebra math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following properties are correct for a cyclic quadrilateral $ABCD$?"
            options = [
                "Opposite angles sum to 180°",
                "Exterior angle is equal to interior opposite angle",
                "Sum of all four interior angles is 360°",
                "The vertices lie on a single circle"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options are standard properties of cyclic quadrilaterals."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Geometry", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            triplets = [(10, 6, 16), (13, 5, 24), (15, 9, 24), (25, 7, 48), (17, 8, 30)]
            val1, val2, ans = random.choice(triplets)
            question = f"In a circle of radius {val1} cm, a chord is drawn at a distance of {val2} cm from the center. Find the length of the chord in cm."
            explanation = f"Using Pythagoras theorem on the right triangle formed by the radius, perpendicular from center, and half chord: $\\text{{half-chord}} = \\sqrt{{{val1}^2 - {val2}^2}} = \\sqrt{{{val1**2 - val2**2}}} = {ans//2}$. Chord length = 2 * {ans//2} = {ans} cm."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Geometry", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_qa(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            val1 = random.randint(1, 10) * 100
            val2 = random.choice([10, 20, 30])
            sp = val1 + (val1 * val2) // 100
            question = f"A retailer purchases a product at cost price CP = {val1} INR, and sells it at a profit of {val2}%. What is the selling price of the product?"
            options = [f"{sp} INR", f"{sp + 10} INR", f"{sp - 10} INR", f"{sp + 20} INR"]
            correct = f"{sp} INR"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Selling Price = Cost Price * (1 + Profit/100) = {val1} * (1 + {val2}/100) = {sp} INR."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Arithmetic", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["commercial math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements regarding rates of work and efficiency are CORRECT?"
            options = [
                "If a person completes work in N days, their rate of work per day is 1/N.",
                "If A is twice as efficient as B, A takes half the time B takes to complete the work.",
                "If two people work together with daily rates R1 and R2, their combined rate is R1 + R2.",
                "Efficiency is inversely proportional to the time required to complete a fixed task."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All statements are basic work-time efficiency invariants."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Work and Time", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(10, 20)
            val2 = random.randint(20, 30)
            val3 = random.randint(30, 40)
            # Make sum divisible by 4
            s = val1 + val2 + val3
            val4 = ((s // 4) + 1) * 4 - s
            ans = (val1 + val2 + val3 + val4) // 4
            question = f"What is the mathematical average (arithmetic mean) of the numbers: {val1}, {val2}, {val3}, and {val4}?"
            explanation = f"Average = (Sum of elements) / 4 = ({val1} + {val2} + {val3} + {val4}) / 4 = {val1+val2+val3+val4} / 4 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Arithmetic", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["arithmetic division"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            val1 = random.randint(5, 20)
            val2 = random.randint(2, 8)
            question = f"A machine prints {10 * val1} pages in 10 minutes. How many pages does it print in {val2} minutes?"
            options = [str(val1 * val2), str(val1 * val2 + 10), str(val1 * val2 - 10), str(val1 * val2 + 20)]
            correct = str(val1 * val2)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Rate = {10 * val1} / 10 = {val1} pages/minute. In {val2} minutes: {val2} * {val1} = {val1 * val2} pages."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Rates", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["rates math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            val1 = 2
            val2 = 3
            val3 = random.randint(10, 50)
            total = (val1 + val2) * val3
            question = f"If A and B start a business with investments in the ratio {val1}:{val2}, and the total profit is {total} INR, which of the following statements are CORRECT?"
            options = [
                f"A's share of profit is {val1 * val3} INR.",
                f"B's share of profit is {val2 * val3} INR.",
                "Total profit is divided in the ratio of their investments.",
                f"B receives {(val2 - val1) * val3} INR more than A."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = f"Profits are shared in the ratio {val1}:{val2}. A's share = {val1}/{val1+val2} * {total} = {val1*val3} INR. B's share = {val2}/{val1+val2} * {total} = {val2*val3} INR. Difference = B's - A's = {val2*val3 - val1*val3} INR."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Partnership", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["ratio sharing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.choice([5, 10, 15, 20, 25, 30])
            ans = int(val1 * 3.6)
            question = f"If a bike travels at {val1} m/s, what is its speed in km/h?"
            explanation = f"Speed in km/h = Speed in m/s * 18/5 = {val1} * 3.6 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Speed and Distance", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["unit conversion"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            rates = [(1000, 1100, 10), (2000, 2200, 10), (4000, 4800, 20), (5000, 6000, 20)]
            val1, val2, pct = random.choice(rates)
            question = f"A sum of money compounded annually becomes {val1} INR in 2 years and {val2} INR in 3 years. What is the rate of interest per annum?"
            options = [f"{pct}%", f"{pct + 5}%", f"{pct - 5}%", "15%"]
            correct = f"{pct}%"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"The difference in amount between year 2 and year 3 is the interest earned on year 2 amount. Interest = {val2} - {val1} = {val2 - val1} INR. Rate = ({val2 - val1}) / {val1} * 100 = {pct}%."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Compound Interest", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["commercial math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "A jar contains a mixture of milk and water. Which of the following operations will decrease the concentration of milk in the jar?"
            options = [
                "Adding pure water to the jar",
                "Replacing a portion of the mixture with pure water",
                "Adding a mixture of milk and water that has a lower concentration of milk than the current mixture",
                "Removing a portion of the mixture and not replacing it"
            ]
            correct = ["A", "B", "C"]
            explanation = "Removing a portion of the mixture does not change the ratio/concentration of milk. The other three operations add more water relative to milk, decreasing the milk concentration."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Mixtures", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["ratio sharing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = 10
            val2 = 15
            val3 = 3
            # work done = 3 * (1/10 + 1/15) = 3 * (5/30) = 0.5
            # remaining work = 0.5 -> 50%
            ans = 50
            question = f"A and B can complete a task in {val1} and {val2} days respectively. They work together for {val3} days. What is the remaining percentage of work left to be done?"
            explanation = f"Daily rates: A = 1/{val1}, B = 1/{val2}. Combined daily rate = 1/{val1} + 1/{val2} = 5/30 = 1/6. In {val3} days, work completed = {val3} * (1/6) = 1/2 = 50%. Remaining work = 100% - 50% = 50%."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Work and Time", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["commercial math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_mr(diff, q_type, idx, q_id, sub_upper, primes):
    if diff == "easy":
        if q_type == "MCQ":
            p1 = primes[idx % 5]
            p2 = primes[(idx + 1) % 5 + 5]
            p3 = primes[(idx + 2) % 5 + 10]
            comp = random.choice([4, 6, 8, 9, 10, 12])
            question = f"Identify the composite number (odd one out) in the sequence: {p1}, {p2}, {p3}, and {comp}."
            options = [str(comp), str(p1), str(p2), str(p3)]
            correct = str(comp)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"{p1}, {p2}, and {p3} are prime numbers. {comp} is a composite number, making it the odd one out."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Puzzles", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["number classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            k = random.randint(5, 15)
            question = f"Which of the following mathematical operations yield the value {k}?"
            options = [
                f"{k - 2} + 2",
                f"{k * 2} - {k}",
                f"{k + 5} - 5",
                f"{2 * k} / 2"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = f"All options evaluate exactly to {k}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Arithmetic Operations", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 10)
            val2 = random.randint(3, 8)
            ans = val1 + 4 * val2
            question = f"What is the next number in the arithmetic progression sequence: {val1}, {val1+val2}, {val1+2*val2}, {val1+3*val2}, _____?"
            explanation = f"The common difference is {val2}. Next term = {val1+3*val2} + {val2} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Puzzles", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["pattern completion"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            # Code value: D(4)+O(15)+G(7) = 26
            question = "If BAT is coded as 23 (2+1+20) and CAT is coded as 24 (3+1+20), what is the code for the word DOG?"
            options = ["26", "22", "28", "24"]
            correct = "26"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "D = 4, O = 15, G = 7. Sum = 4 + 15 + 7 = 26."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Coding Sequences", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["coding math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            p1, p2, p3 = 2, 3, 5
            comp = 4
            question = f"Which of the following numbers are prime numbers?"
            options = [str(p1), str(p2), str(p3), str(comp)]
            correct = ["A", "B", "C"]
            explanation = "2, 3, and 5 are prime numbers because they have only two positive factors: 1 and themselves. 4 is composite (divisible by 1, 2, 4)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Properties", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 185
            question = "Find the missing number in the sequence: 4, 9, 20, 43, 90, ?"
            explanation = "The pattern is: x_n = x_{n-1} * 2 + (n-1). 4*2+1 = 9; 9*2+2 = 20; 20*2+3 = 43; 43*2+4 = 90; 90*2+5 = 185."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Puzzles", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["pattern completion"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "If 'sky is blue' is coded as '4 8 2', 'blue water is clear' is coded as '8 1 2 6', and 'clear sky' is '4 1', what is the code for 'water'?"
            options = ["6", "8", "2", "4"]
            correct = "6"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Comparing statements: 'sky' is 4, 'clear' is 1. 'blue' and 'is' are 8 and 2. Therefore, in 'blue water is clear' (8 1 2 6), the remaining code for 'water' is 6."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Coding Sequences", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["analogy logic"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "A person travels 10 km North, turns left and travels 5 km, then turns left again and travels 10 km. Which of the following statements are CORRECT?"
            options = [
                "The person is 5 km away from the starting point.",
                "The person is facing South.",
                "The person is directly West of the starting point.",
                "The total distance traveled is 25 km."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "Tracing the path: Start at (0,0). North 10 -> (0,10). Left (West) 5 -> (-5, 10). Left (South) 10 -> (-5,0). Distance from start is 5 km West. Facing South. Total distance = 10 + 5 + 10 = 25 km."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Direction Sense", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 216
            question = "What is the value of the missing term in the sequence: 1, 8, 27, 64, 125, ?"
            explanation = "The sequence represents the cubes of consecutive natural numbers: 1^3, 2^3, 3^3, 4^3, 5^3. The next term is 6^3 = 216."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Puzzles", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["pattern completion"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_va(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Select the correct option to fill in the blank:\n\n`The committee _____ divided in their opinions yesterday.`"
            options = ["were", "was", "is", "are"]
            correct = "were"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "When a collective noun indicates division among its members, a plural verb ('were') is used."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Grammar", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["grammar parsing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following vocabulary pairs represent CORRECT synonym pairings?"
            options = [
                "Magnify / Enlarge",
                "Timid / Shy",
                "Abundant / Plentiful",
                "Rapid / Quick"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All pairs represent accurate synonym associations."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["word matching"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 6
            question = "Calculate the number of vowels (letters matching A, E, I, O, U) in the word: `EXAMINATION`."
            explanation = "The vowels in 'EXAMINATION' are E, A, I, A, I, O, which gives a count of 6."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["string analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "Identify the antonym of the word 'ELEVATE'."
            options = ["Lower", "Raise", "Promote", "Ascend"]
            correct = "Lower"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Elevate means to raise. The opposite is lower."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["word matching"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following sentences contain grammatical errors?"
            options = [
                "Neither of the two candidates have submitted their resume.",
                "One of my friends are going to London.",
                "Each of the students was given a book.",
                "He has been working since three hours."
            ]
            correct = ["A", "B", "D"]
            explanation = "A should use singular 'has'. B should use singular 'is' (One of my friends is...). D should use 'for' instead of 'since' for a duration."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Grammar", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["grammar parsing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 5
            question = "How many letters are in the word that is the synonym of 'Huge' and starts with 'G'?"
            explanation = "The word is GIANT, which contains 5 letters."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["string size"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Choose the correct spelling:"
            options = ["Acquiesce", "Acquese", "Acquiece", "Acquiesc"]
            correct = "Acquiesce"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The correct spelling is 'Acquiesce' (to accept something reluctantly but without protest)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Spelling", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["dictionary spelling"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following words are spelled correctly?"
            options = [
                "Millennium",
                "Accommodation",
                "Questionnaire",
                "Liaison"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options are spelled correctly."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Spelling", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["dictionary spelling"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 4
            question = "Find the number of syllables in the word `INDUSTRIOUS`."
            explanation = "The word 'in-dus-tri-ous' contains exactly 4 syllables."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["string analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_vr(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Choose the word that completes the analogy:\n\n`Book : Read :: Fork : _____`"
            options = ["Eat", "Sleep", "Write", "Draw"]
            correct = "Eat"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "A book is read; a fork is used to eat. This is a functional relationship analogy."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Analogies", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["analogy logic"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Consider premises: 'All dogs are animals. All golden retrievers are dogs.' Which of the following conclusions are CORRECT?"
            options = [
                "All golden retrievers are animals.",
                "Some animals are dogs.",
                "If it is not an animal, it is not a golden retriever.",
                "Some dogs are golden retrievers."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All assertions represent valid deductive conclusions of the premises."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syllogisms", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["syllogism checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 1
            question = "If 'CAT' is coded as 'DBU' (+1 shift), what is the letter shift distance value?"
            explanation = "The shift is exactly +1. C -> D (+1), A -> B (+1), T -> U (+1)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Coding Sequences", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["coding math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "Select the pair that exhibits the same relation: Light : Dark :: _____"
            options = ["Hot : Cold", "Sun : Moon", "Black : Ink", "Heavy : Load"]
            correct = "Hot : Cold"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Light and Dark are antonyms, just like Hot and Cold."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Analogies", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["analogy logic"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Statements: All cars are vehicles. Some vehicles are electric. Which statements are CORRECT?"
            options = [
                "A car is a vehicle.",
                "If a vehicle is electric, it is not necessarily a car.",
                "It is possible that some cars are electric.",
                "It is possible that no cars are electric."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "These conclusions follow standard Venn diagram overlapping models."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syllogisms", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["syllogism checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 6
            question = "How many letters are in the antonym of 'COMPLEX'?"
            explanation = "The antonym of complex is 'SIMPLE' which has 6 letters."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vocabulary", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["string size"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Statement: 'The government has decided to increase the import duty on electronic goods.' Which of the following is a logical course of action?"
            options = [
                "The domestic electronics manufacturers should increase their production.",
                "The government should lower tax on other goods.",
                "The import of electronic goods should be completely banned.",
                "Consumers should stop buying electronic items."
            ]
            correct = "The domestic electronics manufacturers should increase their production."
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Increasing import duty protects domestic industry, so increasing domestic production is a logical course of action."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Course of Action", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["logical deduction"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following arguments weaken the claim: 'Social media improves interpersonal relationships'?"
            options = [
                "Studies show that high social media use correlates with increased loneliness.",
                "People often replace face-to-face interactions with text-based ones.",
                "Online interactions can lead to misunderstandings due to lack of non-verbal cues.",
                "Social media allows people to stay in touch across long distances."
            ]
            correct = ["A", "B", "C"]
            explanation = "A, B, and C present negative impacts on relationships, weakening the claim. D presents a positive impact, strengthening it."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Critical Reasoning", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["argument weakening"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 5
            question = "In the word 'REASONING', what is the index (1-based) of the first occurrence of letter 'O'?"
            explanation = "R(1)-E(2)-A(3)-S(4)-O(5)-N(6)-I(7)-N(8)-G(9). First 'O' is at index 5."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "String Analysis", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["string analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_lr(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "A is B's brother. B is C's sister. What is A's relation to C?"
            options = ["Brother", "Sister", "Uncle", "Father"]
            correct = "Brother"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "A is the brother of B, who is the sister of C. This means they are all siblings, so A is C's brother."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Blood Relations", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["relational mapping"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Consider the ordering constraints: 'A is taller than B. B is taller than C.' Which of the following statements are CORRECT?"
            options = [
                "A is taller than C.",
                "C is shorter than A.",
                "C is shorter than B.",
                "A is the tallest among the three."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "By transitivity, A > B > C. Therefore all options are correct."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Ordering", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["order checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 5
            question = "A person walks 3 km East, and then turns and walks 4 km North. How far (in km) is the person from their starting point?"
            explanation = "Distance = sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5 km."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Directions", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["vector math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A is to the left of B. B is to the left of C. Who is in the middle?"
            options = ["B", "A", "C", "Cannot be determined"]
            correct = "B"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The order from left to right is A - B - C, so B is in the middle."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Seating Arrangement", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["ordering"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "If X is older than Y, and Y is older than Z, which statements are CORRECT?"
            options = [
                "X is older than Z.",
                "Z is younger than X.",
                "Z is younger than Y.",
                "X is the oldest."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "X > Y > Z. All statements are true."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Ordering", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["order checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 90
            question = "A clock shows 3:00. What is the angle in degrees between the hour hand and minute hand?"
            explanation = "At 3:00, the hour hand is at 3 and the minute hand is at 12. Angle = 3 * 30 degrees = 90 degrees."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Clock Puzzles", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["angle math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Five people A, B, C, D, E are sitting in a circle facing the center. A is between E and D. B is to the immediate right of E. Who is to the immediate left of D?"
            options = ["C", "A", "B", "E"]
            correct = "C"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Arranging clockwise: E - B - C - D - A. D is between C and A. Immediate left of D (clockwise) is C."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Seating Arrangement", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["ordering"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "If P is taller than Q, R is shorter than P, and S is taller than T but shorter than Q, which of the following statements must be CORRECT?"
            options = [
                "P is taller than S.",
                "Q is taller than T.",
                "P is taller than T.",
                "S is taller than T."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "P > Q > S > T. This means P, Q, and S are all taller than T, and P is taller than S."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Ordering", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["order checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 42
            question = "If in a row of students, Anil is 12th from the left and Sunil is 18th from the right, and they interchange positions, Anil becomes 25th from the left. How many students are there in the row?"
            explanation = "Sunil's old position is Anil's new position from the right, which is 18th. Anil's new position from the left is 25th. Total = 25 + 18 - 1 = 42."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Row Arrangement", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["order checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_sa(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            val1, val2, val3 = 3, 4, 5
            ans = val1 * val2 * val3
            question = f"A larger solid block is composed of smaller unit cubes. If the dimensions are {val1} x {val2} x {val3}, how many unit cubes are used?"
            options = [str(ans), str(ans + 5), str(ans - 5), str(ans + 10)]
            correct = str(ans)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Volume = width * height * depth = {val1} * {val2} * {val3} = {ans} unit cubes."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Block Counting", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["volume calculation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following alphabetic characters exhibit vertical line symmetry?"
            options = ["A", "H", "M", "T"]
            correct = ["A", "B", "C", "D"]
            explanation = "All these letters are symmetric about a vertical line down the middle."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Symmetries", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["symmetry checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(3, 8)
            ans = val1 + 1
            question = f"A regular pyramid has a base containing exactly {val1} sides. How many corner vertices exist?"
            explanation = f"A pyramid has {val1} base vertices plus 1 apex vertex, total {val1 + 1}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "3D Shapes", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "If a square is rotated by 90 degrees clockwise, how many edges remain horizontal?"
            options = ["2", "0", "1", "4"]
            correct = "2"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "A square has 2 horizontal and 2 vertical edges. After rotation, vertical edges become horizontal, so there are still 2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Rotations", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["rotation geometry"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following shapes have rotational symmetry of order 4 (restored to original form at 90, 180, 270, 360 degrees)?"
            options = ["Square", "Regular octagon", "Circle", "Equilateral triangle"]
            correct = ["A", "B", "C"]
            explanation = "Square (order 4), Octagon (order 8, includes order 4), and Circle (infinite order, includes order 4) have it. Equilateral triangle has order 3 symmetry."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Symmetries", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["symmetry checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 6
            question = "How many faces does a standard cube have?"
            explanation = "A standard cube has 6 faces."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "3D Shapes", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "A cube of side 4 cm is painted red on all faces and cut into 1 cm cubes. How many small cubes have exactly 3 faces painted?"
            options = ["8", "12", "24", "4"]
            correct = "8"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Only the corner cubes have exactly 3 faces painted. A cube always has 8 corners, so the answer is 8."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "3D Shapes", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following 3D shapes are Platonic solids?"
            options = ["Tetrahedron", "Hexahedron (Cube)", "Octahedron", "Dodecahedron"]
            correct = ["A", "B", "C", "D"]
            explanation = "All four are regular Platonic solids."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "3D Shapes", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 30
            question = "How many edges does an icosahedron have?"
            explanation = "An icosahedron has 20 faces, 12 vertices, and 30 edges."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "3D Shapes", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["spatial geometry counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_aa(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            val1 = random.randint(10, 25)
            val2 = random.randint(15, 30)
            question = f"Consider the sales table:\n\n| Company | Year 1 Sales (M$) | Year 2 Sales (M$) |\n|---|---|---|\n| Company A | {val1} | 20 |\n| Company B | 30 | {val2} |\n\nWhat is the ratio of Company A's Year 1 sales to Company B's Year 2 sales?"
            options = [f"{val1}:{val2}", f"{val1 + 2}:{val2}", f"{val1}:{val2 + 2}", "1:1"]
            correct = f"{val1}:{val2}"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Company A's Year 1 sales is {val1}. Company B's Year 2 sales is {val2}. The ratio is {val1}:{val2}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["data reading"], "representation": ["table"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements regarding general data analysis are CORRECT?"
            options = [
                "Sales growth can be calculated as (Year 2 - Year 1) / Year 1.",
                "If sales increase while costs remain constant, profit must increase.",
                "A pie chart represents the proportional share of components to a total sum.",
                "A line graph is ideal for representing continuous trend updates over time."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All statements correctly state data analysis and plotting properties."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(10, 30) * 2
            val2 = random.randint(20, 40) * 2
            ans = (val1 + val2) // 2
            question = f"Calculate the average sales (in millions) across the two years: Year 1 = {val1}, Year 2 = {val2}."
            explanation = f"Average = (Year 1 + Year 2) / 2 = ({val1} + {val2}) / 2 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["arithmetic math"], "representation": ["table"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            val1 = random.randint(10, 50)
            question = f"If a store's sales were {10 * val1} last year and increased by 50% this year, what are this year's sales?"
            options = [str(15 * val1), str(10 * val1), str(20 * val1), str(12 * val1)]
            correct = str(15 * val1)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Increase = 50% of {10 * val1} = {5 * val1}. New sales = {10 * val1} + {5 * val1} = {15 * val1}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["commercial math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "A table shows sales: Year 1 = 10, Year 2 = 12, Year 3 = 15. Which statements are CORRECT?"
            options = [
                "Sales increased from Year 1 to Year 2.",
                "Sales increased from Year 2 to Year 3.",
                "The growth rate from Year 1 to Year 2 was 20%.",
                "Sales grew continuously across the three years."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "Sales grew continuously (10 -> 12 -> 15). Growth Year 1 to 2 = (12-10)/10 * 100% = 20%."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["comparative checks"], "representation": ["table"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(10, 50)
            ans = 3 * val1
            question = f"If a factory output was {val1} tons, and we triple it, what is the new output in tons?"
            explanation = f"New output = 3 * {val1} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["arithmetic math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Statement: 'Should all major public sector banks in India be privatized?'\nArguments:\nI. Yes, it will improve efficiency and customer service.\nII. No, it will lead to job losses and affect rural banking."
            options = ["Both arguments I and II are strong", "Only argument I is strong", "Only argument II is strong", "Neither argument I nor II is strong"]
            correct = "Both arguments I and II are strong"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Both arguments present valid socioeconomic and operational perspectives and are strong."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Sufficiency", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["logical deduction"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "In a company, the ratio of male to female employees is 3:2. If there are 500 employees, which of the following statements are CORRECT?"
            options = [
                "There are 300 male employees.",
                "There are 200 female employees.",
                "Male employees constitute 60% of the workforce.",
                "Female employees constitute 40% of the workforce."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "Males = 500 * 3/5 = 300 (60%). Females = 500 * 2/5 = 200 (40%). All options are correct."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Data Interpretation", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["comparative checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 85
            question = "The average weight of 8 men is increased by 2.5 kg when a new man replaces one of them who weighs 65 kg. What is the weight of the new man in kg?"
            explanation = "Increase in total weight = 8 * 2.5 = 20 kg. Since the new man replaces a 65 kg man and increases the total by 20 kg, the new man's weight = 65 + 20 = 85 kg."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Averages", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["arithmetic math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_ar(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "What is the next logical step in the sequence:\n\n`[* - -]`, `[- * -]`, `[- - *]`, `_____`?"
            options = ["`[* - -]`", "`[- * -]`", "`[- - *]`", "`[* * *]`"]
            correct = "`[* - -]`"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The star '*' shifts right by one position at each step and wraps around to the beginning, creating a cyclic shift pattern."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequences", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["pattern translation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following geometric transformations on a regular 2D square preserve its outer shape profile?"
            options = [
                "Rotation by 90 degrees clockwise.",
                "Rotation by 180 degrees counter-clockwise.",
                "Reflection across its vertical center axis.",
                "Reflection across its main diagonal axis."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "A regular square has 4-fold rotational symmetry and reflectional symmetry across diagonals and center lines."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transformations", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["symmetry checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 6)
            val2 = random.randint(3, 8)
            ans = 4 * val1 * val2
            question = f"A grid of cells has {val1} rows and {val2} columns. If we double both the number of rows and columns, how many total cells will the new expanded grid have?"
            explanation = f"Original cells = {val1} * {val2} = {val1*val2}. New cells = (2*{val1}) * (2*{val2}) = 4 * {val1} * {val2} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transformations", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["dimension scaling"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "What shape comes next in sequence: Triangle, Square, Pentagon, _____"
            options = ["Hexagon", "Heptagon", "Octagon", "Square"]
            correct = "Hexagon"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The sequence represents regular polygons with increasing side count: 3 (Triangle), 4 (Square), 5 (Pentagon), so the next is 6 (Hexagon)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequences", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["pattern matching"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are regular polygons?"
            options = [
                "Equilateral triangle",
                "Square",
                "Regular pentagon",
                "Regular hexagon"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "Regular polygons must have all sides equal and all angles equal, which is true for all options."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transformations", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(3, 10)
            ans = val1 + 3
            question = f"If a shape with {val1} sides increases its side count by 3, how many sides does it have?"
            explanation = f"New sides = {val1} + 3 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequences", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["arithmetic math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "If figure A is related to B by a 90-degree clockwise rotation and color inversion, find the matching figure in analogy C : D."
            options = ["Figure 1", "Figure 2", "Figure 3", "Figure 4"]
            correct = "Figure 1"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The relation is a 90-degree clockwise rotation combined with color inversion."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Analogies", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["pattern translation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following shapes possess rotational symmetry of order greater than 1?"
            options = [
                "Circle",
                "Equilateral Triangle",
                "Rectangle",
                "Scalene Triangle"
            ]
            correct = ["A", "B", "C"]
            explanation = "Circle (infinite), Equilateral Triangle (order 3), and Rectangle (order 2) have rotational symmetry. Scalene triangle has order 1."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transformations", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["symmetry checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            ans = 8
            question = "What is the order of rotational symmetry of a regular octagon?"
            explanation = "A regular octagon is symmetric under rotations of multiples of 360/8 = 45 degrees, so it has rotational symmetry of order 8."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequences", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["symmetry checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def main():
    base_dir = "datasets"
    subjects = ["ma", "mr", "qa", "va", "vr", "lr", "sa", "aa", "ar"]
    subject_map = {
        "ma": "MA",
        "mr": "MR",
        "qa": "QA",
        "va": "VA",
        "vr": "VR",
        "lr": "LR",
        "sa": "SA",
        "aa": "AA",
        "ar": "AR"
    }
    difficulties = ["easy", "medium", "hard"]
    diff_folders = {"easy": "ej", "medium": "mj", "hard": "hj"}
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    print("Starting generation of 150 additional files per subject and difficulty...")
    
    total_written = 0
    for sub in subjects:
        sub_upper = subject_map[sub]
        for diff in difficulties:
            diff_f = diff_folders[diff]
            
            # Ensure directories exist
            os.makedirs(os.path.join(base_dir, sub, diff_f, "quesj"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, sub, diff_f, "ansj"), exist_ok=True)
            os.makedirs(os.path.join(base_dir, sub, diff_f, "solnj"), exist_ok=True)
            
            for file_idx in range(26, 176):
                # Unique seed per file, subject, difficulty to ensure diversity
                seed_val = hash(f"{sub}_{diff}_{file_idx}") & 0xffffffff
                random.seed(seed_val)
                
                q_file_name = f"{sub}{file_idx:02d}{diff_f[0]}q.json"
                a_file_name = f"{sub}{file_idx:02d}{diff_f[0]}a.json"
                s_file_name = f"{sub}{file_idx:02d}{diff_f[0]}s.json"
                
                questions_list = []
                answers_list = []
                solutions_list = []
                
                for q_type in ["MCQ", "MSQ", "NAT"]:
                    q_id = f"GCS27-{sub_upper}-{diff[0].upper()}-{q_type}-{file_idx:03d}"
                    
                    question_data = None
                    if sub == "ma":
                        question_data = generate_ma(diff, q_type, file_idx, q_id, sub_upper, primes)
                    elif sub == "qa":
                        question_data = generate_qa(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "mr":
                        question_data = generate_mr(diff, q_type, file_idx, q_id, sub_upper, primes)
                    elif sub == "va":
                        question_data = generate_va(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "vr":
                        question_data = generate_vr(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "lr":
                        question_data = generate_lr(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "sa":
                        question_data = generate_sa(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "aa":
                        question_data = generate_aa(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "ar":
                        question_data = generate_ar(diff, q_type, file_idx, q_id, sub_upper)
                    
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
