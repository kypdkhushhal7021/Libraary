import requests

# Frappe API endpoint to fetch books
FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library"

# Function to fetch books containing "Harry" in the title
def fetch_harry_books(num_books):
    params = {
        'title': 'Harry',
        'publisher':'Scholastic Inc.'
    }

    try:
        response = requests.get(FRAPPE_API_URL, params=params)

        if response.status_code == 200:
            data = response.json().get('message', [])
            return data
        else:
            print("Failed to fetch books. Status code:", response.status_code)
            return []

    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return []

if __name__ == "__main__":
    # Specify the number of books to fetch
    num_books = 3  # Change this to the desired number of books

    # Fetch books containing "Harry" in the title
    harry_books = fetch_harry_books(num_books)

    if harry_books:
        # Print the fetched books
        print(f"Books containing 'Harry' in the title (first {num_books} books):")
        for idx, book in enumerate(harry_books[:num_books], start=1):
            print(f"{idx}. Title: {book['title']}, Author: {book['authors']}, Publisher: {book.get('publisher', 'N/A')}")
    else:
        print("No books containing 'Harry' in the title found.")
