import streamlit as st
import openai
import os

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPEN_API_KEY")
# changesf


def generate_email(prompt, email_type, email_length):
    # Adjust temperature, max_tokens, etc. according to your needs
    temperature = 0.7
    max_tokens_map = {
        'short': 150,
        'regular': 300,
        'long': 600,
        'super long': 1200
    }
    max_tokens = max_tokens_map[email_length]

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


# Streamlit webpage layout
st.title('Email Generator')

# User inputs
email_type = st.radio(
    'What type of email would you like to generate?',
    ('formal', 'informal', 'informative')
)

email_length = st.selectbox(
    'Select the length of the email:',
    ('short', 'regular', 'long', 'super long')
)

subject = st.text_input('Enter the subject of your email:')
description = st.text_area(
    'Enter a brief description or the body of your email:')
restrictions = st.text_input(
    'Enter any words that must be included in the email:')

if st.button('Generate Email'):
    # Construct a prompt for the ChatGPT API based on user input
    prompt = f"Write a {email_type} email about '{subject}' that is {email_length}. The email should be {email_length} and include the following points: {description}. Please include these words: {restrictions}."

    # Call the function to generate the email
    email_content = generate_email(prompt, email_type, email_length)

    # Display the generated email
    st.subheader('Generated Email:')
    st.write(email_content)

    # Provide options to copy or download the email
    st.download_button('Download Email', email_content,
                       file_name='generated_email.txt')
    st.code(email_content)

# Tips to improve the application:
# 1. Add user authentication if needed.
# 2. Implement advanced text editing features for the generated email.
# 3. Include an option to send the email directly from the application.
# 4. Add functionality to save user preferences for future use.
# 5. Ensure compliance with email sending limits and best practices to avoid spamming.
# 6. Provide multilingual support for generating emails in different languages.
