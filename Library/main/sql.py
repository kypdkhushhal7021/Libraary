import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('books.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT,
        password TEXT
    )
''')

# Insert data into the table
cursor.execute("INSERT INTO users (username,email, password) VALUES (?, ?, ?)", ('8848', '8848@digital.com','8848'))
cursor.execute("INSERT INTO users (username,email, password) VALUES (?, ?, ?)", ('admin', 'admin@digital.com','admin'))

# Commit the changes and close the connection
conn.commit()
conn.close()
