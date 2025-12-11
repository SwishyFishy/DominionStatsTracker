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
    rows = api.execute("SELECT * FROM expanded_games AS g LEFT JOIN player_went_first AS one ON g.g_id = one.g_id LEFT JOIN player_went_second AS two ON g.g_id = two.g_id LEFT JOIN player_went_third AS three ON g.g_id = three.g_id LEFT JOIN player_went_fourth AS four ON g.g_id = four.g_id;").fetchall()
    column_names = [name[0] for name in api.description]
    data_dict = [dict(zip(column_names, row)) for row in rows]

    players = api.execute("SELECT name FROM players WHERE name NOT LIKE 'no winner';").fetchall()
    column_names = [name[0] for name in api.description]
    player_dict = [dict(zip(column_names, player)) for player in players]
    
    # Close the database connection
    db.close()

    #return data_dict
    #return players

    # Render homepage using most current data
    return render_template("home.jinja", PASSED_data = data_dict, PASSED_players = player_dict)

# Define game submission handler
@app.route('/newgame', methods=['POST'])
def newgame():

    # Extract data
    num_players = request.form['num_players']
    p1 = request.form['player1']
    p2 = request.form['player2']
    p3 = request.form['player3']
    p4 = request.form['player4']
    p1_t1 = request.form['player1_t1_coin']
    p1_t2 = request.form['player1_t2_coin']
    p2_t1 = request.form['player2_t1_coin']
    p2_t2 = request.form['player2_t2_coin']
    p3_t1 = request.form['player3_t1_coin']
    p3_t2 = request.form['player3_t2_coin']
    p4_t1 = request.form['player4_t1_coin']
    p4_t2 = request.form['player4_t2_coin']
    p1_score = request.form['player1_score']
    p2_score = request.form['player2_score']
    p3_score = request.form['player3_score']
    p4_score = request.form['player4_score']
    winner = request.form['winner']
    end = request.form['end_condition']
    ktype = request.form['kingdom_type']
    notes = request.form['notes']
    sets = request.form['sets']

    # Connect to database
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()

    # Insert new game record
    try:
        api.execute("INSERT INTO expanded_games VALUES (NULL, ?, ?, ?, ?, ?, ?);", [num_players, winner, end, ktype, notes, sets])
        rowid = api.lastrowid
        api.execute("INSERT INTO player_went_first VALUES (?, ?, ?, ?, ?);", [rowid, p1, p1_score, p1_t1, p1_t2])
        api.execute("INSERT INTO player_went_second VALUES (?, ?, ?, ?, ?);", [rowid, p2, p2_score, p2_t1, p2_t2])
        api.execute("INSERT INTO player_went_third VALUES (?, ?, ?, ?, ?);", [rowid, p3, p3_score, p3_t1, p3_t2])
        api.execute("INSERT INTO player_went_fourth VALUES (?, ?, ?, ?, ?);", [rowid, p4, p4_score, p4_t1, p4_t2])

        db.commit()

    except sqlite3.Error:
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