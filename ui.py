from flask import Flask, request, render_template, redirect, url_for
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
    
    # Close the database connection
    db.close()

    # Insert row data into labelled dictionary
    column_names = [name[0] for name in api.description]
    data_dict = [dict(zip(column_names, row)) for row in rows]
    #return data_dict

    # Render homepage using most current data
    return render_template("home.jinja", PASSED_data = data_dict)

# Define game submission page
@app.route('/newgame', methods=['POST'])
def newgame():

    # Extract data
    p1 = request.form['player1']
    p2 = request.form['player2']
    p1_t1 = request.form['player1_t1_coin']
    p1_t2 = request.form['player1_t2_coin']
    p2_t1 = request.form['player2_t1_coin']
    p2_t2 = request.form['player2_t2_coin']
    p1_score = request.form['player1_score']
    p2_score = request.form['player2_score']
    winner = request.form['winner']
    end = request.form['end_condition']
    ktype = request.form['kingdom_type']
    notes = request.form['sets']

    # Connect to database
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()

    # Insert new game record
    try:
        api.execute("INSERT INTO games VALUES(NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [p1, p2, p1_score, p2_score, winner, p1_t1, p1_t2, p2_t1, p2_t2, end, ktype, notes])
        db.commit()
    except sqlite3.Error as e:
        return redirect(url_for('error'))

    # Close the database connection
    db.close()
    
    # Return to the homepage
    return redirect(url_for('home'))

@app.route('/error')
def error():
    return "Error"

# Start webpage
if __name__ == '__main__':
    app.run(debug = True)