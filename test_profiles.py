
from scoring.proficiency_scoring import (
    load_questions,
    load_role_targets,
    load_learning_catalog,
    calculate_overall_score,
    calculate_domain_scores,
    classify_proficiency,
    compare_role_targets,
    recommend_learning,
)

# Four synthetic employee profiles
# high = strongest answer, low = weakest answer
# medium = intermediate answer, where available

employees = [
    {
        "id": "EMP001",
        "role": "Individual Contributor",
        "default": "medium",
        "overrides": {
            "AI Literacy": "high",
            "Evaluation & Verification": "low",
            "Responsible AI": "low",
        },
    },
    {
        "id": "EMP002",
        "role": "People Manager",
        "default": "high",
        "overrides": {
            "Human Oversight": "low",
        },
    },
    {
        "id": "EMP003",
        "role": "Senior Leader",
        "default": "high",
        "overrides": {
            "Prompting & Interaction": "low",
        },
    },
    {
        "id": "EMP004",
        "role": "AI Workflow Owner",
        "default": "high",
        "overrides": {},
    },
]


def select_answer(question, performance):
    scores = question["scores"]

    # Sort available answers by their actual point values
    ranked = sorted(
        scores,
        key=lambda option: scores[option]
    )

    if performance == "high":
        return ranked[-1]

    if performance == "low":
        return ranked[0]

    # Select intermediate credit when available.
    # Binary questions use the lower-scoring answer.
    middle = [
        option for option in ranked
        if 0 < scores[option] < 4
    ]

    return middle[0] if middle else ranked[0]


def run_tests():
    questions = load_questions()
    role_targets = load_role_targets()
    catalog = load_learning_catalog()

    assert len(questions) == 24
    assert len(role_targets) == 6
    assert len(catalog) == 8

    print("AI WORKFORCE SIMULATED EMPLOYEE TESTS")
    print("=" * 45)

    for employee in employees:
        responses = {}

        for question in questions:
            performance = employee["overrides"].get(
                question["domain"],
                employee["default"]
            )

            responses[question["id"]] = select_answer(
                question,
                performance
            )

        assert len(responses) == len(questions)

        overall, categories = calculate_overall_score(
            questions, responses
        )

        domains = calculate_domain_scores(
            questions, responses
        )

        comparison, attainment = compare_role_targets(
            domains,
            employee["role"],
            role_targets
        )

        recommendations = recommend_learning(
            comparison,
            catalog
        )

        print(f"\nEmployee: {employee['id']}")
        print(f"Role: {employee['role']}")
        print(f"Overall score: {overall:.1f}/100")
        print(f"Level: {classify_proficiency(overall)}")
        print(f"Role attainment: {attainment:.1f}%")

        print("\nDomain Results:")
        for domain, score in domains.items():
            status = (
                "Met"
                if comparison[domain]["meets_target"]
                else "Gap"
            )
            print(f"  {domain}: {score:.1f}% - {status}")

        print("\nLearning Recommendations:")
        if not recommendations:
            print("  No additional learning required.")
        else:
            for item in recommendations:
                print(
                    f"  [{item['priority']}] "
                    f"{item['title']}"
                )

        # Verify scoring boundaries
        assert 0 <= overall <= 100
        assert 0 <= attainment <= 100
        assert len(domains) == 8

        # Check important expected outcomes
        if employee["id"] == "EMP002":
            assert not comparison[
                "Human Oversight"
            ]["meets_target"]

        if employee["id"] == "EMP003":
            assert domains[
                "Responsible AI"
            ] == 100

        if employee["id"] == "EMP004":
            assert overall == 100
            assert attainment == 100
            assert len(recommendations) == 0

        print("-" * 45)

    print("\nALL FOUR SIMULATED EMPLOYEE TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
