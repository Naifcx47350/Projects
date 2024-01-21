
import openai
import os
import requests
import json
import streamlit as st
import time

def load_lottiefile(filepath: str):
    if "http" in filepath:
        r = requests.get(filepath)
        return r.json()
    else:
        with open(filepath) as f:
            return json.load(f)


# ? Loading the lottie file
lottie_file = load_lottiefile("Animation/robot.json")


def display_notice():
    st.markdown("### Privacy Notice")
    st.text("Your inputs are sent to OpenAI for email generation.")
    st.text("Please ensure you don't input sensitive data.")


def sidebar_features():
    st.sidebar.title("Email Generator Sidebar")

    # ? 1. About Section
    st.sidebar.header("About")
    st.sidebar.markdown(
        """
            - This app is built using OpenAI's.
            - to generate emails based on user input.
        """
    )

    # ? 2. Feedback Form
    telegram_icon = "https://cdn3.iconfinder.com/data/icons/social-icons-33/512/Telegram-16.png"
    st.sidebar.header("Feedback")
    st.sidebar.subheader("Provide Feedback on my Telegram:")
    feedback_url = "https://t.me/Naifcx4735"

    html_code = f"""
    <ul style="list-style-type: none; padding-left: 0;">
        <li><a href="{feedback_url}" target="_blank"><img src="{telegram_icon}" width="20" height="20"/>  Feedback</a></li>
    """

    st.sidebar.markdown(html_code, unsafe_allow_html=True)

    # ? 3. Social Media
    st.sidebar.header("Follow me on:")

    # Replace with your actual icon URL
    github_icon = "https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-16.png"
    twitter_icon = "https://cdn4.iconfinder.com/data/icons/social-media-black-white-2/1227/X-16.png"
    linkedin_icon = "https://cdn2.iconfinder.com/data/icons/social-media-2285/512/1_Linkedin_unofficial_colored_svg-16.png"

    github_link = "https://github.com/Naifcx47350"
    twitter_link = "https://twitter.com/Naif4735"
    linkedin_link = "https://www.linkedin.com/in/naif-alsahabi-085720249/"

    html_code = f"""
    <ul style="list-style-type: none; padding-left: 0;">
        <li><a href="{github_link}" target="_blank"><img src="{github_icon}" width="20" height="20"/> GitHub</a></li>
        <li><a href="{twitter_link}" target="_blank"><img src="{twitter_icon}" width="20" height="20"/> X(Twitter)</a></li>
        <li><a href="{linkedin_link}" target="_blank"><img src="{linkedin_icon}" width="20" height="20"/> LinkedIn</a></li>
    </ul>
    """

    st.sidebar.markdown(html_code, unsafe_allow_html=True)

    # ? 4. Usage Tips
    st.sidebar.header("Usage Tips")
    st.sidebar.markdown(
        """
            - Don't input sensitive data.
            - currently if you change the mode from full customization to just the essentials, the app will not show the previously generated emails. so please download them before changing the mode.
            - Provide as much information as possible.
            - Provide a clear description , subject and purpose.
            - The restrictions can be words to include or exclude, a specific format, or any other restrictions you would like to put on the email.
            - You can view the previously generated emails by clicking on the expander below the generate email button.
        """
    )


def show_progress_bar():
    """Show progress bar while generating email."""
    progress_bar = st.progress(0)
    for i in range(50, 101, 10):
        time.sleep(0.2)
        progress_bar.progress(i)
    time.sleep(1)
    progress_bar.empty()
    return progress_bar


def choose_salutation():
    # ? Selecting the salutation category
    salutation_category = st.radio(
        'Select the type of salutation:',
        ('General', 'Formal', 'Friendly', 'Time-based', 'Specific')
    )

    # ? Defining the salutations
    salutations = {
        'General': ['Hello', 'Hi', 'Greetings', 'To whom it may concern', 'Hey'],
        'Formal': ['Dear [Name]', 'Dear Sir/Madam', 'Dear Dr. [Name]', 'Attention: [Department/Title]'],
        'Friendly': ['Hey there', 'Hiya', 'Howdy'],
        'Time-based': ['Good morning', 'Good afternoon', 'Good evening'],
        'Specific': ['Dear Team', 'Dear valued customer', 'Dear [Company Name]', 'Dear Hiring Manager', 'Dear HR Department']
    }

    chosen_salutation = st.selectbox(
        'Choose a salutation:', salutations[salutation_category])
    return chosen_salutation
