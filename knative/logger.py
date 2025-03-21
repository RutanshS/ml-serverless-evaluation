from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log_event():
    event = request.get_json()
    predicted_class = event['predicted_class']
    confidence = event['confidence']

    # Log the event to the console (or write to a file, database, etc.)
    print(f"Predicted Class: {predicted_class}, Confidence: {confidence}")

    return '', 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8082)
