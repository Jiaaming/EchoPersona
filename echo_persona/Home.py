import os

import streamlit as st

# Initialize session state variables
if 'openai_api_key' not in st.session_state:
	st.session_state.openai_api_key = os.environ.get("OPENAI_API_KEY")

if 'serper_api_key' not in st.session_state:
	st.session_state.serper_api_key = os.environ.get("SERPER_API_KEY")

if 'volc_ak' not in st.session_state:
	st.session_state.volc_ak = os.environ.get("VOLC_AK")

if 'volc_sk' not in st.session_state:
	st.session_state.volc_sk = os.environ.get("VOLC_SK")

st.set_page_config(page_title="Home", page_icon="🦜️🔗")

st.header("Welcome to EchoPersona! 👋")

st.markdown(
    """

    """
)
