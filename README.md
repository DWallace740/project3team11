# Healthy Living, Diverse Challenges: Exploring Health Trends by Topic and Region

## Overview

This project is a comprehensive data visualization initiative focused on chronic disease trends. By leveraging an interactive Dash web application and SQLite for database integration, we aim to provide an intuitive platform for exploring key health topics, uncovering patterns, and facilitating informed decision-making. The project combines data analysis with interactive visualizations to highlight the relationships between chronic diseases, demographic factors, and lifestyle risks.

### Key Research Questions

1. **How do health issues and their key measures, including risk factors, compare across topics, and what patterns or differences emerge in their importance and connections?**
2. **How does smoking status correlate with the prevalence of COPD?**
3. **How do cardiovascular disease rates differ across gender, age, and lifestyle factors like diet and exercise?**

---

## Instructions

### **Clone the Repository**
1. Clone this repository to your local machine:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

### **Install Dependencies**
2. Ensure Python is installed on your machine. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

### **Set Up the SQLite Database**
3. Initialize the database with the provided dataset by running:
   ```bash
   python setup_database.py
   ```

### **Run the Application**
4. Start the Dash application to interact with the visualizations:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:8050`.

---

## Features



## Data Analysis

### Key Insights

1. **Health Issues Across Topics**:
   - Analysis of average values across health topics revealed significant disparities in key measures like risk factors and prevalence rates.
   - Bar charts highlighted topics with higher average values, allowing users to identify areas requiring more attention.

2. **Smoking Status and COPD**:
   - Scatter plots demonstrated a strong correlation between smoking status and COPD prevalence.
   - This finding emphasizes the importance of anti-smoking campaigns in reducing COPD-related health burdens.

3. **Cardiovascular Disease and Lifestyle Factors**:
   - Using bubble charts and filters, we explored how cardiovascular disease rates differ across demographic factors such as gender and age.
   - Key lifestyle indicators like diet and exercise were visually analyzed, revealing actionable insights for public health interventions.

4. **Comparative Analysis of Topics and Questions**:
   - The heatmap visualization allowed a high-level overview of how health measures differ across top topics and questions.
   - This tool helped identify patterns and focus areas for further investigation.

### Statistical Preprocessing

- The "Value" column was normalized to ensure consistency across all visualizations.
- Outliers were identified and treated appropriately to prevent skewed results.
- Data aggregation techniques (e.g., grouping by topic and averaging) were applied to simplify and enhance interpretability of results.

---

- **Dynamic Visualizations**:
  - **Bar Chart**: Average values by health topics.
  - **Bubble Chart**: Relationship between topics and average values.
  - **Scatter Plot**: Trends for specific questions and topics.
  - **Heatmap**: Comparative analysis of top topics and questions.
- **User Interaction**:
  - Dropdown menus and filters for customized data exploration.
  - Fully interactive charts using Dash and Plotly.js.
- **Database Integration**:
  - The dataset is stored and accessed using SQLite, ensuring efficient and reliable data handling.

---

## Ethical Considerations

- **Data Privacy**: The dataset has been anonymized, ensuring that no personally identifiable information is present.
- **Accuracy and Integrity**: Data preprocessing was conducted to ensure consistency and prevent misrepresentation.
- **Accessibility**: The application is designed to be intuitive for a wide range of users, regardless of their technical background.
- **Transparency**: Full documentation of data sources and external code is included to ensure reproducibility.

---

## Handling Mixed Data Types

One challenge encountered was the "Value" column in the dataset, which contained mixed data types (e.g., integers and floats). To address this, we:
- Preprocessed and standardized the column values to ensure uniformity.
- Applied rigorous cleaning techniques to facilitate accurate analysis and visualization.

This preprocessing step ensures the reliability of all visualizations.

---

## Resources Used

- **ChatGPT (AI Assistant)**: Assisted with structuring code, debugging, analyzing data, and formatting this document.
- **Xpert Learning Assistant**: Provided additional support for understanding web scraping and data analysis concepts.
- **Pandas Documentation**: Helped with DataFrame manipulations and data cleaning.
- **Dash and Plotly Documentation**: Used for building interactive visualizations.
- **SQLite Documentation**: Assisted with setting up and managing the SQLite database.
- **BeautifulSoup Documentation**: Used for extracting HTML content (if applicable).
- **Splinter Documentation**: Provided automated browsing and HTML rendering guidance (if applicable).

---

## References

### **Data Source**
- The dataset was sourced from the [CDC Chronic Disease Indicators](https://chronicdata.cdc.gov/).

### **Code References**
- Dash and Plotly documentation: [Dash Docs](https://dash.plotly.com/), [Plotly Docs](https://plotly.com/python/)
- SQLite database setup: [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## About the Team

This project was collaboratively developed by:

- **Victoria Mendez**
- **Daena Wallace**
- **Avery Javier**

Our goal is to highlight critical health trends and empower users to derive actionable insights from the data.

This project was collaboratively developed as part of a data visualization track. Our goal is to highlight critical health trends and empower users to derive actionable insights from the data.

