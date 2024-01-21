
import openai
import os
import requests
import streamlit as st


@st.cache_data
def generate_email(prompt, email_length="regular"):

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


def generate_prompt(email_tone=None, email_length="regular", email_type="formal", email_lang="english", subject="", description="", restrictions=None, Purpose=None, sender_email=None, salutation=None,):
    prompt_base = f"""
    
    As an AI specialized in writing emails, you are tasked with composing an email based on the following details. 
    Ensure the email is complete, coherent, and includes all the provided information. Write the email as if you are sending it.
    all the information will be between 3 backquote characters.
    ```
    salutation: {salutation}
    subject: {subject}
    description: {description}
    email tone: {email_tone}
    email length: {email_length}
    restrictions: {restrictions}
    language: {email_lang}
    """

    if email_type == 'new email':
        return prompt_base + f"purpose: {Purpose}\n```"
    else:
        return prompt_base + f"sender email: {sender_email}\n```"
