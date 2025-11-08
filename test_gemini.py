"""
Test script to verify Gemini API integration for disease prediction
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test if Gemini API is properly configured"""
    print("\n" + "=" * 60)
    print("🧪 Testing Gemini API Integration")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("❌ GEMINI_API_KEY not found or not set in .env file")
        print("💡 Please edit the .env file and add your actual Gemini API key")
        print("💡 Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    print(f"✅ API Key found (length: {len(api_key)} characters)")
    
    try:
        # Initialize Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini API initialized successfully!")
        
        # Test with a simple text prompt
        print("\n🔍 Testing text generation...")
        response = model.generate_content("Say 'Hello, I'm ready to analyze plant diseases!'")
        print(f"✅ Response: {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 Gemini API is working correctly!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error testing Gemini API: {e}")
        print("💡 Make sure your API key is valid")
        return False

if __name__ == '__main__':
    test_gemini_api()
