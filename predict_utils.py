"""
Advanced prediction utility for deepfake detection.
This script allows batch prediction and detailed analysis.
"""

import os
import numpy as np
import tensorflow as tf
from pathlib import Path
from tensorflow.keras.preprocessing import image
import json
from datetime import datetime

class DeepfakeDetector:
    def __init__(self, model_path='deepfake_model.keras', img_size=224):
        """
        Initialize the deepfake detector
        
        Args:
            model_path: Path to the trained model
            img_size: Image size expected by model
        """
        self.img_size = img_size
        self.model = None
        self.model_loaded = False
        
        try:
            self.model = tf.keras.models.load_model(model_path)
            self.model_loaded = True
            print(f"✅ Model loaded successfully from {model_path}")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
    
    def predict_image(self, img_path, return_confidence=True):
        """
        Predict if an image is real or fake
        
        Args:
            img_path: Path to image file  
            return_confidence: If True, return confidence score
            
        Returns:
            Dictionary with prediction and confidence
        """
        if not self.model_loaded:
            return {"error": "Model not loaded", "status": "error"}
        
        try:
            # Load and preprocess image
            img = image.load_img(img_path, target_size=(self.img_size, self.img_size))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0
            
            # Make prediction
            prediction = self.model.predict(img_array, verbose=0)[0][0]
            
            # Threshold at 0.5
            is_real = prediction > 0.5
            result = "Real" if is_real else "Fake"
            confidence = prediction if is_real else (1 - prediction)
            
            return {
                "result": result,
                "confidence": float(confidence),
                "raw_prediction": float(prediction),
                "status": "success",
                "filename": os.path.basename(img_path)
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "status": "error",
                "filename": os.path.basename(img_path)
            }
    
    def predict_batch(self, image_folder):
        """
        Predict multiple images from a folder
        
        Args:
            image_folder: Path to folder containing images
            
        Returns:
            List of predictions for each image
        """
        if not self.model_loaded:
            return {"error": "Model not loaded", "status": "error"}
        
        results = []
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}
        
        image_files = [f for f in os.listdir(image_folder) 
                      if os.path.isfile(os.path.join(image_folder, f)) 
                      and Path(f).suffix.lower() in image_extensions]
        
        print(f"\n📊 Processing {len(image_files)} images...\n")
        
        for i, filename in enumerate(image_files, 1):
            filepath = os.path.join(image_folder, filename)
            result = self.predict_image(filepath)
            results.append(result)
            
            if result.get("status") == "success":
                print(f"{i}. ✅ {filename}: {result['result']} ({result['confidence']:.2%})")
            else:
                print(f"{i}. ❌ {filename}: Error - {result.get('error')}")
        
        return results
    
    def print_summary(self, results):
        """Print summary statistics of batch predictions"""
        successful = [r for r in results if r.get("status") == "success"]
        failed = [r for r in results if r.get("status") == "error"]
        
        if not successful:
            print("\n❌ No successful predictions")
            return
        
        real_count = sum(1 for r in successful if r["result"] == "Real")
        fake_count = sum(1 for r in successful if r["result"] == "Fake")
        avg_confidence = np.mean([r["confidence"] for r in successful])
        
        print("\n" + "="*50)
        print("📊 SUMMARY STATISTICS")
        print("="*50)
        print(f"Total Images: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        print(f"\nReal Images: {real_count} ({real_count/len(successful)*100:.1f}%)")
        print(f"Fake Images: {fake_count} ({fake_count/len(successful)*100:.1f}%)")
        print(f"Average Confidence: {avg_confidence:.2%}")
        print("="*50 + "\n")

def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deepfake Detection Utility')
    parser.add_argument('--image', type=str, help='Path to single image')
    parser.add_argument('--folder', type=str, help='Path to folder of images')
    parser.add_argument('--model', type=str, default='deepfake_model.keras',
                       help='Path to model file')
    
    args = parser.parse_args()
    
    detector = DeepfakeDetector(args.model)
    
    if args.image:
        if os.path.exists(args.image):
            result = detector.predict_image(args.image)
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Image not found: {args.image}")
    
    elif args.folder:
        if os.path.isdir(args.folder):
            results = detector.predict_batch(args.folder)
            detector.print_summary(results)
        else:
            print(f"❌ Folder not found: {args.folder}")
    
    else:
        print("Usage:")
        print("  python predict_utils.py --image path/to/image.jpg")
        print("  python predict_utils.py --folder path/to/images/")
        print("  python predict_utils.py --image path/to/image.jpg --model path/to/model.keras")

if __name__ == '__main__':
    main()
