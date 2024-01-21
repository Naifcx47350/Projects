import os
import streamlit as st
import openai
from dotenv import load_dotenv


def key_check():
    session_state = st.session_state

    # ? Getting the OpenAI API key from the environment variables
    if 'streamlit' in os.environ.get('SERVER_SOFTWARE', '').lower():
        api_key = st.secrets["OPEN_API_KEY"]
    else:
        api_key = os.getenv("OPEN_API_KEY")

    openai.api_key = api_key

    return api_key


# ? Check if the provided OpenAI API key is valid
def is_valid_openai_key(api_key):
    """Check if the provided OpenAI API key is valid."""
    openai.api_key = api_key
    try:
        # ! Make a test call. Here we'll list available engines, which is a lightweight call.
        response = openai.Engine.list()
        if response and 'data' in response:
            return True
    except openai.error.OpenAIError as e:
        # ! Handle specific authentication error
        if "Authentication" in str(e):
            return False
    return False
