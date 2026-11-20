import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create output folder
Path("reports/figures").mkdir(parents=True, exist_ok=True)

# NUMPY:

marks = np.array([
    [78, 85, 90],
    [88, 76, 92],
    [69, 80, 75],
    [95, 89, 84]
])

print("Array shape:", marks.shape)

student_averages = np.mean(marks, axis=1)
print("Student averages:", student_averages)

subject_averages = np.mean(marks, axis=0)
print("Subject averages:", subject_averages)

grace_marks = marks + 5
print("Marks after grace marks:\n", grace_marks)

weights = np.array([0.2, 0.3, 0.5])
weighted_scores = np.dot(grace_marks, weights)
print("Weighted scores:", weighted_scores)


# LOAD EMPLOYEE DATA USING PANDAS:

df = pd.read_csv("data/employees.csv")

print("\nDataFrame information:")
df.info()

print("\nDescriptive statistics:")
print(df.describe())

print("\nUsing loc:")
print(df.loc[0:2, ["name", "salary"]])

print("\nUsing iloc:")
print(df.iloc[0:3, 0:3])

print("\nFiltering employees with salary above 50000:")
print(df[df["salary"] > 50000])


# CREATE DEPARTMENTS CSV:

departments = pd.DataFrame({
    "department": ["Sales", "HR", "IT", "Finance", "Marketing"],
    "head": ["Arun", "Priya", "Rahul", "Karthik", "Not Assigned"],
    "budget": [100000, 80000, 150000, 120000, 50000]
})

departments.to_csv("data/departments.csv", index=False)

# 4. DATA CLEANING:


dirty_df = df.copy()

# Add two missing salaries
dirty_df.loc[0, "salary"] = np.nan
dirty_df.loc[1, "salary"] = np.nan

# Add one duplicate row
dirty_df = pd.concat(
    [dirty_df, dirty_df.iloc[[0]]],
    ignore_index=True
)

print("\nMissing values before cleaning:")
print(dirty_df.isnull().sum())

# Remove duplicate rows
cleaned_df = dirty_df.drop_duplicates()

# Fill missing salaries with median
cleaned_df["salary"] = cleaned_df["salary"].fillna(
    cleaned_df["salary"].median()
)

# Correct data types
cleaned_df["salary"] = pd.to_numeric(
    cleaned_df["salary"], errors="coerce"
)

cleaned_df["name"] = cleaned_df["name"].astype(str)
cleaned_df["department"] = cleaned_df["department"].astype(str)
cleaned_df["city"] = cleaned_df["city"].astype(str)

# Save cleaned data
cleaned_df.to_csv("data/employees_cleaned.csv", index=False)

print("\nData cleaning completed.")

# GROUPBY AND AGGREGATION:

department_summary = cleaned_df.groupby("department").agg(
    headcount=("name", "count"),
    average_salary=("salary", "mean"),
    maximum_salary=("salary", "max")
)

print("\nDepartment summary:")
print(department_summary)

# Print headcount in the expected order
department_order = ["Sales", "HR", "IT", "Finance"]
headcount = department_summary["headcount"].reindex(
    department_order
)

print(
    "Headcount:",
    " | ".join(
        f"{department} {int(count)}"
        for department, count in headcount.items()
    )
)


# MERGING DATAFRAMES:

inner_join = pd.merge(
    cleaned_df, departments,
    on="department",
    how="inner"
)

left_join = pd.merge(
    cleaned_df, departments,
    on="department",
    how="left"
)

outer_join = pd.merge(
    cleaned_df, departments,
    on="department",
    how="outer",
    indicator=True
)

print("\nInner join:")
print(inner_join)

print("\nLeft join:")
print(left_join)

print("\nOuter join:")
print(outer_join)

# Find departments without employees
departments_without_employees = outer_join.loc[
    outer_join["_merge"] == "right_only",
    "department"
].dropna().unique()

print(
    "Outer join: department with no employees listed",
    ", ".join(departments_without_employees)
)

#  MATPLOTLIB - FOUR CHARTS:

# BAR CHART:

plt.figure(figsize=(8, 5))
plt.bar(
    department_summary.index,
    department_summary["average_salary"],
    label="Average salary"
)
plt.title("Average Salary by Department")
plt.xlabel("Department")
plt.ylabel("Average Salary")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/department_salary.png")
plt.close()

print("Insight: The bar chart compares average salaries across departments.")


# HISTOGRAM:

plt.figure(figsize=(8, 5))
plt.hist(
    cleaned_df["salary"],
    bins=5,
    label="Employee salaries"
)
plt.title("Employee Salary Distribution")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/salary_histogram.png")
plt.close()

print("Insight: The histogram shows how employee salaries are distributed.")


# SCATTER PLOT:

plt.figure(figsize=(8, 5))
plt.scatter(
    cleaned_df.index,
    cleaned_df["salary"],
    label="Employee salary"
)
plt.title("Employee Index vs Salary")
plt.xlabel("Employee Index")
plt.ylabel("Salary")
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/salary_scatter.png")
plt.close()

print("Insight: The scatter plot shows salary differences between employees.")


# LINE CHART:

plt.figure(figsize=(8, 5))
plt.plot(
    cleaned_df["name"],
    cleaned_df["salary"],
    marker="o",
    label="Employee salary"
)
plt.title("Employee Salary Comparison")
plt.xlabel("Employee Name")
plt.ylabel("Salary")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("reports/figures/salary_line.png")
plt.close()

print("Insight: The line chart compares salaries across employee names.")


print("\nAll four charts saved successfully.")