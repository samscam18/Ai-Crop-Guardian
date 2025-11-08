from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import json
from datetime import datetime
import uuid
import time
import google.generativeai as genai
from PIL import Image as PILImage
import sys

# ------------------------------------------------------------------
# ✅ Import Config
# ------------------------------------------------------------------
sys.path.append(str(Path(__file__).parent.parent))
from config.config import Config
from utils.recommendation import DiseaseRecommendationEngine
from utils.weather_api import WeatherDataIntegrator

# ------------------------------------------------------------------
# ✅ Flask App Setup
# ------------------------------------------------------------------
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
CORS(app)

Config.create_directories()

# ------------------------------------------------------------------
# ✅ Load Model
# ------------------------------------------------------------------
print("\n🔍 Initializing Gemini API...")

gemini_model = None
weather_api = None

# Disease classes supported by the system
DISEASE_CLASSES = [
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_healthy'
]

def load_model_safely():
    """Initialize Gemini API"""
    global gemini_model, weather_api
    try:
        if not Config.GEMINI_API_KEY:
            print("❌ GEMINI_API_KEY not found in environment variables")
            print("� Please create a .env file with your GEMINI_API_KEY")
            return False
        
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini API initialized successfully!")
        print(f"✅ Model: gemini-2.0-flash-exp")
        print(f"✅ Supported diseases: {len(DISEASE_CLASSES)} classes")

        weather_api = WeatherDataIntegrator(Config.WEATHER_API_KEY)
        return True

    except Exception as e:
        print(f"❌ Failed to initialize Gemini API: {e}")
        return False

# ------------------------------------------------------------------
# ✅ Helpers
# ------------------------------------------------------------------
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_disease_from_image(img_path):
    """Use Gemini Vision API to analyze plant disease"""
    img = None
    try:
        # Open image using PIL
        img = PILImage.open(img_path)
        
        # Create prompt for Gemini
        prompt = f"""You are an expert plant pathologist and agricultural advisor. Analyze this image carefully.

FIRST: Determine if this image shows a plant leaf (from crops like Pepper, Potato, Tomato, or similar vegetables/fruits).

If the image is NOT a plant leaf (e.g., it's a person, animal, object, landscape, etc.), respond with:
{{
    "is_leaf": false,
    "message": "Incorrect image! Please upload a different image with a correct crop leaf."
}}

If the image IS a plant leaf, analyze it for diseases from these classes:
{', '.join(DISEASE_CLASSES)}

For leaf images, provide a COMPLETE diagnosis and treatment plan in this JSON format:
{{
    "is_leaf": true,
    "disease": "exact_disease_class_name_from_list_above",
    "confidence": confidence_percentage_as_number,
    "reasoning": "detailed explanation of symptoms you observed",
    "fertilizer": "Specific NPK fertilizer recommendation (e.g., 'NPK 19-19-19 at 2kg per acre' or 'High potassium 0-0-50 for disease resistance')",
    "immediate_actions": [
        "3-5 urgent actions to take right now"
    ],
    "organic_treatment": [
        "3-5 organic/natural treatment methods with specific measurements"
    ],
    "chemical_treatment": [
        "3-5 chemical treatments with specific products and dosages"
    ],
    "prevention": [
        "3-5 prevention tips for future"
    ]
}}

IMPORTANT INSTRUCTIONS:
- Be strict about validating if the image is actually a plant leaf
- Use ONLY the exact disease names from the list above
- Provide SPECIFIC fertilizer recommendations (mention NPK ratios, amounts, timing)
- Include practical, actionable advice
- Mention specific product names, dosages, and application schedules where possible
- Consider the stage of disease when recommending treatments"""

        # Generate response from Gemini
        response = gemini_model.generate_content([prompt, img])
        response_text = response.text.strip()
        
        # Close the image immediately after sending to Gemini
        if img:
            img.close()
            img = None
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parse JSON response
        result = json.loads(response_text)
        
        # Check if it's a leaf image
        is_leaf = result.get('is_leaf', True)
        if not is_leaf:
            error_message = result.get('message', 'Incorrect image! Please upload a different image with a correct crop leaf.')
            return None, error_message, None
        
        disease = result.get('disease', 'Unknown')
        confidence = float(result.get('confidence', 0))
        
        # Build recommendation object from Gemini response
        recommendation = {
            'disease': disease.replace('___', ' - ').replace('_', ' '),
            'confidence': confidence,
            'reasoning': result.get('reasoning', ''),
            'fertilizer': result.get('fertilizer', 'Consult local agricultural expert for fertilizer recommendation'),
            'immediate_actions': result.get('immediate_actions', []),
            'treatment': {
                'organic': result.get('organic_treatment', []),
                'chemical': result.get('chemical_treatment', [])
            },
            'prevention': result.get('prevention', [])
        }
        
        # Validate disease is in our list
        if disease not in DISEASE_CLASSES:
            # Try to find closest match
            disease_lower = disease.lower().replace(' ', '_')
            for valid_disease in DISEASE_CLASSES:
                if disease_lower in valid_disease.lower():
                    disease = valid_disease
                    break
            else:
                disease = DISEASE_CLASSES[0]  # Default to first class if no match
        
        return disease, confidence, recommendation
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        # Return None to indicate invalid image
        return None, "Incorrect image! Please upload a different image with a correct crop leaf.", None
    except Exception as e:
        print(f"❌ Gemini API error: {e}")
        # Return None to indicate error
        return None, "Incorrect image! Please upload a different image with a correct crop leaf.", None
    finally:
        # Ensure image is closed even if there's an error
        if img:
            try:
                img.close()
            except:
                pass


