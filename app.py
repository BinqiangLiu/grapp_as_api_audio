from gradio_client import Client
import streamlit as st
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from streamlit.components.v1 import html
load_dotenv()
import numpy as np
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import ffmpeg
from gtts import gTTS
from langchain import PromptTemplate, LLMChain
from langchain.memory import StreamlitChatMessageHistory
from streamlit_chat import message
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from streamlit.components.v1 import html
from langchain import HuggingFaceHub
import time
import glob
from googletrans import Translator
import uuid

st.set_page_config(page_title="Gradio App as API WAudio", layout="wide")
st.subheader("Gradio+Streamlit+WAudio+WtMem : Life Enhancing with AI!")

#result=""
if "result" not in st.session_state:
    st.session_state["result"] = ""

css_file = "main.css"
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

hf_token=os.getenv('hf_token')

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""
#user_query=st.text_input("Enter your query here: ")
st.session_state["user_query"]=st.text_input("Enter your query here: ")

client = Client("https://binqiangliu-llama2-txt-gen.hf.space/")
#if user_query !="" and not user_query.strip().isspace() and not user_query == "" and not user_query.strip() == "" and not user_query.isspace():
if st.session_state["user_query"] !="" and not st.session_state["user_query"].strip().isspace() and not st.session_state["user_query"] == "" and not st.session_state["user_query"].strip() == "" and not st.session_state["user_query"].isspace():    
    with st.spinner("AI Thinking...Please wait a while to Cheers!"):
        #result = client.predict(user_query, api_name="/predict")
        st.session_state["result"] = client.predict(st.session_state["user_query"], api_name="/predict")
        st.write("AI Reponse: ")
        #st.write(result)
        st.write(st.session_state["result"])

translator = Translator()
def text_to_speech(input_language, output_language, text):
    if text is None:
        print("Input empty.")        
    else:
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, slow=False)
#        trans_txt_tts_file_name = str(uuid.uuid4()) + ".mp3"
        tts_file_name = str(uuid.uuid4()) + ".mp3"
        tts.save(tts_file_name)                      
#      st.audio(audio, format="audio/mpeg") 
#      audio_bytes = tts_audio_file.read()
        st.audio(tts_file_name, format="audio/mpeg")
#        tts.save("translationresult.mp3")        
#        tts_audio_file=tts.save(tts_file_name)        
        return trans_text

st.write("---")

if "output_text" not in st.session_state:
    st.session_state["output_text"] = ""

if "ai_response_audio" not in st.session_state:
    st.session_state["ai_response_audio"] = None
#ai_response_audio = st.checkbox("语音播放AI助手回复", key="ai_audio_cbox")   
st.session_state["ai_response_audio"] = st.checkbox("语音播放AI助手回复", key="ai_audio_cbox")   
if st.session_state["ai_response_audio"]:
  out_lang = st.selectbox("请选择希望用来听AI回复的语言", ("English", "Chinese"), key="output_lang")
  if out_lang == "English":
    output_language = "en"
  elif out_lang == "Chinese":
    output_language = "zh-CN"
  if st.session_state["result"] =="" or st.session_state["result"].strip().isspace() or st.session_state["result"] == "" or st.session_state["result"].strip() == ""  or st.session_state["result"].isspace():
    print("No AI Response Yet.")
    st.write("请确认您已经向AI助手提问并获得回复。")
  else:
    in_lang_1 = st.selectbox("请确认AI助手输出内容的语言", ("Chinese", "English"), key="input_lang_1")
    if in_lang_1 == "Chinese":
        input_language_1 = "zh-CN"
    elif in_lang_1 == "English":
        input_language_1 = "en"    
    #output_text = text_to_speech(input_language_1, output_language, st.session_state["result"])
    st.session_state["output_text"] = text_to_speech(input_language_1, output_language, st.session_state["result"])
