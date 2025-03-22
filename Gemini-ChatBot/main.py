import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Gemini-Flash!",
    page_icon=":brain:",  
    layout="centered",  
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Flash AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-1.5-flash')

# Function to translate roles for Streamlit
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chatbot title
st.title("🤖 Gemini Flash - ChatBot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user
user_prompt = st.chat_input("Ask Gemini-Flash...")
if user_prompt:
    # Display user message
    st.chat_message("user").markdown(user_prompt)

    # Create assistant message container
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # Placeholder to update text dynamically
        full_response = ""  # Store full response progressively

        # Stream response **character-by-character** for a typing effect
        for chunk in st.session_state.chat_session.send_message(user_prompt, stream=True):
            for char in chunk.text:
                full_response += char  # Append character to response
                response_placeholder.markdown(full_response + "▌")  # Add cursor effect
                time.sleep(0.01)  # Adjust speed for smooth effect

        response_placeholder.markdown(full_response)  # Final display without cursor
