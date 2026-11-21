
import json
from pathlib import Path

# Locate our assessment questions
BASE_DIR = Path(__file__).resolve().parent.parent
QUESTION_FILE = BASE_DIR / "data" / "assessment_questions.json"

# Assessment category weights
WEIGHTS = {
    "practical": 0.60,
    "knowledge": 0.30,
    "reflection": 0.10
}

# Load the questions
def load_questions():
    with open(QUESTION_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

    
# Load role-specific proficiency expectations
def load_role_targets():
    role_file = BASE_DIR / "data" / "role_targets.json"

    with open(role_file, "r", encoding="utf-8") as file:
        return json.load(file)


# Load the learning recommendation catalog
def load_learning_catalog():
    catalog_file = BASE_DIR / "data" / "learning_catalog.json"

    with open(catalog_file, "r", encoding="utf-8") as file:
        return json.load(file)



# Calculate overall proficiency
def calculate_overall_score(questions, responses):
    category_scores = {}

    for category, weight in WEIGHTS.items():
        category_questions = [
            q for q in questions if q["type"] == category
        ]

        earned = sum(
            q["scores"][responses[q["id"]]]
            for q in category_questions
        )

        maximum = len(category_questions) * 4

        percentage = (
            earned / maximum * 100
            if maximum > 0 else 0
        )

        category_scores[category] = percentage

    overall = sum(
        category_scores[category] * weight
        for category, weight in WEIGHTS.items()
    )

    return round(overall, 2), category_scores


# Calculate scores for all eight competency domains
def calculate_domain_scores(questions, responses):
    domain_scores = {}

    domains = list(dict.fromkeys(
        q["domain"] for q in questions
    ))

    for domain in domains:
        domain_questions = [
            q for q in questions
            if q["domain"] == domain
        ]

        earned = sum(
            q["scores"][responses[q["id"]]]
            for q in domain_questions
        )

        maximum = len(domain_questions) * 4

        domain_scores[domain] = round(
            earned / maximum * 100, 2
        ) if maximum else 0

    return domain_scores


# Compare employee domain scores with role expectations
def compare_role_targets(domain_scores, role_name, role_targets):
    thresholds = {
        1: 25,
        2: 50,
        3: 70,
        4: 85
    }

    if role_name not in role_targets:
        raise ValueError(f"Unknown employee role: {role_name}")

    results = {}

    for domain, level in role_targets[role_name].items():
        actual_score = domain_scores[domain]
        required_score = thresholds[level]

        results[domain] = {
            "actual_score": actual_score,
            "target_score": required_score,
            "gap": round(max(0, required_score - actual_score), 2),
            "meets_target": actual_score >= required_score
        }

    attainment = (
        sum(item["meets_target"] for item in results.values())
        / len(results) * 100
    )

    return results, round(attainment, 2)


# Generate personalized learning recommendations
def recommend_learning(comparison, learning_catalog):
    recommendations = []

    for item in learning_catalog:
        domain = item["domain"]

        if domain not in comparison:
            continue

        result = comparison[domain]

        if result["meets_target"]:
            continue

        gap = result["gap"]

        # Prioritize critical responsible AI and oversight gaps
        if domain in ["Responsible AI", "Human Oversight"] and gap >= 20:
            priority = "Critical"
            priority_rank = 0
        elif gap >= 30:
            priority = "High"
            priority_rank = 1
        elif gap >= 10:
            priority = "Moderate"
            priority_rank = 2
        else:
            priority = "Low"
            priority_rank = 3

        recommendations.append({
            "domain": domain,
            "title": item["title"],
            "objective": item["objective"],
            "activity": item["activity"],
            "estimated_minutes": item["estimated_minutes"],
            "gap": gap,
            "priority": priority,
            "priority_rank": priority_rank
        })

    recommendations.sort(
        key=lambda x: (x["priority_rank"], -x["gap"])
    )

    return recommendations



# Determine proficiency classification
def classify_proficiency(score):
    if score < 25:
        return "Foundational"
    elif score < 50:
        return "Developing"
    elif score < 70:
        return "Applied"
    elif score < 85:
        return "Advanced"
    else:
        return "Advanced (Leadership Review Eligible)"


# Test our scoring engine
if __name__ == "__main__":
    questions = load_questions()

    role_targets = load_role_targets()

    print("\nRole Targets Loaded:")
    for role in role_targets:
        print(f"- {role}")


     # Simulate an employee with varying AI proficiency
    # Scores vary across the eight competency domains
    target_scores = [
        4, 2, 4,     # AI Literacy
        4, 2, 4,     # Prompting & Interaction
        2, 4, 2,     # Workflow Integration
        0, 2, 0,     # Evaluation & Verification
        2, 0, 2,     # Responsible AI
        4, 2, 2,     # Human Oversight
        4, 4, 2,     # AI Collaboration
        2, 4, 2      # Change Readiness
    ]

    responses = {}

    for question, target in zip(questions, target_scores):
        matching_answers = [
            option
            for option, points in question["scores"].items()
            if points == target
        ]

        responses[question["id"]] = (
            matching_answers[0]
            if matching_answers
            else min(question["scores"], key=question["scores"].get)
        )



    # Display competency domain results
    domain_results = calculate_domain_scores(
        questions, responses
    )

    print("\nCompetency Domain Results:")
    for domain, result in domain_results.items():
        print(f"{domain}: {result:.1f}%")


    # Test role-specific competency expectations
    selected_role = "Individual Contributor"

    comparison, attainment = compare_role_targets(
        domain_results,
        selected_role,
        role_targets
    )

    print(f"\nRole: {selected_role}")
    print(f"Role Target Attainment: {attainment:.1f}%")

    print("\nRole-Specific Competency Results:")

    for domain, result in comparison.items():
        status = (
            "Meets Target"
            if result["meets_target"]
            else "Development Needed"
        )

        print(
            f"{domain}: {result['actual_score']:.1f}% "
            f"(Target: {result['target_score']}%) - {status}"
        )


    # Generate learning recommendations
    learning_catalog = load_learning_catalog()

    recommendations = recommend_learning(
        comparison,
        learning_catalog
    )

    print("\nPersonalized Learning Recommendations:")
    print("-------------------------------------")

    if not recommendations:
        print("All role-specific competency targets have been met.")
    else:
        for number, item in enumerate(recommendations, start=1):
            print(f"\n{number}. {item['title']}")
            print(f"   Domain: {item['domain']}")
            print(f"   Priority: {item['priority']}")
            print(f"   Competency Gap: {item['gap']:.1f} points")
            print(f"   Activity: {item['activity']}")
            print(f"   Estimated Time: {item['estimated_minutes']} minutes")
