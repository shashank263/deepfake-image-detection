import os
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load trained model with error handling
try:
    model = tf.keras.models.load_model('deepfake_model.keras')
    model_loaded = True
    print("✅ Model loaded successfully")
except:
    model_loaded = False
    model = None
    print("⚠️ Model not found. Please train the model first.")

# Image size must match training
IMG_SIZE = 224

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def predict_image(img_path):
    img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0

    prediction = model.predict(img_array)[0][0]
    
    # INVERTED LOGIC: If prediction is high, it's FAKE (model learned pattern is inverted)
    if prediction > 0.5:
        result = "Deepfake Detected"
        confidence = prediction * 100
        is_fake = True
    else:
        result = "Real"
        confidence = (1 - prediction) * 100
        is_fake = False
    
    return {
        "result": result,
        "is_fake": is_fake,
        "confidence": round(confidence, 2),
        "raw_prediction": round(prediction, 4)
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return "Error: Model not loaded. Please train the model first."
    
    if 'file' not in request.files:
        return "Error: No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "Error: No selected file"
    
    # Validate file type
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
    file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if file_ext not in allowed_extensions:
        return "Error: Invalid file type. Please upload an image."

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        prediction_data = predict_image(file_path)
        return render_template(
            'result.html',
            result=prediction_data['result'],
            confidence=prediction_data['confidence'],
            is_fake=prediction_data['is_fake'],
            image_path=file_path,
            raw_prediction=prediction_data['raw_prediction']
        )
    except Exception as e:
        return f"Error processing image: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
