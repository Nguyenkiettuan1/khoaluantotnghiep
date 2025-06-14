import os
from dotenv import load_dotenv
from openai import OpenAI
import os
import google.generativeai as genai

class DeepSeekConfig:
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )
        
    def generate_content(self, prompt: str, model_name: str = "deepseek/deepseek-chat-v3-0324:free") -> str:
        """
        Generate content using DeepSeek model
        Args:
            prompt (str): The input prompt
            model_name (str): Name of the model to use
        Returns:
            str: Generated content
        """
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.1,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""

class OpenAIConfig:
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
        
    def generate_content(self, prompt: str, model_name: str = "gpt-4o-mini") -> str:
        """
        Generate content using OpenAI model
        Args:
            prompt (str): The input prompt
            model_name (str): Name of the model to use
        Returns:
            str: Generated content
        """
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model_name,
                temperature=0.1,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""


class GeminiConfig:
    def __init__(self):
        load_dotenv()

        self.api_key = "AIzaSyB-b4UetfksOsOoumm-Kn9f9HheR_Yq0FU"
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
    def get_model(self, model_name="gemini-2.5-pro-preview-05-06") -> genai.GenerativeModel:
        """
        Get a Gemini model instance
        Args:
            model_name (str): Name of the model to use
        Returns:
            GenerativeModel: A Gemini model instance
        """
        return genai.GenerativeModel(model_name)
    
    def generate_content(self, prompt: str, model_name: str = "gemini-2.5-pro-preview-05-06") -> str:
        """
        Generate content using the specified model
        Args:
            prompt (str): The input prompt
            model_name (str): Name of the model to use
        Returns:
            str: Generated content
        """
        try:
            model = self.get_model(model_name)
            response = model.generate_content(prompt)
            if response and hasattr(response, 'text'):
                return response.text
            return ""
        except Exception as e:
            print(f"Error generating content: {e}")
            return ""
    
    def generate_response(self, prompt: str, model_name: str = "gemini-2.5-pro-preview-05-06") -> str:
        """
        Generate a response using the specified model (alias for generate_content)
        Args:
            prompt (str): The input prompt
            model_name (str): Name of the model to use
        Returns:
            str: Generated response
        """
        return self.generate_content(prompt, model_name)

gemini = GeminiConfig()
deepseek = DeepSeekConfig()
openai_client = OpenAIConfig()
