# AI Workforce Learning & Proficiency Framework

**Python | Streamlit | Plotly | Pandas | Workforce Analytics | AI Competency Assessment**

A Python and Streamlit application designed to assess individual AI proficiency, identify role-specific competency gaps, generate personalized learning recommendations, and analyze organizational AI workforce readiness.

The framework integrates a **24-question competency assessment**, six employee-role profiles, eight competency domains, and an interactive analytics dashboard using **1,500 synthetic employee records**.

**Project Status:** Functional Prototype  
**Focus:** Applied AI | Workforce Development | Learning Analytics | Assessment Design  
**Dataset:** Synthetic / Demonstration

---

## 1. Project Overview

As organizations introduce artificial intelligence into workplace operations, workforce development requires more than providing employees with access to AI tools. Organizations also need methods for understanding employee proficiency, identifying development needs, measuring readiness across different job functions, and prioritizing learning opportunities.

The **AI Workforce Learning & Proficiency Framework** demonstrates how structured assessments, transparent scoring methods, personalized learning activities, and interactive analytics can work together to support workforce development.

The application consists of two primary components.

### Individual AI Proficiency Assessment

An interactive, role-based assessment evaluating AI knowledge, practical decision-making, and self-reported practices across eight competency domains.

Employees can review their responses before submission and receive proficiency results, role-specific competency comparisons, and personalized learning recommendations.

### Organizational AI Workforce Analytics

An interactive dashboard examining simulated employee proficiency, training participation, AI adoption, management support, and organizational competency gaps.

Users can filter workforce results by department and employee role, identify training priorities, and export recommended learning activities.

---

## 2. Application Preview

### Individual Assessment

![Individual AI Assessment](screenshots/individual_assessment/Individual_Assessment_Preview_1.png)

*Employee role selection and structured AI competency assessment.*

### Organizational Workforce Analytics

![Organizational AI Workforce Analytics](workforce_analytics/Organizational%20AI%20Workforce%20Analytics_Preview_1.png)

*Interactive dashboard showing workforce filters, proficiency indicators, role-target attainment, and competency gaps.*

---

## 3. Key Features

### Individual Assessment

- 24 questions across eight AI competency domains
- Six employee-role profiles
- Practical, knowledge, and reflection-based assessment items
- Weighted overall proficiency scoring
- Domain-level competency scores
- Role-specific proficiency targets
- Assessment progress tracking
- Response review before submission
- Interactive competency visualizations
- Personalized learning recommendations
- Four learning priority classifications
- Ability to start a new assessment

### Workforce Analytics

- Interactive department and employee-role filters
- Organizational proficiency scorecards
- Workforce proficiency distribution
- Department-level proficiency comparisons
- Organizational competency scores
- Approved AI tool access indicators
- Employee training participation
- AI usage frequency
- Management support measures
- Role-specific competency gap analysis
- Organizational learning priorities
- Downloadable learning priorities in CSV format

---

## 4. AI Competency Framework

The assessment evaluates eight domains representing different dimensions of AI knowledge, workplace application, responsibility, and organizational readiness.

| Competency Domain | Assessment Focus |
|---|---|
| AI Literacy | Understanding AI concepts, capabilities, and limitations |
| Prompting & Interaction | Communicating effectively with AI systems |
| Workflow Integration | Incorporating AI into work processes |
| Evaluation & Verification | Assessing and validating AI-generated outputs |
| Responsible AI | Privacy, fairness, bias, and responsible AI use |
| Human Oversight | Human judgment, accountability, and supervision |
| AI Collaboration | Working effectively with AI-assisted processes |
| Change Readiness | Adapting to AI-related workplace changes |

Each competency domain contains three assessment questions, resulting in 24 questions overall.

These domains connect the individual assessment with organizational competency analytics and learning recommendations.

---

## 5. Employee Role Profiles

The framework supports six employee-role profiles with differentiated proficiency expectations.

| Employee Role | Primary Responsibilities |
|---|---|
| Individual Contributor | Uses AI to support individual work activities |
| People Manager | Oversees employees and supports responsible AI adoption within teams |
| Learning & Development Professional | Supports workplace learning, training, and competency development |
| Data or Technical Professional | Works with data, analytics, technical systems, or AI applications |
| AI Workflow Owner | Supports AI-enabled workflow implementation and management |
| Senior Leader | Provides organizational strategy, governance, and oversight |

Role-specific competency expectations are stored in:

`data/role_targets.json`

Each role is assigned a target proficiency level for each of the eight competency domains.

These role definitions and target levels are prototype design assumptions rather than externally validated occupational standards.

---

## 6. Individual Assessment Design

The assessment includes three categories of questions.

| Category | Purpose | Weight |
|---|---|---:|
| Practical | Scenario-based application and decision-making | 60% |
| Knowledge | Understanding AI concepts and appropriate use | 30% |
| Reflection | Self-reported practices and awareness | 10% |
| **Total** | | **100%** |

Each assessment question includes scored response options, with scores ranging from 0 to 4.

Questions may have different numbers of response options based on their scenario or structure. All items use the same maximum possible score of four points for normalization.

### Assessment Navigation

The application guides employees through eight competency sections and tracks their assessment progress.

Before submitting, employees can review completed responses and return to individual competency sections.

