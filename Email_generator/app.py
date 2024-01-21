from config import setup_config
from validation import is_valid_openai_key, key_check
from utils import display_notice, sidebar_features, lottie_file, choose_salutation, show_progress_bar
from streamlit_lottie import st_lottie
from prompts import generate_prompt, generate_email

import streamlit as st
import time


def main():
    setup_config()
    api_key = key_check()
    is_valid_openai_key(api_key)
    sidebar_features()

    st.title('Email Generator')

    is_valid_key = is_valid_openai_key(api_key)

    if not is_valid_key:
        st.error(
            "Its seem like the api key for the app has expired, please contact the developer to provide a new one.")
        st.stop()

    left_column, right_column = st.columns(2)
    with left_column:
        st.subheader(
            "welcome to the email generator app, this app will help you generate an email based on the information you provide.")

    with right_column:
        st_lottie(lottie_file, speed=1, height=150,
                  key="initial", loop=True, reverse=False)

    # ? Initializing the generated emails list
    if 'generated_emails' not in st.session_state:
        st.session_state.generated_emails = []

    mode_choice = st.radio(
        "How detailed do you want your email customization to be?",
        ["Just the essentials", "Full customization"]
    )

    if mode_choice == "Full customization":
        st.markdown(
            "### Full customization mode")
        st.markdown(
            "In this mode you will be able to customize the email as much as you want.")

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
        email_lang = st.radio(
            'What type of email would you like to generate?',
            ('English', 'Arabic', 'Spanish')
        )

        # * to prevent the app from providing an incomplete email
        if email_lang == 'Arabic' and email_length == 'short' or email_lang == 'Arabic' and email_length == 'super long':
            email_length = 'regular'

        st.markdown('---')

        salutation = choose_salutation()

        st.markdown('---')

        if email_type == 'new email':
            st.subheader('New Email')

            # ? Defining the purpose of the email
            Purpose = st.text_input(
                'Enter the purpose of your email:', placeholder='e.g., Schedule a meeting, Request information, Provide feedback..')
            sender_email = None
        else:
            st.subheader('Reply to Email')

            # ? getting the sender email for the reply
            sender_email = st.text_area(
                'Enter the sender email:', placeholder='Enter the key content or main points of the email you received and are replying to. E.g., Your inquiry about our product range, Your request for a meeting on Thursday, etc.')
            Purpose = None

        # ? Defining the subject of the email
        subject = st.text_input('Enter the subject of your email:',
                                placeholder='e.g., Meeting Request, Project Update, Invoice Details...')

        # ? Defining the description of the email
        description = st.text_area(
            'Enter a brief description or the body of your email:', placeholder='e.g., I would like to discuss..., Please find attached..., Regarding your inquiry about...')

        # ? Selecting any restrictions for the email
        restrictions = st.text_area(
            'Enter any restrictions for the email, such as words to include or exclude:', placeholder='e.g., Avoid technical jargon, Include pricing details, Keep it concise...') if st.checkbox('Do you have any restrictions to put in this email?') else 'no restrictions'

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
                                     email_lang, subject, description, restrictions, Purpose, sender_email, salutation)
            try:

                email_content = generate_email(
                    prompt, email_length)
                progress_bar = show_progress_bar()
                st.session_state.generated_emails.append(email_content)

                st.subheader('Generated Email:')
                st.text_area("Generated Email:", email_content, height=400)

                st.download_button('Download Email', email_content,
                                   file_name='generated_email.txt')

            except Exception as e:
                progress_bar = show_progress_bar()
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

    elif mode_choice == "Just the essentials":
        st.markdown(
            "### Just the essentials mode")
        st.markdown(
            "In this mode you will be able to customize the email with the essentials only.")

        # ? Selecting the default tone of email
        email_tone = "formal"
        email_length = "regular"
        email_lang = "english"
        salutation = "Dear [Name]"

        email_type = st.radio(
            'what is the type of email you would like to generate?',
            ('new email', 'reply to email')
        )

        st.markdown('---')

        if email_type == 'new email':
            st.subheader('New Email')

            # ? Defining the purpose of the email
            Purpose = st.text_input(
                'Enter the purpose of your email:', placeholder='e.g., Schedule a meeting, Request information, Provide feedback...')

        else:
            st.subheader('Reply to Email')

            # ? getting the sender email for the reply
            sender_email = st.text_area(
                'Enter the sender email:', placeholder='Enter the key content or main points of the email you received and are replying to. E.g., Your inquiry about our product range, Your request for a meeting on Thursday, etc.')
        # ? Defining the subject of the email
        subject = st.text_input('Enter the subject of your email:',
                                placeholder='e.g., Meeting Request, Project Update, Invoice Details...')

        # ? Defining the description of the email
        description = st.text_area(
            'Enter a brief description or the body of your email:', placeholder='e.g., I would like to discuss..., Please find attached..., Regarding your inquiry about...')

        # ? Selecting any restrictions for the email
        restrictions = st.text_area(
            'Enter any restrictions for the email, such as words to include or exclude:',  placeholder='e.g., Avoid technical jargon, Include pricing details, Keep it concise...') if st.checkbox('Do you have any restrictions to put in this email?') else 'no restrictions'

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
                                     email_lang, subject, description, restrictions, Purpose, salutation)
            try:
                email_content = generate_email(
                    prompt, email_length)
                progress_bar = show_progress_bar()
                st.session_state.generated_emails.append(email_content)

                st.subheader('Generated Email:')
                st.text_area("Generated Email:", email_content, height=400)

                st.download_button('Download Email', email_content,
                                   file_name='generated_email.txt')

            except Exception as e:
                progress_bar = show_progress_bar()
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
