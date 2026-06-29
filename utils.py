import psycopg2
import re
from psycopg2.extras import execute_values

db_params = {
    'host' : "localhost",
    'port' : "5433",
    'dbname' : "postgres",
    'user' : "postgres",
    'password' : "123"    
}


def insert_f(values, table):

    # connect to db
    conn = psycopg2.connect(**db_params)
    # open a cursor for interaction with db
    cursor = conn.cursor()

    query = f'INSERT INTO {table} VALUES %s'
    execute_values(cursor, query, values)

    # commit changes
    conn.commit()

    # close connection
    cursor.close()
    conn.close()


def select_f(query):
    '''query = SQL query to get data'''
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute(query)
    output = cursor.fetchall()

    conn.close()

    return output