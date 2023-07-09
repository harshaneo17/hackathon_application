import sqlite3
import logging as log


'''https://docs.python.org/3/library/sqlite3.html'''

# Connect to the SQLite database
conn = sqlite3.connect('questions.db') #The returned Connection object conn represents the connection to the on-disk database
cursor = conn.cursor() #In order to execute SQL statements and fetch results from SQL queries, we will need to use a database cursor.

# Create a table to store questions and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')

def save_question_answer(question, answer):
    """The INSERT statement implicitly opens a transaction, which needs to be committed before changes are saved in the database. 
    Call con.commit() on the connection object to commit the transaction"""
    cursor.execute('INSERT INTO questions (question, answer) VALUES (?,?)', (question, answer)) 
    conn.commit()
    log.info('Question and answer saved successfully')