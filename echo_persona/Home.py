from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")

if 'CATEGORIES' not in st.session_state:
    st.session_state.CATEGORIES = {}

if 'HOBBIES' not in st.session_state:
    st.session_state.HOBBIES = {}

if 'PERSONALITIES' not in st.session_state:
    st.session_state.PERSONALITIES = {}

if 'docsearch' not in st.session_state:
    st.session_state.docsearch = None

st.set_page_config(page_title="Home", page_icon="🦜️🔗")

st.header("Welcome to EchoPersona! 👋")

st.markdown(
    """

    """
)
