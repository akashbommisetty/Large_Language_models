import os
from dotenv import load_dotenv
import google.generativeai as genai

# Explicitly specify the .env file path
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path)

# Configure Google Gemini API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure API key is loaded
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Make sure the .env file is set up correctly.")

genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-1.5-flash")

def translate(input_language, output_language, input_text):
    prompt = (
        f"You are a helpful assistant that translates {input_language} to {output_language}.\n\n"
        f"Input: {input_text}\n\n"
        "Provide a clear and accurate translation."
    )

    response = model.generate_content(prompt)

    return response.text if response else "Error: No response from Gemini API"