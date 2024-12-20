import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
# Ensure the .env file contains: GOOGLE_API_KEY="api_key"

load_dotenv()

def configure_model():
    """
    Configures the Google Generative AI model using the API key.
    Returns the generative model.
    """
    # Retrieve the Google API key securely from environment variables
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key is not set. Please check the .env file.")
    genai.configure(api_key=api_key)
    return genai
