from flask import Flask, request, jsonify
import os
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your frontend (GitHub Pages)

# Make sure to create a folder to store the generated files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/checkout', methods=['POST'])
def checkout():
    try:
        # Get the order data from the frontend
        data = request.get_json()
        email = data.get('email')
        total_price = data.get('totalPrice')
        items = data.get('items')

        # Create the data string with the '|' separator
        file_content = f"{email}|{len(items)}|{total_price}\n"
        for item in items:
            file_content += f"{item}\n"

        # Generate a unique file name
        file_name = f"{uuid.uuid4()}.txt"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

        # Save the file to the server
        with open(file_path, 'w') as file:
            file.write(file_content)

        # Return a URL where the frontend can download the file
        file_url = f"https://your-backend-url.onrender.com/{UPLOAD_FOLDER}/{file_name}"

        return jsonify({'success': True, 'fileUrl': file_url})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error processing the order'}), 500


@app.route('/uploads/<filename>')
def download_file(filename):
    return app.send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)
