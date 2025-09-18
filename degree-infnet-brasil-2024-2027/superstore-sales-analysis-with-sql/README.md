# Superstore Sales Analysis with SQL

## 📌 Project Overview
This project explores the **Superstore dataset** using advanced **SQL window functions and aggregations**.  
The main objective is to analyze profitability, customer behavior, and sales trends across categories, regions, and time using ranking functions, cumulative metrics, and moving averages.

The analysis demonstrates how SQL can be used not only for querying data but also for **complex business analytics**.

---

## 📊 Key Analyses Performed

### 1. Product and Customer Rankings
- **Ranking by Profit per Category (RANK, DENSE_RANK)**  
  - Compared ranking methods and explained differences in handling ties.  
- **Ranking Customers by Sales Quantity (ROW_NUMBER)**  
  - Sequential ranking of top buyers within each segment.

### 2. Sales and Profit Differences
- **Profit Difference per Order (LAG)**  
  - Measured change in profit between consecutive orders of the same customer.  
- **Quantity Difference per Order (LEAD)**  
  - Compared sales quantities between current and next orders.  
- **Detecting Large Fluctuations**  
  - Identified customers with order variations greater than 500 in sales, combining `LAG` and `LEAD`.

### 3. Moving Averages and Cumulative Sums
- **Moving Average of Profit by State**  
  - Rolling average of profit over the last 3 orders.  
- **Customer Sales in Last 4 Orders**  
  - Running sum of sales over a defined window.  
- **Cumulative Orders by Sub-Category**  
  - Tracked growth of orders over time.

### 4. Window Reuse for Efficiency
- Defined a reusable SQL window for ranking products by region and category.  
- Calculated `RANK`, `ROW_NUMBER`, and average discount in the same query.  
- **Benefit**: cleaner, more efficient, and easier to maintain queries.

### 5. Advanced Business Insights
- **Monthly Regional Sales Ranking**  
  - Identified top-performing regions each month.  
- **Customer Purchase History**  
  - Counted cumulative number of orders per customer.  
- **Top 5 Customers by Monthly Profit Growth**  
  - Detected customers with the largest profit increase compared to previous months.

---

## 🧠 Skills and Competencies Developed
- **SQL Advanced Analytics**
  - Ranking functions: `RANK`, `DENSE_RANK`, `ROW_NUMBER`.  
  - Time-series analysis with `LAG` and `LEAD`.  
  - Moving averages, cumulative counts, and rolling sums.  
  - Reusable `WINDOW` clauses for more efficient queries.  

- **Analytical Thinking**
  - Detecting anomalies in customer behavior (e.g., sudden sales spikes).  
  - Segmenting insights by **region, category, sub-category, and customer**.  
  - Turning raw transactional data into actionable business metrics.  

- **Data Communication**
  - Translating SQL outputs into **business insights**.  
  - Explaining differences between ranking approaches.  
  - Providing a clear narrative for decision-making.

---

## 📂 Dataset
- **File:** `superstoreutf8_.csv`  
- Contains order-level data including:  
  - **Sales, Profit, Discount, Quantity**  
  - **Customer, Segment, Region, State**  
  - **Category and Sub-Category**  
  - **Order Date**  

The dataset is commonly used in business intelligence and analytics training to simulate real-world retail operations.

---

## 🛠️ Tech Stack
- [SQL](https://en.wikipedia.org/wiki/SQL) 🗄️  
- Deepnote (SQL execution environment)  
- Window Functions, Aggregations, and CTEs  

---

✅ This README showcases **advanced SQL techniques** and how they can be applied for **business performance analysis, customer segmentation, and trend detection**.
