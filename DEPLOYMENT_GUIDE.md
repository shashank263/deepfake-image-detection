# 🚀 FREE Deployment Guide - Deepfake Detection AI

## Best Free Options Ranked

### 1️⃣ **Hugging Face Spaces** (HIGHLY RECOMMENDED) ⭐⭐⭐⭐⭐
**Free forever • No credit card • Best for ML projects**

- ✅ Completely free (no time limits)
- ✅ Supports TensorFlow/Keras models
- ✅ Easy GitHub integration
- ✅ 2GB RAM (enough for your model)
- ✅ Perfect for AI projects
- ✅ Built-in file upload support

**Setup Time:** 5 minutes

---

### 2️⃣ **Streamlit Cloud** (EASIEST) ⭐⭐⭐⭐⭐
**Free • Simplest UI • Best for ML demos**

- ✅ Completely free
- ✅ No servers to manage
- ✅ Beautiful UI with minimal code
- ✅ Great for ML/AI projects
- ✅ Direct GitHub sync

**Setup Time:** 10 minutes

---

### 3️⃣ **Railway.app** ⭐⭐⭐⭐
**Free tier + cheap upgrade • Docker support**

- ✅ Free starter credits ($5/month)
- ✅ Easy GitHub integration
- ✅ Good for Flask apps
- ✅ Auto-deploys on push

**Setup Time:** 15 minutes

---

## EASIEST: Deploy with Streamlit (Recommended for You)

### Step 1: Create `streamlit_app.py`

Create a new file in your project root:

```python
import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Page config
st.set_page_config(
    page_title="Deepfake Detection AI",
    page_icon="🔍",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    body {
        background: linear-gradient(135deg, #0f0c29 0%, #1a0e3a 50%, #16213e 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a0e3a 50%, #16213e 100%);
    }
    h1 {
        color: #00f5ff;
        text-align: center;
        text-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
    }
    .stMetric {
        background: rgba(20, 30, 70, 0.6);
        border-radius: 10px;
        padding: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    try:
        model = tf.keras.models.load_model('deepfake_model.keras')
        return model
    except:
        st.error("❌ Model not found. Please train the model first using: `python train_cnn.py`")
        return None

# Title
st.markdown("# 🔍 Deepfake Detection AI")
st.markdown("Upload an image and instantly analyze if it's real or AI-generated")

# Model loading
model = load_model()

if model:
    # Upload file
    uploaded_file = st.file_uploader(
        "📤 Upload Image",
        type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
        help="Supported formats: JPG, PNG, GIF, BMP (Max 200MB)"
    )

    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
        
        with col2:
            st.markdown("### Analysis Result")
            
            # Prepare image
            img_array = image.resize((224, 224))
            img_array = np.array(img_array, dtype='float32') / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Predict
            with st.spinner('🧠 Analyzing image...'):
                prediction = model.predict(img_array, verbose=0)[0][0]
                
                if prediction > 0.5:
                    result = "Deepfake Detected"
                    confidence = round(prediction * 100, 2)
                    color = "🔴"
                else:
                    result = "Real"
                    confidence = round((1 - prediction) * 100, 2)
                    color = "🟢"
            
            # Display results
            st.metric(
                label=f"{color} Result",
                value=result,
                delta=f"{confidence}% confidence"
            )
            
            # Details
            st.info(f"""
            **Verdict Details:**
            - Detection: {result}
            - Confidence: {confidence}%
            - Raw Score: {round(prediction, 4)}
            """)

else:
    st.warning("⚠️ Model loading failed. Train the model first!")
    st.code("python train_cnn.py", language="bash")
```

### Step 2: Create `requirements_streamlit.txt`

```
streamlit==1.28.0
tensorflow==2.21.0
numpy==2.2.6
pillow==10.0.0
```

### Step 3: Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Add Streamlit deployment"
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection.git
git push -u origin main
```

### Step 4: Deploy on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Connect your GitHub repo
4. Select:
   - **Repository:** your-deepfake-detection-repo
   - **Branch:** main
   - **Main file path:** streamlit_app.py
5. Click "Deploy" ✨

**That's it! Your app is live in 2 minutes!**

---

## ALTERNATIVE: Deploy with Hugging Face Spaces

### Step 1: Create Hugging Face Account

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up (free)
3. Go to [Spaces](https://huggingface.co/spaces)
4. Click "Create new Space"

### Step 2: Upload Your Project

```bash
# Clone your Hugging Face space
git clone https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection
cd deepfake-detection

