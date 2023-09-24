import random

FRAPPE_API_BASE_URL = "https://frappe.io/api/method/frappe-library"

def generate_random_page():
    return random.randint(1, 10)

def generate_api_url():
    page = generate_random_page()
    return f"{FRAPPE_API_BASE_URL}?page={page}&title=and"

# Example usage
for i in range(5):  # Run for 5 iterations
    api_url = generate_api_url()
    print(f"Iteration {i+1}: {api_url}")
