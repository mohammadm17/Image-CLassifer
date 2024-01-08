from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import joblib
import numpy as np
import tensorflow as tf
import logging
from PIL import Image
import io

app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Load the pre-trained model
model = tf.keras.models.load_model('mnist_model')



@app.route('/')
def index():
     
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_b64 = data['image']

        # Convert base64 string to image
        image = Image.open(io.BytesIO(base64.b64decode(image_b64))).convert("L")
        image = image.resize((28, 28))

        # Convert to NumPy array and normalize pixel values
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # Make a prediction using the loaded model
        prediction = model.predict(image_array)

        # Get the predicted class
        predicted_class = np.argmax(prediction)

        result = {'predicted_class': int(predicted_class)}
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

       


if __name__ == '__main__':
    app.run(debug=True)
