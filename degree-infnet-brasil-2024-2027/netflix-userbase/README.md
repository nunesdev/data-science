# 📺 Netflix Subscribers – Data Analysis with Python

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)  
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-success?logo=pandas)](https://pandas.pydata.org/)  
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-orange?logo=plotly)](https://matplotlib.org/)  
[![Seaborn](https://img.shields.io/badge/Seaborn-Statistical%20Plots-blueviolet?logo=plotly)](https://seaborn.pydata.org/)  
[![Status](https://img.shields.io/badge/Status-Completed-brightgreen)](#)  

---

## 📂 Dataset

The dataset `dataset_netflix.csv` contains **2,500 subscribers**, with the following attributes:

- **User ID** → Unique subscriber identifier.  
- **Subscription Type** → Plan type (Basic, Standard, Premium).  
- **Monthly Revenue** → Monthly revenue per user.  
- **Join Date** → Date of subscription.  
- **Last Payment Date** → Date of last payment.  
- **Country** → Country of residence.  
- **Age** → User age.  
- **Gender** → User gender.  
- **Device** → Main access device (Laptop, Smartphone, Tablet, etc.).  
- **Plan Duration** → Duration of the subscription plan.  

---

## 🔍 Analysis Steps

1. **Initial Exploration**
   - Checked DataFrame size and structure (`.head()`, `.tail()`, `.info()`).
   - Descriptive statistics (`.describe()`) for numeric columns.

2. **Data Types & Cleaning**
   - Converted **date fields** (`Join Date`, `Last Payment Date`) to `datetime`.  
   - Converted **categorical fields** (`Subscription Type`, `Country`, `Gender`, `Device`, `Plan Duration`) to `category`.  
   - Improved efficiency and enabled temporal operations.

3. **Exploratory Analysis**
   - Histograms for **Monthly Revenue** distribution.  
   - Boxplot of **Age by Subscription Type**.  
   - Country-level analysis of subscribers.  
   - Pie chart for subscription type proportions.  
   - Scatter plot: **Age vs Monthly Revenue**.  

4. **Filtering & Business Scenarios**
   - Users with last payment **older than 6 months**.  
   - Simulation: **+10% revenue increase** for mobile users (Smartphone/Tablet).  
   - Reversion of modifications for testing scenarios.  

5. **Hierarchical Indexing**
   - MultiIndex created with **Country** and **Subscription Type** for drill-down queries.

6. **Aggregations**
   - Grouped by **Country & Subscription Type** → calculated **mean & median revenue**.  
   - Created **Age Groups (<18, 18–30, 31–45, 46–60, 60+)** to analyze behavior across generations.  
   - Simulated **Weekly Hours Watched** and applied engagement bonus for users ≤30 years old.

---

## 📊 Key Insights

| Area | Key Finding |
|------|-------------|
| **Revenue** | Values concentrated on discrete plan prices (10, 12, 15 USD). |
| **Age Profile** | Very similar distribution across plans – age is not a determinant factor in plan choice. |
| **Countries** | Clear concentration in certain regions (e.g., US, Spain, Canada). |
| **Devices** | Higher adoption of laptops, but mobile users were used for revenue simulation. |
| **Engagement** | 18–30 age group shows highest average watch hours. |

---

## 🛠 Skills Acquired

- **Data Wrangling**: Type conversion (dates, categories), filtering, cleaning.  
- **Descriptive Statistics**: Summary measures, mean, median, standard deviation.  
- **Visualization**: Histograms, boxplots, bar charts, scatter plots, pie charts.  
- **Indexing & Aggregation**: MultiIndex operations, groupby with aggregations.  
- **Business Simulation**: "What-if" analysis (mobile user revenue increase).  
- **Data Storytelling**: Communicating findings with charts and insights.  

---

## 🚀 Next Steps

- Build **dashboards** with interactive filters (by country, age group, device).  
- Expand with **time-series analysis** (subscription trends).  
- Integrate external datasets (e.g., content consumption) for richer insights.  
- Apply **predictive modeling** (churn prediction, lifetime value).  

---

✍️ Author: **Bruno Reis**  
📅 Date: September/2025  
