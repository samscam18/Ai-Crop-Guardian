class DiseaseRecommendationEngine:
    """Generate treatment recommendations for diseases"""
    
    # Complete disease knowledge base
    DISEASE_INFO = {
        'Tomato___Early_blight': {
            'description': 'Fungal disease causing dark spots with concentric rings on leaves',
            'symptoms': [
                'Dark brown spots with concentric rings (target-like pattern)',
                'Yellow halo around spots',
                'Lower leaves affected first',
                'Leaf drop and defoliation',
                'Small black lesions on stems'
            ],
            'treatment': {
                'organic': [
                    'Remove infected leaves immediately and destroy',
                    'Apply neem oil spray (2ml/L water) weekly',
                    'Use copper-based fungicides (Bordeaux mixture)',
                    'Improve air circulation between plants',
                    'Apply baking soda solution (1 tbsp/gallon)',
                    'Use compost tea as foliar spray'
                ],
                'chemical': [
                    'Chlorothalonil 500g/L at 2ml/L water',
                    'Mancozeb 75% WP at 2g/L',
                    'Azoxystrobin 250g/L at 1ml/L',
                    'Apply every 7-10 days during infection',
                    'Alternate fungicides to prevent resistance'
                ]
            },
            'prevention': [
                'Practice 3-year crop rotation',
                'Use drip irrigation instead of overhead watering',
                'Mulch to prevent soil splash onto leaves',
                'Plant resistant varieties if available',
                'Maintain proper plant spacing (45-60cm)',
                'Remove crop debris after harvest',
                'Avoid working with wet plants'
            ],
            'fertilizer': 'Balanced NPK 19-19-19, increase potassium for disease resistance'
        },
        
        'Tomato___Late_blight': {
            'description': 'Devastating fungal disease that can destroy entire crops within days',
            'symptoms': [
                'Water-soaked lesions on leaves',
                'White fuzzy mold on leaf undersides',
                'Rapid spread in cool, wet conditions',
                'Brown spots on stems',
                'Fruit rot with greasy appearance',
                'Entire plant collapse possible'
            ],
            'treatment': {
                'organic': [
                    '🚨 URGENT: Remove and burn infected plants immediately',
                    'Apply copper fungicide at first sign',
                    'Increase plant spacing drastically',
                    'Stop all overhead irrigation',
                    'Apply Bacillus subtilis biological fungicide',
                    'Remove volunteer plants from previous season'
                ],
                'chemical': [
                    'Metalaxyl + Mancozeb at 2.5g/L (systemic action)',
                    'Cymoxanil + Famoxadone at 2ml/L',
                    'Dimethomorph 50% WP at 1g/L',
                    'Apply every 5-7 days during outbreak',
                    'Use preventive sprays in cool, humid weather'
                ]
            },
            'prevention': [
                'Use certified disease-free seeds only',
                'Monitor weather forecasts (high risk at 15-25°C + rain)',
                'Apply preventive fungicides before symptoms',
                'Destroy volunteer potato and tomato plants',
                'Plant in well-drained areas',
                'Avoid planting near potatoes',
                'Consider resistant varieties'
            ],
            'fertilizer': 'Reduce nitrogen, increase phosphorus (0-20-20) and potassium for stronger plants'
        },
        
        'Tomato___Bacterial_spot': {
            'description': 'Bacterial disease causing dark spots on leaves, stems, and fruit',
            'symptoms': [
                'Small dark spots with yellow halos',
                'Spots may merge to form large lesions',
                'Leaf edges turn yellow and die',
                'Defoliation in severe cases',
                'Raised spots on fruit',
                'Reduced fruit quality'
            ],
            'treatment': {
                'organic': [
                    'Remove and destroy infected plant parts',
                    'Apply copper-based bactericides (copper hydroxide)',
                    'Avoid working with plants when wet',
                    'Sanitize all tools with 10% bleach solution',
                    'Improve air circulation',
                    'Remove weeds that harbor bacteria'
                ],
                'chemical': [
                    'Copper hydroxide at 2g/L water',
                    'Streptomycin sulfate (where legally permitted)',
                    'Copper + Mancozeb combination products',
                    'Apply weekly during wet weather',
                    'Begin applications preventively'
                ]
            },
            'prevention': [
                'Use resistant varieties (check local recommendations)',
                'Use certified disease-free seeds',
                'Avoid overhead irrigation completely',
                'Disinfect tools between plants',
                'Remove crop debris immediately after harvest',
                '2-3 year rotation away from tomatoes/peppers',
                'Control insect vectors'
            ],
            'fertilizer': 'Balanced NPK with adequate calcium (reduces susceptibility)'
        },
        
        'Tomato___healthy': {
            'description': '✅ Your tomato plant appears healthy with no visible disease symptoms!',
            'symptoms': [
                'Vibrant green leaves',
                'No spots, lesions, or discoloration',
                'Normal growth pattern',
                'Good leaf structure'
            ],
            'treatment': {
                'organic': [
                    '✓ No treatment needed',
                    'Continue regular care routine',
                    'Monitor weekly for any changes',
                    'Maintain good cultural practices'
                ],
                'chemical': []
            },
            'prevention': [
                'Continue current care practices',
                'Regular monitoring and inspection',
                'Proper watering (1-2 inches per week)',
                'Maintain balanced nutrition',
                'Good air circulation',
                'Mulch around plants',
                'Practice crop rotation'
            ],
            'fertilizer': 'Continue balanced fertilization (10-10-10 or 5-10-10 NPK)'
        },
        
        'Potato___Early_blight': {
            'description': 'Common fungal disease affecting potato foliage and tubers',
            'symptoms': [
                'Target-like spots with concentric rings',
                'Lower, older leaves affected first',
                'Brown lesions on stems',
                'Yellowing around lesions',
                'Progressive upward movement',
                'Tuber infection at harvest'
            ],
            'treatment': {
                'organic': [
                    'Remove infected lower leaves',
                    'Apply baking soda spray (1 tbsp/gallon water)',
                    'Use copper fungicide weekly',
                    'Apply compost tea as foliar spray',
                    'Maintain adequate soil moisture',
                    'Improve plant nutrition'
                ],
                'chemical': [
                    'Chlorothalonil 72% WP at 2g/L',
                    'Azoxystrobin 23% SC at 1ml/L',
                    'Mancozeb at labeled rates',
                    'Apply every 7-10 days',
                    'Begin at first symptom appearance'
                ]
            },
            'prevention': [
                'Use certified seed potatoes',
                'Hill up soil around plants',
                'Provide adequate nitrogen during growth',
                'Water at base, not overhead',
                'Remove volunteer potatoes',
                'Destroy crop residue after harvest',
                '3-4 year crop rotation'
            ],
            'fertilizer': 'NPK 10-10-20, adequate nitrogen during vegetative growth'
        },
        
        'Potato___Late_blight': {
            'description': 'Serious disease that caused the Irish Potato Famine - can destroy crops rapidly',
            'symptoms': [
                'Water-soaked dark lesions on leaves',
                'White fungal growth on leaf undersides',
                'Brown-black stems',
                'Rapid plant collapse',
                'Tuber rot with reddish-brown flesh',
                'Foul odor from rotting tubers'
            ],
            'treatment': {
                'organic': [
                    '🚨 EMERGENCY ACTION REQUIRED',
                    'Remove entire infected plants within 24 hours',
                    'Do NOT compost infected material - burn it',
                    'Apply copper fungicide to surrounding plants',
                    'Harvest healthy tubers immediately if possible',
                    'Hill up soil to protect tubers'
                ],
                'chemical': [
                    'Metalaxyl-based systemic fungicides',
                    'Cymoxanil at 2ml/L for curative action',
                    'Chlorothalonil for protectant action',
                    'Apply every 5 days during outbreaks',
                    'Tank mix systemic + protectant'
                ]
            },
            'prevention': [
                'Use resistant varieties (check local recommendations)',
                'Destroy volunteer plants and cull piles',
                'Monitor weather (high risk: 15-25°C + high humidity)',
                'Apply preventive sprays before symptoms',
                'Hill plants properly',
                'Ensure good drainage',
                'Early harvest if disease appears nearby'
            ],
            'fertilizer': 'Balanced nutrition, avoid excess nitrogen which increases susceptibility'
        },
        
        'Potato___healthy': {
            'description': '✅ Your potato plant is healthy and disease-free!',
            'symptoms': [
                'Dark green, vigorous foliage',
                'No lesions or spots',
                'Normal plant structure',
                'Good tuber development expected'
            ],
            'treatment': {
                'organic': [
                    '✓ No treatment necessary',
                    'Continue monitoring',
                    'Maintain current practices'
                ],
                'chemical': []
            },
            'prevention': [
                'Continue proper hilling',
                'Consistent watering',
                'Monitor for pests',
                'Maintain nutrition',
                'Regular inspection',
                'Good weed control'
            ],
            'fertilizer': 'Continue balanced program, increase potassium as tubers develop'
        },
        
        'Pepper_bell___Bacterial_spot': {
            'description': 'Bacterial disease causing spots on leaves and fruit of pepper plants',
            'symptoms': [
                'Small, dark spots on leaves',
                'Yellow halos around spots',
                'Leaf drop and defoliation',
                'Raised spots on fruit',
                'Fruit may become unmarketable',
                'Reduced yields'
            ],
            'treatment': {
                'organic': [
                    'Remove infected leaves promptly',
                    'Apply copper bactericide (copper hydroxide)',
                    'Avoid overhead watering',
                    'Sanitize hands and tools frequently',
                    'Improve air circulation',
                    'Remove plant debris'
                ],
                'chemical': [
                    'Copper hydroxide at 2-3g/L',
                    'Fixed copper products',
                    'Apply weekly during wet periods',
                    'Begin preventively at transplanting',
                    'Continue through fruit set'
                ]
            },
            'prevention': [
                'Use disease-free transplants',
                'Hot water seed treatment (50°C for 25 min)',
                'Drip irrigation only',
                'Wide plant spacing (45-60cm)',
                '3-year rotation',
                'Control weeds',
                'Disinfect stakes and cages'
            ],
            'fertilizer': 'Balanced NPK, adequate calcium for fruit quality'
        },
        
        'Pepper_bell___healthy': {
            'description': '✅ Your pepper plant is healthy with no disease symptoms!',
            'symptoms': [
                'Dark green leaves',
                'No spots or lesions',
                'Good fruit set',
                'Normal growth'
            ],
            'treatment': {
                'organic': [
                    '✓ Continue current care',
                    'Regular monitoring',
                    'Maintain practices'
                ],
                'chemical': []
            },
            'prevention': [
                'Consistent watering',
                'Proper fertilization',
                'Pest monitoring',
                'Good air flow',
                'Mulching',
                'Support plants as needed'
            ],
            'fertilizer': 'Balanced NPK, increase potassium during fruiting (5-10-10)'
        }
    }
    
    @classmethod
    def get_recommendation(cls, disease_code, confidence):
        """Get comprehensive recommendation for a disease"""
        
        # Check if we have info for this disease
        if disease_code not in cls.DISEASE_INFO:
            return cls._generic_recommendation(disease_code, confidence)
        
        info = cls.DISEASE_INFO[disease_code]
        
        # Determine severity based on confidence
        severity = cls._determine_severity(disease_code, confidence)
        
        # Clean disease name for display
        disease_name = disease_code.replace('___', ' - ').replace('_', ' ')
        
        return {
            'disease': disease_name,
            'disease_code': disease_code,
            'confidence': confidence,
            'severity': severity,
            'description': info['description'],
            'symptoms': info['symptoms'],
            'treatment': info['treatment'],
            'prevention': info['prevention'],
            'fertilizer': info['fertilizer'],
            'immediate_actions': cls._get_immediate_actions(severity, info, disease_code),
            'monitoring': cls._get_monitoring_plan(severity),
            'economic_impact': cls._get_economic_impact(severity)
        }
    
    @classmethod
    def _determine_severity(cls, disease_code, confidence):
        """Determine disease severity"""
        
        # Healthy plants have no severity
        if 'healthy' in disease_code.lower():
            return 'none'
        
        # Late blight is always serious
        if 'Late_blight' in disease_code:
            if confidence > 0.7:
                return 'high'
            elif confidence > 0.5:
                return 'medium'
            else:
                return 'uncertain'
        
        # Other diseases based on confidence
        if confidence < 0.6:
            return 'uncertain'
        elif confidence < 0.75:
            return 'low'
        elif confidence < 0.90:
            return 'medium'
        else:
            return 'high'
    
    @classmethod
    def _get_immediate_actions(cls, severity, info, disease_code):
        """Get immediate action items based on severity"""
        
        if 'healthy' in disease_code.lower():
            return [
                '✓ Plant is healthy - no action needed',
                '✓ Continue regular monitoring',
                '✓ Maintain good cultural practices'
            ]
        
        if severity == 'high':
            actions = [
                '🚨 URGENT: Inspect entire field immediately',
                '🚨 Isolate affected area to prevent spread',
                '🚨 Begin treatment within 24 hours'
            ]
            if info['treatment']['chemical']:
                actions.extend(info['treatment']['chemical'][:2])
            return actions
            
        elif severity == 'medium':
            return [
                '⚠️ Monitor closely over next 3 days',
                '⚠️ Begin treatment as soon as possible',
                info['treatment']['organic'][0],
                info['treatment']['organic'][1] if len(info['treatment']['organic']) > 1 else ''
            ]
        elif severity == 'low':
            return [
                '✓ Early detection - good timing',
                '✓ Preventive measures should be sufficient',
                info['treatment']['organic'][0]
            ]
        else:
            return [
                '❓ Confidence is low - consider getting expert confirmation',
                'Take clear photos of symptoms',
                'Monitor for symptom progression'
            ]
    
    @classmethod
    def _get_monitoring_plan(cls, severity):
        """Get monitoring recommendations"""
        if severity == 'high':
            return 'Daily inspection required. Document spread with photos. Check weather forecasts.'
        elif severity == 'medium':
            return 'Check every 2-3 days. Monitor new growth areas and adjacent plants.'
        elif severity == 'low':
            return 'Weekly inspection sufficient. Watch for symptom development.'
        elif severity == 'none':
            return 'Continue regular weekly monitoring for any changes.'
        else:
            return 'Daily monitoring until diagnosis is confirmed by expert.'
    
    @classmethod
    def _get_economic_impact(cls, severity):
        """Estimate economic impact"""
        impacts = {
            'high': {
                'yield_loss': '30-70%',
                'quality_impact': 'Severe - unmarketable produce',
                'recommendation': 'Immediate intervention critical. Consider crop insurance.'
            },
            'medium': {
                'yield_loss': '10-30%',
                'quality_impact': 'Moderate - reduced market value',
                'recommendation': 'Timely treatment will minimize losses.'
            },
            'low': {
                'yield_loss': '<10%',
                'quality_impact': 'Minimal if treated promptly',
                'recommendation': 'Early intervention will prevent spread.'
            },
            'none': {
                'yield_loss': '0%',
                'quality_impact': 'No impact - plant is healthy',
                'recommendation': 'Continue preventive care for best yields.'
            },
            'uncertain': {
                'yield_loss': 'Unknown until confirmed',
                'quality_impact': 'To be determined',
                'recommendation': 'Get expert confirmation before treatment.'
            }
        }
        return impacts.get(severity, impacts['uncertain'])
    
    @classmethod
    def _generic_recommendation(cls, disease_code, confidence):
        """Generic recommendation for unlisted diseases"""
        disease_name = disease_code.replace('___', ' - ').replace('_', ' ')
        
        return {
            'disease': disease_name,
            'disease_code': disease_code,
            'confidence': confidence,
            'severity': 'uncertain',
            'description': 'Detailed information not available in our database.',
            'symptoms': ['Consult local agricultural expert for identification'],
            'treatment': {
                'organic': [
                    'Isolate affected plants',
                    'Document symptoms with photos',
                    'Contact agricultural extension office'
                ],
                'chemical': []
            },
            'prevention': [
                'General good agricultural practices',
                'Regular monitoring',
                'Proper sanitation'
            ],
            'fertilizer': 'Maintain balanced nutrition as per soil test',
            'immediate_actions': [
                'Take clear photos from multiple angles',
                'Isolate affected plants if possible',
                'Contact local agricultural extension service',
                'Do not apply treatments until diagnosis confirmed'
            ],
            'monitoring': 'Daily monitoring and documentation until expert consultation',
            'economic_impact': {
                'yield_loss': 'Unknown',
                'quality_impact': 'Requires expert assessment',
                'recommendation': 'Seek professional agricultural advice immediately'
            }
        }

# Quick test
if __name__ == '__main__':
    print("Testing Recommendation Engine...")
    print("=" * 60)
    
    # Test with different diseases
    test_cases = [
        ('Tomato___Early_blight', 0.92),
        ('Potato___Late_blight', 0.88),
        ('Tomato___healthy', 0.95)
    ]
    
    for disease, conf in test_cases:
        rec = DiseaseRecommendationEngine.get_recommendation(disease, conf)
        print(f"\n✅ {rec['disease']}")
        print(f"   Severity: {rec['severity']}")
        print(f"   Confidence: {conf*100:.1f}%")
    
    print("\n" + "=" * 60)
    print("🎉 Recommendation Engine Ready!")
    print("=" * 60)