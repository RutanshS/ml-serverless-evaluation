# from flask import Flask, request, jsonify
# import numpy as np
# from PIL import Image
# import tensorflow as tf
# from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

# app = Flask(__name__)

# # Load the pretrained MobileNetV2 model (weights='imagenet' loads the ImageNet-trained weights)
# model = MobileNetV2(weights='imagenet')

# def preprocess_image(image):
#     # Preprocess the image (resize, normalize, etc. for MobileNetV2)
#     image = image.resize((224, 224))  # Resize the image to 224x224 for MobileNetV2
#     image = np.array(image)  # Convert image to numpy array
#     image = preprocess_input(image)  # Preprocess the image for MobileNetV2
#     return np.expand_dims(image, axis=0)  # Add batch dimension

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Check if the file is part of the request
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400
    
#     try:
#         # Open the image file
#         img = Image.open(file)
        
#         # Preprocess the image
#         processed_img = preprocess_image(img)
        
#         # Make predictions
#         predictions = model.predict(processed_img)
        
#         # Decode the predictions (returns top 5 classes)
#         decoded_predictions = decode_predictions(predictions, top=1)[0]  # Get the top 1 prediction
        
#         # Prepare the response
#         predicted_class = decoded_predictions[0][1]  # Class label
#         confidence = float(decoded_predictions[0][2])  # Convert confidence to a native Python float
        
#         return jsonify({'predicted_class': predicted_class, 'confidence': confidence})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=8080)


from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
import requests

app = Flask(__name__)

# Load the pretrained MobileNetV2 model
model = MobileNetV2(weights='imagenet')

# Knative broker URL
BROKER_URL = "http://default-broker.demo.svc.cluster.local/"

def preprocess_image(image):
    """ Preprocess the image for MobileNetV2 model. """
    image = image.resize((224, 224))
    image = np.array(image)
    image = preprocess_input(image)
    return np.expand_dims(image, axis=0)

def send_event(predicted_class, confidence):
    """ Sends classification results as a CloudEvent to Knative broker. """
    event_data = {
        "predicted_class": predicted_class,
        "confidence": confidence
    }

    headers = {
        "Ce-SpecVersion": "1.0",
        "Ce-Type": "ml.prediction",
        "Ce-Source": "ml-service",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(BROKER_URL, json=event_data, headers=headers)
        response.raise_for_status()  # Ensure it raises an error if the event fails
        print("Event sent successfully!")
    except Exception as e:
        print(f"Failed to send event: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    """ Handles incoming image, processes it, and returns a prediction. """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Load and preprocess the image
        img = Image.open(file)
        processed_img = preprocess_image(img)

        # Perform prediction
        predictions = model.predict(processed_img)
        decoded_predictions = decode_predictions(predictions, top=1)[0]

        # Extract class and confidence
        predicted_class = decoded_predictions[0][1]
        confidence = float(decoded_predictions[0][2])

        # Send the event to Knative broker
        send_event(predicted_class, confidence)

        # Return prediction response
        return jsonify({'predicted_class': predicted_class, 'confidence': confidence})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
