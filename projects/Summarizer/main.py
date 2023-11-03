import os
from PyPDF2 import PdfFileReader, PdfFileWriter

import openai
from dotenv import load_dotenv

import streamlit as st

load_dotenv()

openai.api_key = os.getenv("OPEN_API_KEY")


def load_files():
    text = ""
    data_der = os.path.join(os.getcwd(), "data")

    for file in os.listdir(data_der):
        if file.endswith(".txt"):
            with open(os.path.join(data_der, file), "r") as f:
                text += f.read()
    return text


def extract_pdf(pdf_file):
    with open(pdf_file, "r") as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        pages = pdf.getNumPages()
        text = ""
        for i in range(pages):
            page = pdf.getPage(i)
            text += page.extractText()
    return text


def get_response(prompt):
    prompt = f'''
    You are an expert in summarizing text. You will be given a text delimited by four backquote characters,
    make sure to capture the main points, key arguments, and any supporting evidence presented in the article.
    your summary should be informative and will structured, ideally it should be 3-5 sentences long, 
    but it can be longer if absolutely necessary.
    
    Text:````{prompt}````
    '''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,

            },
        ],
    )
    return response['choices'][0]['message']['content']


def main():
    text = load_files()
    response = get_response(text)

    print(response)


if __name__ == '__main__':
    main()
