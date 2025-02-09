import streamlit as st
import google.generativeai as genai
from docx import Document
import base64
import datetime
import random
import string
from io import BytesIO
from googletrans import Translator

translator = Translator()

# Konfigurasi API Gemini
genai.configure(api_key="AIzaSyBVxnF32zKe4Q6vtMI34JzBI0WjKBtYNb8")  # Gantilah dengan API Key yang benar

context_bot2 = "Given a topic, write CV in a concise, professional manner for"

def interact_with_ai(user_input, context):
    cv_keywords = ['write cv', 'compose cv', 'create cv']
    contains_cv_keyword = any(keyword in user_input.lower() for keyword in cv_keywords)

    if contains_cv_keyword:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"{context}\n{user_input}")
        return response.text  # Mengembalikan teks hasil AI
    else:
        return "Keyword tidak ditemukan, gunakan kata kunci yang sesuai."

# Fungsi untuk menerjemahkan teks ke bahasa yang dipilih
def translate_text(text, dest_language):
    if text is None:
        return ""  
    translation = translator.translate(text, dest=dest_language)
    return translation.text if translation else ""  

# Fungsi untuk menyimpan ke file Word
def save_to_word(content):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    file_name = f"CV_{timestamp}_{random_string}.docx"
    
    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_name)

    return file_name

# UI Streamlit
st.title("Automating CV Creation with AI")
st.text("Use appropriate keywords to create CV: ")
st.text("'write cv', 'compose cv', 'create cv'")

user_input = st.text_area("Prompt:", max_chars=2000)
language_choice = st.selectbox("Select Language for Translation:", ("Indonesian", "English", "Spanish", "French", "Hindi", "Russian", "Italian", "Portuguese", "Arabic", "Chinese (Simplified)"))
submit_button = st.button("Submit")

if submit_button:
    if user_input.strip() == "done":
        st.warning("Thank you! You have completed the conversation.")
    else:
        # Terjemahkan prompt ke bahasa Inggris terlebih dahulu
        english_input = translate_text(user_input, "en")
        ai_response = interact_with_ai(english_input, context_bot2)
        
        translated_response = translate_text(ai_response, language_choice)  
        st.text_area("Result (Translated):", value=translated_response, height=200)

        # Simpan ke file Word dan tampilkan tombol download
        file_name = save_to_word(translated_response)  
        with open(file_name, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
        
        st.markdown(
            f'<a href="data:file/docx;base64,{b64}" download="{file_name}" '
            f'style="background-color:#008CBA;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;">'
            f'Download Result as Word</a>',
            unsafe_allow_html=True
        )
