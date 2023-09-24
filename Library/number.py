import requests

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
            print("Failed to fetch books. Status code:", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return []

if __name__ == "__main__":
    # Numbers of books to fetch
    num_books_list = [5, 18, 50]

    for num_books in num_books_list:
        # Fetch the specified number of books
        books = fetch_books(num_books)

        print(f"\nPrinting {num_books} books:")
        for idx, book in enumerate(books, start=1):
            print(f"{idx}. Title: {book['title']}, Author: {book['authors']}")
