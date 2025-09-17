# Spotify Dataset Analysis with Python

## 📌 Project Overview
This project explores a **Spotify dataset** using **Python, Pandas, and Matplotlib**.  
The main objective is to analyze track-level metadata, generate descriptive statistics, and visualize patterns in popularity, duration, danceability, loudness, keys, and genres.

The notebook applies a variety of techniques for exploratory data analysis (EDA), focusing on how musical features are distributed and related.

---

## 📊 Key Analyses Performed
1. **Bar Chart – Tracks per Genre**  
   - Counted total number of songs by `track_genre`.  
   - **Insight**: Shows genre representation in the dataset, highlighting balance or bias across categories.

2. **Line Plots with Subplots**  
   - Compared **average popularity** and **average track duration** (in minutes) across genres.  
   - **Insight**: Useful to contrast popularity trends with musical length.

3. **Distribution Analysis**  
   - **Histogram** of *danceability*.  
   - **Scatter plot** of *loudness vs. danceability*.  
   - **Insight**: Identified that loudness does not strongly correlate with danceability. Some extreme values may indicate anomalies or missing data.

4. **Proportions and Cyclical Data**  
   - **Pie chart** of musical keys distribution (`C, D, E, … B`).  
   - **Polar plot** of average danceability by musical key.  
   - **Insight**: Highlights tonal preferences and cyclical music patterns in the dataset.

5. **Aggregations with Pandas + Matplotlib**  
   - Bar chart of average *danceability* by musical key.  
   - Horizontal bar chart of average *energy* by genre.  
   - **Insight**: Combining Pandas and Matplotlib makes it easy to summarize and visualize key relationships.

---

## 🧠 Skills and Competencies Developed
- **Python for Data Analysis**
  - Data cleaning and preparation with Pandas.  
  - Feature engineering (mapping musical keys, converting duration to minutes).  

- **Data Visualization with Matplotlib**
  - Multiple chart types: bar, histogram, scatter, pie, polar.  
  - Subplots for comparative insights.  
  - Aesthetic adjustments (labels, titles, grids, rotations).  

- **Analytical Thinking**
  - Identification of patterns and anomalies (e.g., unusual loudness values).  
  - Cross-feature exploration (popularity vs. duration, loudness vs. danceability).  

- **Communication of Insights**
  - Clear, structured analysis with both quantitative and visual evidence.  

---

## 📂 Dataset
- **File:** `dataset.csv` (Spotify track-level data)  
- **Source:** [Kaggle – Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)  
- Contains information such as track ID, artist, genre, popularity, duration, energy, danceability, loudness, and musical key.  

---

## 🛠️ Tech Stack & Libraries
- [Python](https://www.python.org/) 🐍  
- [Pandas](https://pandas.pydata.org/) 📊  
- [NumPy](https://numpy.org/) 🔢  
- [Matplotlib](https://matplotlib.org/) 🎨  

---

✅ This README highlights the Python-based workflow, combining **data wrangling, visualization, and interpretation** into a structured portfolio project.
