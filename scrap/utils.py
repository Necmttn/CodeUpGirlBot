import sqlite3


database = '/app/db/database.db'


def get_connection_to_db(filename):
    return sqlite3.connect(filename)


def query_db(query, args=()):
    conn = get_connection_to_db(database)
    return conn.execute(query, args)
