
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI Workforce Analytics",
    page_icon="📊",
    layout="wide"
)

# Locate and load the workforce dataset
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "synthetic_workforce.csv"

@st.cache_data
def load_workforce_data():
    return pd.read_csv(DATA_FILE)

df = load_workforce_data()

# Dashboard header
st.title("Organizational AI Workforce Analytics")

st.write(
    "Explore AI proficiency, role readiness, and workforce "
    "development needs across a synthetic organization."
)

st.caption(
    "Demonstration using 1,500 synthetic employee records."
)

# ---------------------------------------
# Workforce Filters
# ---------------------------------------

st.divider()
st.subheader("Workforce Filters")

col1, col2 = st.columns(2)

with col1:
    selected_departments = st.multiselect(
        "Department",
        options=sorted(df["department"].unique()),
        default=sorted(df["department"].unique())
    )

with col2:
    selected_roles = st.multiselect(
        "Employee Role",
        options=sorted(df["role"].unique()),
        default=sorted(df["role"].unique())
    )

# Apply selected filters
filtered_df = df[
    df["department"].isin(selected_departments)
    & df["role"].isin(selected_roles)
]

if filtered_df.empty:
    st.warning("No employees match the selected filters.")
    st.stop()


# ---------------------------------------
# Workforce Overview
# ---------------------------------------

st.divider()
st.subheader("Workforce Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Employees",
    f"{len(filtered_df):,}"
)

col2.metric(
    "Average AI Proficiency",
    f"{filtered_df['overall_proficiency_score'].mean():.1f}/100"
)

col3.metric(
    "Average Role Attainment",
    f"{filtered_df['role_target_attainment_pct'].mean():.1f}%"
)

col4.metric(
    "Average Competency Gaps",
    f"{filtered_df['competency_gaps_count'].mean():.1f}"
)

# ---------------------------------------
# Workforce Proficiency Distribution
# ---------------------------------------

st.divider()
st.subheader("Workforce Proficiency Distribution")

level_order = [
    "Foundational",
    "Developing",
    "Applied",
    "Advanced",
    "Advanced (Leadership Review Eligible)"
]

distribution = (
    filtered_df["proficiency_level"]
    .value_counts()
    .reindex(level_order, fill_value=0)
    .reset_index()
)

distribution.columns = ["Proficiency Level", "Employees"]

fig_distribution = px.bar(
    distribution,
    x="Proficiency Level",
    y="Employees",
    text="Employees",
    title="Employees by AI Proficiency Classification"
)

fig_distribution.update_layout(
    xaxis_title="",
    yaxis_title="Number of Employees"
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True
)

# ---------------------------------------
# AI Proficiency by Department
# ---------------------------------------

st.divider()
st.subheader("AI Proficiency by Department")

department_scores = (
    filtered_df.groupby("department", as_index=False)[
        "overall_proficiency_score"
    ]
    .mean()
    .sort_values("overall_proficiency_score")
)

fig_departments = px.bar(
    department_scores,
    x="overall_proficiency_score",
    y="department",
    orientation="h",
    title="Average AI Proficiency by Department",
    labels={
        "overall_proficiency_score": "Average Score / 100",
        "department": "Department"
    }
)

fig_departments.update_xaxes(range=[0, 100])

st.plotly_chart(
    fig_departments,
    use_container_width=True
)

# ---------------------------------------
# Organizational Competency Scores
# ---------------------------------------

st.divider()
st.subheader("Organizational Competency Scores")

# Identify the eight competency score columns
domain_columns = [
    column for column in filtered_df.columns
    if column.endswith("_score")
    and column not in [
        "overall_proficiency_score",
        "practical_score",
        "knowledge_score",
        "reflection_score",
        "manager_support_score"
    ]
]

# Calculate average scores
domain_averages = (
    filtered_df[domain_columns]
    .mean()
    .sort_values()
    .reset_index()
)

domain_averages.columns = [
    "Competency Domain",
    "Average Score"
]

# Format domain labels
domain_averages["Competency Domain"] = (
    domain_averages["Competency Domain"]
    .str.replace("_score", "", regex=False)
    .str.replace("_", " ")
    .str.title()
)

# Create the horizontal bar chart
fig_domains = px.bar(
    domain_averages,
    x="Average Score",
    y="Competency Domain",
    orientation="h",
    title="Average AI Competency Scores",
    labels={
        "Average Score": "Average Score / 100"
    }
)

fig_domains.update_xaxes(range=[0, 100])

st.plotly_chart(
    fig_domains,
    use_container_width=True
)

st.caption(
    "These bars represent average competency scores, "
    "not the percentage of employees below their "
    "role-specific proficiency targets."
)

# ---------------------------------------
# AI Adoption & Training Insights
# ---------------------------------------

st.divider()
st.header("AI Adoption & Training Insights")

