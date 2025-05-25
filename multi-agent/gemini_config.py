import os
from dotenv import load_dotenv
import google.generativeai as genai

class GeminiConfig:
    def __init__(self):
        load_dotenv()

        self.api_key = "AIzaSyB-b4UetfksOsOoumm-Kn9f9HheR_Yq0FU"
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
    def get_model(self, model_name="gemini-2.5-pro-exp-03-25"):
        """
        Get a Gemini model instance
        Args:
            model_name (str): Name of the model to use
        Returns:
            GenerativeModel: A Gemini model instance
        """
        return genai.GenerativeModel(model_name)
    
    def generate_response(self, prompt, model_name="gemini-2.5-pro-preview-05-06"):
        """
        Generate a response using the specified model
        Args:
            prompt (str): The input prompt
            model_name (str): Name of the model to use
        Returns:
            str: Generated response
        """
        
        model = self.get_model(model_name)
        response = model.generate_content(prompt)
        return response.text

# Create a global instance
gemini = GeminiConfig()