import sys
from pathlib import Path
import cv2
import numpy as np

sys.path.append(str(Path(__file__).parent))

from models.predict import DiseasePredictor

def test_model():
    """Test the new model with various images"""
    
    print("=" * 70)
    print("TESTING NEW MODEL")
    print("=" * 70)
    
    predictor = DiseasePredictor(
        'models/saved_models/best_model.h5',
        'models/saved_models/class_indices.json'
    )
    
    # Test with dataset images
    test_cases = [
        ('data/datasets/Tomato___Early_blight', 'Tomato Early Blight'),
        ('data/datasets/Tomato___healthy', 'Tomato Healthy'),
        ('data/datasets/Potato___Late_blight', 'Potato Late Blight'),
    ]
    
    print("\nTesting with real leaf images:")
    print("-" * 70)
    
    for folder, expected in test_cases:
        folder_path = Path(folder)
        if folder_path.exists():
            # Get first image
            images = list(folder_path.glob('*.jpg')) + list(folder_path.glob('*.JPG'))
            if images:
                test_img = images[0]
                results = predictor.predict(str(test_img))
                
                if results[0].get('error'):
                    print(f"✗ {expected:30s} → ERROR: {results[0]['error']}")
                else:
                    pred = results[0]
                    status = "✓" if expected.lower() in pred['disease'].lower() else "✗"
                    print(f"{status} {expected:30s} → {pred['disease']:30s} ({pred['percentage']:.1f}%)")
    
    print("\n" + "=" * 70)
    print("Test complete! Check accuracy above.")
    print("=" * 70)

if __name__ == '__main__':
    test_model()