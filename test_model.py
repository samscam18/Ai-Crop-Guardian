import tensorflow as tf
import json
from pathlib import Path

print("Testing your pretrained model...")
print("=" * 60)

# Test 1: Load model
try:
    model = tf.keras.models.load_model('models/saved_models/best_model.h5')
    print("✅ Model loaded successfully!")
    print(f"   Input shape: {model.input_shape}")
    print(f"   Output shape: {model.output_shape}")
    print(f"   Total parameters: {model.count_params():,}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# Test 2: Load class indices
try:
    with open('models/saved_models/class_indices.json', 'r') as f:
        class_indices = json.load(f)
    print(f"\n✅ Class indices loaded!")
    print(f"   Number of classes: {len(class_indices)}")
    print(f"   Classes: {list(class_indices.keys())}")
except Exception as e:
    print(f"❌ Error loading class indices: {e}")
    exit(1)

# Test 3: Check compatibility
num_classes = model.output_shape[-1]
if num_classes == len(class_indices):
    print(f"\n✅ Model and class indices match!")
    print(f"   Both have {num_classes} classes")
else:
    print(f"\n❌ Mismatch!")
    print(f"   Model expects {num_classes} classes")
    print(f"   Class indices has {len(class_indices)} classes")
    exit(1)

print("\n" + "=" * 60)
print("🎉 ALL TESTS PASSED! Your model is ready to use!")
print("=" * 60)