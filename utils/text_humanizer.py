
import re
import random
from utils.llm_integration import LLMIntegration

class TextHumanizer:
    def __init__(self):
        self.llm = LLMIntegration()
    
    def humanize_text(self, text):
        """Main method to humanize text using multiple techniques"""
        try:
            # First pass: LLM-based humanization
            humanized = self.llm.humanize_text(text)
            
            # Second pass: Add some manual variations
            humanized = self._add_natural_variations(humanized)
            
            return humanized
        except Exception as e:
            # Fallback to basic humanization if LLM fails
            return self._basic_humanization(text)
    
    def _add_natural_variations(self, text):
        """Add natural writing variations"""
        # Add some sentence structure variations
        sentences = text.split('. ')
        if len(sentences) > 1:
            # Occasionally start with a different sentence
            if random.random() < 0.3:
                sentences = sentences[1:] + [sentences[0]]
                text = '. '.join(sentences) + '.'
        
        # Add some natural punctuation variations
        text = text.replace(';', ',').replace('--', '-')
        
        return text
    
    def _basic_humanization(self, text):
        """Basic text humanization without LLM"""
        # Simple replacements to make text more natural
        replacements = {
            'utilize': 'use',
            'facilitate': 'help',
            'implement': 'set up',
            'optimize': 'improve',
            'leverage': 'use',
            'paradigm': 'model',
            'synergy': 'teamwork'
        }
        
        for formal, informal in replacements.items():
            text = re.sub(rf'\\b{formal}\\b', informal, text, flags=re.IGNORECASE)
        
        return text
EOL