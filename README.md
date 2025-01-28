# Healthy Living, Diverse Challenges: Exploring Health Trends by Topic and Region

## Overview

This project explores health trends across chronic diseases, demographic factors, and lifestyle risks using interactive visualizations and a centralized dataset. It is designed for both technical and non-technical users, offering insights into the interconnectedness of health issues and their contributing factors.

### Purpose 
The primary goal of this project is to:

- Identify patterns and connections in health data.
- Provide actionable insights into risk factors and outcomes for chronic diseases.
- Offer an interactive, user-friendly dashboard to analyze key measures.

---

### Key Research Questions

1. **How do health issues and their key measures, including risk factors, compare across topics?**
2. **How does smoking affect the risk of developing chronic obstructive pulmonary disease (COPD)?**
3. **How do cardiovascular disease rates differ across gender, age?**

---

### Getting Started
This repository contains all the necessary files for exploring the project. Depending on your technical expertise, you can either:

- Use the presentation to understand the key findings visually.
- Run the Dash app for an interactive exploration of the dataset.
- Use the HTML visualization for a spatial view of health trends.
- Analyze the dataset using the Jupyter notebook.

## Project Features 
1. Presentation 
 - Summarizes major health trends. 
 - Provides visual insights into COPD
 - Explains key findins without requiring techinical skills. 

2. Interactive Dashboard (Project)
Built with Dash and Plotly.
Connects to an SQLite database for dynamic data querying.
Allows users to filter by topic, location, demographic factors (age, sex, race), and time.

 - Visualizes data through:
 - Bar charts (health data by location).
 - Line charts (trends over time).
 - Scatterplots (correlation between confidence limits).
 - Top 10 metric rankings.

3. Choropleth Map (final_test_index.html)
Displays health trends geographically using Leaflet.js.
Users can filter age groups and gender distributions across states.
Pulls data from GeoJSON format, allowing an interactive exploration of health disparities.

4. Data Analysis (Project3_Group11_Notebook.ipynb)
Exploratory Data Analysis (EDA) for chronic disease trends.
Data cleaning steps applied before visualization.
Uses pandas, matplotlib, seaborn, and SQLite for structured analysis

---
## **Technical Details**
### **Tech Stack**
- **Backend**: Python, SQLite
- **Frontend**: Dash, Plotly, HTML, Leaflet.js
- **Database**: SQLite
- **Data Source**: [CDC Chronic Disease Indicators](https://chronicdata.cdc.gov/

### **Repository Structure**
```
├── Individual Notebooks/          # Contains Jupyter notebooks for analysis
├── Output/                        # Processed data and visualization outputs
├── Resources/                     # Raw dataset, database files
├── html_visualization/            # Choropleth map files
│   ├── index.html                 # File used for interactive visual on live server
│   ├── geojson_data_json_format.js
│   ├── raw_json_data.js
│   ├── style.css
├── Project3_Group11_Notebook.ipynb  # Jupyter notebook for data analysis and dash app
├── README.md                        # Project documentation
├── requirements.txt                 # Dependencies
├── Project3_11_Presentation.pdf     # PDF File of Presentation Slides 
├── .gitignore                       # Git ignore rules
```

---
## **Installation & Setup**
1. **Clone the Repository**
   ```bash
   git clone https://github.com/DWallace740/project3team11.git
   cd project3team11
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Dash App**
   ```bash
   python dash_app.py
   ```
   - Open a web browser and go to **`http://127.0.0.1:8050/`** to view the dashboard.

5. **Open the Choropleth Map**
   - Navigate to `html_visualization/index.html` and open with a live server in VS Code to display in web browser.

---
## Data Analysis
### Data Cleaning Process
- Removed unnecessary columns and duplicate values to streamline the dataset.
- Standardized age, gender, and demographic categories for consistency.
- Reorganized data structure to enhance querying efficiency.
- Stored the cleaned dataset in SQLite for faster access and better integration with the dashboard.

- A more detailed breakdown of the cleaning process is available in the presentation slides.

### **Key Findings**
- **Health Variations**: Health issues exhibit significant variation across topics, with clear connections between lifestyle risks and chronic diseases like obesity, diabetes, and cardiovascular disease.
- **Smoking and COPD**: Smoking is a primary driver of COPD risk and progression, disproportionately impacting older adults and women.
- **Cardiovascular Disease Trends**: Cardiovascular disease rates vary across gender and age, highlighting the importance of targeted interventions for at-risk groups.

### **Takeaways**
- Chronic diseases are interconnected with social determinants and lifestyle factors.
- Preventive measures and public health campaigns can significantly reduce risks and improve outcomes.

For a full summary, refer to the **presentation**.

---

## Ethical Considerations

- **Data Privacy**: The dataset has been anonymized, ensuring that no personally identifiable information is present.
- **Accuracy and Integrity**: Data preprocessing was conducted to ensure consistency and prevent misrepresentation.
- **Transparency**: Full documentation of data sources and external code is included to ensure reproducibility.

---

## Resources Used

- **ChatGPT (AI Assistant)**: Assisted with structuring code, debugging, analyzing data, and formatting this document.
- **Xpert Learning Assistant**: Provided additional support for understanding data analysis concepts.
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

- This project was collaboratively developed as part of a data visualization track.
---

## **License**
This project is licensed under the **MIT License**.
