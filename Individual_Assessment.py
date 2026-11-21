
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# ---------------------------------------
# Page configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI Workforce Proficiency Framework",
    page_icon="🧠",
    layout="wide"
)


@st.cache_data
def load_assessment_data():
    return (
        load_questions(),
        load_role_targets(),
        load_learning_catalog()
    )


questions, role_targets, learning_catalog = load_assessment_data()

domains = list(dict.fromkeys(
    q["domain"] for q in questions
))

role_descriptions = {
    "Individual Contributor":
        "An employee who uses AI to support everyday work "
        "without formal responsibility for managing staff.",

    "People Manager":
        "A supervisor responsible for employees, team "
        "performance, and appropriate AI oversight.",

    "Learning & Development Professional":
        "A professional who designs training, develops "
        "employee skills, and evaluates learning outcomes.",

    "Data or Technical Professional":
        "An employee who works with data, technology, "
        "automation, or technical AI applications.",

    "AI Workflow Owner":
        "An employee responsible for implementing, "
        "maintaining, or overseeing AI-supported workflows.",

    "Senior Leader":
        "A director or executive responsible for strategy, "
        "organizational governance, and transformation."
}

# ---------------------------------------
# Session state
# ---------------------------------------

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "section" not in st.session_state:
    st.session_state.section = 0

if "results" not in st.session_state:
    st.session_state.results = None


def save_answer(question_id, widget_key):
    answer = st.session_state[widget_key]

    if answer is None:
        st.session_state.answers.pop(question_id, None)
    else:
        st.session_state.answers[question_id] = answer


def reset_assessment():
    st.session_state.answers = {}
    st.session_state.section = 0
    st.session_state.results = None


def change_role():
    reset_assessment()


# ---------------------------------------
# Application header
# ---------------------------------------

st.title("AI Workforce Learning & Proficiency Framework")

st.write(
    "Assess your AI proficiency, identify competency gaps, "
    "and explore personalized learning recommendations."
)

st.caption(
    "Prototype assessment using transparent, role-based "
    "scoring. Results are developmental indicators."
)

st.divider()

# ---------------------------------------
# Role selection
# ---------------------------------------

st.subheader("1. Select Your Employee Role")

selected_role = st.selectbox(
    "Which role best describes your responsibilities?",
    list(role_targets.keys()),
    key="employee_role",
    on_change=change_role
)

st.info(role_descriptions[selected_role])

st.divider()

# ---------------------------------------
# Results page
# ---------------------------------------

