import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Deepfake Detection AI",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a0e3a 50%, #16213e 100%);
    }
    
    /* Main content */
    [data-testid="stMain"] {
        background: transparent;
    }
    
    /* Text colors */
    h1, h2, h3 {
        color: #00f5ff !important;
    }
    
    p {
        color: #b0b0b0 !important;
    }
    
    /* Upload section */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #00f5ff !important;
        border-radius: 15px !important;
        background: rgba(20, 30, 70, 0.6) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00f5ff 0%, #a78bfa 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        box-shadow: 0 0 20px rgba(0, 245, 255, 0.4) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 40px rgba(0, 245, 255, 0.8) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: rgba(20, 30, 70, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(0, 245, 255, 0.1) !important;
        border-left: 4px solid #00f5ff !important;
        border-radius: 8px !important;
    }
    
    .stWarning {
        background: rgba(255, 100, 0, 0.1) !important;
        border-left: 4px solid #ff6400 !important;
        border-radius: 8px !important;
    }
    
    .stError {
        background: rgba(255, 0, 100, 0.1) !important;
        border-left: 4px solid #ff0064 !important;
        border-radius: 8px !important;
    }
    
    /* Columns */
    [data-testid="column"] {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Load model with caching
@st.cache_resource
def load_model():
    """Load the trained deepfake detection model"""
    try:
        model = tf.keras.models.load_model('deepfake_model.keras')
        return model
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

# Main title
st.markdown("""
<h1 style="text-align: center; font-size: 3em; margin-bottom: 10px;">
🔍 Deepfake Detection AI
</h1>
<p style="text-align: center; color: #b0b0b0; font-size: 1.1em;">
Upload an image and instantly analyze if it's <span style="color: #00f5ff;">real or AI-generated</span>
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# Load model
model = load_model()

if model is None:
    st.error("""
    ❌ **Model not found!**
    
    Please train the model first by running:
    ```bash
    python train_cnn.py
    ```
    
    The training process takes about 30 minutes and will create the file `deepfake_model.keras`.
    """)
else:
    # Create two columns
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            label_visibility="collapsed",
            help="Supported: JPG, PNG, GIF, BMP (Max 200MB)"
        )
    
    if uploaded_file is not None:
        # Display uploaded image
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, caption="Uploaded Image")
        
        # Process and display results
        with col2:
            st.markdown("### 🔬 Analysis Result")
            
            # Prepare image for prediction
            img_for_pred = image.resize((224, 224))
            img_array = np.array(img_for_pred, dtype='float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Get prediction
            with st.spinner('🧠 Analyzing image with neural network...'):
                prediction = model.predict(img_array, verbose=0)[0][0]
                
                # Determine result
                if prediction > 0.5:
                    result = "Deepfake Detected"
                    confidence = round(prediction * 100, 2)
                    is_fake = True
                    emoji = "⚠️"
                else:
                    result = "Real"
                    confidence = round((1 - prediction) * 100, 2)
                    is_fake = False
                    emoji = "✅"
            
            # Display result with color coding
            st.markdown(f"""
            <div style="background: {'rgba(255, 0, 100, 0.15)' if is_fake else 'rgba(0, 255, 100, 0.15)'}; 
                        border: 2px solid {'#ff0064' if is_fake else '#00ff64'}; 
                        border-radius: 15px; 
                        padding: 25px; 
                        text-align: center;
                        box-shadow: 0 0 30px {'rgba(255, 0, 100, 0.3)' if is_fake else 'rgba(0, 255, 100, 0.3)'}"
            >
                <h2 style="color: {'#ff0064' if is_fake else '#00ff64'}; margin: 0;">
                    {emoji} {result}
                </h2>
                <p style="color: #e0e0e0; font-size: 1.3em; margin: 10px 0; font-weight: bold;">
                    {confidence}% Confidence
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("")
            
            # Show analysis details
            st.info(f"""
            **📊 Analysis Details:**
            - **Detection Result:** {result}
            - **Confidence Score:** {confidence}%
            - **Raw Model Output:** {round(prediction, 4)}
            - **Model:** MobileNetV2 (Transfer Learning)
            """)
            
            # Verdict message
            if is_fake:
                st.warning("""
                ⚠️ **DEEPFAKE DETECTED**
                
                This image has been flagged as potentially AI-generated or manipulated. 
                It may have been created using deep learning techniques or digital modification.
                """)
            else:
                st.success("""
                ✅ **AUTHENTIC IMAGE**
                
                This image appears to be genuine and unmodified with high confidence.
                No signs of AI generation or deepfake techniques detected.
                """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 30px;">
    <p>🔬 Powered by TensorFlow & MobileNetV2</p>
    <p>Built with ❤️ for Deepfake Detection</p>
</div>
""", unsafe_allow_html=True)
