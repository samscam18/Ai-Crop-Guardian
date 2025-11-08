# Gemini AI Integration Setup

## ✅ What Changed

The crop disease prediction system now uses **Google Gemini 2.0 Flash** AI model instead of the local TensorFlow model. This provides:

- ✨ More accurate disease detection using advanced AI
- 🚀 No need to train or maintain local ML models
- 🎯 Better handling of various image conditions
- 💡 Natural language reasoning for diagnoses

## 🔑 Getting Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## 📝 Setup Instructions

### Step 1: Add Your API Key

1. Open the `.env` file in the project root (`crop_diesease_system/.env`)
2. Replace `YOUR_GEMINI_API_KEY_HERE` with your actual API key:

```env
GEMINI_API_KEY=AIzaSyC_your_actual_key_here
```

### Step 2: Test the Integration

Run the test script to verify your API key works:

```powershell
.\.venv\Scripts\python.exe test_gemini.py
```

You should see:

```
✅ API Key found
✅ Gemini API initialized successfully!
🎉 Gemini API is working correctly!
```

### Step 3: Start the Server

```powershell
.\.venv\Scripts\python.exe backend\app.py
```

The server will start on http://localhost:5000

### Step 4: Test Disease Prediction

1. Open http://localhost:5000/upload in your browser
2. Upload a plant leaf image
3. The Gemini AI will analyze it and provide:
   - Disease diagnosis
   - Confidence level
   - Treatment recommendations

## 🎯 Supported Diseases

- Pepper Bell: Bacterial Spot, Healthy
- Potato: Early Blight, Late Blight, Healthy
- Tomato: Bacterial Spot, Early Blight, Late Blight, Healthy

## 🔧 Troubleshooting

### "GEMINI_API_KEY not found"

- Make sure you edited the `.env` file
- Check that the file is in the `crop_diesease_system` folder
- Verify there are no extra spaces around the API key

### "API key not valid"

- Double-check you copied the entire API key
- Generate a new API key from Google AI Studio
- Make sure the API key has proper permissions

### Rate Limits

- Free tier: 60 requests per minute
- If you hit limits, wait a minute or upgrade your plan

## 📦 Dependencies Installed

- `google-generativeai` - Official Gemini SDK
- `Pillow` - Image processing

## 💰 Pricing (as of Nov 2025)

Gemini 2.0 Flash is **FREE** up to:

- 1,500 requests per day
- 1 million tokens per day

This is more than enough for development and small-scale usage!

## 🎉 Benefits Over TensorFlow Model

| Feature           | Old (TensorFlow)         | New (Gemini)           |
| ----------------- | ------------------------ | ---------------------- |
| Model Size        | ~500MB                   | Cloud-based            |
| Training Required | Yes                      | No                     |
| Accuracy          | Limited to training data | State-of-the-art AI    |
| Setup Complexity  | High (C++ build tools)   | Simple (API key)       |
| Reasoning         | No explanation           | Provides reasoning     |
| Updates           | Manual retraining        | Automatic improvements |

## 🚀 Next Steps

You can now:

- Test with various plant images
- Customize the disease classes in `backend/app.py`
- Add more plant types
- Integrate with mobile apps
- Deploy to production

Happy farming! 🌾
