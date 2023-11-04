import streamlit as st
import openai
import os
from dotenv import load_dotenv
import time


load_dotenv()


# ! to run this app you need to provide your openai api key in the api_key variable below
api_key = os.getenv("OPEN_API_KEY")

if not api_key:
    st.error("OpenAI API key not found. Please ensure it's set in your environment.")
    st.stop()

# ? defining the openai api key
openai.api_key = api_key


@st.cache_data
def generate_email(prompt, email_tone, email_length):

    temperature = 0.7

    max_tokens_map = {
        'short': 150,
        'regular': 300,
        'long': 600,
        'super long': 1200
    }

    max_tokens = max_tokens_map[email_length]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are an expert system in the field of writing emails. 
                                Generate emails based on the provided instructions."""
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']


def display_notice():
    st.markdown("### Privacy Notice")
    st.text("Your inputs are sent to OpenAI for email generation.")
    st.text("Please ensure you don't input sensitive data.")


def generate_prompt(email_tone, email_length, email_type, email_Language, subject, description, restrictions, Purpose=None, Sender_Email=None, salutation=None):
    prompt_base = f"""
    you are an expert system in the field of writing emails.
    your will be provided with some specific information about the email that you need to write.
    please write the email accordingly. the information will be between 3 backquote characters.
    please make sure to include all the information provided in the email.

    ```
    salutation: {salutation}
    subject: {subject}
    description: {description}
    email tone: {email_tone}
    email length: {email_length}
    restrictions: {restrictions}
    language: {email_Language}
    """

    if email_type == 'new email':
        return prompt_base + f"purpose: {Purpose}\n```"
    else:
        return prompt_base + f"sender email: {Sender_Email}\n```"


def sidebar_features():
    st.sidebar.title("Email Generator Sidebar")

    # ? 1. About Section
    st.sidebar.header("About")
    st.sidebar.text(
        "This app is built using OpenAI's ")
    st.sidebar.text(
        "to generate emails based on user input.")

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


def main():
    sidebar_features()
    st.title('Email Generator')
    st.subheader(
        "welcome to the email generator app, this app will help you generate an email based on the information you provide.")

    if 'generated_emails' not in st.session_state:
        st.session_state.generated_emails = []

    # ? Selecting the tone of email
    email_tone = st.radio(
        'What is the tone of the email you would like to generate?',
        ('formal', 'informal', 'informative')
    )

    # ? Selecting the length of the email
    email_length = st.selectbox(
        'Select the length of the email:',
        ('short', 'regular', 'long', 'super long')
    )

    email_type = st.radio(
        'what is the type of email you would like to generate?',
        ('new email', 'reply to email')
    )

    # ? Selecting the language of the email
    email_Language = st.radio(
        'What type of email would you like to generate?',
        ('English', 'Arabic', 'Spanish')
    )

    st.markdown('---')

    salutation = choose_salutation()

    st.markdown('---')

    if email_type == 'new email':
        st.subheader('New Email')

        # ? Defining the purpose of the email
        Purpose = st.text_input('Enter the purpose of your email:')

    else:
        st.subheader('Reply to Email')

        # ? getting the sender email for the reply
        Sender_Email = st.text_area('Enter the sender email:')

    # ? Defining the subject of the email
    subject = st.text_input('Enter the subject of your email:')

    # ? Defining the description of the email
    description = st.text_area(
        'Enter a brief description or the body of your email:')

    # ? Selecting any restrictions for the email
    restrictions = st.text_area(
        'Enter any restrictions for the email, such as words to include or exclude:') if st.checkbox('Do you have any restrictions to put in this email?') else 'no restrictions'

    st.markdown('---')

    display_notice()

    st.markdown('---')

    # ? Generate the email
    if st.button('Generate Email'):

        if not subject or not description:
            st.warning(
                "Please provide both a subject and a description for the email.")
            return

        prompt = generate_prompt(email_tone, email_length, email_type,
                                 email_Language, subject, description, restrictions, Purpose, salutation)
        try:

            email_content = generate_email(prompt, email_tone, email_length)
            progress_bar = show_progress_bar()
            st.session_state.generated_emails.append(email_content)

            st.subheader('Generated Email:')
            st.text_area("Generated Email:", email_content, height=400)

            st.download_button('Download Email', email_content,
                               file_name='generated_email.txt')

        except Exception as e:
            progress_bar.empty()
            st.error(
                'Something went wrong, please try again or contact the developer.')
            st.error(e)

        st.markdown('---')
        # ? View generated emails
        for idx, email in enumerate(st.session_state.generated_emails, start=1):
            with st.expander(f"View Generated Email no. {idx}"):
                st.text_area("Generated Email:", email_content,
                             height=400, key=idx)
                st.download_button(
                    f'Download Email {idx}', email, file_name=f'generated_email_{idx}.txt')

    st.caption('Made by Naif Alsahabi')
    st.caption('v1.0')


if __name__ == '__main__':
    main()
