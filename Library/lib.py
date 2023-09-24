import requests

# Frappe API endpoint to fetch books
FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library"

# Function to fetch books containing "Harry" in the title
def fetch_harry_books():
    params = {
        'title': 'Harry'
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
    # Fetch books containing "Harry" in the title
    harry_books = fetch_harry_books()

    if harry_books:
        # Print the fetched books
        print("Books containing 'Harry' in the title:")
        for book in harry_books:
            print(f"Title: {book['title']}, Author: {book['authors']}")
    else:
        print("No books containing 'Harry' in the title found.")
