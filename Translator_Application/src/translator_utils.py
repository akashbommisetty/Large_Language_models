import os
from dotenv import load_dotenv
import google.generativeai as genai

# Configure Google Gemini API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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

