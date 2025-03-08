from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="PDF Summarizer",
    page_icon=":brain:",
    layout="centered"
)

# Get API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Streamlit UI
st.title("🤖 AI PDF Summarizer")
st.sidebar.header("Upload PDF")

uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Load PDF and process it
    pdf_reader = PyPDFLoader("temp.pdf")
    documents = pdf_reader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    # Create vector embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Create retrieval chain
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template("""Given the following conversation and a follow-up question,
    rephrase the follow-up question to be a standalone question.

    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:""")

    qa = ConversationalRetrievalChain.from_llm(
        llm=gemini_model,
        retriever=vectorstore.as_retriever(),
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        return_source_documents=True,
        verbose=False
    )

    # Initialize chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("Chat with PDF 📜")

    # Input field for user's question (Located at bottom)
    user_input = st.chat_input("Ask something about the PDF...")

    if user_input:
        # Append user input to session state history
        st.session_state.chat_history.append(("user", user_input))

        # Get AI response
        result = qa({"question": user_input, "chat_history": st.session_state.chat_history})

        # Append AI response to session state history
        st.session_state.chat_history.append(("assistant", result["answer"]))

    # Display all chat history in chronological order (newest messages at the bottom)
    for role, content in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(content)
