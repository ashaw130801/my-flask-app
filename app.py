from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define the path to the txt file to save emails
FILE_PATH = "emails.txt"

# Route to handle email submission
@app.route('/submit', methods=['POST'])
def submit_email():
    # Get email from the form data
    email = request.form.get('email')

    if email:
        # Save email to txt file, separated by '|'
        with open(FILE_PATH, "a") as file:
            file.write(email + '|')

        return jsonify({"message": "Email saved successfully!"}), 200
    else:
        return jsonify({"error": "No email provided!"}), 400

if __name__ == "__main__":
    app.run(debug=True)