from flask import Flask, render_template
import sqlite3

# Initialize webpage
app = Flask(__name__)

# Define webpage home
@app.route('/')
def home():

    # Get data
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()
    rows = api.execute("SELECT * FROM games;").fetchall()

    # Insert row data into labelled dictionary
    column_names = [name[0] for name in api.description]
    data_dict = [dict(zip(column_names, row)) for row in rows]
    #return data_dict

    # Render homepage using most current data
    return render_template("home.htmlj2", PASSED_data = data_dict)

# Start webpage
if __name__ == '__main__':
    app.run(debug = True)