""" Render_template = renders visual elements written in html code
request, redirect = makes it possible to click through webpage """
from flask import Flask, render_template, request, redirect, url_for 
import psycopg2
from flask_bcrypt import Bcrypt
import re

""" REMEMBER TO CHANGE VALUES"""
db = "dbname='XXX' user='XXX' password='XXX' host='localhost' port='5432'"

conn = psycopg2.connect(db)

print("Database connected successfully")

cur = conn.cursor()

conn.commit()

app = Flask(__name__)
crypt = Bcrypt(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/createaccount", methods=['POST', 'GET'])
def createaccount():
    cur = conn.cursor()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not re.match('^[a-zA-Z0-9]+$', username):
            error = 'Username must contain only numbers and letters'
        else:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user:
                return 'Username already exists'
            hashed_password = crypt.generate_password_hash(password).decode('utf-8')
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
    return render_template('createaccount.html', error=error)

@app.route("/login", methods=['POST', 'GET'])
def login():
    cur = conn.cursor()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not re.match('^[a-zA-Z0-9]+$', username):
            error = 'Username must contain only numbers and letters'
        else:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user and crypt.check_password_hash(user[1], password):
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',error="Wrong password or Username")
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/dashboard/players")
def players():
    cur = conn.cursor()
    cur.execute("""
                SELECT scorer, COUNT(scorer) as goals 
                FROM goalscorers 
                WHERE own_goal = 'false' AND NOT scorer = 'NA' 
                GROUP BY scorer ORDER BY goals DESC
    """)
    players = cur.fetchall()
    return render_template('players.html', players=players)

@app.route("/dashboard/teams")
def teams():
    cur = conn.cursor()
    cur.execute("""
        SELECT team, COUNT(team) as wins 
        FROM (
            SELECT home_team as team FROM results WHERE home_score > away_score
            UNION ALL
            SELECT away_team as team FROM results WHERE away_score > home_score
        ) AS winners
        GROUP BY team
        ORDER BY wins DESC
    """)
    most_wins_team = cur.fetchall()

    cur.execute("SELECT SUM(home_score + away_score) as total_goals FROM results")
    total_goals = cur.fetchone()
    return render_template('teams.html', most_wins_team=most_wins_team, total_goals=total_goals[0])

@app.route('/search', methods=['POST', 'GET'])
def search():
    cur = conn.cursor()
    query = request.args.get('query')
    if not query:
        return render_template('dashboard.html', message="Please enter a player name")
    cur.execute("""
        SELECT 
            goalscorers.team,
            results.date,
            results.home_team,
            results.away_team,
            COUNT(CASE WHEN own_goal = false THEN scorer END) AS "Goals", 
            COUNT(CASE WHEN own_goal = true THEN scorer END) AS "Own Goal",
            COUNT(CASE WHEN penalty = true THEN scorer END) AS "Penalty Goals"
        FROM goalscorers
        JOIN results ON goalscorers.game_id = results.game_id
        WHERE scorer ILIKE %s 
        GROUP BY goalscorers.team, 
                results.date, 
                results.home_team,
                results.away_team
    """, (query,))
    results = cur.fetchall()
    if results:
        return render_template('dashboard.html', results=results, player=query)
    else: 
        return render_template('dashboard.html', message=f"No data was found for {query}, try another player")

if __name__ == "__main__":
    app.run(debug=True)

cur.close()
conn.close()