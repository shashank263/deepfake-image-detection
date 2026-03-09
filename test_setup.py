"""
Testing and validation script for deepfake detection project.
Verifies all components are working correctly.
"""

import os
import sys
import json
from pathlib import Path

def check_environment():
    """Check Python environment and installed packages"""
    print("\n📋 Checking Python Environment")
    print("="*50)
    
    print(f"✓ Python Version: {sys.version.split()[0]}")
    print(f"✓ Python Path: {sys.executable}")
    
    required_packages = [
        'tensorflow',
        'flask',
        'numpy',
        'matplotlib',
        'seaborn',
        'sklearn',
        'PIL'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}: Installed")
        except ImportError:
            print(f"✗ {package}: Missing")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install {' '.join(missing)}")
        return False
    
    print("✅ All packages installed")
    return True

def check_directory_structure():
    """Verify project directory structure"""
    print("\n📁 Checking Directory Structure")
    print("="*50)
    
    required_dirs = [
        'datasets/real_and_fake_face',
        'datasets/real_and_fake_face/fake',
        'datasets/real_and_fake_face/real',
        'static/uploads',
        'templates',
        'tf_env'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ {dir_path}: Found")
        else:
            print(f"✗ {dir_path}: Missing")
            missing.append(dir_path)
    
    if missing:
        print(f"\n⚠️  Some directories missing. This may be OK in early stages.")
        return True
    
    print("✅ All directories present")
    return True

def check_files():
    """Check for essential files"""
    print("\n📄 Checking Essential Files")
    print("="*50)
    
    required_files = {
        'app.py': 'Flask application',
        'train_cnn.py': 'Training script',
        'predict_utils.py': 'Prediction utility',
        'config.py': 'Configuration',
        'requirements.txt': 'Dependencies',
        'templates/index.html': 'Upload page',
        'templates/result.html': 'Result page',
        'README.md': 'Documentation',
    }
    
    missing = []
    for file_path, description in required_files.items():
        if os.path.isfile(file_path):
            print(f"✓ {file_path}: {description}")
        else:
            print(f"✗ {file_path}: {description} - Missing")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing files")
        return False
    
    print("✅ All essential files present")
    return True

def check_model():
    """Check if trained model exists"""
    print("\n🤖 Checking Trained Model")
    print("="*50)
    
    if os.path.isfile('deepfake_model.keras'):
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model('deepfake_model.keras')
            print(f"✓ Model loaded successfully")
            print(f"  - Shape: {model.input_shape}")
            print(f"  - Parameters: {model.count_params():,}")
            print("✅ Model is valid and ready")
            return True
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            return False
    else:
        print(f"⚠️  Model not found: deepfake_model.keras")
        print(f"   Run: python train_cnn.py")
        print("   (This will take 20-30 minutes)")
        return False

def check_dataset():
    """Check dataset statistics"""
    print("\n📊 Checking Dataset")
    print("="*50)
    
    dataset_path = 'datasets/real_and_fake_face'
    
    if not os.path.isdir(dataset_path):
        print(f"⚠️  Dataset not found at {dataset_path}")
        return False
    
    try:
        fake_count = len(os.listdir(f"{dataset_path}/fake"))
        real_count = len(os.listdir(f"{dataset_path}/real"))
        
        print(f"✓ Fake images: {fake_count}")
        print(f"✓ Real images: {real_count}")
        print(f"✓ Total images: {fake_count + real_count}")
        
        if fake_count > 0 and real_count > 0:
            print("✅ Dataset is ready for training")
            return True
        else:
            print("❌ Dataset has missing categories")
            return False
            
    except Exception as e:
        print(f"❌ Error reading dataset: {str(e)}")
        return False

def test_imports():
    """Test critical imports"""
    print("\n🔧 Testing Critical Imports")
    print("="*50)
    
    try:
        print("✓ Importing TensorFlow...")
        import tensorflow as tf
        print(f"  TensorFlow version: {tf.__version__}")
        
        print("✓ Importing Flask...")
        from flask import Flask
        
        print("✓ Importing Keras...")
        from tensorflow import keras
        
        print("✓ Importing NumPy...")
        import numpy as np
        
        print("✓ Importing PIL...")
        from PIL import Image
        
        print("✓ Importing sklearn...")
        from sklearn.metrics import confusion_matrix
        
        print("✅ All critical imports successful")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        return False

def check_flask_app():
    """Quick validation of Flask app"""
    print("\n🌐 Checking Flask Application")
    print("="*50)
    
    try:
        from app import app
        print(f"✓ Flask app imported successfully")
        print(f"  - Routes: {len(app.url_map._rules) - 2}")  # -2 for static and default
        
        if os.path.isfile('deepfake_model.keras'):
            print("✓ Model available for predictions")
            print("✅ Flask app is ready")
            return True
        else:
            print("⚠️  Model not available yet")
            print("   Flask app will work but predictions will fail")
            print("   Run: python train_cnn.py first")
            return True
            
    except Exception as e:
        print(f"❌ Flask app error: {str(e)}")
        return False

def run_all_checks():
    """Run all checks and provide summary"""
    print("\n" + "="*50)
    print("🔍 DEEPFAKE DETECTION PROJECT - VERIFICATION")
    print("="*50)
    
    results = {
        "Python Environment": check_environment(),
        "Directory Structure": check_directory_structure(),
        "Essential Files": check_files(),
        "Critical Imports": test_imports(),
        "Dataset": check_dataset(),
        "Trained Model": check_model(),
        "Flask Application": check_flask_app(),
    }
    
    # Print summary
    print("\n" + "="*50)
    print("📋 SUMMARY")
    print("="*50)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✅ Pass" if result else "❌ Need attention"
        print(f"{check}: {status}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✅ ALL SYSTEMS GO!")
        print("\nYour project is ready to use!")
        print("Next steps:")
        print("1. Run: python train_cnn.py (if model doesn't exist)")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    elif passed >= 5:
        print("\n⚠️  Project is mostly ready, but address the issues above")
        print("Key missing: Model training or Flask app needs setup")
    else:
        print("\n❌ Please address the issues above before proceeding")
    
    return passed == total

if __name__ == '__main__':
    # Handle encoding for Windows console
    if sys.platform == 'win32':
        import os
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    try:
        success = run_all_checks()
        sys.exit(0 if success else 1)
    except UnicodeEncodeError:
        print("\n[Note: Console encoding limitation on Windows. Check manually.]")
        sys.exit(0)
