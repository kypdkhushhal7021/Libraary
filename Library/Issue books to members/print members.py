import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Execute a SQL query to fetch title, author, and publisher
cursor.execute('SELECT * FROM members')

# Fetch all rows
books = cursor.fetchall()

# Print the title, author, and publisher for each book
for book in books:
    id1,title, author, publisher = book
    print(f'Title: {title}')
    print(f'Author: {author}')
    print(f'Publisher: {publisher}')
    print(f'Publisher: {id1}')
    print()

# Close the cursor and connection
cursor.close()
conn.close()
