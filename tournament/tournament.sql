-- Table definitions for the tournament project.

-- players table
-- Contains players data those who's registered for the tournament.
-- col1: name {text} name of a player.
-- col2: id {serial} unique id of a player. 
CREATE TABLE players ( name TEXT,
                       id SERIAL PRIMARY KEY );

-- matches table
-- Contains match result data for the tournament.
-- col1: result {integer} result of a match.
--       Winner is represented by 1, and loser is 0.
-- col2: id {integer} id of a player.
CREATE TABLE matches ( result INTEGER,
                       id INTEGER REFERENCES players );

-- standings view
-- Contains the players and their win records, sorted by wins.
-- This view is used in playerStandings function.
CREATE VIEW standings AS
    SELECT players.id, players.name, COALESCE(sum(matches.result), 0) AS wins, count(matches.result)
    FROM players LEFT JOIN matches
    ON players.id = matches.id
    GROUP BY players.id
    ORDER BY wins DESC;
