
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "synthetic_workforce.csv"

df = pd.read_csv(DATA_FILE)

print("\nAI WORKFORCE DATA VALIDATION")
print("-" * 40)

# Workforce record checks
assert len(df) == 1500, "Incorrect employee count"
assert df["employee_id"].is_unique, "Duplicate employee IDs"
assert df["department"].nunique() == 8, "Missing departments"
assert df["role"].nunique() == 6, "Missing employee roles"

# Missing data
missing_count = int(df.isna().sum().sum())
assert missing_count == 0, "Missing values detected"

# Check score boundaries
score_columns = [
    column for column in df.columns
    if column.endswith("_score")
]

score_columns += [
    "overall_proficiency_score",
    "role_target_attainment_pct"
]

score_columns = list(dict.fromkeys(score_columns))

for column in score_columns:
    assert df[column].between(0, 100).all(), (
        f"Invalid scores in {column}"
    )

# Role target attainment must use eight domains
valid_attainment = {
    round(count / 8 * 100, 2)
    for count in range(9)
}

assert df["role_target_attainment_pct"].round(2).isin(
    valid_attainment
).all(), "Invalid role attainment value"

# Competency gaps range from zero to eight
assert df["competency_gaps_count"].between(0, 8).all()

print(f"Employee records: {len(df)}")
print(f"Unique employee IDs: {df['employee_id'].nunique()}")
print(f"Departments: {df['department'].nunique()}")
print(f"Roles: {df['role'].nunique()}")
print(f"Missing values: {missing_count}")
print(f"Score columns checked: {len(score_columns)}")

print("\nALL WORKFORCE DATA VALIDATION CHECKS PASSED!")
