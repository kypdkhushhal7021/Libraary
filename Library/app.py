from flask import Flask, render_template
import requests

app = Flask(__name__)

# Frappe API endpoint
FRAPPE_API_URL = "https://frappe.io/api/method/frappe-library?page=2&title=and"

@app.route("/")
def index():
    try:
        response = requests.get(FRAPPE_API_URL)

        if response.status_code == 200:
            data = response.json().get('message', [])
        else:
            data = []

    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        data = []

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
