from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Function to fetch titles and authors from the database
def fetch_titles_and_authors():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select titles and authors
    cursor.execute("SELECT title, author FROM books")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return titles and authors
    return rows

# Function to fetch member names from the database
def fetch_member_names():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Execute SQL query to select member names
    cursor.execute("SELECT name FROM members")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Return member names
    return rows

@app.route('/')
def index():
    # Fetch titles and authors from the database
    titles_and_authors = fetch_titles_and_authors()

    # Fetch member names from the database
    member_names = fetch_member_names()

    return render_template('index.html', titles_and_authors=titles_and_authors, member_names=member_names)

if __name__ == "__main__":
    app.run(port=7000)
