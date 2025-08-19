# Student Performance Analysis with SQL

## 📌 Project Overview

This project explores the **Students Performance dataset** using **SQL queries**.
The main goal is to analyze students’ performance across **Math, Reading, and Writing scores**, segmenting results into performance ranges, and identifying patterns by demographics and preparation courses.

The analysis was conducted inside a SQL environment connected to the dataset, with queries designed to generate meaningful aggregations and comparisons.

---

## 📊 Key Analyses Performed

1. **Math Score Distribution**

   * Created manual bins: `0–40`, `41–70`, `71–100`.
   * Counted the number of students in each bin.
   * **Insight**: Most students fall between 41–70 points.

2. **Cross-Subject Performance**

   * Calculated average Reading and Writing scores for each Math range.
   * **Insight**: Higher math performance correlates with better reading and writing outcomes.

3. **Reading Score Segmentation**

   * Created bins for Reading (`0–50`, `51–80`, `81–100`).
   * Compared distributions overall and by **gender**.
   * **Insight**: Female students show stronger representation in the top reading category.

4. **Parental Education and Ethnicity**

   * Counted distinct categories for **parental education** and **ethnicity**, highlighting dataset diversity.

5. **Writing Score Segmentation**

   * Similar binning strategy for Writing scores.
   * Reinforced performance consistency across skills.

6. **Impact of Test Preparation Course**

   * Compared students who **completed** the preparation course vs. those with **none**.
   * Metrics calculated:

     * Average scores (Math, Reading, Writing)
     * Score ranges (max – min)
   * **Insight**: Preparation courses positively impact student performance.

---

## 📈 Visualizations

Some complementary Python visualizations were created using **Matplotlib**:

* Distribution of Math Scores
* Average Reading & Writing by Math Score Range
* Reading Distribution by Gender
* Writing Score Distribution
* Boxplot: Math Scores vs. Test Preparation Course

(Plots are stored in the repository inside the `figures/` folder.)

---

## 🧠 Skills and Competencies Developed

* **SQL Data Exploration**

  * Use of `CASE WHEN` for manual binning of continuous variables.
  * Grouping with `GROUP BY` and aggregations (`COUNT`, `AVG`, `MAX`, `MIN`).
  * Filtering and ordering results for interpretability.

* **Analytical Thinking**

  * Designing meaningful score ranges to capture performance levels.
  * Cross-analysis between subjects and demographics.
  * Extracting insights about the role of preparation courses.

* **Data Communication**

  * Translating raw query results into **interpretable summaries**.
  * Structuring results for visualization and reporting.

---

## 📂 Dataset

* **File:** `StudentsPerformance.csv`
* **Source:** [Kaggle – Students Performance in Exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams?resource=download)
* Contains demographic information and scores for **Math, Reading, and Writing**.
* Widely used for educational performance analysis.

---

