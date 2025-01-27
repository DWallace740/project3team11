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
data = pd.read_csv(file_path)

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
# Initialize Dash app
app = dash.Dash(__name__)
server = app.server
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
    html.H3("Project 11 Team 3", style={
        "textAlign": "center", 
        "color": "#2c3e50", 
        "fontWeight": "bold", 
        "fontSize": "24px"
    }),
    html.P(
        "Healthy Living, Diverse Challenges: Exploring Health Trends by Topic and Region",
        style={
            "textAlign": "center", 
            "color": "#DA70D6", 
            "fontSize": "18px", 
            "marginBottom": "10px", 
            "fontWeight": "bold"
        }
    ),
   
    html.H4("Overview of the Visualizations", style={
        "textAlign": "center", 
        "color": "#4B0082", 
        "fontWeight": "bold", 
        "marginTop": "20px", 
        "fontSize": "20px"
    }),
    html.P(
        "This dashboard provides a series of interactive charts that illustrate key trends, correlations, and "
        "comparisons related to Social Determinants of Health. Each chart dynamically updates based on the filters "
        "applied, offering a tailored analysis of the selected dataset. Below is a breakdown of what each chart represents:",
        style={
            "textAlign": "left", 
            "color": "#34495e", 
            "fontSize": "18px", 
            "marginBottom": "20px"
        }
    ),
    html.Ul([
        html.Li([
            html.Span("Average Values by Location: ", style={"fontWeight": "bold"}), 
            "This bar chart displays the average values"
            "for the selected topic across different locations (e.g., states or territories). "
            "It helps compare geographic variations and identify areas"
            " with higher or lower averages for specific social determinants."
        ], style={"textAlign": "left", "marginBottom": "10px"}),
        html.Li([
            html.Span("Trends Over Time: ", style={"fontWeight": "bold"}), 
            "The line chart illustrates how the average values change over time. This visualization helps identify patterns, improvements, "
            "or declines for the selected topic over multiple years."
        ], style={"textAlign": "left", "marginBottom": "10px"}),
        html.Li([
            html.Span("Correlation Between Confidence Limits: ", style={"fontWeight": "bold"}), 
            "The scatterplot shows the relationship between the high and low confidence limits for the data. It highlights the consistency "
            "or variability within the dataset and may indicate trends in data reliability."
        ], style={"textAlign": "left", "marginBottom": "10px"}),
        html.Li([
            html.Span("Top 10 Metrics for Social Determinants: ", style={"fontWeight": "bold"}), 
            "This bar chart ranks the top 10 metrics or questions with the highest average values. It provides insight into the most prominent "
            "or impactful factors within the dataset."
        ], style={"textAlign": "left", "marginBottom": "10px"}),
        html.Li([
            html.Span("Filter Panel: ", style={"fontWeight": "bold"}), 
            "The filter panel allows users to narrow the scope of the visualizations by selecting specific years, demographic variables (e.g., age, sex, race/ethnicity), "
            "and topics. This helps customize the analysis to suit specific areas of interest."
        ], style={"textAlign": "left", "marginBottom": "10px"})
    ], style={
        "fontSize": "15px", 
        "color": "#34495e", 
        "marginBottom": "20px", 
        "paddingLeft": "0px", 
        "listStyleType": "none"
    }),
    html.H4("Important Notes on Filters", style={
        "textAlign": "center", 
        "fontWeight": "bold", 
        "color": "#4B0082", 
        "marginTop": "20px", 
        "fontSize": "20px"
    }),
    html.Ul([
        html.Li("Applying more than two filters may result in no data being displayed.", 
                style={"marginBottom": "15px", "textAlign": "center"}),
        html.Li("Start with one or two filters for broader insights, then refine further.", 
                style={"marginBottom": "15px", "textAlign": "center"}),
    ], style={
        "fontSize": "14px", 
        "color": "#4B0082", 
        "marginBottom": "20px", 
        "paddingLeft": "0px", 
        "listStyleType": "none"
    })
], style={"marginBottom": "30px"}),

    # Filters Section
    html.Div([
        html.Label("Select Topic:", style={"fontWeight": "bold", "color": "#2c3e50"}),
        dcc.Dropdown(id="topic-dropdown", options=[{"label": t, "value": t} for t in topics], value=topics[0]),
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
    dcc.Graph(id="location-bar-chart"),
    dcc.Graph(id="line-chart"),
    dcc.Graph(id="scatter-plot"),
    dcc.Graph(id="top-questions-chart")
])

