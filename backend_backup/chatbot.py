import re
from datetime import datetime

class CropDiseaseChatbot:
    """Rule-based chatbot for crop disease assistance"""
    
    def __init__(self):
        self.conversation_history = []
        self.intents = self._load_intents()
        
    def _load_intents(self):
        """Load intent patterns and responses"""
        return {
            'greeting': {
                'patterns': [r'\b(hi|hello|hey|greetings)\b'],
                'responses': [
                    "Hello! I'm your crop disease assistant. How can I help you today?",
                    "Hi there! I can help you with crop diseases, treatments, and prevention. What would you like to know?",
                    "Greetings! Ask me anything about crop diseases and I'll do my best to help."
                ]
            },
            'disease_query': {
                'patterns': [
                    r'\b(what is|tell me about|explain|describe)\b.*\b(disease|blight|spot|mold)\b',
                    r'\b(symptoms|signs)\b.*\b(disease)\b'
                ],
                'responses': [
                    "I can help you learn about various crop diseases. Which specific disease would you like to know about? (e.g., Early Blight, Late Blight, Bacterial Spot)"
                ]
            },
            'treatment': {
                'patterns': [
                    r'\b(how to|treatment|cure|control|manage|remedy)\b',
                    r'\b(what should i do|how do i treat)\b'
                ],
                'responses': [
                    "For proper treatment, I need to know which disease you're dealing with. Have you uploaded an image for diagnosis, or do you know the disease name?"
                ]
            },
            'prevention': {
                'patterns': [
                    r'\b(prevent|prevention|avoid|protect)\b',
                    r'\b(stop|keep away)\b'
                ],
                'responses': [
                    "Prevention is key! Common preventive measures include:\n- Crop rotation\n- Proper spacing for air circulation\n- Drip irrigation (avoid overhead watering)\n- Using disease-resistant varieties\n- Regular monitoring\n\nWhich crop are you growing?"
                ]
            },
            'organic': {
                'patterns': [
                    r'\b(organic|natural|non-chemical|eco-friendly)\b',
                    r'\b(neem|compost|baking soda)\b'
                ],
                'responses': [
                    "Organic options include:\n- Neem oil spray (1-2%)\n- Copper-based fungicides\n- Baking soda solution\n- Compost tea\n- Proper cultural practices\n\nWhich disease are you treating?"
                ]
            },
            'weather': {
                'patterns': [
                    r'\b(weather|temperature|humidity|rain|climate)\b'
                ],
                'responses': [
                    "Weather plays a crucial role in disease development:\n- High humidity (>75%) favors fungal diseases\n- Warm temperatures (25-30°C) accelerate disease spread\n- Wet leaves from rain/dew promote infections\n\nWould you like weather-based disease risk assessment for your location?"
                ]
            },
            'pesticide': {
                'patterns': [
                    r'\b(pesticide|fungicide|chemical|spray)\b'
                ],
                'responses': [
                    "Chemical treatments should be used judiciously:\n- Always follow label instructions\n- Wear protective equipment\n- Observe pre-harvest intervals\n- Rotate chemical classes to prevent resistance\n\nWhich disease needs treatment?"
                ]
            },
            'upload': {
                'patterns': [
                    r'\b(upload|scan|image|photo|picture)\b'
                ],
                'responses': [
                    "You can upload an image of the affected plant leaf for AI-powered diagnosis. Use the upload page to:\n1. Take a clear photo of the leaf\n2. Upload the image\n3. Get instant disease identification\n4. Receive treatment recommendations"
                ]
            },
            'help': {
                'patterns': [r'\b(help|assist|support|guide)\b'],
                'responses': [
                    "I can assist you with:\n✓ Disease identification\n✓ Treatment recommendations\n✓ Prevention strategies\n✓ Organic solutions\n✓ Weather-based risk assessment\n✓ Fertilizer recommendations\n\nWhat would you like to know?"
                ]
            }
        }
    
    def get_response(self, user_message, context=None):
        """Generate response to user message"""
        
        # Store in history
        self.conversation_history.append({
            'user': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Clean and lowercase message
        message_lower = user_message.lower().strip()
        
        # Check for context-specific responses
        if context and 'disease' in context:
            response = self._get_contextual_response(message_lower, context)
            if response:
                return {
                    'response': response,
                    'intent': 'contextual',
                    'timestamp': datetime.now().isoformat()
                }
        
        # Match intents
        for intent_name, intent_data in self.intents.items():
            for pattern in intent_data['patterns']:
                if re.search(pattern, message_lower):
                    import random
                    response = random.choice(intent_data['responses'])
                    
                    self.conversation_history[-1]['bot'] = response
                    
                    return {
                        'response': response,
                        'intent': intent_name,
                        'timestamp': datetime.now().isoformat(),
                        'suggestions': self._get_suggestions(intent_name)
                    }
        
        # Default response
        default_response = "I'm not sure I understood that. Could you rephrase? You can ask me about disease symptoms, treatments, prevention methods, or upload an image for diagnosis."
        
        return {
            'response': default_response,
            'intent': 'unknown',
            'timestamp': datetime.now().isoformat(),
            'suggestions': ['Upload an image', 'Common diseases', 'Prevention tips']
        }
    
    def _get_contextual_response(self, message, context):
        """Generate context-aware responses"""
        disease = context.get('disease', '')
        
        if 'treatment' in message or 'cure' in message:
            return f"For {disease}, I recommend checking the detailed treatment plan in your diagnosis results. It includes both organic and chemical options with specific dosages."
        
        if 'prevent' in message:
            return f"To prevent {disease} in the future:\n- Use disease-free seeds\n- Practice crop rotation\n- Maintain proper plant spacing\n- Monitor regularly for early detection"
        
        return None
    
    def _get_suggestions(self, intent):
        """Get follow-up suggestions"""
        suggestions = {
            'greeting': ['How to identify diseases?', 'Upload an image', 'Common treatments'],
            'disease_query': ['Early Blight info', 'Late Blight info', 'Prevention tips'],
            'treatment': ['Organic treatments', 'Chemical options', 'Best practices'],
            'prevention': ['Crop rotation tips', 'Resistant varieties', 'Monitoring schedule'],
            'weather': ['Risk assessment', 'Current conditions', 'Forecast'],
            'upload': ['Start diagnosis', 'How it works', 'Accuracy info']
        }
        return suggestions.get(intent, ['How can you help?', 'Upload image', 'More info'])
