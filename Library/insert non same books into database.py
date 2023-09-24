import sqlite3
import requests

# Frappe API endpoint to fetch books
FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library"

# Function to fetch books containing "Harry" in the title and publisher as "Scholastic Inc."
def fetch_harry_books(num_books):
    params = {
        'title': 'Harry',
        'publisher': 'Scholastic Inc.'
    }

    try:
        response = requests.get(FRAPPE_API_URL, params=params)

        if response.status_code == 200:
            data = response.json().get('message', [])
            return data[:num_books]  # Return the specified number of books
        else:
            print("Failed to fetch books. Status code:", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return []

# Function to insert books into SQLite database, avoiding duplicates based on title and publisher
def insert_books_to_db(books):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Create the books table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            publisher TEXT
        )
    ''')

    for book in books:
        title = book.get('title', '')
        author = book.get('authors', '')
        publisher = book.get('publisher', '')

        # Check if the book already exists based on title and publisher
        cursor.execute("SELECT * FROM books WHERE title = ? AND publisher = ?", (title, publisher))
        existing_book = cursor.fetchone()

        # If the book doesn't already exist, insert it
        if not existing_book:
            cursor.execute("INSERT INTO books (title, author, publisher) VALUES (?, ?, ?)", (title, author, publisher))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Specify the number of books to fetch
    num_books = 6  # Change this to the desired number of books

    # Fetch books containing "Harry" in the title and publisher as "Scholastic Inc."
    harry_books = fetch_harry_books(num_books)

    if harry_books:
        # Insert books into the database, avoiding duplicates based on title and publisher
        insert_books_to_db(harry_books)

        # Print the fetched books
        print(f"Books containing 'Harry' in the title and published by 'Scholastic Inc.' (first {num_books} books):")
        for idx, book in enumerate(harry_books, start=1):
            print(f"{idx}. Title: {book['title']}, Author: {book['authors']}, Publisher: {book.get('publisher', 'N/A')}")
    else:
        print("No books containing 'Harry' in the title and published by 'Scholastic Inc.' found.")
