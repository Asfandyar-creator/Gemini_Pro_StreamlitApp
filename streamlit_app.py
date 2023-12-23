import streamlit as st
import os
import pathlib
import textwrap
from constant import API_KEY
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
from PIL import Image

os.environ['API_KEY'] = API_KEY
genai.configure(api_key=os.getenv("API_KEY"))

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))



# Define a function for each app page
def page_1():
    st.header("Gemini Q&A Demo (Single Response)")
    input = st.text_input("Input: ", key="input_1")
    submit = st.button("Ask the question")

    if submit:
        response = get_gemini_response(input)
        st.subheader("The Response is")
        st.write(response)

def page_2():
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    st.header("Gemini Q&A Demo (Streamed Response)")
    input = st.text_input("Input: ", key="input_2")
    submit = st.button("Ask the question")

    if submit:
        response = chat.send_message(input, stream=True)
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)
            print("_"*80)
        st.write(chat.history)

def page_3():
    st.header("Gemini Image Demo")
    input = st.text_input("Input Prompt: ", key="input_3")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Tell me about the image")

    if submit:
        response = get_gemini_response(input, image)
        st.subheader("The Response is")
        st.write(response)


# Define multipage app structure
app_pages = {
    "Q&A Demo (Single Response)": page_1,
    "Q&A Demo (Streamed Response)": page_2,
    "Gemini Image Demo": page_3
}

# Shared function for generating Gemini responses
def get_gemini_response(question, image=""):
    if image:
        model = genai.GenerativeModel('gemini-pro-vision')
        response = model.generate_content([question, image])
    else:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(question)
    return response.text

# Display the selected app page
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Choose a page", app_pages.keys())
app_pages[selected_page]()
