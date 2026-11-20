#!/usr/bin/env python
# coding: utf-8

# # Employee Data Analysis
# 
# ## 1. Project Overview
# 
# ## 2. NumPy Analysis
# 
# ## 3. Employee Data Exploration
# 
# ## 4. Data Cleaning
# 
# ## 5. Department Analysis
# 
# ## 6. Data Merging
# 
# ## 7. Data Visualisation
# 
# ## 8. Performance Measurement
# 
# ## 9. Key Findings

# In[ ]:


# EMPLOYEE DATA ANALYSIS - WEEK 1 ASSESSMENT

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create output folder
Path("../reports/figures").mkdir(parents=True, exist_ok=True)

# NUMPY ANALYSIS:

marks = np.array([
    [78, 85, 90],
    [88, 76, 92],
    [69, 80, 75],
    [95, 89, 84]
])

print("NUMPY ANALYSIS")

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

# LOAD EMPLOYEE DATA:

df = pd.read_csv("data/employees.csv")

print("\nEMPLOYEE DATA")
print(df.head())

print("\nDATAFRAME INFORMATION")
df.info()

print("\nDESCRIPTIVE STATISTICS")
display(df.describe())

print("\nUSING LOC")
display(df.loc[0:2, ["name", "salary"]])

print("\nUSING ILOC")
display(df.iloc[0:3, 0:3])

print("\nFILTERING EMPLOYEES WITH SALARY ABOVE 50000")
display(df[df["salary"] > 50000])

# 3. DATA CLEANING:

dirty_df = df.copy()

# Introduce two missing salaries
dirty_df.loc[0, "salary"] = np.nan
dirty_df.loc[1, "salary"] = np.nan

# Introduce one duplicate row
dirty_df = pd.concat(
    [dirty_df, dirty_df.iloc[[0]]],
    ignore_index=True
)

print("\nMISSING VALUES BEFORE CLEANING")
print(dirty_df.isnull().sum())

# Remove duplicate records
cleaned_df = dirty_df.drop_duplicates().copy()

# Fill missing salaries using median
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
cleaned_df.to_csv(
    "data/employees_cleaned.csv",
    index=False
)

print("\nDATA CLEANING COMPLETED")
print(cleaned_df.dtypes)

# 4. CREATE DEPARTMENTS CSV:

departments = pd.DataFrame({
    "department": [
        "Sales", "HR", "IT", "Finance", "Marketing"
    ],
    "head": [
        "Arun", "Priya", "Rahul", "Karthik", "Not Assigned"
    ],
    "budget": [
        100000, 80000, 150000, 120000, 50000
    ]
})

departments.to_csv(
    "data/departments.csv",
    index=False
)

print("\nDEPARTMENTS DATA")
display(departments)

# GROUPBY AND AGGREGATION:

department_summary = cleaned_df.groupby("department").agg(
    headcount=("name", "count"),
    average_salary=("salary", "mean"),
    maximum_salary=("salary", "max")
)

print("\nDEPARTMENT SUMMARY")
display(department_summary)

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

# DATA MERGING:

inner_join = pd.merge(
    cleaned_df,
    departments,
    on="department",
    how="inner"
)

left_join = pd.merge(
    cleaned_df,
    departments,
    on="department",
    how="left"
)

outer_join = pd.merge(
    cleaned_df,
    departments,
    on="department",
    how="outer",
    indicator=True
)

print("\nINNER JOIN")
display(inner_join)

print("\nLEFT JOIN")
display(left_join)

print("\nOUTER JOIN")
display(outer_join)

departments_without_employees = outer_join.loc[
    outer_join["_merge"] == "right_only",
    "department"
].dropna().unique()

print(
    "Departments without employees:",
    ", ".join(departments_without_employees)
)

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

plt.savefig("../reports/figures/department_salary.png")
plt.show()
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

plt.savefig("../reports/figures/salary_histogram.png")
plt.show()
plt.close()

print("Insight: The histogram shows the distribution of employee salaries.")

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

plt.savefig("../reports/figures/salary_scatter.png")
plt.show()
plt.close()

print("Insight: The scatter plot shows salary differences between employees.")

# 10. LINE CHART:

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

plt.savefig("../reports/figures/salary_line.png")
plt.show()
plt.close()

print("Insight: The line chart compares salaries across employees.")

# 11. PERFORMANCE MEASUREMENT:

print("\nPERFORMANCE MEASUREMENT")

get_ipython().run_line_magic('timeit', 'df["salary"].mean()')

# 12. KEY FINDINGS:

print("\nKEY FINDINGS")

print("1. Employee data contains eight original records.")
print("2. Missing salary values were filled using the median.")
print("3. Duplicate employee records were removed.")
print("4. IT has the highest employee headcount.")
print("5. Marketing is the department without employees.")

print("\nEMPLOYEE ANALYSIS COMPLETED SUCCESSFULLY")


# In[ ]:




