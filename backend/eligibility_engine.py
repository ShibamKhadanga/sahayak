"""
Eligibility Prediction Engine
Uses rule-based AI to predict which government schemes a user qualifies for
Searches web for each scheme's application link
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def predict_eligibility(user_profile):
    """
    Predict which government schemes the user is eligible for
    
    Args:
        user_profile: Dictionary with user data
            {
                'age': 65,
                'income': 30000,
                'gender': 'male',
                'education': 'graduate',
                'state': 'chhattisgarh',
                'category': 'general',
                'is_student': False,
                'is_employed': False,
                'disability': None
            }
    
    Returns:
        List of eligible schemes with confidence scores
    """
    try:
        age = int(user_profile.get('age', 0))
        income = int(user_profile.get('income', 0))
        gender = user_profile.get('gender', '').lower()
        education = user_profile.get('education', '').lower()
        state = user_profile.get('state', 'india').lower()
        category = user_profile.get('category', 'general').lower()
        is_student = user_profile.get('is_student', False)
        is_employed = user_profile.get('is_employed', True)
        disability = user_profile.get('disability')
        
        eligible_schemes = []
        
        # Age-based schemes
        if age >= 60:
            eligible_schemes.append({
                'name': 'Old Age Pension Scheme',
                'confidence': 0.95 if income < 48000 else 0.70,
                'reasons': [
                    'Age 60 or above',
                    'Income below threshold' if income < 48000 else 'Check income eligibility'
                ],
                'category': 'pension',
                'priority': 'high'
            })
            
            eligible_schemes.append({
                'name': 'Senior Citizen Health Card',
                'confidence': 0.90,
                'reasons': ['Age 60 or above'],
                'category': 'health',
                'priority': 'medium'
            })
            
            eligible_schemes.append({
                'name': 'Free Bus Pass for Senior Citizens',
                'confidence': 0.85,
                'reasons': ['Age 60 or above', 'State benefit'],
                'category': 'transport',
                'priority': 'low'
            })
        
        if age >= 18 and age <= 35:
            eligible_schemes.append({
                'name': 'PM Mudra Yojana (Youth Loan)',
                'confidence': 0.75,
                'reasons': ['Age 18-35', 'For self-employment'],
                'category': 'loan',
                'priority': 'medium'
            })
            
            if not is_employed:
                eligible_schemes.append({
                    'name': 'PM Kaushal Vikas Yojana (Skill Development)',
                    'confidence': 0.80,
                    'reasons': ['Age 18-35', 'Skill training program'],
                    'category': 'skill',
                    'priority': 'high'
                })
        
        # Income-based schemes
        if income < 48000:
            eligible_schemes.append({
                'name': 'BPL (Below Poverty Line) Card',
                'confidence': 0.95,
                'reasons': ['Annual income below ₹48,000'],
                'category': 'welfare',
                'priority': 'high'
            })
            
            eligible_schemes.append({
                'name': 'Antyodaya Anna Yojana (Subsidized Ration)',
                'confidence': 0.90,
                'reasons': ['Low income', 'Food security program'],
                'category': 'food',
                'priority': 'high'
            })
        
        if income < 250000:
            eligible_schemes.append({
                'name': 'PM Ayushman Bharat (Health Insurance)',
                'confidence': 0.85,
                'reasons': ['Income below ₹2.5 lakh'],
                'category': 'health',
                'priority': 'high'
            })
            
            if age < 40:
                eligible_schemes.append({
                    'name': 'PM Awas Yojana (Housing Scheme)',
                    'confidence': 0.75,
                    'reasons': ['Income below ₹2.5 lakh', 'For first-time home buyers'],
                    'category': 'housing',
                    'priority': 'medium'
                })
        
        # Education-based schemes
        if is_student:
            if income < 800000:
                eligible_schemes.append({
                    'name': 'National Scholarship Portal',
                    'confidence': 0.90,
                    'reasons': ['Student', 'Family income eligible'],
                    'category': 'education',
                    'priority': 'high'
                })
            
            if category in ['sc', 'st', 'obc']:
                eligible_schemes.append({
                    'name': 'SC/ST/OBC Scholarship Scheme',
                    'confidence': 0.95,
                    'reasons': ['Student', 'Reserved category'],
                    'category': 'education',
                    'priority': 'high'
                })
            
            eligible_schemes.append({
                'name': 'PM Vidya Lakshmi Education Loan',
                'confidence': 0.80,
                'reasons': ['Student', 'Interest subsidy available'],
                'category': 'education',
                'priority': 'medium'
            })
        
        # Gender-specific schemes
        if gender == 'female':
            eligible_schemes.append({
                'name': 'PM Beti Bachao Beti Padhao Yojana',
                'confidence': 0.75,
                'reasons': ['Female empowerment scheme'],
                'category': 'women',
                'priority': 'medium'
            })
            
            if age >= 18 and age <= 40:
                eligible_schemes.append({
                    'name': 'Mahila Udyam Nidhi (Women Entrepreneur Loan)',
                    'confidence': 0.70,
                    'reasons': ['Female', 'Age 18-40', 'Business loan'],
                    'category': 'loan',
                    'priority': 'medium'
                })
            
            # Widow pension
            marital_status = user_profile.get('marital_status', '').lower()
            if marital_status == 'widow' and age >= 40:
                eligible_schemes.append({
                    'name': 'Widow Pension Scheme',
                    'confidence': 0.98,
                    'reasons': ['Widow', 'Age 40+'],
                    'category': 'pension',
                    'priority': 'high'
                })
        
        # Disability schemes
        if disability:
            eligible_schemes.append({
                'name': 'Disability Pension Scheme',
                'confidence': 0.95,
                'reasons': ['Certified disability', 'Monthly pension'],
                'category': 'pension',
                'priority': 'high'
            })
            
            eligible_schemes.append({
                'name': 'Artificial Limbs Scheme',
                'confidence': 0.85,
                'reasons': ['Certified disability', 'Free aids/appliances'],
                'category': 'health',
                'priority': 'medium'
            })
        
        # State-specific schemes (Chhattisgarh)
        if 'chhattisgarh' in state or 'cg' in state:
            if income < 100000:
                eligible_schemes.append({
                    'name': 'Mukhyamantri Kanya Vivah Yojana',
                    'confidence': 0.80,
                    'reasons': ['Chhattisgarh resident', 'Low income family'],
                    'category': 'welfare',
                    'priority': 'low'
                })
        
        # Farmer schemes
        occupation = user_profile.get('occupation', '').lower()
        if 'farmer' in occupation or 'agriculture' in occupation:
            eligible_schemes.append({
                'name': 'PM Kisan Samman Nidhi',
                'confidence': 0.95,
                'reasons': ['Small/marginal farmer', '₹6000/year benefit'],
                'category': 'agriculture',
                'priority': 'high'
            })
            
            eligible_schemes.append({
                'name': 'Fasal Bima Yojana (Crop Insurance)',
                'confidence': 0.85,
                'reasons': ['Farmer', 'Crop protection'],
                'category': 'agriculture',
                'priority': 'medium'
            })
        
        # Employment schemes
        if not is_employed and age >= 18 and age <= 60:
            eligible_schemes.append({
                'name': 'MGNREGA (Rural Employment Guarantee)',
                'confidence': 0.80,
                'reasons': ['Unemployment', '100 days guaranteed work'],
                'category': 'employment',
                'priority': 'high'
            })
        
        # Sort by priority and confidence
        priority_map = {'high': 3, 'medium': 2, 'low': 1}
        eligible_schemes.sort(
            key=lambda x: (priority_map[x['priority']], x['confidence']),
            reverse=True
        )
        
        # Return top 5
        return eligible_schemes[:5]
        
    except Exception as e:
        logger.error(f"Error in predict_eligibility: {e}")
        return []

def explain_eligibility(scheme_name, user_profile):
    """
    Explain why user is or isn't eligible for a specific scheme
    """
    try:
        # Get all predictions
        all_schemes = predict_eligibility(user_profile)
        
        # Find the scheme
        for scheme in all_schemes:
            if scheme['name'].lower() == scheme_name.lower():
                return {
                    'eligible': True,
                    'confidence': scheme['confidence'],
                    'reasons': scheme['reasons'],
                    'priority': scheme['priority']
                }
        
        # Not in eligible list - explain why not
        age = int(user_profile.get('age', 0))
        income = int(user_profile.get('income', 0))
        
        reasons = []
        
        if 'pension' in scheme_name.lower() and age < 60:
            reasons.append('Age below 60 years (pension requires 60+)')
        
        if 'scholarship' in scheme_name.lower() and not user_profile.get('is_student'):
            reasons.append('Not currently a student')
        
        if 'bpl' in scheme_name.lower() and income >= 48000:
            reasons.append('Income above BPL threshold (₹48,000)')
        
        return {
            'eligible': False,
            'reasons': reasons if reasons else ['Criteria not met']
        }
        
    except Exception as e:
        logger.error(f"Error in explain_eligibility: {e}")
        return {'eligible': False, 'reasons': ['Unable to determine']}

def get_missing_info(user_profile):
    """
    Identify what information is missing to better predict eligibility
    """
    required_fields = ['age', 'income', 'gender', 'state']
    optional_fields = ['education', 'occupation', 'marital_status', 'disability']
    
    missing_required = [f for f in required_fields if not user_profile.get(f)]
    missing_optional = [f for f in optional_fields if not user_profile.get(f)]
    
    return {
        'missing_required': missing_required,
        'missing_optional': missing_optional,
        'completeness': (
            len(required_fields) - len(missing_required)
        ) / len(required_fields)
    }

if __name__ == '__main__':
    # Test eligibility prediction
    print("Testing Eligibility Engine...")
    
    # Test profile 1: Elderly person
    profile1 = {
        'age': 65,
        'income': 30000,
        'gender': 'male',
        'state': 'chhattisgarh',
        'category': 'general',
        'is_student': False,
        'is_employed': False
    }
    
    print("\nProfile 1: 65-year-old, ₹30,000 income")
    schemes = predict_eligibility(profile1)
    for i, scheme in enumerate(schemes, 1):
        print(f"{i}. {scheme['name']} ({scheme['confidence']:.0%} confident)")
        print(f"   Reasons: {', '.join(scheme['reasons'])}")
    
    # Test profile 2: Student
    profile2 = {
        'age': 20,
        'income': 150000,
        'gender': 'female',
        'state': 'chhattisgarh',
        'category': 'sc',
        'is_student': True,
        'is_employed': False
    }
    
    print("\n\nProfile 2: 20-year-old SC female student")
    schemes = predict_eligibility(profile2)
    for i, scheme in enumerate(schemes, 1):
        print(f"{i}. {scheme['name']} ({scheme['confidence']:.0%} confident)")
        print(f"   Reasons: {', '.join(scheme['reasons'])}")
