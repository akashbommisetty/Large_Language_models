import streamlit as st

st.set_page_config(
    page_title="Translator.AI",
    page_icon="🈶",
    layout="centered"
)

# Streamlit page title
st.title("🈶 Translator App")

col1, col2 = st.columns(2)

with col1:
    input_languages_list = [
        "English", "French", "German", "Latin", "Spanish", "Hindi", "Tamil", "Telugu", "Marathi", 
        "Italian", "Portuguese", "Russian", "Chinese", "Japanese", "Korean", "Arabic", "Turkish", 
        "Greek", "Dutch", "Swedish", "Danish", "Finnish", "Polish", "Hebrew", "Bengali", "Malayalam", 
        "Gujarati", "Urdu", "Punjabi", "Thai", "Vietnamese"
    ]
    input_language = st.selectbox(label="Input Language", options=input_languages_list)

with col2:
    output_languages_list = []
    for lang in input_languages_list:
        if lang != input_language:
            output_languages_list.append(lang)
    output_language = st.selectbox(label="Output Language", options=output_languages_list)

input_text = st.text_area("Type the text to be translated")

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



if st.button("Translate"):
    translated_text = translate(input_language, output_language, input_text)
    st.success(translated_text)
