
from utils.huggingface_integration import HuggingFaceIntegration
from config import Config

class LLMIntegration:
    def __init__(self):
        self.config = Config()
        self.hf_integration = HuggingFaceIntegration()
    
    def generate_text(self, prompt, context_text=None):
        """Generate text using Hugging Face"""
        return self.hf_integration.generate_text(prompt, context_text)
    
    def humanize_text(self, text):
        """Humanize AI-generated text"""
        return self.hf_integration.humanize_text(text)
EOL