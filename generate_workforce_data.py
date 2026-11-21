
import random
from pathlib import Path

import pandas as pd

from scoring.proficiency_scoring import (
    load_questions,
    load_role_targets,
    calculate_overall_score,
    calculate_domain_scores,
    classify_proficiency,
    compare_role_targets,
)

# ---------------------------------------
# Configuration
# ---------------------------------------

random.seed(42)

EMPLOYEE_COUNT = 1500

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "data" / "synthetic_workforce.csv"

DEPARTMENTS = {
    "Operations": 0.20,
    "Human Resources": 0.12,
    "Learning & Development": 0.10,
    "Customer Service": 0.18,
    "Technology": 0.15,
    "Finance": 0.12,
    "Marketing": 0.08,
    "Leadership": 0.05,
}

ROLES = [
    "Individual Contributor",
    "People Manager",
    "Learning & Development Professional",
    "Data or Technical Professional",
    "AI Workflow Owner",
    "Senior Leader",
]

# Simulated department differences.
# These are design assumptions, not real-world findings.
DEPARTMENT_SKILL_ADJUSTMENTS = {
    "Operations": 0.00,
    "Human Resources": 0.00,
    "Learning & Development": 0.08,
    "Customer Service": -0.05,
    "Technology": 0.12,
    "Finance": 0.02,
    "Marketing": 0.05,
    "Leadership": 0.07,
}


# ---------------------------------------
# Employee role assignment
# ---------------------------------------

def assign_role(department):
    if department == "Leadership":
        weights = [0.10, 0.15, 0.05, 0.05, 0.10, 0.55]

    elif department == "Technology":
        weights = [0.15, 0.10, 0.05, 0.45, 0.20, 0.05]

    elif department == "Learning & Development":
        weights = [0.15, 0.10, 0.60, 0.05, 0.05, 0.05]

    else:
        weights = [0.60, 0.20, 0.03, 0.05, 0.10, 0.02]

    return random.choices(ROLES, weights=weights, k=1)[0]


# ---------------------------------------
# Simulate assessment responses
# ---------------------------------------

def simulate_responses(questions, skill_level):
    responses = {}

    for question in questions:
        options = list(question["scores"].keys())

        # Higher skill increases the probability of
        # selecting higher-scoring responses.
        response_weights = []

        for option in options:
            points = question["scores"][option]
            adjusted_skill = min(max(skill_level, 0.05), 0.95)

            weight = (
                adjusted_skill ** (points / 2)
                * (1 - adjusted_skill) ** ((4 - points) / 2)
            )

            response_weights.append(weight)

        selected = random.choices(
            options,
            weights=response_weights,
            k=1
        )[0]

        responses[question["id"]] = selected

    return responses


# ---------------------------------------
# Create workforce dataset
# ---------------------------------------

def generate_workforce():
    questions = load_questions()
    role_targets = load_role_targets()

    employees = []

    departments = list(DEPARTMENTS.keys())
    department_weights = list(DEPARTMENTS.values())

    for employee_number in range(1, EMPLOYEE_COUNT + 1):

        department = random.choices(
            departments,
            weights=department_weights,
            k=1
        )[0]

        role = assign_role(department)

        # Assign a simulated skill level
        skill_level = random.uniform(0.25, 0.90)

        skill_level += DEPARTMENT_SKILL_ADJUSTMENTS[
            department
        ]

        skill_level = min(max(skill_level, 0.05), 0.95)

        # Generate responses and calculate proficiency
        responses = simulate_responses(
            questions,
            skill_level
        )

        overall, category_scores = calculate_overall_score(
            questions,
            responses
        )

        domain_scores = calculate_domain_scores(
            questions,
            responses
        )

        comparison, attainment = compare_role_targets(
            domain_scores,
            role,
            role_targets
        )

        # Separate organizational adoption indicators
        training_participation = random.choice(
            ["Completed", "In Progress", "Not Started"]
        )

        ai_usage_frequency = random.choice(
            ["Daily", "Weekly", "Monthly", "Rarely", "Never"]
        )

        approved_tool_access = random.choice([True, False])

        manager_support = random.randint(1, 5)

        employee = {
            "employee_id": f"EMP{employee_number:04d}",
            "department": department,
            "role": role,
            "overall_proficiency_score": overall,
            "proficiency_level": classify_proficiency(overall),
            "role_target_attainment_pct": attainment,
            "training_participation": training_participation,
            "ai_usage_frequency": ai_usage_frequency,
            "approved_tool_access": approved_tool_access,
            "manager_support_score": manager_support,
        }

        # Add assessment category scores
        for category, score in category_scores.items():
            column = f"{category}_score"
            employee[column] = round(score, 2)

        # Add eight competency domain scores
        for domain, score in domain_scores.items():
            column = (
                domain.lower()
                .replace(" & ", "_")
                .replace(" ", "_")
            )

            employee[f"{column}_score"] = score

        # Add number of domains needing development
        employee["competency_gaps_count"] = sum(
            not item["meets_target"]
            for item in comparison.values()
        )

        employees.append(employee)

    df = pd.DataFrame(employees)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(OUTPUT_FILE, index=False)

    return df


# ---------------------------------------
# Run generator
# ---------------------------------------

if __name__ == "__main__":

    workforce = generate_workforce()

    print("\nSYNTHETIC AI WORKFORCE DATASET")
    print("--------------------------------")

    print(f"Employees generated: {len(workforce)}")
    print(f"Departments: {workforce['department'].nunique()}")
    print(f"Employee roles: {workforce['role'].nunique()}")

    print(
        "Average proficiency score:",
        round(
            workforce["overall_proficiency_score"].mean(),
            2
        )
    )

    print("\nProficiency Distribution:")
    print(workforce["proficiency_level"].value_counts())

    print("\nDepartment Distribution:")
    print(workforce["department"].value_counts())

    print(f"\nDataset saved to: {OUTPUT_FILE}")
