# 🏋️‍♂️ Data Analysis with Python – Gym Members

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)  
[![Pandas](https://img.shields.io/badge/Pandas-Analysis-success?logo=pandas)](https://pandas.pydata.org/)  
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen)](#)  

> An **Exploratory Data Analysis (EDA)** project using **Python** and **Pandas** to explore the behavior of members from a fictional gym.

---

## 📂 Dataset

The file `gym_membership.csv` contains information about **1,000 members**, including:

| Category            | Examples                             |
|---------------------|--------------------------------------|
| **Personal Data**   | ID, gender, age, birthday            |
| **Membership Plan** | Standard, Premium                    |
| **Attendance**      | Visits per week, days per week       |
| **Extra Services**  | Personal trainer, sauna, drinks      |
| **Preferences**     | Favorite group class, favorite drink |

---

## 🔍 Analysis Steps

1. **Loading and initial inspection**
   - Checked if DataFrame is empty
   - Dimensions (rows and columns)
   - Column names and data types (`dtypes`)
   - Checked for data consistency

2. **General information**
   - `.info()` to check null values and data types
   - `.head()` and `.tail()` to preview data

3. **Descriptive statistics**
   - `.describe()` for numeric and categorical columns
   - Most frequent values with `.mode()`

4. **Specific calculations**
   - 📅 Average training days per week  
   - 🏃‍♂️ Average visits per week  
   - 🎯 Standard deviation of age  
   - 🥤 Number of different favorite drinks  
   - 💪 Most popular group class  

5. **Summary DataFrame**
   - Focused on relevant variables for future insights:
     - `Age`
     - `abonoment_type`
     - `visit_per_week`
     - `days_per_week`
     - `avg_time_in_gym`
     - `attend_group_lesson`
     - `personal_training`
     - `uses_sauna`

---

## 📊 Key Insights

| Metric                           | Value          |
|----------------------------------|----------------|
| Avg. training days/week          | 2.68 days      |
| Avg. visits/week                  | 2.68 visits    |
| Age standard deviation           | 10.82 years    |
| Different favorite drinks        | 36             |
| Most popular group class         | BodyPump       |

---

## 📈 Visualizations

Here’s an example of how future visualizations can be added to enrich the analysis:

<p align="center">
  <img src="assets/age_distribution.png" alt="Age Distribution" width="500"/>
</p>

> Example: Distribution of gym members' ages.  
*(This chart can be generated with Matplotlib/Seaborn and stored inside an `assets/` folder in your repo.)*

---

## 🛠 Skills Acquired

| Skill Area                        | Description |
|-----------------------------------|-------------|
| **Data manipulation (Pandas)**   | CSV reading, inspection, filtering, and DataFrame creation |
| **Descriptive statistics**       | Means, standard deviations, modes, counts |
| **Data cleaning & organization** | Handling null values, fixing inconsistent data types |
| **Analytical thinking**          | Interpreting metrics and identifying relevant variables |
| **Documentation**                | Clear structure of analysis and reproducibility |

---

## 🚀 Next Steps
- 📊 Create interactive visualizations with **Matplotlib** and **Seaborn**
- 📈 Correlation analysis between variables
- 🧠 Predictive modeling for customer retention
- 🔍 Customer segmentation based on behavior

---

💡 **Author:** Bruno Reis  
📅 **Date:** August/2025  
