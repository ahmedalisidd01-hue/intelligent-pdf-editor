


import requests
import os
from config import Config
import time

class HuggingFaceIntegration:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.HUGGINGFACE_API_KEY
        self.model = self.config.HUGGINGFACE_MODEL
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        
    def generate_text(self, prompt, context_text=None):
        """Generate text using Hugging Face API"""
        try:
            if context_text:
                full_prompt = f"Context: {context_text}\\n\\nInstruction: {prompt}"
            else:
                full_prompt = prompt
            
            return self._query_huggingface(full_prompt)
        except Exception as e:
            raise Exception(f"Hugging Face generation failed: {str(e)}")
    
    def _query_huggingface(self, prompt):
        """Query Hugging Face API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                if 'generated_text' in result[0]:
                    return result[0]['generated_text'].strip()
                else:
                    # Try to extract text from different response formats
                    return str(result[0]).strip()
            elif isinstance(result, dict) and 'generated_text' in result:
                return result['generated_text'].strip()
            else:
                return str(result)
                
        except requests.exceptions.RequestException as e:
            if response.status_code == 503:
                # Model is loading, wait and retry
                time.sleep(15)
                return self._query_huggingface(prompt)
            else:
                raise Exception(f"Hugging Face API error: {str(e)}")
    
    def humanize_text(self, text):
        """Humanize AI-generated text to avoid detection"""
        humanization_prompt = f"""
        Rewrite the following text to make it sound more human and natural while preserving the original meaning. 
        Use varied sentence structures, natural phrasing, and avoid repetitive patterns.
        
        Text to humanize: {text}
        
        Provide only the humanized version:
        """
        
        return self.generate_text(humanization_prompt)
EOL