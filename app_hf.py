import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Load model
try:
    model = tf.keras.models.load_model('deepfake_model.keras')
except:
    model = None

def predict_deepfake(image):
    if model is None:
        return "❌ Model not loaded. Please ensure deepfake_model.keras exists."
    
    # Prepare image
    img_array = image.resize((224, 224))
    img_array = np.array(img_array, dtype='float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    prediction = model.predict(img_array, verbose=0)[0][0]
    
    if prediction > 0.5:
        result = f"🔴 **DEEPFAKE DETECTED**\n\nConfidence: {prediction*100:.2f}%\n\nThis image appears to be AI-generated or manipulated."
    else:
        result = f"🟢 **REAL IMAGE**\n\nConfidence: {(1-prediction)*100:.2f}%\n\nThis image appears to be authentic and unmodified."
    
    return result

# Create Gradio interface
with gr.Blocks(title="Deepfake Detection AI", theme=gr.themes.Soft(primary_hue="cyan")) as demo:
    gr.Markdown("""
    # 🔍 Deepfake Detection AI
    Upload an image to instantly analyze if it's real or AI-generated
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Image")
        with gr.Column():
            output = gr.Textbox(label="Analysis Result", lines=5)
    
    submit_btn = gr.Button("🚀 Analyze Image", variant="primary")
    submit_btn.click(fn=predict_deepfake, inputs=image_input, outputs=output)
    
    gr.Markdown("""
    ---
    **Powered by TensorFlow & MobileNetV2**
    
    Built for detecting deepfakes and AI-generated images.
    """)

if __name__ == "__main__":
    demo.launch()
