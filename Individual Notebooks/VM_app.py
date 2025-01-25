import sqlite3
import json
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Database connection function
def get_filtered_data_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('../Resources/U.S._Chronic_Disease_Indicators_2.sqlite')
    cursor = conn.cursor()

    # Define the specific questions you want to filter by
    questions_to_filter = (
        'Current cigarette smoking among adults',
        'Chronic obstructive pulmonary disease among adults'
    )

    # Modify the query to filter by specific questions
    query = f"""
    SELECT Year, Value, Question
    FROM `U.S._Chronic_Disease_Indicators`
    WHERE Question IN ({', '.join(['?' for _ in questions_to_filter])})
    """
    cursor.execute(query, questions_to_filter)

    # Fetch all the data from the query result
    data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data into a list of dictionaries
    result = []
    for row in data:
        result.append({
            'Year': row[0],  # Year column from DB
            'COPD_Prevalence': row[1],  # Value column from DB
            'Category': row[2]  # Question column from DB
        })

    return result

# Route to serve the data as JSON
@app.route('/data')
def get_data():
    data = get_filtered_data_from_db()  # Get filtered data from the database
    return jsonify(data)  # Convert Python data to JSON and send it to the frontend

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
