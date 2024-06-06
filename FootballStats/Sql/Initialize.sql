DROP TABLE IF EXISTS goalscorers;
DROP TABLE IF EXISTS results;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    username VARCHAR(24) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username)
);

CREATE TABLE goalscorers (
    date DATE,
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    team VARCHAR(255),
    scorer VARCHAR(255),
    minute VARCHAR(255),
    own_goal VARCHAR(255),
    penalty VARCHAR(255)
);

CREATE TABLE results(
    game_id INT PRIMARY KEY,
    date DATE,
    home_team VARCHAR(255),
    away_team VARCHAR(255),
    home_score INT,
    away_score INT,
    tournament VARCHAR(255),
    city VARCHAR(255),
    country VARCHAR(255),
    neutral VARCHAR(255)
);

/* Replace path with ABSOLUTE PATH ON FILESYSTEM */
COPY goalscorers(date, home_team, away_team, team, scorer, minute, own_goal, penalty)
FROM '/Users/bernardo/Desktop/DIS/FootballStats/data/goalscorers.csv'
DELIMITER ','
CSV HEADER;

COPY results(game_id, date, home_team, away_team, home_score, away_score, tournament, city, country, neutral)
FROM '/Users/bernardo/Desktop/DIS/FootballStats/data/results.csv'
DELIMITER ','
CSV HEADER;

ALTER TABLE goalscorers
ALTER COLUMN minute TYPE INT USING (NULLIF(minute, 'NA')::int);

ALTER TABLE goalscorers
ADD COLUMN game_id INT;

UPDATE goalscorers g
SET game_id = r.game_id
FROM results r
WHERE g.date = r.date AND g.home_team = r.home_team AND g.away_team = r.away_team;

ALTER TABLE goalscorers
ADD CONSTRAINT fk_game_id
FOREIGN KEY (game_id)
REFERENCES results(game_id);

ALTER TABLE goalscorers
ALTER COLUMN own_goal TYPE BOOLEAN USING 
(CASE WHEN own_goal = 'NA' THEN NULL 
WHEN own_goal = 'TRUE' THEN TRUE 
WHEN  own_goal = 'FALSE' THEN FALSE END);

ALTER TABLE goalscorers
ALTER COLUMN penalty TYPE BOOLEAN USING 
(CASE WHEN penalty = 'NA' THEN NULL 
WHEN penalty = 'FALSE' THEN FALSE 
WHEN penalty = 'TRUE' THEN TRUE END);