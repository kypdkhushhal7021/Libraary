from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Frappe API endpoint to fetch books
FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library?page=2&title=and"

# Function to fetch a specified number of books
def fetch_books(num_books):
    try:
        response = requests.get(FRAPPE_API_URL)

        if response.status_code == 200:
            data = response.json().get('message', [])
            return data[:num_books]  # Return the specified number of books
        else:
            return []

    except requests.exceptions.RequestException:
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import_books', methods=['GET'])
def import_books():
    num_books = int(request.args.get('num_books'))
    books = fetch_books(num_books)
    return jsonify(books)

if __name__ == "__main__":
    app.run(port=1000)
