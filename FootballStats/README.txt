How to run FootballStats project. Assuming python3 and pip3 is installed:

1. Install requirements in the terminal:
pip3 install -r requirements.txt

3. In app.py, set your own database, username and password.

3. In 'Initialize.sql' change the directory to the full path of 'goalscorers.csv' and 'results.csv'.
NOTE: If this is not run as super-user there might be issues with using COPY within the .SQL file.
if this is the case follow the instructions further down.

4. Initialize the database by running the SQL file in the terminal:
psql -d dbname -U user -f sql/Initialize.sql

5. Activation of the virtual env in the terminal:
source env/bin/activate

6. Run the web application in the terminal:
python3 app.py  

How to use the web application:

1. Create account:
You start by pressing the 'Create Account' button, you then get redirected to a page 
where you choose your username and password. Only letters and numbers are allowed in the username.
If account creation was successful you should be redirected to the login screen.

2. Login: 
Now you can login onto your account by typing in your username and password.

3. Dashboard:
On the dashboard you will see a search bar and two buttons.

    3.1. Search bar:
    In the search bar, you can search for your favorite football players.
    When searching for a player different goal stats will show up about that player.
    The Search bar should not be case sensitive but you should write the full name of
    the football player.

    Example use:
        1. Type "Cristiano Ronaldo"
        2. Press "Search"
        3. Enjoy!

    3.2. Players:
    If you press the "Players" button, you will get redirected to a page that shows a list with the most
    scoring player at the top and the least scoring player at the bottom.

    3.3. Teams:
    If you press the "Teams" button, you will get redirected to a page that shows a list with the most
    winning team at the top and the least winning team at the buttom.

################ Instructions if COPY fails within Initialize.SQL ################

1. Navigate to Initialize.sql

2. Out-comment everything BUT the CREATE TABLE statements and DROP TABLE statements.

3. Run 'psql -d dbname -U user -f sql/initialize.sql' in terminal to create the tables

4. Run 'psql -d dbname -U user' in terminal

5. Run '\copy goalscorers(date, home_team, away_team, team, scorer, minute, own_goal, penalty) FROM '/Users/bernardo/Desktop/DIS/FootballStats/data/goalscorers.csv' DELIMITER ',' CSV HEADER;'
    in terminal.

6. Run '\copy results(game_id, date, home_team, away_team, home_score, away_score, tournament, city, country, neutral) FROM '/Users/bernardo/Desktop/DIS/FootballStats/data/results.csv' DELIMITER ',' CSV HEADER;'

7. Exit psql in terminal by writting 'Exit' followed by enter

8. The out-commented piece of Initialize.sql file should now be un-out-commented (remove the comment symbols)

9. Out-comment the COPY Statements

10. Out-comment the CREATE TABLE and DROP TABLE statements

11. Run 'psql -d footballstats -U bernardo -f sql/initialize.sql' In the terminal
    
    Expected output:
    ALTER TABLE
    ALTER TABLE
    UPDATE 44110
    ALTER TABLE
    ALTER TABLE
    ALTER TABLE

13. Write source env/bin/activate to activate the virtual enviornment

14. Run python3 app.py

15 Copy the http:// ... line into your browser

16. ENJOY!