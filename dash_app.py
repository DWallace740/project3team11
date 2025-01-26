import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import sqlite3
import textwrap
import dash
from dash import dcc, html, Input, Output
import os

# Define the relative file path
file_path = os.path.join("Resources", "final2_cleaned_dataset.csv")

# Define the relative SQLite database path for deployment
db_file = "Resources/DW_cleaned_data.db"

# Connect to SQLite database (creates the file if it doesn't exist)
conn = sqlite3.connect(db_file)
cursor = conn.cursor()


# Define the table schema based on the dataset columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS health_data (
    Year INTEGER,
    Sex TEXT,
    Age TEXT,
    Grade TEXT,
    Race_Ethnicity TEXT,
    DataSource TEXT,
    Location TEXT,
    LocationID TEXT,
    LocationID_1 INTEGER,
    Geolocation TEXT,
    Topic TEXT,
    TopicID TEXT,
    Question TEXT,
    QuestionID TEXT,
    Value REAL,
    DataValueUnit TEXT,
    DataValueType TEXT,
    DataValueTypeID TEXT,
    LowConfidenceLimit REAL,
    HighConfidenceLimit REAL
)
''')

# Commit the table creation
conn.commit()

# Load data from the DataFrame into the SQLite table
data.to_sql('health_data', conn, if_exists='replace', index=False)

# Confirm data insertion by querying the database
row_count = cursor.execute('SELECT COUNT(*) FROM health_data').fetchone()[0]
print(f"Rows inserted into the database: {row_count}")

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Health Measures Dashboard"

# Connect to SQLite and load unique options for dropdowns
conn = sqlite3.connect(db_file)
topics = pd.read_sql_query('SELECT DISTINCT Topic FROM health_data', conn)['Topic'].tolist()
locations = pd.read_sql_query('SELECT DISTINCT Location FROM health_data', conn)['Location'].tolist()
years = pd.read_sql_query('SELECT DISTINCT Year FROM health_data', conn)['Year'].sort_values().tolist()
sexes = ['All'] + pd.read_sql_query('SELECT DISTINCT Sex FROM health_data', conn)['Sex'].tolist()
ages = ['All'] + pd.read_sql_query('SELECT DISTINCT Age FROM health_data', conn)['Age'].tolist()
races = ['All'] + pd.read_sql_query('SELECT DISTINCT "Race/Ethnicity" FROM health_data', conn)['Race/Ethnicity'].tolist()
conn.close()

# Define the app layout
app.layout = html.Div(style={"backgroundColor": "#f9f9f9", "fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[
    # App Title
    html.H1("Interactive Health Measures Dashboard", style={
        "textAlign": "center",
        "color": "#2c3e50",
        "fontWeight": "bold",
        "fontSize": "36px",
        "marginBottom": "10px"
    }),

    # Introduction Section
    html.Div([
        html.H3("Project 11 Team 3", style={"textAlign": "center", "color": "#2c3e50", "fontWeight": "bold"}),
        html.P(
            "Healthy Living, Diverse Challenges: Exploring Health Trends by Topic and Region",
            style={"textAlign": "center", "color": "#34495e", "fontSize": "18px", "marginBottom": "10px"}
        ),
        html.P(
            "This dashboard empowers users to uncover key health trends by exploring topics, regions," 
            "and demographics. Dive into interactive visualizations to identify patterns, reveal insights," 
            "and better understand the relationships between chronic diseases, health risks," 
            "and social determinants. Our mission: Make data-driven decision-making accessible" 
            "and impactful for all.",
            style={"textAlign": "center", "color": "#34495e", "fontSize": "16px", "marginBottom": "20px"}
        )
    ], style={"marginBottom": "30px"}),

    # Filters Section
    html.Div([
        html.Label("Select Topic:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="topic-dropdown", options=[{"label": t, "value": t} for t in topics], value=topics[0]),
        html.Label("Select Location:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="location-dropdown", options=[{"label": l, "value": l} for l in locations], value=locations[0]),
        html.Label("Select Year:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Slider(id="year-slider", min=min(years), max=max(years), step=1, value=min(years),
                   marks={year: str(year) for year in years})
    ], style={"width": "50%", "margin": "auto", "padding": "20px", "border": "1px solid #ddd", "borderRadius": "10px", "backgroundColor": "#ffffff"}),

    # Demographic Filters Section
    html.Div([
        html.Label("Select Sex:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="sex-dropdown", options=[{"label": s, "value": s} for s in sexes], value='All'),
        html.Label("Select Age:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="age-dropdown", options=[{"label": a, "value": a} for a in ages], value='All'),
        html.Label("Select Race/Ethnicity:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="race-dropdown", options=[{"label": r, "value": r} for r in races], value='All')
    ], style={"width": "50%", "margin": "auto", "padding": "20px", "border": "1px solid #ddd", "borderRadius": "10px", "backgroundColor": "#ffffff", "marginTop": "20px"}),

    # Graphs Section
    dcc.Graph(id="bar-chart"),
    dcc.Graph(id="choropleth-map"),
    dcc.Graph(id="line-chart"),
    dcc.Graph(id="scatter-plot"),
    dcc.Graph(id="top-questions-chart")
])

# Define callback to update visuals
@app.callback(
    Output("bar-chart", "figure"),
    Output("choropleth-map", "figure"),
    Output("line-chart", "figure"),
    Output("scatter-plot", "figure"),
    Output("top-questions-chart", "figure"),
    Input("topic-dropdown", "value"),
    Input("location-dropdown", "value"),
    Input("year-slider", "value"),
    Input("sex-dropdown", "value"),
    Input("age-dropdown", "value"),
    Input("race-dropdown", "value")
)
def update_visuals(selected_topic, selected_location, selected_year, selected_sex, selected_age, selected_race):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Build a base query
    query = f'''
    SELECT * FROM health_data
    WHERE Topic = "{selected_topic}" 
    AND Location = "{selected_location}" 
    AND Year = {selected_year}
    '''
    
    # Add demographic filters to the query
    if selected_sex != 'All':
        query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        query += f' AND "Race/Ethnicity" = "{selected_race}"'

    # Query the database
    data = pd.read_sql_query(query, conn)

    # Query for trends over time
    trend_query = f'''
    SELECT Year, AVG(Value) as AvgValue FROM health_data
    WHERE Topic = "{selected_topic}" AND Location = "{selected_location}"
    '''
    if selected_sex != 'All':
        trend_query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        trend_query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        trend_query += f' AND "Race/Ethnicity" = "{selected_race}"'
    trend_query += " GROUP BY Year"
    trend_data = pd.read_sql_query(trend_query, conn)

    # Query for top 10 questions
    top_questions_query = f'''
    SELECT Question, AVG(Value) as AvgValue FROM health_data
    WHERE Topic = "{selected_topic}"
    GROUP BY Question
    ORDER BY AvgValue DESC
    LIMIT 10
    '''
    top_questions_data = pd.read_sql_query(top_questions_query, conn)

    # Add line breaks to long question labels
    top_questions_data['Question'] = top_questions_data['Question'].apply(
        lambda q: "<br>".join(textwrap.wrap(q, width=40))
    )

    conn.close()

    # Create Visuals
    # Bar Chart
    bar_fig = px.bar(data, x="Question", y="Value", title=f"Bar Chart for {selected_topic} in {selected_location} ({selected_year})")
    bar_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        plot_bgcolor="#f9f9f9", paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Choropleth Map
    map_fig = px.choropleth(data, locations="LocationID", locationmode="USA-states", color="Value",
                            title="Geographic Distribution of Measures")
    map_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        geo=dict(bgcolor="#f9f9f9"),
        paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Line Chart
    line_fig = px.line(trend_data, x="Year", y="AvgValue", title=f"Trends for {selected_topic} in {selected_location}")
    line_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        plot_bgcolor="#f9f9f9", paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Scatterplot
    scatter_fig = px.scatter(data, x="LowConfidenceLimit", y="HighConfidenceLimit",
                              title="Correlation Between Confidence Limits")
    scatter_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        plot_bgcolor="#f9f9f9", paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Top 10 Questions Chart with Multi-Line Labels
    top_questions_fig = px.bar(
        top_questions_data,
        x="Question",
        y="AvgValue",
        title=f"Top 10 Questions for {selected_topic}",
        labels={"Question": "Questions", "AvgValue": "Average Value"}
    )
    top_questions_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        xaxis={"title": "Questions", "titlefont": {"size": 18, "color": "#34495e"}},
        yaxis={"title": "Average Value", "titlefont": {"size": 18, "color": "#34495e"}},
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    return bar_fig, map_fig, line_fig, scatter_fig, top_questions_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
