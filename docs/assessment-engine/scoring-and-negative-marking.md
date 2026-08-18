# Assessment Scoring & Negative Marking Policy

The Gandheevijaya scoring engine evaluates student submissions using server-side evaluation rules tailored for GATE CS, SSC, and Banking exams.

## Question Type Evaluation Rules

### 1. Multiple Choice Questions (MCQ)
- **Correct Selection**: $+M$ (where $M$ is the assigned question marks).
- **Incorrect Selection**: $-N$ (where $N = |negative\_marks|$, e.g., $-0.33$ or $-0.25$).
- **Unanswered**: $0.0$.

### 2. Multiple Select Questions (MSQ)
- **100% Exact Set Match**: $+M$.
- **Incorrect Set**: $-N$ penalty or $0.0$ depending on quiz configuration (All-or-Nothing policy).
- **Unanswered**: $0.0$.

### 3. Numerical Answer Type (NAT)
- **Numeric Value Match (within tolerance $\pm 0.01$)**: $+M$.
- **Incorrect Numeric Value**: $0.0$ (No negative marking for NAT per GATE standards).
- **Unanswered**: $0.0$.

## Performance Summary Formulas

- **Score**:
  $$\text{Score} = \sum \text{Marks Awarded} - \sum \text{Penalties}$$
- **Percentage**:
  $$\text{Percentage} = \frac{\text{Score}}{\text{Total Marks}} \times 100$$
- **Accuracy**:
  $$\text{Accuracy} = \frac{\text{Correct Count}}{\text{Attempted Count}} \times 100$$
- **Attempted Count**: $\text{Correct Count} + \text{Incorrect Count}$.
- **Unanswered Count**: $\text{Total Questions} - \text{Attempted Count}$.
