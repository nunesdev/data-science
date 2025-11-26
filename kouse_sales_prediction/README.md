# Data Quality Assessment - King County Housing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Library-Pandas-150458)
![Status](https://img.shields.io/badge/Status-Completed-green)

This project presents an in-depth data quality analysis of the **King County House Sales** dataset (`kc_house_data.csv`). The primary objective was to perform a technical diagnosis to identify statistical anomalies, logical inconsistencies, and integrity failures that could compromise future modeling.

Developed as part of the **Data Quality** course in the Data Science degree program at **Infnet**.

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Topics Covered](#-topics-covered)
- [Key Findings](#-key-findings)
- [Technologies Used](#-technologies-used)
- [Skills Acquired](#-skills-acquired)
- [Next Steps](#-next-steps)

## 📖 About the Project
Data quality is the foundation of any Data Science project. In this notebook, we go beyond simple exploration, applying rigorous validation techniques to ensure dataset reliability. The analysis focuses on distinguishing between natural market outliers and data entry errors or corruption.

## 🚀 Topics Covered

The analysis was structured around four main pillars:

1.  **Exploration & Typing:**
    * [cite_start]Initial assessment using `.info()` and `.describe()` to understand data structure[cite: 16].
    * [cite_start]Verification of expected vs. actual data types (e.g., handling dates stored as objects) [cite: 565-590].

2.  **Outlier Detection (Univariate):**
    * [cite_start]Comparative implementation of three statistical methods: **IQR** (Interquartile Range) [cite: 142][cite_start], **MAD** (Median Absolute Deviation) [cite: 161][cite_start], and **Z-Score**[cite: 174].
    * [cite_start]Creation of a sensitivity comparison table to evaluate how each method flags anomalies[cite: 215].

3.  **Logical Consistency (Business Rules):**
    * [cite_start]Domain validation (e.g., checking for non-positive prices)[cite: 275].
    * [cite_start]Temporal consistency (e.g., ensuring `yr_renovated` is not earlier than `yr_built`)[cite: 284].
    * [cite_start]Structural integrity (e.g., houses with 0 bedrooms or 0 bathrooms) [cite: 276-278].

4.  **Integrity & Visualization:**
    * [cite_start]Verification of unique primary keys (`id`) and duplicate handling[cite: 601].
    * [cite_start]Visual analysis using `pairplots`, `scatterplots`, and `countplots` to spot patterns and anomalies (like rare bedroom counts)[cite: 505, 560].

## 🔍 Key Findings

* [cite_start]**MAD Robustness:** The MAD method proved to be much more sensitive to the skewed nature of real estate data, detecting **3,095 outliers** for `sqft_lot` compared to only **347** detected by Z-Score [cite: 244-245].
* [cite_start]**Logical Inconsistencies:** We identified critical data entry errors, including **13 houses** recorded with 0 or fewer bedrooms [cite: 420] [cite_start]and **10 instances** where the renovation year was inconsistent with the construction year[cite: 424].
* [cite_start]**Duplicity:** The dataset contains **353 duplicate IDs**[cite: 654], suggesting resales or logging errors that require deduplication strategies.

## 🛠 Technologies Used

* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Visualization:** Seaborn, Matplotlib
* **Environment:** Deepnote / Jupyter Notebook

## 💡 Skills Acquired

* **Data Sanitization:** Ability to create complex boolean masks to filter "Dirty Data" based on logic rules.
* **Statistical Analysis:** Practical understanding of the differences between parametric (Z-score) and robust (MAD/IQR) statistics for anomaly detection.
* **Domain Validation:** Translating real-world business rules (real estate logic) into automated validation code.
* **Reporting:** Technical documentation of data issues, classifying them by severity and impact.

## 👣 Next Steps

Based on the diagnosis, the recommended actions for the project's evolution are:

1.  **ID Management:** Investigate the 353 duplicate IDs to decide between keeping the most recent record (representing a resale) or removing exact duplicates.
2.  **Type Correction:** Convert the `date` column to `datetime` format to enable proper time-series analysis.
3.  **Inconsistency Cleaning:** Remove or impute data for the properties with 0 bedrooms/bathrooms and correct the chronological renovation errors.
4.  **Feature Engineering:** Create new variables based on the cleaned data (e.g., `property_age`).

---
*Author: Bruno Nunes Reis*