After all 24 questions are completed, the assessment becomes ready for submission.

### Assessment Interpretation

The questions provide structured developmental indicators through knowledge items, scenario-based decisions, and self-reported practices.

The assessment does not independently observe employee job performance and has not undergone formal psychometric validation.

Because each domain contains only three questions, domain-level scores should be interpreted as preliminary developmental indicators.

---

## 7. Scoring Methodology

The application uses transparent, rule-based calculations implemented in:

`scoring/proficiency_scoring.py`

### 7.1 Assessment Category Scores

Scores within each assessment category are normalized to a 0–100 scale.

**Formula:**

Category Score = (Points Earned / Maximum Available Points) × 100

The maximum available points equal the number of questions in a category multiplied by four.

### 7.2 Overall AI Proficiency

The overall proficiency score uses weighted category results.

**Formula:**

Overall Proficiency = (Practical × 0.60) + (Knowledge × 0.30) + (Reflection × 0.10)

**Illustrative calculation:**

| Category | Score | Weight | Weighted Result |
|---|---:|---:|---:|
| Practical | 75 | 60% | 45 |
| Knowledge | 80 | 30% | 24 |
| Reflection | 60 | 10% | 6 |
| **Overall Proficiency** | | | **75/100** |

The model emphasizes practical application and decision-making.

These weights are explicit design choices, not empirically validated predictors of workplace performance.

### 7.3 Competency Domain Scores

Each domain contains three questions with a maximum score of four points each.

**Maximum Domain Points:**

3 × 4 = 12

**Formula:**

Domain Score = (Domain Points Earned / 12) × 100

**Example:**

An employee earns 8 of 12 possible points in AI Literacy.

(8 / 12) × 100 = **66.67/100**

Domain scores are calculated independently.

The overall proficiency score uses weighted assessment categories, while domain scores measure performance on questions associated with individual competencies.

---

## 8. Role-Specific Proficiency Targets

Each competency domain is evaluated against a target associated with the employee's selected role.

| Target Level | Required Score |
|---|---:|
| Level 1 | 25 |
| Level 2 | 50 |
| Level 3 | 70 |
| Level 4 | 85 |

Employees meet a competency target when their actual domain score equals or exceeds the required threshold.

### Competency Gap Calculation

**Formula:**

Competency Gap = Maximum of (0, Target Score − Actual Score)

**Example:**

- Target score: 70
- Actual score: 50
- Competency gap: 20 points

### Role-Target Attainment

Role-target attainment represents the percentage of competency domains in which an employee meets the assigned proficiency target.

**Formula:**

Role-Target Attainment = (Domains Meeting Target / 8) × 100

If an employee meets five of eight competency targets:

(5 / 8) × 100 = **62.5%**

Role-target attainment is not interchangeable with overall AI proficiency.

### Discrete Score Considerations

Domain results are derived from a limited number of scored questions, creating discrete score possibilities.

Therefore, small adjustments to proficiency thresholds may not always change an employee's attainment classification.

---

## 9. Personalized Learning Recommendations

After completing the assessment, employees receive learning recommendations linked to competencies that fall below their assigned role targets.

The recommendation system is deterministic and rule-based. It uses explicit Python conditions and a predefined learning catalog rather than generating recommendations through a language model.

Learning activities are stored in:

`data/learning_catalog.json`

### Priority Classification

| Priority | Classification Rule |
|---|---|
| Critical | Responsible AI or Human Oversight gap of at least 20 points |
| High | Other qualifying gaps of at least 30 points |
| Moderate | Remaining gaps of at least 10 points |
| Low | Remaining positive gaps below 10 points |

Rules are evaluated in order.

For example, a Responsible AI gap of 35 points receives a Critical priority rather than High.

Recommendations are sorted first by priority level and then by gap magnitude.

Competencies meeting their assigned role targets are excluded from recommendations.

### Learning Recommendation Details

Each recommended activity includes:

- Competency domain
- Learning title
- Learning objective
- Suggested learning activity
- Estimated completion time
- Competency gap
- Priority classification

Priority thresholds are prototype development rules. A Critical priority indicates a designated learning need, not a validated determination of workplace risk or employee qualification.

---

## 10. Organizational AI Workforce Analytics

The organizational dashboard demonstrates how individual assessment indicators can be examined across a simulated workforce.

The dataset includes 1,500 synthetic employees distributed across eight departments and six employee roles.

### Workforce Overview Metrics

| Metric | Calculation |
|---|---|
| Employees | Number of employee records after filtering |
| Average AI Proficiency | Mean of overall proficiency scores |
| Average Role Attainment | Mean of individual attainment percentages |
| Average Competency Gaps | Mean number of unmet competency targets per employee |

These measures are recalculated according to the selected department and employee-role filters.

### Synthetic Demonstration Results

| Workforce Indicator | Result |
|---|---:|
| Employees | 1,500 |
| Average AI Proficiency | 57.3/100 |
| Average Role Attainment | 32.6% |
| Average Competency Gaps | 5.4 |
| Approved AI Tool Access | 48.1% |
| Training Completed | 31.7% |
| Daily AI Usage | 21.3% |
| Average Manager Support | 3.0/5 |

These values come from generated demonstration records and do not represent actual organizational outcomes.

### Workforce Proficiency Distribution

The dashboard visual