st.write(
    "Explore access to approved AI tools, training "
    "participation, AI usage frequency, and management "
    "support across the selected workforce."
)

# Calculate adoption and training metrics
tool_access_pct = (
    filtered_df["approved_tool_access"].mean() * 100
)

training_completed_pct = (
    filtered_df["training_participation"]
    .eq("Completed")
    .mean() * 100
)

daily_usage_pct = (
    filtered_df["ai_usage_frequency"]
    .eq("Daily")
    .mean() * 100
)

average_support = (
    filtered_df["manager_support_score"].mean()
)

# Display four summary metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Approved AI Tool Access",
    f"{tool_access_pct:.1f}%"
)

col2.metric(
    "Training Completed",
    f"{training_completed_pct:.1f}%"
)

col3.metric(
    "Daily AI Usage",
    f"{daily_usage_pct:.1f}%"
)

col4.metric(
    "Average Manager Support",
    f"{average_support:.1f}/5"
)

# ---------------------------------------
# Employee Training Participation
# ---------------------------------------

st.divider()
st.subheader("Employee Training Participation")

training_order = [
    "Not Started",
    "In Progress",
    "Completed"
]

training_counts = (
    filtered_df["training_participation"]
    .value_counts()
    .reindex(training_order, fill_value=0)
    .reset_index()
)

training_counts.columns = [
    "Training Status",
    "Employees"
]

fig_training = px.bar(
    training_counts,
    x="Training Status",
    y="Employees",
    text="Employees",
    title="AI Training Participation"
)

fig_training.update_layout(
    xaxis_title="",
    yaxis_title="Number of Employees"
)

st.plotly_chart(
    fig_training,
    use_container_width=True
)

# ---------------------------------------
# AI Usage Frequency
# ---------------------------------------

st.divider()
st.subheader("AI Usage Frequency")

usage_order = [
    "Daily",
    "Weekly",
    "Monthly",
    "Rarely",
    "Never"
]

usage_counts = (
    filtered_df["ai_usage_frequency"]
    .value_counts()
    .reindex(usage_order, fill_value=0)
    .reset_index()
)

usage_counts.columns = [
    "Usage Frequency",
    "Employees"
]

fig_usage = px.bar(
    usage_counts,
    x="Usage Frequency",
    y="Employees",
    text="Employees",
    title="How Frequently Employees Use AI"
)

fig_usage.update_layout(
    xaxis_title="",
    yaxis_title="Number of Employees"
)

st.plotly_chart(
    fig_usage,
    use_container_width=True
)

# ---------------------------------------
# Approved AI Tool Access by Department
# ---------------------------------------

st.divider()
st.subheader("Approved AI Tool Access by Department")

department_access = (
    filtered_df.groupby("department", as_index=False)[
        "approved_tool_access"
    ]
    .mean()
)

department_access["Access Percentage"] = (
    department_access["approved_tool_access"] * 100
)

department_access = department_access.sort_values(
    "Access Percentage"
)

fig_access = px.bar(
    department_access,
    x="Access Percentage",
    y="department",
    orientation="h",
    title="Approved AI Tool Access by Department",
    labels={
        "department": "Department",
        "Access Percentage": "Employees With Access (%)"
    }
)

fig_access.update_xaxes(
    range=[0, 100],
    ticksuffix="%"
)

st.plotly_chart(
    fig_access,
    use_container_width=True
)

# ---------------------------------------
# Management Support for AI Adoption
# ---------------------------------------

st.divider()
st.subheader("Management Support for AI Adoption")

department_support = (
    filtered_df.groupby("department", as_index=False)[
        "manager_support_score"
    ]
    .mean()
    .sort_values("manager_support_score")
)

fig_support = px.bar(
    department_support,
    x="manager_support_score",
    y="department",
    orientation="h",
    title="Average Manager Support by Department",
    labels={
        "manager_support_score": "Average Support Rating",
        "department": "Department"
    }
)

fig_support.update_xaxes(range=[0, 5])

st.plotly_chart(
    fig_support,
    use_container_width=True
)

st.caption(
    "All workforce records are synthetic. "
    "Proficiency, training, and adoption patterns "
    "are generated for demonstration purposes."
)

# ---------------------------------------
# Role-Specific Competency Gap Analysis
# ---------------------------------------

import json

st.divider()
st.header("Role-Specific Competency Gap Analysis")

st.write(
    "Identify the percentage of employees who fall below "
    "their assigned role-specific proficiency targets."
)

# Load the six employee role target profiles
ROLE_TARGETS_FILE = BASE_DIR / "data" / "role_targets.json"

with open(ROLE_TARGETS_FILE, "r", encoding="utf-8") as file:
    role_targets = json.load(file)

