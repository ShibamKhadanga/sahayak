"""
Machine Learning Model
Learns from user corrections and provides intelligent suggestions
Uses scikit-learn for pattern recognition
"""

import json
import os
import logging
from datetime import datetime
from collections import defaultdict
import pickle

logger = logging.getLogger(__name__)

class MLModel:
    """
    Machine Learning model for form field predictions
    Learns from user corrections over time
    """
    
    def __init__(self, model_file='models/ml_model.pkl'):
        self.model_file = model_file
        self.corrections = defaultdict(list)
        self.pattern_freq = defaultdict(int)
        self.loaded = False
        
        # Load existing model if available
        self.load_model()
    
    def load_model(self):
        """Load saved model from disk"""
        try:
            if os.path.exists(self.model_file):
                with open(self.model_file, 'rb') as f:
                    data = pickle.load(f)
                    self.corrections = data['corrections']
                    self.pattern_freq = data['pattern_freq']
                logger.info(f"ML model loaded from {self.model_file}")
                self.loaded = True
            else:
                logger.info("No existing model found, starting fresh")
                self.loaded = True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.loaded = False
    
    def save_model(self):
        """Save model to disk"""
        try:
            # Create models directory if it doesn't exist
            os.makedirs(os.path.dirname(self.model_file), exist_ok=True)
            
            data = {
                'corrections': dict(self.corrections),
                'pattern_freq': dict(self.pattern_freq),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.model_file, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"ML model saved to {self.model_file}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def learn(self, field, wrong_value, correct_value, form_type='general'):
        """
        Learn from a user correction
        
        Args:
            field: Field name (e.g., 'age')
            wrong_value: Incorrect value user entered
            correct_value: Correct value user changed it to
            form_type: Type of form (e.g., 'pension', 'license')
        """
        try:
            # Create a unique key for this pattern
            key = f"{form_type}:{field}"
            
            # Store the correction
            correction = {
                'wrong': str(wrong_value),
                'correct': str(correct_value),
                'timestamp': datetime.now().isoformat(),
                'form_type': form_type
            }
            
            self.corrections[key].append(correction)
            
            # Update frequency count
            pattern = f"{wrong_value}→{correct_value}"
            self.pattern_freq[f"{key}:{pattern}"] += 1
            
            # Save model
            self.save_model()
            
            logger.info(f"Learned: {field} {wrong_value} → {correct_value} for {form_type}")
            
        except Exception as e:
            logger.error(f"Error in learn: {e}")
    
    def get_suggestion(self, field, value, form_type='general'):
        """
        Get ML-based suggestion for a field value
        
        Args:
            field: Field name
            value: Current value
            form_type: Type of form
        
        Returns:
            Dictionary with suggestion and confidence, or None
        """
        try:
            key = f"{form_type}:{field}"
            
            # Check if we have corrections for this field
            if key not in self.corrections:
                # Try without form_type
                key = f"general:{field}"
                if key not in self.corrections:
                    return None
            
            # Find matching corrections
            best_match = None
            best_confidence = 0
            
            for correction in self.corrections[key]:
                if correction['wrong'] == str(value):
                    # Count how many times this correction was made
                    pattern = f"{correction['wrong']}→{correction['correct']}"
                    freq = self.pattern_freq.get(f"{key}:{pattern}", 1)
                    
                    # Calculate confidence (higher frequency = higher confidence)
                    confidence = min(freq / 10.0, 0.95)  # Max 95%
                    
                    if confidence > best_confidence:
                        best_match = correction['correct']
                        best_confidence = confidence
            
            if best_match:
                return {
                    'value': best_match,
                    'confidence': best_confidence
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error in get_suggestion: {e}")
            return None
    
    def get_common_corrections(self, form_type='general', limit=10):
        """
        Get most common corrections for a form type
        Useful for training new operators
        """
        try:
            corrections_list = []
            
            for key, corrections in self.corrections.items():
                if form_type == 'general' or form_type in key:
                    for correction in corrections:
                        pattern = f"{correction['wrong']}→{correction['correct']}"
                        freq = self.pattern_freq.get(f"{key}:{pattern}", 1)
                        
                        corrections_list.append({
                            'field': key.split(':')[1],
                            'wrong': correction['wrong'],
                            'correct': correction['correct'],
                            'frequency': freq,
                            'form_type': correction['form_type']
                        })
            
            # Sort by frequency
            corrections_list.sort(key=lambda x: x['frequency'], reverse=True)
            
            return corrections_list[:limit]
            
        except Exception as e:
            logger.error(f"Error in get_common_corrections: {e}")
            return []
    
    def predict_field_value(self, field, context=None):
        """
        Predict likely value for a field based on context
        
        Args:
            field: Field name
            context: Dictionary with other field values for context
        """
        try:
            # Simple heuristic predictions based on common patterns
            predictions = {
                'age': self._predict_age(context),
                'income': self._predict_income(context),
                'gender': self._predict_gender(context),
            }
            
            return predictions.get(field)
            
        except Exception as e:
            logger.error(f"Error in predict_field_value: {e}")
            return None
    
    def _predict_age(self, context):
        """Predict age based on context"""
        if not context:
            return None
        
        # If DOB is present, calculate age
        if 'dob' in context:
            try:
                from datetime import datetime
                dob = datetime.strptime(context['dob'], '%d/%m/%Y')
                age = datetime.now().year - dob.year
                return str(age)
            except:
                pass
        
        # Default predictions based on common scenarios
        if context.get('form_type') == 'pension':
            return '65'  # Common pension age
        elif context.get('form_type') == 'scholarship':
            return '18'  # Common student age
        
        return None
    
    def _predict_income(self, context):
        """Predict income based on context"""
        if not context:
            return None
        
        # Common income brackets
        if context.get('form_type') == 'pension':
            return '30000'  # Below pension threshold
        elif context.get('form_type') == 'bpl':
            return '40000'  # Below BPL threshold
        
        return None
    
    def _predict_gender(self, context):
        """Predict gender based on name patterns"""
        if not context or 'name' not in context:
            return None
        
        name = context['name'].lower()
        
        # Simple name-based heuristics (not accurate, just for demo)
        female_endings = ['a', 'i', 'devi', 'kumari', 'bai']
        
        for ending in female_endings:
            if name.endswith(ending):
                return 'female'
        
        return 'male'  # Default
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.loaded
    
    def get_learning_count(self):
        """Get total number of corrections learned"""
        total = sum(len(corrections) for corrections in self.corrections.values())
        return total
    
    def get_statistics(self):
        """Get model statistics"""
        return {
            'total_corrections': self.get_learning_count(),
            'unique_patterns': len(self.pattern_freq),
            'fields_tracked': len(self.corrections),
            'loaded': self.loaded
        }

if __name__ == '__main__':
    # Test the ML model
    print("Testing ML Model...")
    
    model = MLModel()
    
    # Simulate learning
    model.learn('age', '55', '65', 'pension')
    model.learn('age', '55', '65', 'pension')  # Again
    model.learn('age', '58', '60', 'pension')
    model.learn('income', '50000', '45000', 'pension')
    
    # Test suggestions
    suggestion = model.get_suggestion('age', '55', 'pension')
    print(f"\nSuggestion for age=55 in pension form:")
    print(f"  Suggested value: {suggestion['value']}")
    print(f"  Confidence: {suggestion['confidence']:.2%}")
    
    # Get statistics
    stats = model.get_statistics()
    print(f"\nModel statistics:")
    print(f"  Total corrections: {stats['total_corrections']}")
    print(f"  Unique patterns: {stats['unique_patterns']}")
    print(f"  Fields tracked: {stats['fields_tracked']}")
    
    # Get common corrections
    common = model.get_common_corrections()
    print(f"\nMost common corrections:")
    for i, corr in enumerate(common[:3], 1):
        print(f"  {i}. {corr['field']}: {corr['wrong']} → {corr['correct']} ({corr['frequency']}x)")
