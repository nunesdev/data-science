# Feature Engineering & Data Transformation - Palmer Penguins

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/Library-Scikit--Learn-orange)
![Pandas](https://img.shields.io/badge/Library-Pandas-150458)
![Status](https://img.shields.io/badge/Status-Completed-green)

This project features a series of practical exercises focused on **Feature Engineering** and **Data Transformation** using the classic *Palmer Penguins* dataset. The primary goal was to apply linear algebra and statistical preprocessing concepts essential for building robust Machine Learning models.

Developed as part of the **Data Science & AI** degree program.

## 📌 Table of Contents
- [About the Project](#-about-the-project)
- [Topics Covered](#-topics-covered)
- [Key Insights](#-key-insights)
- [Technologies Used](#-technologies-used)
- [Skills Acquired](#-skills-acquired)

## 📖 About the Project
A Machine Learning model's performance often depends more on how the data is presented than on the algorithm itself. This repository documents the journey of transforming raw variables into optimized features, exploring everything from data discretization to advanced normalization and regularization techniques.

## 🧠 Topics Covered

The analysis was structured into 12 practical exercises covering:

1.  **ML Fundamentals:** Understanding features and their role in model performance.
2.  **Applied Linear Algebra:** Identifying scalars, vectors, and multi-dimensional spaces.
3.  **Discretization (Binning):** Fixed bins (`pd.cut`) vs. Variable/Quantile bins (`pd.qcut`).
4.  **Custom Transformations:** Using `FunctionTransformer` for personalized logic (Log, Inverse Exponential).
5.  **Distribution Handling:** Applying `PowerTransformer` (Yeo-Johnson) to achieve Gaussian distributions.
6.  **Scaling:** Practical comparison between `MinMaxScaler` and `StandardScaler`.
7.  **Regularization:** Implementing linear regression with **L2-Norm (Ridge)** to control overfitting.

## 🔍 Key Insights

* **Distribution vs. Scale:** While `StandardScaler` only centers the data, `PowerTransformer` changes the distribution shape, which is crucial for models assuming Gaussian priors.
* **Bin Balancing:** Variable binning proved superior for ensuring balanced groups, preventing the model from under-representing specific data ranges.
* **A "Common Language":** Min-Max normalization is indispensable for data visualization, allowing the comparison of distinct units (grams vs. millimeters) on a proportional plane.



## 🛠 Technologies Used

* **Language:** Python
* **Data Manipulation:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn
* **Visualization:** Matplotlib, Seaborn

## 🎓 Skills Acquired

* **Applied Statistics:** Ability to choose between parametric and robust transformations.
* **Preprocessing Pipelines:** Mastery of tools that integrate transformations into ML workflows.
* **Analytical Thinking:** Translating biological measurements into optimized mathematical vectors.

---
*Author: Bruno Nunes Reis*
