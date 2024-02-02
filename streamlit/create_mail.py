import streamlit as st
import google.generativeai as palm
from docx import Document
import base64
import datetime
import random
import string

from io import BytesIO

from googletrans import Translator

translator = Translator()

# Konfigurasi API
palm.configure(api_key="AIzaSyDS__6q4C6Hh3fdaSMpuX_mxAJe-f354J8")

context_bot2 = "Given a topic, write cv in a concise, professional manner for"

def interact_with_ai(user_input, context):
    cv_keywords = ['write cv', 'compose cv', 'create cv']
    contains_cv_keyword = any(keyword in user_input.lower() for keyword in cv_keywords)

    if contains_cv_keyword:
        response = palm.chat(
            context=context,
            messages=[user_input]
        )
        return response.last or ""  # Mengembalikan respons terakhir atau string kosong jika respons adalah None
    else:
        return "The bot can only assist in CV creation. Please enter the CV related prompt."

# Fungsi untuk menerjemahkan teks ke bahasa yang dipilih
def translate_text(text, dest_language):
    if text is None:
        return ""  # Mengembalikan string kosong jika teks bernilai None
    else:
        translation = translator.translate(text, dest=dest_language)
        return translation.text if translation else ""  # Mengembalikan teks terjemahan atau string kosong jika terjemahan tidak berhasil

# Fungsi untuk menyimpan ke file Word
def save_to_word(content, bot_option):
    # Mendapatkan timestamp saat ini untuk membuat nama file unik
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    # Menghasilkan random string sebagai bagian dari nama file
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    # Menambahkan data ke dokumen Word dengan nama file yang unik
    file_prefix = "CV"
    file_name = f"{file_prefix}_{timestamp}_{random_string}.docx"
    doc = Document()
    doc.add_paragraph(content)
    doc.save(file_name)

    return file_name

st.title("Automating CV Creation with AI")

bot_option = st.sidebar.radio("Select Bot:", ("Create CV",))
if bot_option == "Create CV":
    st.title("Create CV")
    st.text("Use appropriate keywords to create CV: : ")
    st.text("'write cv', 'compose cv', 'create cv'")
    st.text(" ")

st.sidebar.markdown(
    '<div style="position: fixed; bottom: 0; left: 0; width: 100%; padding: 10px; font-size: 15px; color: #ffff; box-shadow: 0px -1px 5px rgba(0, 0, 0, 0.1); display: flex; align-items: center; justify-content: flex-start;"><img src="https://cdn-icons-png.flaticon.com/512/106/106852.png" style="width: 20px; margin-right: 5px;">Frederick H.S </div>',
    unsafe_allow_html=True
)

user_input = st.text_area("Prompt : ")
language_choice = st.selectbox("Select Language for Translation:", ("Indonesian", "English", "Spanish", "French", "Hindi", "Russian", "Italian", "Portuguese", "Arabic", "Mandarin"))
submit_button = st.button("Submit")
download_button = False

if submit_button:
    if user_input.strip() == "done":
        st.warning("Thank you! You have completed the conversation.")
    else:
        # Terjemahkan prompt ke bahasa Inggris terlebih dahulu
        english_input = translate_text(user_input, "en")
        ai_response = interact_with_ai(english_input, context_bot2)
        download_button = True 
        
        translated_response = translate_text(ai_response, language_choice)  # Terjemahkan respon bot ke bahasa yang dipilih
        st.text_area("Result (Translated):", value=translated_response, height=200)

        if "The bot can only assist in email creation. Please enter the email related prompt." not in ai_response:
            if download_button:  # Menampilkan tombol unduh jika respons tersedia
                file_name = save_to_word(translated_response, bot_option)  # Simpan respon terjemahan ke dalam dokumen Word

                # Menampilkan tombol unduh dengan tautan ke file output.docx
                st.markdown(
                    f'<a href="data:file/docx;base64,{base64.b64encode(open(file_name, "rb").read()).decode()}" '
                    f'download="{file_name}" '
                    f'style="background-color:#008CBA;color:white;padding:10px 20px;text-decoration:none;border-radius:5px;display:inline-block;margin-top:10px;">'
                    f'Download Result as Word'
                    f'</a>',
                    unsafe_allow_html=True
                )
