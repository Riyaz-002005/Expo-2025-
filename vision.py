import streamlit as st  
st.set_page_config(page_title="Image Recognition App" , page_icon=":camera:", layout="centered", initial_sidebar_state="expanded")

from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai
from PIL import Image
import base64

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(input, image):
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
            background-image: linear-gradient(180deg, #FFFFFF 0%, #6284FF 50%, #FF0000 100%);
            background-size: cover;
        }
        header {
            opacity: 0.5; /* Change this value to adjust the transparency */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the gradient background
set_background()


st.markdown("<h1 style='font-style: italic;'>ChatBot with Image Recognition</h1>", unsafe_allow_html=True)
input = st.text_input(" ChatBox: ", key="input")

uploaded_file = st.file_uploader("Upload or Drag and Drop an image... ", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

st.markdown(
    """
    <style>
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .stApp {
        animation: fadeIn 1s ease-in-out;
    }
    .stButton>button {
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        background-color: rgba(0, 0, 0, 0.2);
        color: white;
        border: 2px solid white;
        animation: pulse 2s infinite;
        backdrop-filter: blur(20%);
    }
    .stButton>button:hover {
        transform: scale(1.1);
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        background-color: rgba(0, 0, 0, 0.4);
    }
    .stSuccess {
        animation: fadeIn 1s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

submit=st.button("Generate Response")

if submit:
    if image is None:
        st.warning("Please upload an image first.", icon="⚠️")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input, image)
        st.success("Response generated!", icon="✅")
        st.write(response)