# Define callback to update visuals
@app.callback(
    Output("location-bar-chart", "figure"),
    Output("line-chart", "figure"),
    Output("scatter-plot", "figure"),
    Output("top-questions-chart", "figure"),
    Input("topic-dropdown", "value"),
    Input("year-slider", "value"),
    Input("sex-dropdown", "value"),
    Input("age-dropdown", "value"),
    Input("race-dropdown", "value")
)
def update_visuals(selected_topic, selected_year, selected_sex, selected_age, selected_race):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)

    # Query for location values
    location_query = f'''
    SELECT Location, AVG(Value) as AvgValue FROM health_data
    WHERE Topic = "{selected_topic}" AND Year = {selected_year}
    '''
    if selected_sex != 'All':
        location_query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        location_query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        location_query += f' AND "Race/Ethnicity" = "{selected_race}"'
    location_query += ' GROUP BY Location ORDER BY AvgValue DESC'

    location_data = pd.read_sql_query(location_query, conn)

    # Query for trends over time
    trend_query = f'''
    SELECT Year, AVG(Value) as AvgValue FROM health_data
    WHERE Topic = "{selected_topic}"
    '''
    if selected_sex != 'All':
        trend_query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        trend_query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        trend_query += f' AND "Race/Ethnicity" = "{selected_race}"'
    trend_query += ' GROUP BY Year'

    trend_data = pd.read_sql_query(trend_query, conn)

    # Query for scatterplot (High and Low Confidence Limits)
    scatter_query = f'''
    SELECT LowConfidenceLimit, HighConfidenceLimit FROM health_data
    WHERE Topic = "{selected_topic}" AND Year = {selected_year}
    '''
    if selected_sex != 'All':
        scatter_query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        scatter_query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        scatter_query += f' AND "Race/Ethnicity" = "{selected_race}"'

    scatter_data = pd.read_sql_query(scatter_query, conn)

    # Query for top 10 questions
    top_questions_query = f'''
    SELECT Question, AVG(Value) as AvgValue FROM health_data
    WHERE Topic = "{selected_topic}"
    '''
    if selected_sex != 'All':
        top_questions_query += f' AND Sex = "{selected_sex}"'
    if selected_age != 'All':
        top_questions_query += f' AND Age = "{selected_age}"'
    if selected_race != 'All':
        top_questions_query += f' AND "Race/Ethnicity" = "{selected_race}"'
    top_questions_query += ' GROUP BY Question ORDER BY AvgValue DESC LIMIT 10'

    top_questions_data = pd.read_sql_query(top_questions_query, conn)

    # Add line breaks to long question labels
    top_questions_data['Question'] = top_questions_data['Question'].apply(
        lambda q: "<br>".join(textwrap.wrap(q, width=40))
    )

    conn.close()


    # Create Visuals
    # Bar Chart for Locations
    location_bar_fig = px.bar(
        location_data,
        x="Location",
        y="AvgValue",
        title=f"Average Values by Location for {selected_topic} ({selected_year})",
        labels={"Location": "Location", "AvgValue": "Average Value"}
    )
    location_bar_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        xaxis_tickangle=-45,
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Line Chart
    line_fig = px.line(trend_data, x="Year", y="AvgValue", title=f"Trends for {selected_topic}")
    line_fig.update_layout(
        title={"x": 0.5, "font": {"size": 24, "color": "#2c3e50"}},
        plot_bgcolor="#f9f9f9", paper_bgcolor="#ffffff",
        font={"family": "Arial", "color": "#2c3e50"}
    )

    # Scatterplot for Confidence Limits
    scatter_fig = px.scatter(scatter_data, x="LowConfidenceLimit", y="HighConfidenceLimit",
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

      # Create visuals with "No data available" placeholders
    if location_data.empty:
        location_bar_fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            showarrow=False,
            font={"size": 20}
        )
    else:
        location_bar_fig = px.bar(
            location_data,
            x="Location",
            y="AvgValue",
            title=f"Average Values by Location for {selected_topic} ({selected_year})"
        )

    if trend_data.empty:
        line_fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            showarrow=False,
            font={"size": 20}
        )
    else:
        line_fig = px.line(trend_data, x="Year", y="AvgValue", title=f"Trends for {selected_topic}")

    if scatter_data.empty:
        scatter_fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            showarrow=False,
            font={"size": 20}
        )
    else:
        scatter_fig = px.scatter(scatter_data, x="LowConfidenceLimit", y="HighConfidenceLimit",
                                  title="Correlation Between Confidence Limits")

    if top_questions_data.empty:
        top_questions_fig = go.Figure().add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            showarrow=False,
            font={"size": 20}
        )
    else:
        top_questions_fig = px.bar(
            top_questions_data,
            x="Question",
            y="AvgValue",
            title=f"Top 10 Questions for {selected_topic}"
        )

    return location_bar_fig, line_fig, scatter_fig, top_questions_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


