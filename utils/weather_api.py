import requests
from datetime import datetime

class WeatherDataIntegrator:
    """Integrate real-time weather data"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5"
        
    def get_current_weather(self, location):
        """Get current weather data"""
        if not self.api_key:
            return self._get_mock_weather()
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'location': location,
                'temperature': round(data['main']['temp'], 1),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].title(),
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'feels_like': round(data['main']['feels_like'], 1),
                'timestamp': datetime.now().isoformat(),
                'success': True
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            return self._get_mock_weather()
    
    def get_forecast(self, location, days=3):
        """Get weather forecast"""
        if not self.api_key:
            return []
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': days * 8  # 3-hour intervals
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast = []
            for item in data['list']:
                forecast.append({
                    'date': item['dt_txt'],
                    'temperature': round(item['main']['temp'], 1),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].title(),
                    'rain_probability': item.get('pop', 0) * 100  # Probability of precipitation
                })
            
            return forecast
        except Exception as e:
            print(f"Forecast API Error: {e}")
            return []
    
    def assess_disease_risk(self, weather_data):
        """Assess disease risk based on weather conditions"""
        if not weather_data.get('success'):
            return []
        
        temp = weather_data.get('temperature', 25)
        humidity = weather_data.get('humidity', 50)
        
        risks = []
        
        # Fungal disease risk (Blights)
        if humidity > 80 and 15 < temp < 30:
            risks.append({
                'type': 'Fungal Diseases (Early & Late Blight)',
                'risk_level': 'HIGH',
                'reason': f'High humidity ({humidity}%) and moderate temperature ({temp}°C) create ideal conditions for fungal growth',
                'preventive_action': 'Apply preventive fungicide immediately. Improve air circulation. Avoid overhead watering.',
                'diseases': ['Tomato Late Blight', 'Potato Late Blight', 'Early Blight']
            })
        elif humidity > 70 and 20 < temp < 30:
            risks.append({
                'type': 'Fungal Diseases',
                'risk_level': 'MEDIUM',
                'reason': f'Elevated humidity ({humidity}%) favorable for fungal spores',
                'preventive_action': 'Monitor plants closely. Consider preventive fungicide application.',
                'diseases': ['Early Blight', 'Late Blight']
            })
        
        # Bacterial disease risk
        if temp > 28 and humidity > 65:
            risks.append({
                'type': 'Bacterial Diseases',
                'risk_level': 'MEDIUM',
                'reason': f'Warm ({temp}°C) and humid ({humidity}%) conditions favor bacterial growth',
                'preventive_action': 'Avoid overhead watering. Use drip irrigation. Sanitize tools regularly.',
                'diseases': ['Bacterial Spot']
            })
        
        # Heat stress
        if temp > 35:
            risks.append({
                'type': 'Heat Stress',
                'risk_level': 'HIGH',
                'reason': f'Very high temperature ({temp}°C) causing plant stress',
                'preventive_action': 'Increase irrigation frequency. Provide shade if possible. Apply mulch.',
                'diseases': ['General stress increases disease susceptibility']
            })
        
        # Cold stress
        if temp < 10:
            risks.append({
                'type': 'Cold Stress',
                'risk_level': 'MEDIUM',
                'reason': f'Low temperature ({temp}°C) slowing plant growth',
                'preventive_action': 'Protect plants from frost. Reduce watering frequency.',
                'diseases': ['Slowed growth increases disease window']
            })
        
        # Low risk / ideal conditions
        if not risks and 18 <= temp <= 28 and 40 <= humidity <= 70:
            risks.append({
                'type': 'Optimal Growing Conditions',
                'risk_level': 'LOW',
                'reason': f'Temperature ({temp}°C) and humidity ({humidity}%) are in ideal range',
                'preventive_action': 'Continue regular monitoring. Maintain good cultural practices.',
                'diseases': []
            })
        
        return risks
    
    @staticmethod
    def _get_mock_weather():
        """Return mock weather data when API is unavailable"""
        return {
            'location': 'Unknown',
            'temperature': 28,
            'humidity': 65,
            'pressure': 1013,
            'description': 'Partly Cloudy',
            'wind_speed': 3.5,
            'clouds': 40,
            'feels_like': 30,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'note': 'Weather API unavailable - using sample data'
        }

# Test the weather API
if __name__ == '__main__':
    import sys
    sys.path.append('..')
    from config.config import Config
    
    print("Testing Weather Integration...")
    print("=" * 60)
    
    weather_api = WeatherDataIntegrator(Config.WEATHER_API_KEY)
    
    # Test current weather
    print("\n[1/2] Getting current weather...")
    weather = weather_api.get_current_weather('Bengaluru, India')
    
    print(f"\n📍 Location: {weather['location']}")
    print(f"🌡️  Temperature: {weather['temperature']}°C (feels like {weather['feels_like']}°C)")
    print(f"💧 Humidity: {weather['humidity']}%")
    print(f"☁️  Conditions: {weather['description']}")
    print(f"💨 Wind: {weather['wind_speed']} m/s")
    
    # Test disease risk
    print("\n[2/2] Assessing disease risks...")
    risks = weather_api.assess_disease_risk(weather)
    
    if risks:
        print(f"\nFound {len(risks)} risk factor(s):")
        for risk in risks:
            print(f"\n⚠️  {risk['type']} - {risk['risk_level']}")
            print(f"   Reason: {risk['reason']}")
            print(f"   Action: {risk['preventive_action']}")
    
    print("\n" + "=" * 60)
    print("✅ Weather integration ready!")