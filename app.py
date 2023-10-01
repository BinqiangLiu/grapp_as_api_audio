from gradio_client import Client
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from streamlit.components.v1 import html
load_dotenv()

st.set_page_config(page_title="Gradio App as API", layout="wide")
st.subheader("Gradio+Streamlit+WtMem : Life Enhancing with AI!")

css_file = "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

hf_token=os.getenv('hf_token')

user_query=st.text_input("Enter your query here: ")

client = Client("https://binqiangliu-llama2-txt-gen.hf.space/")
if user_query !="" and not user_query.strip().isspace() and not user_query == "" and not user_query.strip() == "" and not user_query.isspace():
    with st.spinner("AI Thinking...Please wait a while to Cheers!"):
        result = client.predict(user_query, api_name="/predict")
        st.write("AI Reponse: ")
        st.write(result)
