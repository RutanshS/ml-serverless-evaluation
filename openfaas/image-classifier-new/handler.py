import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json

# Load the pre-trained MobileNetV2 model
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def preprocess_image(image):
    image = image.resize((224, 224))
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image

def classify_image(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]
    return decoded_predictions

def handle(event, context):
    try:
        image_bytes = event.body
        predictions = classify_image(image_bytes)

        # Convert numpy.float32 to Python float
        predictions_serializable = [
            (class_id, class_name, float(confidence))  # Convert to Python float
            for class_id, class_name, confidence in predictions
        ]

        return {
            "statusCode": 200,
            "body": json.dumps(predictions_serializable)  # Serialize to JSON
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})  # Return error as JSON
        }