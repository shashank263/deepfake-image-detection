import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from sklearn.metrics import confusion_matrix, classification_report

# ==============================
# 1️⃣ Dataset Path
# ==============================

dataset_dir = os.path.join(os.getcwd(), "datasets", "real_and_fake_face")

img_size = 224
batch_size = 32

# ==============================
# 2️⃣ Data Generators
# ==============================

datagen = ImageDataGenerator(
    rescale=1./255,
    horizontal_flip=True,
    rotation_range=20,
    zoom_range=0.2,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    subset='validation',
    shuffle=False
)

print("Class mapping:", train_generator.class_indices)

# ==============================
# 3️⃣ Model (Transfer Learning)
# ==============================

base_model = MobileNetV2(
    input_shape=(img_size, img_size, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.3)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("\n" + "="*50)
print("🔧 Model Architecture")
print("="*50)
model.summary()

# ==============================
# 4️⃣ Callbacks
# ==============================

early_stop = EarlyStopping(
    monitor='val_loss', 
    patience=5, 
    restore_best_weights=True,
    verbose=1
)

checkpoint = ModelCheckpoint(
    'deepfake_model.keras',
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=3,
    min_lr=1e-7,
    verbose=1
)

# ==============================
# 5️⃣ Training
# ==============================

print("\n" + "="*50)
print("🚀 Starting Model Training")
print("="*50)
print(f"Dataset: {dataset_dir}")
print(f"Image Size: {img_size}x{img_size}")
print(f"Batch Size: {batch_size}")
print("="*50 + "\n")

history = model.fit(
    train_generator,
    epochs=25,
    validation_data=val_generator,
    callbacks=[early_stop, checkpoint, reduce_lr],
    verbose=1
)

# Save final model
model.save('deepfake_model_final.keras')
print("\n✅ Model training complete.")

# ==============================
# 6️⃣ Evaluation
# ==============================

print("\n" + "="*50)
print("📊 Model Evaluation")
print("="*50)

val_loss, val_accuracy = model.evaluate(val_generator)
print(f"✅ Validation Accuracy: {val_accuracy * 100:.2f}%")
print(f"✅ Validation Loss: {val_loss:.4f}")

# Predictions
y_true = val_generator.classes
y_pred_prob = model.predict(val_generator, verbose=0)
y_pred = (y_pred_prob > 0.5).astype(int).reshape(-1)

# Confusion Matrix
cm = confusion_matrix(y_true, y_pred)

print("\n🔍 Confusion Matrix:")
print(cm)
print("\n" + "="*50)

print("\n📄 Classification Report:")
print(classification_report(y_true, y_pred, target_names=['fake', 'real']))

# ==============================
# 7️⃣ Plot Confusion Matrix
# ==============================

plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['fake', 'real'],
            yticklabels=['fake', 'real'],
            cbar_kws={'label': 'Count'})
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.title("Confusion Matrix - Deepfake Detection")
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=100)
plt.show()

print("\n✅ Confusion matrix saved as 'confusion_matrix.png'")

# ==============================
# 8️⃣ Plot Training History
# ==============================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'], label='Train Accuracy')
axes[0].plot(history.history['val_accuracy'], label='Validation Accuracy')
axes[0].set_title('Model Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

# Loss plot
axes[1].plot(history.history['loss'], label='Train Loss')
axes[1].plot(history.history['val_loss'], label='Validation Loss')
axes[1].set_title('Model Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig('training_history.png', dpi=100)
plt.show()

print("✅ Training history saved as 'training_history.png'")
print("\n" + "="*50)
print("🎉 ALL DONE! Model is ready for deployment.")
print("="*50)
