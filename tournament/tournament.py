#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

from functools import update_wrapper
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def decorator(d):
    """Make function d a decorator; d wraps a function fn."""
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def basic_query(fn):
    """A decorator function for basic SELECT queries."""
    def _fn():
        conn = connect()
        cur = conn.cursor()
        response = fn(cur)
        conn.close()
        return response
    return _fn

@decorator
def transaction_query(fn):
    """A decorator function for queries that create transaction."""
    def _fn(*args):
        conn = connect()
        cur = conn.cursor()
        fn(*args, cur=cur)
        conn.commit()
        conn.close()
    return _fn

@transaction_query
def deleteMatches(cur=None):
    """Remove all the match records from the database."""
    sql = "DELETE FROM matches;"
    cur.execute(sql)

@transaction_query
def deletePlayers(cur=None):
    """Remove all the player records from the database."""
    sql = "DELETE FROM players;"
    cur.execute(sql)

@basic_query
def countPlayers(cur=None):
    """Returns the number of players currently registered."""
    sql = "SELECT count(*) FROM players;"
    cur.execute(sql)
    return cur.fetchone()[0]

@transaction_query
def registerPlayer(name, cur=None):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    sql = "INSERT INTO players VALUES (%s);"
    cur.execute(sql, (name,))

@basic_query
def playerStandings(cur=None):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    sql = "SELECT * FROM standings;"
    cur.execute(sql)
    return cur.fetchall()

@transaction_query
def reportMatch(winner, loser, cur=None):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner_sql = "INSERT INTO matches VALUES (1, %s);"
    loser_sql = "INSERT INTO matches VALUES (0, %s);"
    cur.execute(winner_sql, (winner,))
    cur.execute(loser_sql, (loser,))
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    return [(standings[i-1][0], standings[i-1][1], standings[i][0], standings[i][1])
            for i in range(1, len(standings), 2)]
