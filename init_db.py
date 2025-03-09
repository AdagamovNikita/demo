import sqlite3

# Connect to SQLite database (will create it if it doesn't exist)
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Create tasks table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Insert a sample task
cursor.execute('INSERT INTO tasks (title) VALUES (?)', ('Complete Lecture 8',))

# Commit changes and close connection
conn.commit()
conn.close()

print("Database initialized successfully!") 