import streamlit as st
from dotenv import load_dotenv


def setup_config():
    # ? Setting the page configuration
    st.set_page_config(
        page_title="Email Generator",
        page_icon="📧",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={'Get Help': 'https://www.github.com/Naifcx47350'}

    )

    # ? Loading the environment variables
    load_dotenv()
