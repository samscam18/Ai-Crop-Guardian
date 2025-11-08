import unittest
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import tempfile
import shutil

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.config import Config
from data.preprocessing import ImagePreprocessor
from models.predict import DiseasePredictor
from utils.recommendation import DiseaseRecommendationEngine
from utils.weather_api import WeatherDataIntegrator

class TestImagePreprocessing(unittest.TestCase):
    """Test image preprocessing functionality"""
    
    def setUp(self):
        self.preprocessor = ImagePreprocessor(img_size=(224, 224))
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def create_test_image(self, filename='test.jpg'):
        """Create a test image"""
        img = Image.new('RGB', (400, 400), color='green')
        path = Path(self.temp_dir) / filename
        img.save(path)
        return str(path)
    
    def test_load_and_preprocess(self):
        """Test image loading and preprocessing"""
        img_path = self.create_test_image()
        processed = self.preprocessor.load_and_preprocess(img_path)
        
        self.assertEqual(processed.shape, (224, 224, 3))
        self.assertTrue(processed.min() >= 0 and processed.max() <= 1)
    
    def test_batch_preprocessing(self):
        """Test batch image preprocessing"""
        img_paths = [self.create_test_image(f'test{i}.jpg') for i in range(3)]
        batch = self.preprocessor.preprocess_batch(img_paths)
        
        self.assertEqual(batch.shape, (3, 224, 224, 3))

class TestRecommendationEngine(unittest.TestCase):
    """Test recommendation engine"""
    
    def test_get_recommendation(self):
        """Test getting disease recommendations"""
        rec = DiseaseRecommendationEngine.get_recommendation(
            'Tomato_Early_blight',
            confidence=0.85
        )
        
        self.assertIn('disease', rec)
        self.assertIn('treatment_plan', rec)
        self.assertIn('prevention', rec)
        self.assertEqual(rec['disease'], 'Tomato_Early_blight')
    
    def test_severity_determination(self):
        """Test severity level calculation"""
        severity_high = DiseaseRecommendationEngine._determine_severity(0.95, None)
        severity_low = DiseaseRecommendationEngine._determine_severity(0.65, None)
        
        self.assertIn(severity_high, ['medium-high', 'high'])
        self.assertEqual(severity_low, 'low')
    
    def test_unknown_disease(self):
        """Test handling of unknown diseases"""
        rec = DiseaseRecommendationEngine.get_recommendation(
            'Unknown_Disease',
            confidence=0.80
        )
        
        self.assertEqual(rec['severity'], 'uncertain')
        self.assertIn('recommendation', rec)

class TestWeatherIntegration(unittest.TestCase):
    """Test weather API integration"""
    
    def setUp(self):
        self.weather_api = WeatherDataIntegrator('test_api_key')
    
    def test_mock_weather_data(self):
        """Test mock weather data generation"""
        data = self.weather_api._get_mock_weather()
        
        self.assertIn('temperature', data)
        self.assertIn('humidity', data)
        self.assertIn('pressure', data)
    
    def test_disease_risk_assessment(self):
        """Test disease risk assessment"""
        weather_data = {
            'temperature': 28,
            'humidity': 85,
            'pressure': 1013
        }
        
        risks = self.weather_api.assess_disease_risk(weather_data)
        
        self.assertIsInstance(risks, list)
        if risks:
            self.assertIn('type', risks[0])
            self.assertIn('risk_level', risks[0])

class TestConfig(unittest.TestCase):
    """Test configuration"""
    
    def test_config_values(self):
        """Test configuration values"""
        self.assertEqual(Config.IMG_SIZE, (224, 224))
        self.assertIsInstance(Config.DISEASE_CLASSES, list)
        self.assertTrue(len(Config.DISEASE_CLASSES) > 0)
    
    def test_directory_creation(self):
        """Test directory creation"""
        Config.create_directories()
        
        self.assertTrue(Config.DATA_DIR.exists())
        self.assertTrue(Config.MODEL_DIR.exists())
        self.assertTrue(Config.UPLOAD_DIR.exists())

def run_all_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestImagePreprocessing))
    suite.addTests(loader.loadTestsFromTestCase(TestRecommendationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestWeatherIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)

