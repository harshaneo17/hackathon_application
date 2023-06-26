import sqlite3
import logging as log

# Connect to the SQLite database
conn = sqlite3.connect('questions.db')
cursor = conn.cursor()

# Create a table to store questions and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
''')

def save_question_answer(question, answer):
    cursor.execute('INSERT INTO questions (question, answer) VALUES (?,?)', (question, answer))
    conn.commit()
    log.info('Question and answer saved successfully')