"""
Configuration file for deepfake detection project
"""

# Model Configuration
MODEL_CONFIG = {
    'name': 'MobileNetV2-CustomDense',
    'base_model': 'MobileNetV2',
    'img_size': 224,
    'batch_size': 32,
    'epochs': 25,
    'validation_split': 0.2,
}

# Training Configuration
TRAINING_CONFIG = {
    'optimizer': 'adam',
    'loss': 'binary_crossentropy',
    'metrics': ['accuracy'],
    'callbacks': {
        'early_stopping': {
            'monitor': 'val_loss',
            'patience': 5,
            'restore_best_weights': True,
        },
        'model_checkpoint': {
            'monitor': 'val_loss',
            'save_best_only': True,
            'filename': 'deepfake_model.keras'
        },
        'reduce_lr': {
            'monitor': 'val_loss',
            'factor': 0.5,
            'patience': 3,
            'min_lr': 1e-7,
        }
    }
}

# Data Augmentation Configuration
AUGMENTATION_CONFIG = {
    'rescale': 1./255,
    'horizontal_flip': True,
    'rotation_range': 20,
    'zoom_range': 0.2,
    'width_shift_range': 0.1,
    'height_shift_range': 0.1,
    'shear_range': 0.1,
}

# Flask Configuration
FLASK_CONFIG = {
    'DEBUG': False,
    'UPLOAD_FOLDER': 'static/uploads',
    'MAX_CONTENT_LENGTH': 10 * 1024 * 1024,  # 10MB max file size
    'ALLOWED_EXTENSIONS': {'jpg', 'jpeg', 'png', 'gif', 'bmp'},
}

# Dataset Configuration
DATASET_CONFIG = {
    'path': 'datasets/real_and_fake_face',
    'classes': ['fake', 'real'],
    'expected_fake_count': 960,
    'expected_real_count': 1081,
}

# Prediction Configuration
PREDICTION_CONFIG = {
    'confidence_threshold': 0.5,
    'real_confidence_min': 0.95,
    'fake_confidence_min': 0.95,
}
