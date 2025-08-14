# 🏋️‍♂️ Data Analysis with Python – Gym Members

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
    - Used `.info()` to check null values and data types
    - Previewed samples with `.head()` and `.tail()`

3. **Descriptive statistics**
    - `.describe()` for numeric and categorical columns
    - Found most frequent values (`mode()`)

4. **Specific calculations**
    - 📅 **Average** number of training days per week
    - 🏃‍♂️ **Average** visits per week
    - 🎯 **Standard deviation** of age
    - 🥤 **Number** of different favorite drinks
    - 💪 **Most popular** group class

5. **Creation of summary DataFrame**
    - Focused on the most relevant variables:
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

## 🛠 Skills Acquired

| Skill Area                        | Description |
|-----------------------------------|-------------|
| **Data manipulation (Pandas)**   | CSV reading, inspection, filtering, and DataFrame creation |
| **Descriptive statistics**       | Calculating means, standard deviations, modes, counts |
| **Data cleaning & organization** | Identifying null values, fixing inconsistent types |
| **Analytical thinking**          | Interpreting metrics and defining relevant variables |
| **Documentation**                | Structuring code and recording analysis steps |

---

## 🚀 Next Steps
- 📊 Create visualizations with **Matplotlib** and **Seaborn**
- 📈 Analyze correlation between variables
- 🧠 Build a predictive model for customer retention
- 🔍 Segment customers based on behavior

---

💡 **Author:** Bruno Reis  
📅 **Date:** August/2025  
