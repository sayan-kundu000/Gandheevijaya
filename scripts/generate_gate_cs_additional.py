import os
import json
import random

# Prime numbers helper
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def generate_cprog(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            val1 = random.randint(2, 10)
            question = f"What is the output of the following C code snippet?\n```c\n#include <stdio.h>\nint main() {{\n    int x = {val1};\n    int *p = &x;\n    *p = *p + 5;\n    printf(\"%d\", x);\n    return 0;\n}}\n```"
            ans = str(val1 + 5)
            options = [ans, str(val1), "Error", "0"]
            random.shuffle(options)
            correct_letter = chr(65 + options.index(ans))
            explanation = f"Pointer `p` points to `x`. Dereferencing and modifying `*p` directly modifies `x` from {val1} to {val1 + 5}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Pointers", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["pointer dereference"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are valid C variable declaration and initialization statements?"
            options = [
                "int x = 10;",
                "float y = 5.5f;",
                "char c = 'A';",
                "double z = 2.3e4;"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent syntactically correct variable declarations and initializations in C."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syntax", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["syntax check"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(1, 5)
            # f(x) = x + 3 -> recurses once
            ans = val1 + 3
            question = f"Consider the following C function:\n```c\nint f(int n) {{\n    if (n <= 1) return {ans};\n    return f(n-1);\n}}\n```\nFind the value returned by calling `f({val1})`."
            explanation = f"Since the recursion base case returns `{ans}` and the function returns `f(n-1)` without modification, any call `f(n)` returns `{ans}`."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Recursion", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["recursion parsing"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            val1 = random.randint(2, 8)
            question = f"Consider the following C snippet:\n```c\nint arr[] = {{1, 2, 3, 4, 5}};\nint *p = arr;\np += {val1 % 4};\nprintf(\"%d\", *p);\n```\nWhat is printed?"
            ans = str(1 + (val1 % 4))
            options = [ans, "1", "2", "Error"]
            random.shuffle(options)
            correct_letter = chr(65 + options.index(ans))
            explanation = f"Pointer `p` points to elements of `arr`. Incrementing it by {val1 % 4} moves it to index {val1 % 4}, which contains {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Arrays", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["pointer arithmetic"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about C dynamic memory allocation functions are CORRECT?"
            options = [
                "malloc allocates memory blocks without initializing them.",
                "calloc initializes all bits of allocated memory to zero.",
                "free deallocates the memory allocated by malloc/calloc.",
                "realloc can increase or decrease the size of allocated memory."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard behaviors of malloc, calloc, free, and realloc in C."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Memory Management", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["standard properties checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(3, 8)
            ans = val1 * (val1 + 1) // 2
            question = f"Calculate the number of times `printf` is executed in the code below:\n```c\nfor(int i = 1; i <= {val1}; i++) {{\n    for(int j = 1; j <= i; j++) {{\n        printf(\"*\");\n    }}\n}}\n```"
            explanation = f"The loop runs for j = 1..i for each i = 1..{val1}. Total executions = Sum of 1..{val1} = {val1}*({val1}+1)/2 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Loops", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["nested loop analysis"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Trace the output of the C snippet below:\n```c\n#include <stdio.h>\nstruct S {{\n    int x;\n    char y;\n}};\nint main() {{\n    struct S s1 = {{10, 'A'}};\n    struct S s2 = s1;\n    s2.x = 20;\n    printf(\"%d %c\", s1.x, s1.y);\n    return 0;\n}}\n```"
            options = ["10 A", "20 A", "10 B", "20 B"]
            correct = "10 A"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Structures are copied by value in C. Modifying `s2.x` has no effect on `s1.x`, which remains 10."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Structures", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["structure assignment analysis"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about argument passing in C are CORRECT?"
            options = [
                "C uses pass-by-value strictly for all primitive variables.",
                "Passing a pointer to a function simulates pass-by-reference.",
                "Modifying the dereferenced pointer inside the function affects the original caller variable.",
                "Modifying the local pointer parameter copy inside the function does not change the original caller pointer."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options correctly state how parameter passing works in C."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Functions", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["parameter routing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 4)
            # recursions: f(val1)
            # f(n) = n * f(n-1) -> f(n) = n!
            ans = 1
            for k in range(1, val1 + 1):
                ans *= k
            question = f"Consider the following recursive C function with a static variable:\n```c\nint f(int n) {{\n    if (n <= 1) return 1;\n    return n * f(n-1);\n}}\n```\nWhat is the return value of `f({val1})`?"
            explanation = f"The function computes factorial of n. For n = {val1}, return value is {val1}! = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Recursion", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["recursion parsing"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_dsa(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "What is the worst-case time complexity of inserting an element into a Queue implemented using a Singly Linked List (with head and tail pointers)?"
            options = ["O(1)", "O(n)", "O(log n)", "O(n log n)"]
            correct = "O(1)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "With a tail pointer, insertion at the end of a queue (enqueue operation) takes constant time O(1)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Queue", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["complexity analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are properties of a Binary Search Tree (BST)?"
            options = [
                "The left subtree contains only nodes with keys less than the root's key.",
                "The right subtree contains only nodes with keys greater than the root's key.",
                "Both left and right subtrees must also be binary search trees.",
                "Inorder traversal of a BST yields keys in sorted ascending order."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard defining properties and traits of a BST."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "BST", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(5, 25)
            ans = val1 + 1
            question = f"In a strictly binary tree (every node has either 0 or 2 children), if there are {val1} internal nodes, find the number of leaf nodes."
            explanation = f"For any strictly binary tree, Leaf Nodes = Internal Nodes + 1. Leaf Nodes = {val1} + 1 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Trees", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["tree counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "If the inorder traversal of a binary search tree is D B E A F C G and its preorder traversal is A B D E C F G, what is its postorder traversal?"
            options = ["D E B F G C A", "D B E F G C A", "E D B G F C A", "D E B G F C A"]
            correct = "D E B F G C A"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Reconstructing the tree reveals root A, left child B (with children D, E), and right child C (with children F, G). Postorder: D-E-B-F-G-C-A."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Trees", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["tree traversal"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about Max-Heaps are CORRECT?"
            options = [
                "The key in the root node must be greater than or equal to the keys of its children.",
                "A heap is a complete binary tree.",
                "Insertion in a heap takes O(log n) time.",
                "Finding the maximum key in a max-heap takes O(1) time."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard correct assertions about max-heaps."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Heaps", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Height of AVL tree with N nodes
            # If we insert elements in sorted order: 1, 2, 3...
            # An AVL tree preserves log height.
            # Let's ask: What is minimum nodes in AVL tree of height H?
            # N(0) = 1, N(1) = 2, N(2) = 4, N(3) = 7, N(4) = 12
            h = random.choice([2, 3, 4])
            tbl = {2: 4, 3: 7, 4: 12}
            ans = tbl[h]
            question = f"What is the minimum number of nodes required to construct an AVL tree of height {h} (where height of a single node tree is 0)?"
            explanation = f"AVL tree node recurrence: N(h) = N(h-1) + N(h-2) + 1. Base cases: N(0)=1, N(1)=2. N(2)=1+2+1=4. N(3)=2+4+1=7. N(4)=4+7+1=12."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "AVL Trees", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["avl recurrence"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "What is the worst-case number of parent pointer updates when inserting an element into a red-black tree with n nodes?"
            options = ["O(log n)", "O(1)", "O(n)", "O(n log n)"]
            correct = "O(log n)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "While recoloring propagates up the tree (requiring O(log n) color updates and corresponding parent checks), rotation updates are bounded by O(1) constant pointer swaps."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Red-Black Trees", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["tree operations complexity"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about Graph representations are CORRECT?"
            options = [
                "Adjacency matrix representation requires O(V^2) space.",
                "Adjacency list representation requires O(V + E) space.",
                "Checking if edge (u, v) exists takes O(1) time in adjacency matrix.",
                "Checking if edge (u, v) exists takes O(V) worst-case time in adjacency list."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct spatial and temporal trade-offs for adjacency matrices and lists."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graphs", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # B-tree nodes calculation
            # Max keys in B-tree of order m, height h
            t = random.randint(3, 5) # min degree
            # Max keys = 2*t^h - 1
            h = 2
            ans = 2 * (t**h) - 1
            question = f"Find the maximum number of keys that can be stored in a B-Tree of height {h} (where height of root node alone is 0) and minimum degree t = {t}."
            explanation = f"Max keys in B-Tree of min degree t and height h is 2*t^(h) - 1. For t={t}, h={h}: Max keys = 2*{t}^{h} - 1 = 2*{t**h} - 1 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "B-Trees", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["btree key counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_algo(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "What is the worst-case time complexity of Quick Sort when the pivot is always chosen as the minimum or maximum element?"
            options = ["O(n^2)", "O(n log n)", "O(n)", "O(log n)"]
            correct = "O(n^2)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "If the pivot is always the extreme element, partition splits the array into sizes 0 and n-1, leading to a recurrence of T(n) = T(n-1) + O(n) which is O(n^2)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sorting", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["complexity analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following algorithms employ the Greedy design paradigm?"
            options = [
                "Kruskal's algorithm for Minimum Spanning Trees",
                "Prim's algorithm for Minimum Spanning Trees",
                "Dijkstra's algorithm for Single Source Shortest Path",
                "Huffman coding algorithm for compression"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All of these algorithms use the Greedy strategy by choosing local optima at each step."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Design Paradigms", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["paradigm verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.choice([2, 4, 8, 16])
            # T(n) = val1*T(n/2) + n^log2(val1)
            # Master Theorem case 2 or 1
            # Let's do simple: T(n) = 2T(n/2) + n.
            # log_b(a) = log_2(2) = 1. f(n) = n. Case 2: T(n) = Theta(n log n).
            # Let's ask value of exponent of n in complexity.
            ans = 1
            question = f"According to the Master Theorem, if a recurrence is T(n) = 2T(n/2) + n, the asymptotic complexity is Theta(n^k \\log n). Find the value of k."
            explanation = "Here a=2, b=2. n^(log_b a) = n^1. Since f(n) = n, it falls into Master Theorem Case 2. Complexity is Theta(n log n). The exponent k of n is 1."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Recurrences", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["master theorem application"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            val1 = random.randint(20, 100)
            # worst case comparisons in binary search
            import math
            ans = int(math.floor(math.log2(val1)) + 1)
            question = f"What is the maximum number of key comparisons required to search for an element in a sorted array of size {val1} using Binary Search?"
            options = [str(ans), str(ans + 2), str(val1), str(int(val1/2))]
            correct = str(ans)
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = f"Binary search worst case comparisons = floor(log2(n)) + 1 = floor(log2({val1})) + 1 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Searching", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["search comparisons analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements comparing Dynamic Programming (DP) and Greedy methods are CORRECT?"
            options = [
                "Greedy method makes a local choice at each step; DP solves subproblems first.",
                "Greedy method does not guarantee global optimal for all problems, but DP can.",
                "DP relies on overlapping subproblems and optimal substructure.",
                "Greedy algorithms usually run faster than equivalent DP formulations."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options correctly distinguish between Greedy and Dynamic Programming design paradigms."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Design Paradigms", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["paradigm verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Matrix chain multiplication optimal cost
            # Chain of 3 matrices: A1(10x20), A2(20x30), A3(30x40)
            # Cost = min( 10*20*30 + 10*30*40, 20*30*40 + 10*20*40 )
            # Choice 1: (A1 A2) A3 -> 10*20*30 + 10*30*40 = 6000 + 12000 = 18000
            # Choice 2: A1 (A2 A3) -> 20*30*40 + 10*20*40 = 24000 + 8000 = 32000
            ans = 18000
            question = "Find the minimum scalar multiplications required to multiply three matrices $A_1$, $A_2$, $A_3$ of dimensions $10 \\times 20$, $20 \\times 30$, and $30 \\times 40$ respectively."
            explanation = "Multiplying (A1 A2) takes 10*20*30 = 6000 multiplications, resulting in a 10x30 matrix. Multiplying this by A3 takes 10*30*40 = 12000. Total = 18000. Multiplying A1(A2 A3) takes 20*30*40 + 10*20*40 = 32000. Min cost is 18000."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Dynamic Programming", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["optimization math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "If the maximum flow in a network is F, then the capacity of the minimum cut is:"
            options = ["Exactly F", "Greater than or equal to F", "Less than or equal to F", "Cannot be determined"]
            correct = "Exactly F"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "By the Max-Flow Min-Cut Theorem, the maximum flow in a network equals the capacity of its minimum cut."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graph Algorithms", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["theorem check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following problems are known to be NP-complete?"
            options = [
                "The 3-SAT problem",
                "The Vertex Cover problem",
                "The Traveling Salesperson Decision problem",
                "The Independent Set problem"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent classic NP-complete decision problems."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Complexity", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["complexity class verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Dijkstra shortest path
            # Simple graph: S -> A (weight 5), S -> B (weight 2), B -> A (weight 2)
            # Path to A is S->B->A of weight 4.
            ans = 4
            question = "In a graph with vertices S, A, B, edge weights are: w(S, A) = 5, w(S, B) = 2, w(B, A) = 2. Find the length of the shortest path from S to A."
            explanation = "Path S->A has length 5. Path S->B->A has length 2+2 = 4. The shortest path length is 4."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graph Algorithms", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["graph shortest path"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_os(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which of the following CPU scheduling algorithms can potentially lead to starvation?"
            options = ["Shortest Job First (SJF)", "Round Robin (RR)", "First-Come First-Served (FCFS)", "None of these"]
            correct = "Shortest Job First (SJF)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "SJF can lead to starvation if a continuous stream of short processes keeps arriving, preventing longer processes from executing."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Scheduling", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["starvation check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are necessary conditions for a deadlock to occur?"
            options = [
                "Mutual Exclusion",
                "Hold and Wait",
                "No Preemption",
                "Circular Wait"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All four Coffman conditions must hold simultaneously for a deadlock to occur."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Deadlocks", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["deadlock conditions verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 6)
            val2 = random.randint(7, 12)
            ans = val1 + val2
            question = f"Process P1 arrives at time 0 with burst time {val1}. P2 arrives at time 0 with burst time {val2}. Under FCFS (non-preemptive) scheduling, what is the turnaround time of P2 (if P1 is scheduled first)?"
            explanation = f"P1 runs from 0 to {val1}. P2 runs from {val1} to {val1 + val2}. P2's completion time is {val1 + val2}. Turnaround Time = Completion - Arrival = {val1+val2} - 0 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Scheduling", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["scheduling timeline"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A system uses FIFO page replacement with 3 page frames. For reference string: 1, 2, 3, 4, 1, 2, how many page faults occur (initially frames are empty)?"
            options = ["6", "4", "5", "3"]
            correct = "6"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "1: fault (1,-,-); 2: fault (1,2,-); 3: fault (1,2,3); 4: fault (4,2,3); 1: fault (4,1,3); 2: fault (4,1,2). Total page faults = 6."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Memory Management", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["page replacement simulation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about Paging are CORRECT?"
            options = [
                "Paging eliminates external fragmentation.",
                "Paging can suffer from internal fragmentation in the last page frame.",
                "Logical address space is divided into pages.",
                "Physical address space is divided into frames."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options correctly describe characteristics of the paging memory management technique."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Memory Management", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # EAT = Hit_ratio * (TLB_access + RAM_access) + Miss_ratio * (TLB_access + 2 * RAM_access)
            tlb_access = 20
            ram_access = 100
            hit_ratio = 0.90
            # EAT = 0.90 * (20 + 100) + 0.10 * (20 + 200) = 0.9 * 120 + 0.1 * 220 = 108 + 22 = 130 ns
            ans = 130
            question = f"In a paged memory system, TLB access time is {tlb_access} ns and physical memory access time is {ram_access} ns. If TLB hit ratio is 90%, calculate the effective memory access time in ns."
            explanation = f"EAT = hit_ratio * (tlb_access + ram_access) + (1 - hit_ratio) * (tlb_access + 2 * ram_access) = 0.90 * ({tlb_access} + {ram_access}) + 0.10 * ({tlb_access} + 2 * {ram_access}) = 108 + 22 = {ans} ns."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Memory Management", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["memory lookup math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "A system has 3 processes sharing 4 instances of a resource. Each process needs at most k instances. What is the maximum value of k such that deadlock is guaranteed to NOT occur?"
            options = ["2", "1", "3", "4"]
            correct = "2"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "To avoid deadlock, total instances >= processes * (k - 1) + 1. 4 >= 3 * (k - 1) + 1 => 3 >= 3(k-1) => 1 >= k - 1 => k <= 2. Max value is 2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Deadlocks", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["deadlock avoidance analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about Semaphores and Mutexes are CORRECT?"
            options = [
                "A binary semaphore can take values 0 and 1.",
                "A counting semaphore can take arbitrary integer values.",
                "A mutex is essentially a locking mechanism used to synchronize access to a resource.",
                "Only the process that locked a mutex can unlock it, whereas any process can signal a semaphore."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct operational differences and properties of semaphores and mutexes."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Process Synchronization", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # SSTF disk scheduling
            # Requests: 90, 150, head initially at 100.
            # 100 -> 90 (10 cylinders) -> 150 (60 cylinders). Total = 70.
            ans = 70
            question = "A disk queue contains requests for I/O to cylinders: 90 and 150. The read/write head is initially at cylinder 100. Find the total head movement using SSTF (Shortest Seek Time First) scheduling."
            explanation = "From 100, the closer request is 90 (distance 10) vs 150 (distance 50). Head moves 100->90. From 90, head moves 90->150 (distance 60). Total = 10 + 60 = 70 cylinders."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Disk Scheduling", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["disk seek distance math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_dbms(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "A relation is in 2NF (Second Normal Form) if it is in 1NF and:"
            options = [
                "Every non-prime attribute is fully functionally dependent on the primary key.",
                "It has no partial functional dependencies.",
                "It has no transitive functional dependencies.",
                "Every determinant is a candidate key."
            ]
            correct = "Every non-prime attribute is fully functionally dependent on the primary key."
            # Note: "no partial dependencies" is also equivalent. Let's make options distinct:
            options = [
                "Every non-prime attribute is fully functionally dependent on the primary key.",
                "It has no transitive dependencies.",
                "It contains no multivalued dependencies.",
                "Every attribute is atomic."
            ]
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the candidate keys (no partial dependencies)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Normalization", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["normalization checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following represent the ACID properties of database transactions?"
            options = [
                "Atomicity",
                "Consistency",
                "Isolation",
                "Durability"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "ACID stands for Atomicity, Consistency, Isolation, and Durability."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transactions", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 6)
            val2 = random.randint(5, 10)
            ans = val1 * val2
            question = f"If relation R contains {val1} tuples and relation S contains {val2} tuples, how many tuples are in the Cartesian product of R and S?"
            explanation = f"The Cartesian product R x S contains |R| * |S| tuples = {val1} * {val2} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Relational Algebra", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["relational math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A relation R(A, B, C, D) has functional dependencies: A -> B, B -> C, C -> D. The candidate key for R is:"
            options = ["A", "B", "C", "D"]
            correct = "A"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The attribute closure of A is {A}+ = {A, B, C, D}. Thus A is a candidate key."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Normalization", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["candidate key identification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements regarding SQL JOINs are CORRECT?"
            options = [
                "INNER JOIN returns only rows that have matching values in both tables.",
                "LEFT JOIN returns all rows from the left table, and matching rows from the right table.",
                "RIGHT JOIN returns all rows from the right table, and matching rows from the left table.",
                "FULL OUTER JOIN returns all rows when there is a match in either left or right table."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct definitions of standard SQL JOIN operations."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "SQL", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Normal form calculation: 3NF vs BCNF
            # Relation R(A, B, C) with FDs: AB -> C, C -> A.
            # Keys: AB, BC.
            # C -> A has prime attribute A on right. Thus in 3NF. But C is not superkey, so not in BCNF.
            # Ask: what is highest normal form (1 for 1NF, 2 for 2NF, 3 for 3NF, 4 for BCNF).
            ans = 3
            question = "For a relation R(A, B, C) with functional dependencies {AB -> C, C -> A}, what is the highest normal form satisfied by R? (Enter 1 for 1NF, 2 for 2NF, 3 for 3NF, 4 for BCNF)."
            explanation = "Candidate keys are AB and BC. AB -> C satisfies BCNF (AB is key). C -> A: A is prime attribute, which is allowed in 3NF. But C is not a superkey, violating BCNF. Thus the highest normal form satisfied is 3NF (3)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Normalization", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["normal form check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Consider schedule S: r1(x), r2(x), w1(x), w2(x). Is this schedule conflict serializable?"
            options = ["No", "Yes", "Depends on commit order", "Cannot be determined"]
            correct = "No"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Conflicts exist: r1(x)->w2(x) implies T1 must precede T2. r2(x)->w1(x) implies T2 must precede T1. This creates a cycle in the precedence graph, so it is not conflict serializable."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transactions", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["serializability check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about database transaction isolation levels are CORRECT?"
            options = [
                "SERIALIZABLE is the strictest isolation level.",
                "READ UNCOMMITTED allows dirty reads.",
                "READ COMMITTED prevents dirty reads but allows non-repeatable reads.",
                "REPEATABLE READ prevents non-repeatable reads but can allow phantom reads."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct specifications of standard SQL transaction isolation levels."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transactions", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["isolation level checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # B+ tree node access
            h = random.randint(2, 4)
            # lookup requires h + 1 node reads (h index levels + 1 leaf level)
            ans = h + 1
            question = f"In a B+ Tree index with height {h} (where root is at level 0 and leaves are at level {h}), how many disk blocks must be read to retrieve a record for a given search key (excluding the record read itself)?"
            explanation = f"To find a key, we traverse from the root to the leaf node. This requires accessing exactly {h} index nodes and 1 leaf node, which equals {h + 1} block accesses."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Indexing", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["indexing access math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_coa(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which addressing mode calculates the operand's address by adding a constant offset to the Program Counter?"
            options = ["PC-Relative Addressing Mode", "Base Register Addressing Mode", "Indirect Addressing Mode", "Immediate Addressing Mode"]
            correct = "PC-Relative Addressing Mode"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "PC-relative addressing mode computes the target address relative to the current PC using an offset."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Addressing Modes", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are categories of computer hardware interrupts?"
            options = [
                "Maskable Interrupts",
                "Non-Maskable Interrupts",
                "External Interrupts",
                "Internal Interrupts (Traps)"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "Interrupts can be classified as maskable vs non-maskable based on CPU masking, and external vs internal based on trigger source."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Interrupts", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # pipeline speedup: 5 stage, ideal CPI = 1
            # speedup = k
            ans = 5
            question = "A non-pipelined processor takes 5 cycles to execute an instruction. A pipelined version has 5 stages with CPI = 1 in ideal conditions. What is the ideal speedup achieved by the pipeline?"
            explanation = "Speedup = CPI_non_pipelined / CPI_pipelined = 5 / 1 = 5."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Pipelining", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["pipeline math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A 4-way set associative cache has size 16 KB and block size 64 bytes. How many sets are in the cache?"
            options = ["64", "128", "256", "32"]
            correct = "64"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Block size = 64 B. Cache lines = 16 KB / 64 B = 256. Sets = 256 / 4 (associativity) = 64."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Cache Memory", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["cache layout math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following cache replacement policies are commonly used in computer architectures?"
            options = [
                "Least Recently Used (LRU)",
                "First-In First-Out (FIFO)",
                "Least Frequently Used (LFU)",
                "Random Replacement"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard cache replacement strategies used to replace blocks on cache misses."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Cache Memory", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # average access time: h1=0.9, t1=1, t2=10
            # AMAT = t1 + (1-h1)*t2 = 1 + 0.1 * 10 = 2 ns
            ans = 2
            question = "A system has a cache access time of 1 ns and main memory access time of 10 ns. If the cache hit ratio is 90%, calculate the average memory access time (AMAT) in ns."
            explanation = "AMAT = Cache Access + (1 - Hit Ratio) * Memory Access = 1 + (1 - 0.90) * 10 = 1 + 1 = 2 ns."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Cache Memory", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["cache access math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "A 5-stage pipeline has 20% branch instructions. If branch penalty is 2 cycles, what is the average CPI? (Assume base CPI without branches is 1)."
            options = ["1.4", "1.2", "1.6", "1.8"]
            correct = "1.4"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "CPI = Base_CPI + Branch_Frequency * Branch_Penalty = 1 + 0.20 * 2 = 1 + 0.40 = 1.40."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Pipelining", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["pipeline hazards math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about DMA (Direct Memory Access) mode of transfer are CORRECT?"
            options = [
                "DMA bypasses the CPU for data transfers between memory and I/O devices.",
                "The DMA controller becomes the bus master during transfers.",
                "Cycle stealing mode allows DMA to transfer one word at a time, interlaced with CPU cycles.",
                "Burst mode transfers block of data continuously until finished."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct operational characteristics of DMA transfers."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Input-Output System", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # CPI math
            # CPI = 1.0 + 0.05 * 100 = 6.0
            ans = 6
            question = "A processor executes instructions with base CPI = 1.0. If 5% of instructions cause a cache miss that stalls the processor for 100 cycles, what is the new CPI?"
            explanation = "New CPI = Base CPI + Miss Frequency * Miss Penalty = 1.0 + 0.05 * 100 = 1.0 + 5.0 = 6.0."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Pipelining", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["pipeline hazards math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_digitallogic(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which of the following logic gates is classified as a universal gate?"
            options = ["NAND", "AND", "OR", "XOR"]
            correct = "NAND"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "NAND and NOR gates are universal because any Boolean function can be implemented using only these gates."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Logic Gates", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following Boolean algebraic equations represent CORRECT identities?"
            options = [
                "A + 1 = 1",
                "A . 0 = 0",
                "A + A' = 1",
                "A . A' = 0"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent fundamental Boolean laws."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Boolean Algebra", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["boolean checking"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # binary conversion
            val1 = random.randint(10, 30)
            ans = val1
            bin_str = bin(val1)[2:].zfill(8)
            question = f"What is the decimal equivalent of the 8-bit unsigned binary number {bin_str}?"
            explanation = f"Binary {bin_str} = {val1} in decimal."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Number Representation", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["base conversion"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A 4-to-1 Multiplexer has inputs I0, I1, I2, I3. If select lines are S1 S0 = 1 0, what is the output Y?"
            options = ["I2", "I0", "I1", "I3"]
            correct = "I2"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Select input 10 in binary is decimal 2, which routes input I2 to output Y."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Combinational Circuits", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["mux routing"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following circuits belong to the class of sequential logic circuits?"
            options = [
                "JK Flip-flop",
                "Shift Register",
                "Ripple Counter",
                "Priority Encoder"
            ]
            correct = ["A", "B", "C"]
            explanation = "JK Flip-flop, Shift Register, and Ripple Counter contain memory elements (flip-flops) and are sequential. Priority Encoder is combinational."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequential Circuits", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["circuit classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Mod-N counter states
            states = random.choice([8, 10, 16, 24, 32])
            import math
            ans = int(math.ceil(math.log2(states)))
            question = f"Find the minimum number of flip-flops required to design a Mod-{states} counter."
            explanation = f"A Mod-{states} counter requires k flip-flops where 2^k >= {states}. Ceiling(log2({states})) = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sequential Circuits", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["counter size math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "How many 2-to-1 multiplexers are required to implement a 2-input XOR gate?"
            options = ["2", "1", "3", "4"]
            correct = "2"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Y = A XOR B = A'B + AB'. First MUX generates A' (with inputs 1, 0, select A). Second MUX generates Y (with inputs B, B' using first MUX, select A). Total = 2 multiplexers."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Combinational Circuits", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["mux implementation complexity"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about combinational hazards are CORRECT?"
            options = [
                "Static-0 hazard occurs when output is 0 and momentarily transitions to 1 and back to 0.",
                "Static-1 hazard occurs when output is 1 and momentarily transitions to 0 and back to 1.",
                "Dynamic hazard occurs when output changes three or more times when it is supposed to change once.",
                "Hazards can be eliminated by adding redundant gates to cover adjacent K-map loops."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct definitions and techniques for dealing with hazards."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Logic Minimization", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["hazard verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # dual of dual logic
            # number of variables = 3
            # self-dual functions = 2^(2^(n-1)) = 2^(2^2) = 2^4 = 16
            ans = 16
            question = "How many self-dual Boolean functions are possible with 3 variables?"
            explanation = "Number of self-dual functions with n variables is 2^(2^(n-1)). For n=3, 2^(2^(2)) = 2^4 = 16."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Boolean Algebra", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["combinatorial boolean math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_cn(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which layer of the OSI model is responsible for routing packets across networks?"
            options = ["Network Layer", "Transport Layer", "Data Link Layer", "Physical Layer"]
            correct = "Network Layer"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The Network Layer handles packet routing, logical addressing (IP), and subnetting."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "OSI Model", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["layer mapping"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following protocols operate at the Application layer of the TCP/IP suite?"
            options = [
                "DNS (Domain Name System)",
                "SMTP (Simple Mail Transfer Protocol)",
                "HTTP (Hypertext Transfer Protocol)",
                "FTP (File Transfer Protocol)"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent Application layer protocols used for user-level network services."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Protocols", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["protocol classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Subnet hosts: /24 has 256 addresses, 254 usable
            ans = 254
            question = "In an IPv4 network, how many usable host IP addresses are available in a subnet with a /24 mask?"
            explanation = "/24 subnet mask leaves 8 bits for host addresses. Total addresses = 2^8 = 256. Excluding network address (all 0s) and broadcast address (all 1s) leaves 254 usable host addresses."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "IP Addressing", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["subnet math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "What is the network ID for the IP address 192.168.10.35 with subnet mask 255.255.255.224 (/27)?"
            options = ["192.168.10.32", "192.168.10.0", "192.168.10.16", "192.168.10.48"]
            correct = "192.168.10.32"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Host = 35 (binary 00100011). Mask = 224 (binary 11100000). Bitwise AND of 35 and 224 = 32 (binary 00100000). Network ID is 192.168.10.32."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "IP Addressing", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["bitwise subnet check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements comparing TCP and UDP are CORRECT?"
            options = [
                "TCP is connection-oriented, whereas UDP is connectionless.",
                "TCP provides reliable delivery with flow and congestion control.",
                "UDP has lower overhead and latency compared to TCP.",
                "TCP guarantees packet ordering, whereas UDP does not."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct trade-offs and structural differences between TCP and UDP."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Transport Layer", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Tx delay = L / B. L = 1000 bits. B = 1 Mbps = 10^6 bps.
            # Tx = 1000 / 10^6 = 1 ms.
            ans = 1
            question = "A packet of size 1000 bits is sent over a link with bandwidth 1 Mbps. Find the transmission delay in milliseconds."
            explanation = "Tx delay = Packet Size / Bandwidth = 1000 bits / 1,000,000 bps = 0.001 seconds = 1 ms."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Physical Layer", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["transmission math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "A TCP connection is in Congestion Avoidance state with cwnd = 10 MSS. If it receives three duplicate ACKs, what will be the new cwnd (in MSS) under TCP Reno?"
            options = ["5", "1", "10", "8"]
            correct = "5"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "TCP Reno triggers Fast Recovery upon receiving 3 duplicate ACKs. cwnd is halved (ssthresh = cwnd/2 = 5 MSS) and cwnd = ssthresh = 5 MSS."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Congestion Control", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["tcp timeline simulation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following routing protocols are Link State routing protocols?"
            options = [
                "OSPF (Open Shortest Path First)",
                "IS-IS (Intermediate System to Intermediate System)",
                "RIP (Routing Information Protocol)",
                "BGP (Border Gateway Protocol)"
            ]
            correct = ["A", "B"]
            explanation = "OSPF and IS-IS are Link State routing protocols based on Dijkstra's algorithm. RIP is a Distance Vector protocol. BGP is a Path Vector protocol."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Routing", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["protocol classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Sliding window efficiency: efficiency = N / (1 + 2a).
            # Let window size N = 5. a = Tp / Tt = 1.
            # Efficiency = 5 / (1 + 2) = 5/3 = 1.67 -> wait, efficiency cannot exceed 100%!
            # So if N >= 1+2a, efficiency is 1.0 (100%).
            # Let's choose N = 2. a = 1. Efficiency = 2 / 3 = 66.67%.
            # Let's ask in %: round to integer -> 67%.
            # Or choose parameters giving exact int: N = 1, a = 1.5 -> eff = 1 / (1 + 3) = 25%.
            ans = 25
            question = "In a Sliding Window protocol, packet size is 1000 bytes, bandwidth is 10 KB/s, propagation delay is 150 ms. If window size is 1, calculate the efficiency of the protocol in %."
            explanation = "Tt = 1000 bytes / 10,000 bytes/s = 0.1 s = 100 ms. Tp = 150 ms. a = Tp / Tt = 1.5. Efficiency = 1 / (1 + 2a) = 1 / (1 + 3) = 1/4 = 25%."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Sliding Window", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["efficiency calculation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_toc(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which machine model accepts Context-Free Languages?"
            options = ["Pushdown Automata (PDA)", "Deterministic Finite Automata (DFA)", "Linear Bounded Automata (LBA)", "Turing Machine (TM)"]
            correct = "Pushdown Automata (PDA)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Pushdown Automata (PDA), which are finite automata with a stack, recognize Context-Free Languages."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Automata", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["automaton classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following languages are regular?"
            options = [
                "L = { a^n b^m | n >= 0, m >= 0 }",
                "L = { w | length of w is even }",
                "L = { w | w contains substring 'aba' }",
                "L = { a^n b^n | n >= 0 }"
            ]
            correct = ["A", "B", "C"]
            explanation = "A, B, and C can be recognized by Finite Automata. D requires counting matching powers (memory), which is CFG but not regular."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Regular Languages", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["language classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # DFA count for strings ending in a. States: 2.
            ans = 2
            question = "Find the minimum number of states in a DFA that recognizes the language: { w in {a, b}* | w ends with 'a' }."
            explanation = "We need 2 states: State 0 (start, ends in b or empty, non-accepting) and State 1 (ends in a, accepting). Transitions: from 0, on a->1, on b->0. From 1, on a->1, on b->0."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Finite Automata", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["dfa minimization"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "Which grammar format represents Context-Free Grammar where every rule is of format A -> BC or A -> a?"
            options = ["Chomsky Normal Form (CNF)", "Greibach Normal Form (GNF)", "Regular Grammar", "Unrestricted Grammar"]
            correct = "Chomsky Normal Form (CNF)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Chomsky Normal Form requires all production rules to be either A -> BC (two non-terminals) or A -> a (one terminal)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "CFG", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["grammar formats check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following language classes are closed under the intersection operation?"
            options = [
                "Regular Languages",
                "Context-Free Languages",
                "Turing Decidable Languages",
                "Recursively Enumerable Languages"
            ]
            correct = ["A", "C", "D"]
            explanation = "Regular, Decidable, and RE languages are closed under intersection. CFLs are not closed under intersection."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Closure Properties", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["closure properties checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Chomsky CFG non-terminals.
            # For string of length n, derivation length in CNF is 2n - 1.
            n = random.randint(3, 10)
            ans = 2 * n - 1
            question = f"In Chomsky Normal Form CFG, if a derivation of string w takes k steps, what is k if the length of w is {n}?"
            explanation = f"In CNF, deriving a string of length n takes exactly 2n - 1 steps. For n = {n}, steps = 2*{n} - 1 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "CFG", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["derivation length calculation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "Which of the following decision problems is DECIDABLE?"
            options = [
                "Equivalence of two DFAs",
                "Equivalence of two PDAs",
                "Emptiness of a Turing Machine language",
                "Finiteness of a Turing Machine language"
            ]
            correct = "Equivalence of two DFAs"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "DFA equivalence is decidable because we can construct a product automaton. PDA and TM equivalence/emptiness are undecidable (Rice's Theorem)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Decidability", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["decidability verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following problems are known to be UNDECIDABLE?"
            options = [
                "Halting Problem for Turing Machines",
                "Post Correspondence Problem (PCP)",
                "Ambiguity of a Context-Free Grammar",
                "Equivalence of two Context-Free Grammars"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent classic undecidable problems in computational theory."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Decidability", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["decidability verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # DFA count: binary strings divisible by 3.
            ans = 3
            question = "Find the minimum number of states in a DFA that recognizes the language: { w in {0, 1}* | w parsed as binary is divisible by 3 }."
            explanation = "Divisibility by 3 requires keeping track of remainder modulo 3 (rem 0, 1, 2). This requires exactly 3 states, corresponding to remainders 0 (accepting), 1, and 2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Finite Automata", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["dfa minimization"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_cd(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Which compiler phase is responsible for checking syntax and building the parse tree?"
            options = ["Syntax Analysis (Parser)", "Lexical Analysis (Scanner)", "Semantic Analysis", "Code Optimization"]
            correct = "Syntax Analysis (Parser)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Syntax analysis processes tokens generated by scanner and outputs a parse/syntax tree based on CFG rules."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syntax Analysis", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["phase mapping"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following parsing algorithms are classified as bottom-up parsing techniques?"
            options = [
                "Shift-Reduce Parsing",
                "SLR(1) Parsing",
                "LALR(1) Parsing",
                "LL(1) Parsing"
            ]
            correct = ["A", "B", "C"]
            explanation = "Shift-Reduce, SLR, and LALR are bottom-up parsers (building tree from leaves to root). LL(1) is top-down (root to leaves)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syntax Analysis", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["parser classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # token counting
            # e.g. "int x = a + 5;" -> 6 tokens (int, x, =, a, +, 5)
            # wait, let's omit semicolon or count it
            # int(1), x(2), =(3), a(4), +(5), 5(6), ;(7) -> 7 tokens
            ans = 7
            question = "Calculate the number of tokens in the C statement: `int x = a + 5;` according to lexical rules."
            explanation = "Tokens are: `int` (keyword), `x` (identifier), `=` (operator), `a` (identifier), `+` (operator), `5` (constant), `;` (punctuation). Total = 7 tokens."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Lexical Analysis", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["token counting"], "representation": ["code"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "Which of the following represents a loop optimization technique where loop-independent computations are moved outside the loop?"
            options = ["Loop Invariant Code Motion", "Loop Unrolling", "Loop Fusion", "Dead Code Elimination"]
            correct = "Loop Invariant Code Motion"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Loop invariant code motion identifies expressions that yield same result inside loop and moves them to loop header/preheader."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Code Optimization", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["optimization verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following represent intermediate representations (IR) commonly used in compilers?"
            options = [
                "Three-Address Code (TAC)",
                "Abstract Syntax Tree (AST)",
                "Static Single Assignment (SSA) form",
                "Control Flow Graph (CFG)"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent valid intermediate representations at various levels of abstraction in a compiler."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "IR Generation", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["ir classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # FIRST set calculation
            # S -> aSb | e. FIRST(S) = {a, e}. Size is 2.
            ans = 2
            question = "Consider the grammar: S -> a S b | e. Find the number of elements in the set FIRST(S)."
            explanation = "S can derive 'a S b' (which starts with terminal 'a') or 'e' (empty string). Thus FIRST(S) = {a, e}, which contains 2 elements."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syntax Analysis", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["grammar FIRST calculation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "For a grammar with productions: S -> L = R | R, R -> L, L -> * R | id. Is this grammar LR(1) but NOT LALR(1)?"
            options = ["No (It is LALR(1))", "Yes (It is LR(1) but not LALR(1))", "No (It is not even LR(1))", "Cannot be determined"]
            correct = "No (It is LALR(1))"  # Note: actually it is LALR(1). Let's check:
            # S -> L=R | R is LALR(1). Wait, S -> L=R | R, L -> *R | id, R -> L is the classic example of non-LALR(1) or non-LR(1)?
            # It has no shift-reduce conflict in LR(1), but has reduce-reduce conflict when lookaheads are merged in LALR(1).
            # Wait, the classic example is: S -> aAd | bBd | aBe | bAe, A -> c, B -> c. This is LR(1) but not LALR(1).
            # Let's use a simpler known fact: "Is SLR(1) parser subset of LALR(1)?" -> SLR(1) is subset of LALR(1).
            # Let's change question: "Which of the following parser tables has the maximum number of states for a given grammar?"
            options = ["LR(1) Parser", "LALR(1) Parser", "SLR(1) Parser", "LR(0) Parser"]
            correct = "LR(1) Parser"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "LR(1) parser splits states based on lookaheads, resulting in significantly more states than LALR(1) or SLR(1), which merge states with identical core items."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Syntax Analysis", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["parser comparisons"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following compiler optimization strategies are commonly used to optimize loops?"
            options = [
                "Loop Unrolling",
                "Loop Invariant Code Motion",
                "Loop Fusion",
                "Loop Fission"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard loop transformation and optimization techniques."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Code Optimization", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["optimization verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Basic block count
            # 1: x = 0;
            # 2: if (x < 10) goto 5;
            # 3: x = x + 1;
            # 4: goto 2;
            # 5: print(x);
            # Leaders: 1 (start), 3 (target of loop? no, goto target: 5 is leader, 3 is leader because it follows conditional jump 2, 2 is leader because target of jump 4)
            # Leaders are: statement 1, statement 2 (jump target), statement 3 (after jump), statement 5 (jump target).
            # Basic blocks: [1], [2], [3, 4], [5]. Total basic blocks = 4.
            ans = 4
            question = "How many basic blocks are in the three-address code sequence below?\n1: x = 0\n2: if x < 10 goto 5\n3: x = x + 1\n4: goto 2\n5: return x"
            explanation = "Leaders are: 1 (entry statement), 2 (target of goto at 4), 3 (statement following conditional branch at 2), 5 (target of conditional branch at 2). Blocks are: Block 1 (line 1), Block 2 (line 2), Block 3 (lines 3-4), Block 4 (line 5). Total basic blocks = 4."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Code Optimization", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["basic block analysis"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_la(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "What is the determinant of an N x N Identity Matrix?"
            options = ["1", "0", "N", "-1"]
            correct = "1"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The determinant of an identity matrix of any size is always 1."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Matrices", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements about orthogonal matrices are TRUE?"
            options = [
                "The transpose of an orthogonal matrix is equal to its inverse.",
                "The determinant of an orthogonal matrix is either +1 or -1.",
                "The columns of an orthogonal matrix form an orthonormal set.",
                "The rows of an orthogonal matrix form an orthonormal set."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent fundamental defining properties of orthogonal matrices (Q^T * Q = I)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Matrices", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Rank of a simple 3x3 matrix:
            # [1 0 0]
            # [0 1 0]
            # [0 0 0] -> rank 2
            ans = 2
            question = "Find the rank of the 3 x 3 matrix:\n\n$$\\begin{bmatrix} 1 & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 0 \\end{bmatrix}$$"
            explanation = "The matrix is in row-echelon form and has exactly 2 non-zero rows. Therefore, its rank is 2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Matrix Rank", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["matrix analysis"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            val1 = random.randint(2, 6)
            val2 = random.randint(7, 12)
            # Matrix with eigenvalues val1, val2
            # trace = val1 + val2
            question = f"If a 2 x 2 matrix has eigenvalues lambda_1 = {val1} and lambda_2 = {val2}, what is the trace of the matrix?"
            ans = str(val1 + val2)
            options = [ans, str(val1 * val2), str(val1 - val2), "1"]
            random.shuffle(options)
            correct_letter = chr(65 + options.index(ans))
            explanation = "The trace of a matrix is equal to the sum of its eigenvalues: Trace = lambda_1 + lambda_2 = {val1} + {val2} = {val1 + val2}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Eigenvalues", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["eigenvalues math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following are properties of vector spaces?"
            options = [
                "Closed under vector addition.",
                "Closed under scalar multiplication.",
                "Contains a zero vector.",
                "Every vector has an additive inverse."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard axioms defining vector spaces."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Vector Spaces", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["axiom checks"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 6)
            ans = val1
            # Det of diagonal 3x3 matrix: val1, 1, 1
            question = f"Calculate the determinant of the diagonal matrix:\n\n$$\\begin{{bmatrix}} {val1} & 0 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0 & 1 \\end{{bmatrix}}$$"
            explanation = f"The determinant of a diagonal matrix is the product of its diagonal elements: Det = {val1} * 1 * 1 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Determinants", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["matrix analysis"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            val1 = 2
            val2 = 3
            # Eigenvalues of A^2: 4, 9. Sum = 13.
            question = f"If matrix A has eigenvalues {val1} and {val2}, what is the sum of the eigenvalues of A^2?"
            options = ["13", "5", "6", "36"]
            correct = "13"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "If lambda is an eigenvalue of A, then lambda^2 is an eigenvalue of A^2. The eigenvalues of A^2 are 2^2 = 4 and 3^2 = 9. Sum = 4 + 9 = 13."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Eigenvalues", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["eigenvalues math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "For a system of linear equations Ax = B (where A is square), which of the following statements are CORRECT?"
            options = [
                "If det(A) != 0, the system has a unique solution.",
                "If det(A) == 0 and (adj A)B == 0, the system has infinitely many solutions.",
                "If det(A) == 0 and (adj A)B != 0, the system has no solution.",
                "If B = 0 (homogeneous system) and det(A) != 0, only the trivial solution exists."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct conditions for consistency and solutions of linear systems."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Linear Systems", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["consistency verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Cramer's rule
            # x + y = 3
            # x - y = 1
            # Solution: x = 2, y = 1.
            ans = 2
            question = "Solve the system of equations for x:\n\n$$x + y = 3$$\n$$x - y = 1$$"
            explanation = "Adding the two equations: (x+y) + (x-y) = 3 + 1 => 2x = 4 => x = 2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Linear Systems", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["algebra math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_calc(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "Find the limit: $\\lim_{x \\to 2} (x^2 - 4) / (x - 2)$."
            options = ["4", "0", "2", "Undefined"]
            correct = "4"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Lim = (x-2)(x+2)/(x-2) = x+2. As x->2, x+2 -> 4."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Limits", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["limit calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following functions are continuous for all real numbers?"
            options = [
                "f(x) = x^2",
                "f(x) = \\sin(x)",
                "f(x) = e^x",
                "f(x) = |x|"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent continuous functions on the entire real line."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Continuity", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 5)
            # f(x) = x^3. f'(val1) = 3*val1^2
            ans = 3 * (val1**2)
            question = f"If $f(x) = x^3$, find the value of the first derivative $f'(x)$ evaluated at $x = {val1}$."
            explanation = f"Derivative f'(x) = 3x^2. Evaluated at x={val1}: 3 * {val1}^2 = 3 * {val1**2} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Differentiability", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["derivative calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "Find the limit: $\\lim_{x \\to 0} \\sin(5x) / x$."
            options = ["5", "0", "1", "1/5"]
            correct = "5"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Using L'Hopital's rule or standard limit sin(kx)/x -> k as x->0: Lim = 5."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Limits", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["limit calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following conditions are necessary for a function f(x) to have a local maximum at x = c?"
            options = [
                "f'(c) = 0 or f'(c) is undefined (critical point).",
                "If f''(c) exists, then f''(c) <= 0.",
                "The first derivative f'(x) changes sign from positive to negative at c.",
                "f(c) is greater than all values of f(x) in some interval containing c."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent valid characteristics or criteria for local maxima."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Optimization", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["optimization criteria check"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 5)
            # Integral from 0 to val1 of 2x = x^2 evaluated 0..val1 = val1^2
            ans = val1 * val1
            question = f"Evaluate the definite integral: $\\int_{{0}}^{{{val1}}} 2x \\, dx$."
            explanation = f"Integral of 2x is x^2. Evaluated from 0 to {val1}: {val1}^2 - 0 = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Integration", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["integral calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "At what point does the function f(x) = x^3 - 3x^2 have a point of inflection?"
            options = ["x = 1", "x = 0", "x = 2", "x = -1"]
            correct = "x = 1"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "f'(x) = 3x^2 - 6x. f''(x) = 6x - 6. Setting f''(x) = 0 gives x = 1. Since f''(x) changes sign around x=1, it is a point of inflection."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Inflection Points", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["derivative calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following infinite series are convergent?"
            options = [
                "Sum_{n=1..inf} (1 / n^2)",
                "Sum_{n=1..inf} (1 / 2^n)",
                "Sum_{n=1..inf} ((-1)^n / n)",
                "Sum_{n=1..inf} (1 / n)"
            ]
            correct = ["A", "B", "C"]
            explanation = "A is a p-series with p=2 > 1 (convergent). B is a geometric series with r=1/2 < 1 (convergent). C is the alternating harmonic series (convergent by Leibniz test). D is the harmonic series, which diverges."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Series", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["series convergence check"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # area under y = x^2 from 0 to 3: x^3 / 3 evaluated 0..3 = 27 / 3 = 9
            ans = 9
            question = "Find the area under the curve $y = x^2$ bounded by the x-axis and vertical lines $x = 0$ and $x = 3$."
            explanation = "Area = \\int_{0}^{3} x^2 \\, dx = [x^3 / 3]_0^3 = 27/3 - 0 = 9."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Integration", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["integral calculus"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_dm(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "According to the Handshaking Lemma, the sum of degrees of all vertices in any graph is equal to:"
            options = ["Twice the number of edges", "The number of edges", "Half the number of edges", "Number of vertices squared"]
            correct = "Twice the number of edges"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Handshaking Lemma: Sum_{v} deg(v) = 2 * |E|."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graph Theory", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following logical formulas are tautologies?"
            options = [
                "P \\lor \\neg P",
                "\\neg (P \\land \\neg P)",
                "P \\implies P",
                "P \\iff P"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent propositional expressions that are true for all truth values of P."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Mathematical Logic", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["tautology verification"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            val1 = random.randint(2, 6)
            ans = 2**val1
            question = f"How many subsets can be formed from a set containing exactly {val1} elements?"
            explanation = f"A set with n elements has 2^n subsets. For n={val1}, subsets = 2^{val1} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Set Theory", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["set counting"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "A relation R on a set is an equivalence relation if and only if it is:"
            options = [
                "Reflexive, Symmetric, and Transitive",
                "Reflexive, Antisymmetric, and Transitive",
                "Irreflexive, Symmetric, and Transitive",
                "Reflexive, Symmetric, and Asymmetric"
            ]
            correct = "Reflexive, Symmetric, and Transitive"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "An equivalence relation satisfies reflexivity (aRa), symmetry (aRb => bRa), and transitivity (aRb and bRc => aRc)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Relations", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following graphs are planar graphs?"
            options = [
                "K4 (Complete graph with 4 vertices)",
                "K3,3 (Complete bipartite graph on 3 and 3 vertices)",
                "K5 (Complete graph with 5 vertices)",
                "C5 (Cycle graph with 5 vertices)"
            ]
            correct = ["A", "D"]
            explanation = "K4 and C5 are planar. According to Kuratowski's theorem, K5 and K3,3 are non-planar."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graph Theory", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["planarity verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Chromatic number of odd cycle is 3, even is 2.
            val1 = random.choice([5, 7, 9]) # odd cycles
            ans = 3
            question = f"What is the chromatic number of the cycle graph $C_{{{val1}}}$?"
            explanation = f"Every cycle graph C_n has chromatic number 2 if n is even, and 3 if n is odd. Since {val1} is odd, chromatic number is 3."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Graph Theory", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["graph coloring math"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "What is the generating function for the sequence: 1, 1, 1, 1, ...?"
            options = ["1 / (1 - x)", "1 / (1 + x)", "1 / (1 - x)^2", "x / (1 - x)"]
            correct = "1 / (1 - x)"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "The generating function is Sum_{n=0..inf} x^n = 1 + x + x^2 + ... = 1 / (1 - x)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Combinatorics", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["generating function check"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following mathematical structures represent a Lattice (a poset where every pair has a supremum and infimum)?"
            options = [
                "Power set of any set under subset containment (P(S), <=)",
                "Divisors of any integer n under divisibility (D_n, |)",
                "A chain poset (elements are totally ordered)",
                "Real numbers under standard <= relation"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent posets satisfying the lattice supremum/infimum criteria."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Lattices", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["poset structure verification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # recurrence relation
            # T(n) = T(n-1) + 2. T(0) = 1.
            # T(val1) = 2*val1 + 1
            val1 = random.randint(5, 20)
            ans = 2 * val1 + 1
            question = f"Solve the recurrence relation: $a_n = a_{{n-1}} + 2$ with $a_0 = 1$. Find the value of $a_{{{val1}}}$."
            explanation = f"The relation is an arithmetic progression: a_n = a_0 + 2n = 1 + 2n. For n={val1}, a_{{{val1}}} = 1 + 2*{val1} = {ans}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Recurrence Relations", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["recurrence solving"], "representation": ["notation"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def generate_probstat(diff, q_type, idx, q_id, sub_upper):
    if diff == "easy":
        if q_type == "MCQ":
            question = "If two fair dice are rolled, what is the probability of getting a sum of exactly 7?"
            options = ["1/6", "1/12", "1/36", "5/36"]
            correct = "1/6"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Possible outcomes summing to 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) -> 6 outcomes. Total outcomes = 36. Probability = 6/36 = 1/6."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Probability", "subtopic": None,
                    "difficulty": "easy", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["combinatorial probability"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following random variables are classified as discrete random variables?"
            options = [
                "Number of heads in 10 flips of a coin",
                "Number of customer arrivals at a bank counter in 1 hour",
                "The result of rolling a six-sided die",
                "The exact lifetime of a lightbulb (in hours)"
            ]
            correct = ["A", "B", "C"]
            explanation = "A, B, and C have countable outcomes (discrete). D has a continuous range of outcomes (continuous)."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Random Variables", "subtopic": None,
                    "difficulty": "easy", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["distribution classification"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # expectation of fair die roll
            ans = 3.5
            question = "Find the mathematical expectation of rolling a single fair six-sided die."
            explanation = "Expectation = (1 + 2 + 3 + 4 + 5 + 6) / 6 = 21 / 6 = 3.5."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Expectation", "subtopic": None,
                    "difficulty": "easy", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["mean math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    elif diff == "medium":
        if q_type == "MCQ":
            question = "If A and B are independent events with P(A) = 0.3 and P(B) = 0.4, find P(A U B)."
            options = ["0.58", "0.70", "0.12", "0.82"]
            correct = "0.58"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "P(A U B) = P(A) + P(B) - P(A and B). Since independent, P(A and B) = P(A)*P(B) = 0.3 * 0.4 = 0.12. P(A U B) = 0.3 + 0.4 - 0.12 = 0.58."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Probability", "subtopic": None,
                    "difficulty": "medium", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "state-transition reasoning", "reasoning_type": ["algebraic probability"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "For independent random variables X and Y, which of the following variance properties are CORRECT?"
            options = [
                "Var(X + Y) = Var(X) + Var(Y)",
                "Var(X - Y) = Var(X) + Var(Y)",
                "Var(aX) = a^2 * Var(X)",
                "Var(X + b) = Var(X)"
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent standard correct algebraic properties of variance for independent variables."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Variance", "subtopic": None,
                    "difficulty": "medium", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Poisson variance
            val1 = random.choice([2, 3, 5, 8])
            ans = val1
            question = f"If a random variable X follows a Poisson distribution with mean parameter lambda = {val1}, what is the variance of X?"
            explanation = f"For a Poisson distribution, both mean and variance are equal to the parameter lambda. Hence, Variance = {val1}."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Poisson Distribution", "subtopic": None,
                    "difficulty": "medium", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["distribution math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }
    else:  # hard
        if q_type == "MCQ":
            question = "A system consists of 2 components in parallel. The system functions if at least one component works. If each component fails with probability p independently, the system failure probability is:"
            options = ["p^2", "2p - p^2", "1 - p^2", "p"]
            correct = "p^2"
            random.shuffle(options)
            correct_letter = chr(65 + options.index(correct))
            explanation = "Parallel system fails only if all components fail. P(fail) = P(comp1 fails) * P(comp2 fails) = p * p = p^2."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "System Reliability", "subtopic": None,
                    "difficulty": "hard", "type": "MCQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["system probability"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": correct_letter},
                "solution": {"id": q_id, "explanation": explanation}
            }
        elif q_type == "MSQ":
            question = "Which of the following statements regarding a normal distribution are CORRECT?"
            options = [
                "It is symmetric about its mean.",
                "Its mean, median, and mode are all equal.",
                "Approximately 68% of the data falls within one standard deviation of the mean.",
                "Approximately 95% of the data falls within two standard deviations of the mean."
            ]
            correct = ["A", "B", "C", "D"]
            explanation = "All options represent correct characteristics of standard normal probability distributions."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Normal Distribution", "subtopic": None,
                    "difficulty": "hard", "type": "MSQ", "question": question, "options": options,
                    "answer_id": q_id, "pattern_type": "invariant reasoning", "reasoning_type": ["property validation"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": json.dumps(correct)},
                "solution": {"id": q_id, "explanation": explanation}
            }
        else:  # NAT
            # Binomial probability
            # N = 3. p = 0.5. probability of exactly 2 heads.
            # C(3,2) * (0.5)^3 = 3 * 0.125 = 0.375
            ans = 0.375
            question = "A fair coin is tossed 3 times. What is the probability of getting exactly 2 heads?"
            explanation = "Using Binomial formula: P(X=2) = C(3, 2) * (0.5)^2 * (0.5)^1 = 3 * 0.25 * 0.5 = 0.375."
            return {
                "question": {
                    "id": q_id, "subject": sub_upper, "topic": "Binomial Distribution", "subtopic": None,
                    "difficulty": "hard", "type": "NAT", "question": question, "options": None,
                    "answer_id": q_id, "pattern_type": "computational", "reasoning_type": ["binomial probability math"], "representation": ["text"]
                },
                "answer": {"id": q_id, "correct_answer": str(ans)},
                "solution": {"id": q_id, "explanation": explanation}
            }

def main():
    base_dir = "datasets"
    subjects = ["cprog", "dsa", "algo", "os", "dbms", "coa", "digitallogic", "cn", "toc", "cd", "la", "calc", "dm", "probstat"]
    subject_map = {
        "cprog": "PDS",
        "dsa": "DSA",
        "algo": "ALGO",
        "os": "OS",
        "dbms": "DB",
        "coa": "COA",
        "digitallogic": "DL",
        "cn": "CN",
        "toc": "TOC",
        "cd": "CD",
        "la": "LA",
        "calc": "CALC",
        "dm": "DM",
        "probstat": "PROB"
    }
    difficulties = ["easy", "medium", "hard"]
    diff_folders = {"easy": "ej", "medium": "mj", "hard": "hj"}
    
    print("Starting generation of 150 additional files per GATE CS subject and difficulty...")
    
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
                    if sub == "cprog":
                        question_data = generate_cprog(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "dsa":
                        question_data = generate_dsa(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "algo":
                        question_data = generate_algo(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "os":
                        question_data = generate_os(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "dbms":
                        question_data = generate_dbms(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "coa":
                        question_data = generate_coa(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "digitallogic":
                        question_data = generate_digitallogic(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "cn":
                        question_data = generate_cn(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "toc":
                        question_data = generate_toc(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "cd":
                        question_data = generate_cd(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "la":
                        question_data = generate_la(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "calc":
                        question_data = generate_calc(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "dm":
                        question_data = generate_dm(diff, q_type, file_idx, q_id, sub_upper)
                    elif sub == "probstat":
                        question_data = generate_probstat(diff, q_type, file_idx, q_id, sub_upper)
                    
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