# Match competency domains to workforce CSV columns
domain_columns_map = {
    "AI Literacy": "ai_literacy_score",
    "Prompting & Interaction": "prompting_interaction_score",
    "Workflow Integration": "workflow_integration_score",
    "Evaluation & Verification": "evaluation_verification_score",
    "Responsible AI": "responsible_ai_score",
    "Human Oversight": "human_oversight_score",
    "AI Collaboration": "ai_collaboration_score",
    "Change Readiness": "change_readiness_score"
}
gap_results = []

target_thresholds = {
    1: 25,
    2: 50,
    3: 70,
    4: 85
}

for domain, score_column in domain_columns_map.items():

    # Convert role target levels to percentages
    target_percentages = filtered_df["role"].map(
        lambda role: target_thresholds[role_targets[role][domain]]
    )

    # Compare each employee against their own role target
    below_target = (
        filtered_df[score_column] < target_percentages
    )

    gap_results.append({
        "Competency Domain": domain,
        "Employees Below Target": int(below_target.sum()),
        "Gap Rate (%)": round(
            below_target.mean() * 100, 1
        )
    })

gap_df = pd.DataFrame(gap_results)

gap_df = gap_df.sort_values(
    "Gap Rate (%)",
    ascending=True
)

# Display organizational competency gaps
st.dataframe(
    gap_df.sort_values(
        "Gap Rate (%)",
        ascending=False
    ),
    hide_index=True,
    use_container_width=True
)

fig_gaps = px.bar(
    gap_df,
    x="Gap Rate (%)",
    y="Competency Domain",
    orientation="h",
    title="Employees Below Role-Specific Competency Targets",
    text="Gap Rate (%)",
    labels={
        "Gap Rate (%)": "Employees Below Target (%)"
    }
)

fig_gaps.update_xaxes(
    range=[0, 100],
    ticksuffix="%"
)

fig_gaps.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_gaps,
    use_container_width=True
)

st.caption(
    "Each employee's competency score is compared with "
    "the target defined for their assigned employee role. "
    "Percentages reflect the current department and role filters."
)

# ---------------------------------------
# Understanding Your Workforce Analytics
# ---------------------------------------

st.divider()

with st.expander("Understanding Your Workforce Analytics"):

    st.markdown("""
    **Average Competency Score**

    Measures average proficiency within an AI competency
    domain on a scale of 0–100.

    **Competency Gap Rate**

    Represents the percentage of employees who score
    below the proficiency targets for their assigned roles.

    A 70% gap rate means 70% of assessed employees
    did not meet their role-specific target. It does
    not mean their average competency score is 30%.

    **Role Target Attainment**

    Measures the percentage of eight competency domains
    in which an employee meets or exceeds their assigned
    role's proficiency targets.

    Organizational attainment is the average of
    individual employee attainment percentages.

    **Data Interpretation**

    All employee records are synthetic. Results are
    intended for demonstration and workforce learning,
    not validated employee performance evaluation.
    """)


# ---------------------------------------
# Workforce Learning Priorities
# ---------------------------------------

st.divider()
st.header("Workforce Learning Priorities")

st.write(
    "Explore recommended learning activities based on "
    "the most widespread role-specific competency gaps."
)

# Load the learning activity catalog
LEARNING_FILE = BASE_DIR / "data" / "learning_catalog.json"

with open(LEARNING_FILE, "r", encoding="utf-8") as file:
    learning_catalog = json.load(file)

# Connect competency gaps to learning activities
learning_priorities = []

for _, gap in gap_df.iterrows():

    domain = gap["Competency Domain"]

    matching_activities = [
        activity
        for activity in learning_catalog
        if activity["domain"] == domain
    ]

    for activity in matching_activities:

        learning_priorities.append({
            "Competency Domain": domain,
            "Employees Below Target": gap[
                "Employees Below Target"
            ],
            "Gap Rate (%)": gap["Gap Rate (%)"],
            "Recommended Learning Activity": activity["title"],
            "Estimated Minutes": activity["estimated_minutes"]
        })

learning_df = pd.DataFrame(learning_priorities)

learning_df = learning_df.sort_values(
    "Gap Rate (%)",
    ascending=False
)

st.dataframe(
    learning_df,
    hide_index=True,
    use_container_width=True
)

st.caption(
    "Learning priorities are ranked by the percentage "
    "of employees below their role-specific competency "
    "targets. Estimated minutes represent the time "
    "required for each suggested learning activity."
)

# ---------------------------------------
# Export Workforce Learning Priorities
# ---------------------------------------

st.subheader("Export Workforce Learning Priorities")

st.write(
    "Download the learning priorities for the currently "
    "selected departments and employee roles."
)

csv_data = learning_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Learning Priorities (CSV)",
    data=csv_data,
    file_name="workforce_learning_priorities.csv",
    mime="text/csv"
)