# Copy your project files
cp -r /path/to/your/deepfake_detection/* .

# Push to Hugging Face
git add .
git commit -m "Upload deepfake detection"
git push
```

### Step 3: Create `app.py` (Gradio version for easy UI)

```python
import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# Load model
model = tf.keras.models.load_model('deepfake_model.keras')

def predict_deepfake(image):
    # Prepare image
    img_array = image.resize((224, 224))
    img_array = np.array(img_array, dtype='float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Predict
    prediction = model.predict(img_array, verbose=0)[0][0]
    
    if prediction > 0.5:
        result = f"🔴 Deepfake Detected\nConfidence: {prediction*100:.2f}%"
    else:
        result = f"🟢 Real Image\nConfidence: {(1-prediction)*100:.2f}%"
    
    return result

# Create interface
interface = gr.Interface(
    fn=predict_deepfake,
    inputs=gr.Image(type="pil", label="Upload Image"),
    outputs=gr.Textbox(label="Analysis Result"),
    title="🔍 Deepfake Detection AI",
    description="Upload an image to detect if it's real or AI-generated",
    theme=gr.themes.Soft()
)

interface.launch()
```

### Step 4: Create `requirements.txt`

```
gradio==4.0.0
tensorflow==2.21.0
numpy==2.2.6
pillow==10.0.0
```

---

## Comparison Table

| Feature | Streamlit Cloud | HF Spaces | Railway | PythonAnywhere |
|---------|-----------------|-----------|---------|----------------|
| **Cost** | Free ✅ | Free ✅ | $5/mo | $5/mo |
| **Setup Time** | 5 min ⭐ | 10 min | 15 min | 20 min |
| **Best For** | ML demos | ML projects | Full stack | Prototypes |
| **Model Size Limit** | Unlimited | Unlimited | Good | Limited |
| **Ease** | Very easy ⭐ | Easy | Moderate | Moderate |
| **Performance** | Good | Good | Better | Basic |
| **GitHub Sync** | Yes | Yes | Yes | Manual |

---

## Troubleshooting

### "Model not found" Error
```bash
# Train model first
python train_cnn.py

# Wait for completion, then deploy
```

### File Size Too Large
```bash
# Use .gitignore to exclude model during dev
echo "deepfake_model.keras" >> .gitignore

# Then upload model separately or train on deployment server
```

### Import Errors
```bash
# Update requirements.txt with ALL packages
pip freeze > requirements_all.txt
```

---

## Cost Breakdown

| Platform | Monthly Cost | Storage | Bandwidth | CPU |
|----------|-------------|---------|-----------|-----|
| **Streamlit Cloud** | $0 | Unlimited | Unlimited | Shared |
| **HF Spaces** | $0 | Unlimited | Unlimited | Shared |
| **Railway** | $5 | 100GB | Unmetered | Shared |
| **AWS EC2** | $0 (first year) | 30GB | 1GB out | t2.micro |

---

## Quick Start (Copy-Paste Ready)

### Option 1: Streamlit (Easiest)
```bash
# 1. Create streamlit_app.py (copy code from above)
# 2. Test locally
streamlit run streamlit_app.py

# 3. Push to GitHub
git add .
git commit -m "Add Streamlit app"
git push

# 4. Deploy at streamlit.io/cloud
```

### Option 2: Hugging Face Spaces (Most Professional)
```bash
# 1. Create space at huggingface.co/spaces
# 2. Create app.py with Gradio (code above)
# 3. Add requirements.txt
# 4. Push to space repo
git clone https://huggingface.co/spaces/USERNAME/deepfake-detection
cd deepfake-detection
# Add files
git push
```

---

## Live Demo Links

Once deployed, you'll get a public URL like:
- **Streamlit:** `https://deepfake-detection-USERNAME.streamlit.app`
- **HF Spaces:** `https://huggingface.co/spaces/USERNAME/deepfake-detection`

Share these with anyone! 🎉

---

## Need Help?

📚 **Streamlit Docs:** https://docs.streamlit.io/  
📚 **HF Spaces Docs:** https://huggingface.co/docs/hub/spaces  
💬 **Community:** Ask in Streamlit forums or HF Discord

**Total Free Deployment Time: 30 minutes** ⏱️
