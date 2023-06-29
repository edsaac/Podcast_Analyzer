import streamlit as st
import numpy as np
import pandas as pd
from utils import *
import openai
from dotenv import load_dotenv, find_dotenv
import os




_ = load_dotenv(find_dotenv())  # add .env to .gitignore
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Podcast Analyzer", page_icon="🎙️")


# Add image 
st.image(image='imgs\podcast_analyzer.png')

# Choose input type video or transcript
def get_input_type():
    input_type = st.radio("Set your input type", label_visibility='collapsed', key="Podcast URL", 
                          options=["Podcast Video", "Transcript File"], horizontal = True)
    return input_type

input_type = get_input_type()

# Get podcast URL in video or transcript format
def get_text():
    input_text = st.text_input(label="Podcast label", label_visibility='collapsed', placeholder=f"Type Your {input_type} URL...", key="podcast_input")
    return input_text

podcast_url = get_text()

# Check if podcast URL is valid
if podcast_url:
    if is_valid_url(podcast_url):
        st.success('Analyzing...')
    else:
        st.error('URL is not valid')
        st.stop()


