import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Execute a SQL query to fetch title, author, and publisher
cursor.execute('SELECT mem_id, mem_name, book_id, title, username, date_issued, due_date FROM issuedbooks')

# Fetch all rows
books = cursor.fetchall()

# Print the title, author, and publisher for each book
for book in books:
    mem_id, mem_name, book_id, title, username, date_issued, due_date = book
    print(f'ID: {mem_id}')
    print(f'name: {mem_name}')
    print(f'Author: {title}')
    print(f'Publisher: {username}')
    print(f'Date: {date_issued}')
    print(f'Due Date: {due_date}')

# Close the cursor and connection
cursor.close()
conn.close()
