from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Function to get the count of rows in the "books" table
def get_books_count():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Route to display the count on an HTML page
@app.route('/')
def display_count():
    books_count = get_books_count()
    return render_template('index.html', count=books_count)

if __name__ == '__main__':
    app.run(debug=True)
