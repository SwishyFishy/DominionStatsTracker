from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import re

# Initialize webpage
app = Flask(__name__)

###################
# Query Functions #
###################

# Define useful shorthands
combined = "SELECT * FROM expanded_games as g LEFT JOIN player_went_first AS one ON g.g_id = one.game_id LEFT JOIN player_went_second AS two ON g.g_id = two.game_id LEFT JOIN player_went_third AS three ON g.g_id = three.game_id LEFT JOIN player_went_fourth AS four ON g.g_id = four.game_id"

# Return all games in a list
# Each list element is a dictionary representing 1 row that maps column name -> value
def get_games(api: sqlite3.Cursor) -> list[dict]:
    rows = api.execute("SELECT * FROM expanded_games AS g LEFT JOIN player_went_first AS one ON g.g_id = one.game_id LEFT JOIN player_went_second AS two ON g.g_id = two.game_id LEFT JOIN player_went_third AS three ON g.g_id = three.game_id LEFT JOIN player_went_fourth AS four ON g.g_id = four.game_id;").fetchall()
    column_names = [name[0] for name in api.description]
    data_dict = [dict(zip(column_names, row)) for row in rows]
    return data_dict

# Return all players and the number of games played in a list
# Each list element is a dictionary representing 1 row that maps column name -> value
def get_players(api: sqlite3.Cursor) -> list[dict]:
    players = api.execute(f"WITH combined AS ({combined}) SELECT name, COUNT(*) as games FROM combined CROSS JOIN players WHERE (name LIKE first_player_name OR name LIKE second_player_name OR name LIKE third_player_name OR name LIKE fourth_player_name) AND name NOT LIKE 'None' GROUP BY name").fetchall()
    column_names = [name[0] for name in api.description]
    player_dict = [dict(zip(column_names, player)) for player in players]
    return player_dict

# Return a list containing a passed player's wins and winrate
# Each list element is a dictionary representing 1 row that maps column name -> value
def get_player_wins(api: sqlite3.Cursor, player) -> list[dict]:
    rows = api.execute(f"WITH combined AS ({combined}) SELECT winner, COUNT(*) AS wins, printf('%.2f', COUNT(*) * 100.0 / (SELECT COUNT(*) FROM combined WHERE first_player_name LIKE '{player}' OR second_player_name LIKE '{player}' OR third_player_name LIKE '{player}' OR fourth_player_name LIKE '{player}')) as winrate FROM expanded_games WHERE winner LIKE '{player}'").fetchall()
    column_names = [name[0] for name in api.description]
    wins_dict = [dict(zip(column_names, row)) for row in rows]
    return wins_dict

# Return a list containing a passed player's wins and winrate from a passed position in turn order
# List element is a dictionary representing 1 row that maps column name -> value
def get_player_winrate_by_turn(api: sqlite3.Cursor, player, position) -> list[dict]:
    select = "first_player_name"
    
    match position:
        case 2:
            select = "second_player_name"
        case 3:
            select = "third_player_name"
        case 4:
            select = "fourth_player_name"

    rows = api.execute(f"WITH combined AS ({combined}) SELECT {select}, winner, COUNT(*) AS wins, (SELECT COUNT(*) from combined WHERE {select} LIKE '{player}') AS games, printf('%.2f', COUNT(*) * 100.0 / (SELECT COUNT(*) from combined WHERE {select} LIKE '{player}')) AS percentage FROM combined WHERE {select} LIKE '{player}' AND winner LIKE '{player}' GROUP BY winner;").fetchall()
    column_names = [name[0] for name in api.description]
    winrates_dict = [dict(zip(column_names, row)) for row in rows]
    return winrates_dict

#########
# Pages #
#########

# Define webpage home
@app.route('/')
def home():

    # Open database connection
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()

    # Get data
    data_dict = get_games(api)
    player_dict = get_players(api)

    stats = dict(
        wins = [get_player_wins(api, player['name']) for player in player_dict],
        positional_winrates = [(get_player_winrate_by_turn(api, player['name'], position), player, position) for player in player_dict for position in range(1, 5)]
    )
    
    # Close the database connection
    db.close()

    # Render homepage using most current data
    return render_template("home.jinja", zip = zip, PASSED_data = data_dict, PASSED_players = player_dict, PASSED_stats = stats)

# Define game submission handler
@app.route('/newgame', methods=['POST'])
def newgame():

    # Extract data
    p1 = request.form['p1']
    p2 = request.form['p2']
    p3 = request.form['p3']
    p4 = request.form['p4']
    p1_t1 = request.form['p1_t1']
    p1_t2 = request.form['p1_t2']
    p2_t1 = request.form['p2_t1']
    p2_t2 = request.form['p2_t2']
    p3_t1 = request.form['p3_t1']
    p3_t2 = request.form['p3_t2']
    p4_t1 = request.form['p4_t1']
    p4_t2 = request.form['p4_t2']
    p1_score = request.form['p1_score']
    p2_score = request.form['p2_score']
    p3_score = request.form['p3_score']
    p4_score = request.form['p4_score']
    winner = request.form['winner']
    end = request.form['end_condition']
    ktype = request.form['kingdom_type']
    notes = request.form['notes']
    sets = request.form['sets']
    
    # Sort the sets into alphabetical order for consistency in the database
    sets = ' + '.join(sorted(sets.split(' + ')))

    # Connect to database
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()

    # Insert new game record
    try:

        # Define REGEXP function for python
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.match(item) is not None
        db.create_function("REGEXP", 2, regexp)

        # Add to database
        api.execute("INSERT INTO expanded_games VALUES (NULL, ?, ?, ?, ?, ?, ?);", [2 + ((2 if p4 != '' else 1) if p3 != '' else 0), winner, end, ktype, notes, sets])
        rowid = api.lastrowid
        api.execute("INSERT INTO player_went_first VALUES (?, ?, ?, ?, ?);", [rowid, p1, p1_score, p1_t1, p1_t2])
        api.execute("INSERT INTO player_went_second VALUES (?, ?, ?, ?, ?);", [rowid, p2, p2_score, p2_t1, p2_t2])
        if p3 != '':
            api.execute("INSERT INTO player_went_third VALUES (?, ?, ?, ?, ?);", [rowid, p3, p3_score, p3_t1, p3_t2])
        if p4 != '':
            api.execute("INSERT INTO player_went_fourth VALUES (?, ?, ?, ?, ?);", [rowid, p4, p4_score, p4_t1, p4_t2])

        db.commit()

    except sqlite3.Error as e:
        return str(e)
    
    # Always close the database connection
    finally:
        db.close()
    
    # Return to the homepage
    return redirect(url_for('home'))

@app.route('/delete/<row>')
def delete(row):

    # Connect to the database
    db = sqlite3.connect("dominionstats.db")
    api = db.cursor()

    try:
        api.execute("DELETE FROM expanded_games WHERE g_id = ?", [row])

        db.commit()

    except sqlite3.Error as e:
        return str(e)
    
    # Always close the database connection
    finally:
        db.close()

    # Return to the homepage
    return redirect(url_for('home'))

@app.route('/error')
def error():
    return "Error"

# Start webpage
if __name__ == '__main__':
    app.run(debug = True)