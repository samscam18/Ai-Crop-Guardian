import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import json
from config.config import Config
from pathlib import Path


class DiseasePredictor:
    """Handle disease prediction from images"""

    def __init__(self, model_path, class_indices_path, preloaded_model=None):
        """
        Handles disease prediction using a pre-trained model.
        If preloaded_model is provided, uses it instead of reloading from disk.
        """
        if preloaded_model is not None:
            print("🔁 Using preloaded model (skipping reload)...")
            self.model = preloaded_model
        else:
            print("📦 Loading model from file...")
            try:
                self.model = load_model(model_path, compile=False, safe_mode=False)
            except Exception as e1:
                print(f"⚠️ Keras 3 load failed: {e1}")
                print("➡️ Trying TensorFlow legacy load...")
                self.model = tf.keras.models.load_model(model_path, compile=False, safe_mode=False)

        # Load class indices
        import json
        with open(class_indices_path, 'r') as f:
            self.class_indices = json.load(f)
        self.class_labels = list(self.class_indices.keys())

        print(f"✅ Model initialized with {len(self.class_labels)} classes")

        # Load class indices
        with open(class_indices_path, 'r') as f:
            self.class_indices = json.load(f)

        # ✅ Build ordered class list (sorted by index value)
        self.class_names = [cls for cls, idx in sorted(self.class_indices.items(), key=lambda x: x[1])]

        print(f"✅ Model loaded: {model_path}")
        print(f"✅ Classes loaded ({len(self.class_names)}): {self.class_names}")

    def preprocess_image(self, image_path):
        """Preprocess image for EfficientNet model"""
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Cannot read image: {image_path}")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, self.img_size)

        from tensorflow.keras.applications.efficientnet import preprocess_input
        img = preprocess_input(img.astype(np.float32))
        img = np.expand_dims(img, axis=0)
        return img

    def predict(self, image_path, top_k=3):
        """Predict disease from image"""
        img = self.preprocess_image(image_path)

        # Predict
        predictions = self.model.predict(img, verbose=0)[0]

        # ✅ Ensure softmax normalization
        predictions = tf.nn.softmax(predictions).numpy()

        # ✅ Debug info (optional)
        # print("Raw prediction distribution:", predictions)

        # Get top K predictions
        top_indices = np.argsort(predictions)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            results.append({
                'disease': self.class_names[idx],
                'confidence': float(predictions[idx]),
                'percentage': float(predictions[idx] * 100)
            })

        return results
    
   def is_likely_leaf(path, debug=False):
    """
    Returns (is_leaf: bool, score: float, details: dict)
    Score is in [0,1] — higher => more leaf-like.
    """
    details = {}
    try:
        if not os.path.exists(path):
            return False, 0.0, {'error': 'file_not_found'}

        # --- load robustly ---
        img = cv2.imread(path)
        if img is None:
            # fallback reading
            with open(path, 'rb') as f:
                data = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        if img is None:
            return False, 0.0, {'error': 'cannot_read_image'}

        # Normalize size for analysis
        orig_h, orig_w = img.shape[:2]
        small = cv2.resize(img, (256, 256))
        details['orig_shape'] = (orig_h, orig_w)

        # --- color tests (HSV masks) ---
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)

        # green range (tuned)
        low_g = np.array([20, 30, 20])
        high_g = np.array([90, 255, 255])
        mask_g = cv2.inRange(hsv, low_g, high_g)

        # yellow/brown (diseased / variety)
        low_y = np.array([5, 30, 20])
        high_y = np.array([45, 255, 255])
        mask_y = cv2.inRange(hsv, low_y, high_y)

        combined = cv2.bitwise_or(mask_g, mask_y)
        color_ratio = np.sum(combined > 0) / (256 * 256)
        details['color_ratio'] = float(color_ratio)

        # --- texture test (Laplacian) ---
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        texture_var = float(lap.var())
        details['texture_var'] = texture_var

        # --- contour test: find large connected leaf-shaped blobs ---
        # preprocess for contour detection
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # try mask-based threshold if Otsu fails (use color mask)
        if np.sum(th) < 10:
            th = cv2.threshold(combined, 0, 255, cv2.THRESH_BINARY)[1]

        # Morphology to close holes
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
        th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # analyze top contour
        if contours:
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            big = contours[0]
            area = cv2.contourArea(big)
            area_ratio = area / (256 * 256)
            hull = cv2.convexHull(big)
            hull_area = cv2.contourArea(hull) if hull is not None else 0.0
            solidity = area / hull_area if hull_area > 1e-6 else 0.0

            x,y,w,h = cv2.boundingRect(big)
            aspect = float(w)/float(h) if h>0 else 0.0

            details.update({
                'contour_found': True,
                'contour_area': float(area),
                'area_ratio': float(area_ratio),
                'solidity': float(solidity),
                'aspect_ratio': float(aspect),
                'contours_count': len(contours)
            })
        else:
            details.update({
                'contour_found': False,
                'contour_area': 0.0,
                'area_ratio': 0.0,
                'solidity': 0.0,
                'aspect_ratio': 0.0,
                'contours_count': 0
            })

        # --- color diversity and saturation check ---
        sat = hsv[:,:,1]
        sat_mean = float(np.mean(sat))
        details['sat_mean'] = sat_mean
        details['std_color'] = float(np.std(small))

        # --- scoring: combine metrics (weights can be tuned) ---
        # heuristic scoring in [0,1]
        score = 0.0

        # color contribution (favor > ~5% colored leaf pixels)
        color_score = min(max((color_ratio - 0.03) / 0.2, 0.0), 1.0)    # map [0.03..0.23] -> [0..1]
        score += 0.45 * color_score

        # area/contour contribution (need decent blob)
        area_score = min(max((details['area_ratio'] - 0.02) / 0.45, 0.0), 1.0)  # map area_ratio
        score += 0.25 * area_score

        # solidity (leaf tends to have higher solidity)
        solidity_score = min(max((details['solidity'] - 0.4) / 0.6, 0.0), 1.0)
        score += 0.10 * solidity_score

        # texture (not completely smooth)
        tex_score = min(max((texture_var - 10) / 500, 0.0), 1.0)
        score += 0.10 * tex_score

        # color diversity
        colstd_score = min(max((details['std_color'] - 8) / 40, 0.0), 1.0)
        score += 0.10 * colstd_score

        # clamp to [0,1]
        score = max(0.0, min(1.0, score))
        details['score'] = float(score)

        if debug:
            # optionally save intermediate images or print details
            print("▸ leaf detection details:", details)

        # Decide threshold for acceptance (tuneable)
        # If area_ratio is very large, allow lower color_score
        accept_threshold = 0.20
        if details['area_ratio'] > 0.2:
            accept_threshold = 0.12

        is_leaf = score >= accept_threshold and details['contour_found'] is True

        return bool(is_leaf), float(score), details

    except Exception as e:
        return False, 0.0, {'error': str(e)}




    def predict_with_context(self, image_path, weather_data=None, soil_data=None):
        """Enhanced prediction with environmental context"""
        base_predictions = self.predict(image_path)

        if weather_data or soil_data:
            adjusted_predictions = self._adjust_predictions(
                base_predictions, weather_data, soil_data
            )
            return adjusted_predictions

        return base_predictions

    def _adjust_predictions(self, predictions, weather_data, soil_data):
        """Adjust predictions based on environmental context"""
        adjusted = predictions.copy()

        if weather_data:
            humidity = weather_data.get('humidity', 50)
            temp = weather_data.get('temperature', 25)

            for pred in adjusted:
                disease = pred['disease']

                if 'blight' in disease.lower() and humidity > 70:
                    pred['confidence'] = min(pred['confidence'] * 1.1, 1.0)
                elif 'virus' in disease.lower() and temp > 30:
                    pred['confidence'] = min(pred['confidence'] * 1.05, 1.0)

        # Re-normalize confidences
        total = sum(p['confidence'] for p in adjusted)
        for pred in adjusted:
            pred['confidence'] /= total
            pred['percentage'] = pred['confidence'] * 100

        return sorted(adjusted, key=lambda x: x['confidence'], reverse=True)


if __name__ == '__main__':
    print("Testing Disease Predictor...")
    print("=" * 60)

    try:
        model_path = os.path.join(Config.MODEL_DIR, 'best_model.h5')
        class_indices_path = os.path.join(Config.MODEL_DIR, 'class_indices.json')

        predictor = DiseasePredictor(model_path, class_indices_path)

        print("\n✅ Prediction engine initialized successfully!")
        print(f"   Ready to predict {len(predictor.class_indices)} disease classes")
        print("\n" + "=" * 60)
        print("🎉 Predictor is ready to use!")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
