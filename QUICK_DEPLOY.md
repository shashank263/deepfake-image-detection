# ⚡ Quick Deploy in 5 Minutes

## Option 1: Deploy on Streamlit Cloud (EASIEST)

### Step 1️⃣ - Install Streamlit (test locally first)
```bash
pip install streamlit
streamlit run streamlit_app.py
```

### Step 2️⃣ - Push Code to GitHub
```bash
git init
git add .
git commit -m "Deepfake detection app"
git remote add origin https://github.com/YOUR_USERNAME/deepfake-detection
git branch -M main
git push -u origin main
```

### Step 3️⃣ - Deploy on Streamlit
1. Go to **https://streamlit.io/cloud**
2. Click **"New app"**
3. Select:
   - **Repository:** deepfake-detection
   - **Branch:** main
   - **Main file:** streamlit_app.py
4. Click **Deploy**

✅ **DONE!** Your app is live at `https://deepfake-detection-USERNAME.streamlit.app`

---

## Option 2: Deploy on Hugging Face Spaces

### Step 1️⃣ - Create Space
1. Go to **https://huggingface.co/spaces**
2. Click **"Create new Space"**
3. Name: `deepfake-detection`
4. Space type: **Docker**
5. Create Space

### Step 2️⃣ - Clone & Upload
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection
cd deepfake-detection

# Copy your files
cp /path/to/streamlit_app.py .
cp /path/to/requirements_streamlit.txt requirements.txt
cp /path/to/deepfake_model.keras .

# Create Dockerfile
echo "FROM python:3.10
RUN pip install -r requirements.txt
CMD [\"streamlit\", \"run\", \"streamlit_app.py\"]" > Dockerfile
```

### Step 3️⃣ - Push & Deploy
```bash
git add .
git commit -m "Deploy deepfake detection"
git push
```

✅ **DONE!** Your app is live at `https://huggingface.co/spaces/YOUR_USERNAME/deepfake-detection`

---

## Option 3: Deploy on Railway.app ($0 trial)

### Step 1️⃣ - Create Account
- Go to **https://railway.app**
- Sign up with GitHub

### Step 2️⃣ - Deploy
1. Click **"New Project"**
2. Select **"Deploy from GitHub"**
3. Choose your deepfake-detection repo
4. Set environment variable:
   - `STREAMLIT_SERVER_PORT=8000`
5. Deploy!

✅ Your app is live! (First month free)

---

## Cost Comparison

| Platform | Cost | Setup | Model Size |
|----------|------|-------|-----------|
| **Streamlit** | Free ✅ | 5 min ⭐ | Unlimited |
| **HF Spaces** | Free ✅ | 10 min | Unlimited |
| **Railway** | $5/mo | 10 min | Unlimited |

**Recommendation: Streamlit Cloud** 🚀

---

## Important Notes

### Before Deploying:
✅ Train model: `python train_cnn.py`  
✅ Test locally: `streamlit run streamlit_app.py`  
✅ Check `deepfake_model.keras` exists

### Model Upload:
- GitHub has 100MB file limit
- Use **Git LFS** for large models:
```bash
git lfs install
git lfs track "*.keras"
git add .gitattributes deepfake_model.keras
git commit -m "Add model with LFS"
git push
```

### Troubleshooting:
- **"Module not found"** → Add to `requirements_streamlit.txt`
- **"Model not found"** → Train model first
- **Slow startup** → Normal, model loading takes time

---

## Share Your App!

Once deployed, you'll get a public URL. Share it with friends:
- 📱 Mobile friendly
- 🌐 Works on any device
- 🔒 No installation needed
- 🚀 Instant access

Congratulations! 🎉