if st.session_state.results is not None:

    report = st.session_state.results

    st.header("Your AI Proficiency Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Overall Proficiency",
        f"{report['overall']:.1f}/100"
    )

    col2.metric(
        "Proficiency Level",
        report["level"]
    )

    col3.metric(
        "Role Target Attainment",
        f"{report['attainment']:.1f}%"
    )

    st.divider()

    st.subheader("Competency Domain Results")

    comparison = report["comparison"]

    results_df = pd.DataFrame([
        {
            "Competency Domain": domain,
            "Your Score": result["actual_score"],
            "Role Target": result["target_score"],
            "Gap": result["gap"],
            "Status": (
                "Meets Target"
                if result["meets_target"]
                else "Development Needed"
            )
        }
        for domain, result in comparison.items()
    ])

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True
    )

    # Competency comparison visualization
    st.subheader("AI Competency Scores vs. Role Targets")

    chart_df = results_df.iloc[::-1]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=chart_df["Competency Domain"],
            x=chart_df["Your Score"],
            name="Your Score",
            orientation="h",
            marker_color="#1686C7"
        )
    )

    fig.add_trace(
        go.Bar(
            y=chart_df["Competency Domain"],
            x=chart_df["Role Target"],
            name="Role Target",
            orientation="h",
            marker_color="#8EBBE0"
        )
    )

    fig.update_layout(
        barmode="group",
        height=480,
        xaxis=dict(
            title="Proficiency Score (%)",
            range=[0, 105],
            ticksuffix="%"
        ),
        yaxis=dict(title=""),
        legend=dict(
            orientation="h",
            x=0,
            y=1.08
        ),
        margin=dict(
            l=10,
            r=20,
            t=60,
            b=40
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # Personalized learning pathway
    st.subheader("Your Recommended Learning Pathway")

    recommendations = report["recommendations"]

    if not recommendations:
        st.success(
            "You meet all role-specific competency targets."
        )
    else:
        for number, item in enumerate(
            recommendations, start=1
        ):
            with st.expander(
                f"{number}. {item['title']} "
                f"({item['priority']} Priority)"
            ):
                st.write(
                    f"**Domain:** {item['domain']}"
                )
                st.write(
                    f"**Objective:** {item['objective']}"
                )
                st.write(
                    f"**Activity:** {item['activity']}"
                )
                st.write(
                    f"**Estimated Time:** "
                    f"{item['estimated_minutes']} minutes"
                )
                st.write(
                    f"**Competency Gap:** "
                    f"{item['gap']:.1f} points"
                )

    st.divider()

    st.caption(
        "Results support workforce learning and development. "
        "This prototype is not a validated employee "
        "performance evaluation instrument."
    )

    if st.button("Start New Assessment"):
        reset_assessment()
        st.rerun()

# ---------------------------------------
# Assessment and navigation
# ---------------------------------------

else:

    st.subheader("2. Complete the AI Proficiency Assessment")

    answered = len(st.session_state.answers)
    total = len(questions)

    st.progress(answered / total)

    st.caption(
        f"{answered} of {total} questions answered"
    )

    section = st.session_state.section

    # Eight competency sections
    if section < len(domains):

        current_domain = domains[section]

        st.markdown(
            f"### Section {section + 1} of {len(domains)}"
        )

        st.subheader(current_domain)

        current_questions = [
            q for q in questions
            if q["domain"] == current_domain
        ]

        with st.container(border=True):

            for question in current_questions:

                st.markdown(
                    f"**{question['id']}. "
                    f"{question['question']}**"
                )

                options = question["options"]
                widget_key = f"answer_{question['id']}"

                # Restore a saved answer when returning
                # to a previously visited section.
                if widget_key not in st.session_state:
                    st.session_state[widget_key] = (
                        st.session_state.answers.get(
                            question["id"]
                        )
                    )

                st.radio(
                    "Select your answer:",
                    options=list(options.keys()),
                    format_func=lambda key, opts=options: (
                        f"{key}. {opts[key]}"
                    ),
                    index=None,
                    key=widget_key,
                    on_change=save_answer,
                    args=(question["id"], widget_key)
                )

                st.divider()

        previous_col, next_col = st.columns(2)

        with previous_col:
            if section > 0:
                if st.button(
                    "← Previous Section",
                    use_container_width=True
                ):
                    st.session_state.section -= 1
                    st.rerun()

        with next_col:
            if st.button(
                "Next Section →"
                if section < len(domains) - 1
                else "Review Answers →",
                type="primary",
                use_container_width=True
            ):
                st.session_state.section += 1
                st.rerun()

    # ---------------------------------------
    # Review and submission
    # ---------------------------------------

    else:

        st.header("Review Your Assessment")

        st.write(
            "Review your progress before submitting. "
            "You can return to any section to change an answer."
        )

        for index, domain in enumerate(domains):

            domain_questions = [
                q for q in questions
                if q["domain"] == domain
            ]

            completed = sum(
                q["id"] in st.session_state.answers
                for q in domain_questions
            )

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(
                    f"**{domain}** — "
                    f"{completed}/{len(domain_questions)} answered"
                )

            with col2:
                if st.button(
                    "Review",
                    key=f"review_{index}"
                ):
                    st.session_state.section = index
                    st.rerun()

        st.divider()

        missing = [
            q["id"]
            for q in questions
            if q["id"] not in st.session_state.answers
        ]

        if missing:
            st.warning(
                "Please complete all questions before "
                "submitting. Missing: "
                + ", ".join(missing)
            )
        else:
            st.success(
                "All 24 questions are complete. "
                "Your assessment is ready to submit."
            )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "← Previous Section",
                use_container_width=True
            ):
                st.session_state.section = len(domains) - 1
                st.rerun()

        with col2:
            if st.button(
                "Submit Assessment",
                type="primary",
                disabled=bool(missing),
                use_container_width=True
            ):

                responses = st.session_state.answers

                overall, category_scores = (
                    calculate_overall_score(
                        questions,
                        responses
                    )
                )

                domain_scores = calculate_domain_scores(
                    questions,
                    responses
                )

                comparison, attainment = compare_role_targets(
                    domain_scores,
                    selected_role,
                    role_targets
                )

                recommendations = recommend_learning(
                    comparison,
                    learning_catalog
                )

                st.session_state.results = {
                    "overall": overall,
                    "level": classify_proficiency(overall),
                    "attainment": attainment,
                    "comparison": comparison,
                    "recommendations": recommendations
                }

                st.rerun()