def is_likely_leaf(image_path):
    """Simple check if image might be a leaf - using basic image analysis"""
    img = None
    try:
        # Use PIL to do a simple check
        img = PILImage.open(image_path)
        
        # Check if image is reasonable size
        width, height = img.size
        
        # Close the image immediately after checking
        img.close()
        img = None
        
        if width < 50 or height < 50:
            return False
            
        # Check if image has reasonable aspect ratio
        aspect_ratio = max(width, height) / min(width, height)
        if aspect_ratio > 5:  # Too elongated
            return False
        
        # Basic check passed
        return True

    except Exception as e:
        print("⚠️ Leaf detection error:", e)
        return True  # If check fails, allow the image through
    finally:
        # Ensure image is closed even if there's an error
        if img:
            try:
                img.close()
            except:
                pass




# ------------------------------------------------------------------
# ✅ Routes
# ------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/api/chatbot', methods=['POST'])
def chatbot_route():
    """Chatbot endpoint for farmer assistance"""
    if gemini_model is None:
        return jsonify({'success': False, 'error': 'Gemini API not initialized'}), 503
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        # Create comprehensive farmer-focused prompt
        prompt = f"""You are a helpful, friendly agricultural assistant chatbot for Indian farmers. Your name is "Krishi Mitra" (Farm Friend).

CONTEXT:
- You are part of an AI Crop Disease Detection web application
- The app helps farmers identify crop diseases by uploading leaf photos
- You help farmers with: app usage, fertilizer information, disease treatments, farming advice, where to buy supplies

USER QUESTION: {user_message}

INSTRUCTIONS:
1. Answer in simple, easy-to-understand language (assume the farmer may not be highly educated)
2. If the farmer asks in Hindi, respond in Hindi. Otherwise use simple English.
3. Be warm, respectful, and use "🙏" or "Namaste" when appropriate
4. Provide practical, actionable advice
5. When discussing fertilizers:
   - Mention NPK ratios and their meaning
   - Suggest local places to buy (agricultural cooperatives, government stores, local dealers)
   - Mention cheaper alternatives and government schemes
   - Provide approximate prices when relevant
6. When discussing the app:
   - Explain step-by-step how to use it
   - Mention it analyzes leaf photos to detect diseases
   - Explain it provides treatment recommendations
7. Use emojis to make responses friendly: 🌾 🚜 💰 🏪 🌱 📸 etc.
8. If you don't know something specific, suggest contacting local agricultural extension officers
9. Keep responses concise but complete (2-4 paragraphs maximum)
10. Include specific examples and numbers when helpful

IMPORTANT TOPICS TO COVER WHEN RELEVANT:
- How to upload images in the app (go to /upload page)
- NPK fertilizer meanings (N=Nitrogen for leaves, P=Phosphorus for roots, K=Potassium for fruits)
- Where to buy cheap fertilizers (government cooperative societies, Krishi Kendra, local dealers)
- Government schemes like PM-KISAN, Soil Health Card
- Organic alternatives (vermicompost, neem, cow dung manure)
- Disease prevention and treatment
- Best farming practices

Respond naturally and helpfully:"""

        # Generate response using Gemini
        response = gemini_model.generate_content(prompt)
        bot_response = response.text.strip()
        
        return jsonify({
            'success': True,
            'response': bot_response
        })
        
    except Exception as e:
        print(f"❌ Chatbot error: {e}")
        return jsonify({
            'success': False,
            'error': 'Sorry, I encountered an error. Please try again!'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict_route():
    """Main prediction endpoint"""
    if gemini_model is None:
        return jsonify({'success': False, 'error': 'Gemini API not initialized. Please check your GEMINI_API_KEY in .env file'}), 503

    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400

    try:
        # Save uploaded image
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # Predict disease using Gemini AI
        disease, confidence, recommendation = predict_disease_from_image(filepath)
        
        # Check if Gemini detected a non-leaf image
        if disease is None:
            # Add small delay to ensure file is released
            time.sleep(0.1)
            try:
                os.remove(filepath)  # Cleanup
            except Exception as cleanup_error:
                print(f"⚠️ Could not delete file: {cleanup_error}")
            return jsonify({
                'success': False,
                'message': confidence  # confidence contains the error message in this case
            }), 400

        # Basic image validation (backup check)
        if not is_likely_leaf(filepath):
            # Add small delay to ensure file is released
            time.sleep(0.1)
            try:
                os.remove(filepath)  # Optional cleanup
            except Exception as cleanup_error:
                print(f"⚠️ Could not delete file: {cleanup_error}")
            return jsonify({
                'success': False,
                'message': 'Incorrect image! Please upload a different image with a correct crop leaf.'
                }), 400
        
        # Optional: Weather context
        location = request.form.get('location', Config.DEFAULT_LOCATION)
        weather_data = None
        disease_risks = []
        if weather_api:
            weather_data = weather_api.get_current_weather(location)
            disease_risks = weather_api.assess_disease_risk(weather_data)

        # Save to session
        history = session.get('prediction_history', [])
        history.append({
            'timestamp': datetime.now().isoformat(),
            'disease': disease,
            'confidence': confidence
        })
        session['prediction_history'] = history

        return jsonify({
            'success': True,
            'predicted_disease': disease,
            'confidence': round(confidence, 2),
            'recommendation': recommendation,  # Now from Gemini AI!
            'weather': weather_data,
            'disease_risks': disease_risks,
            'image_filename': unique_filename
        })

    except Exception as e:
        print("❌ Prediction error:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

# ------------------------------------------------------------------
# ✅ Run Flask Server
# ------------------------------------------------------------------
if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🌾 CROP DISEASE PREDICTION SERVER STARTING")
    print("=" * 60)
    
    if load_model_safely():
        print("✅ Server ready!")
        print(f"📍 Open http://localhost:{Config.FLASK_PORT}/upload")
        print("=" * 60)
        app.run(host=Config.FLASK_HOST, port=Config.FLASK_PORT, debug=True)
    else:
        print("❌ Failed to initialize Gemini API.")
        print("💡 Make sure you have:")
        print("   1. Created a .env file in the project root")
        print("   2. Added your GEMINI_API_KEY to the .env file")
        print("   3. Get your API key from: https://makersuite.google.com/app/apikey")
