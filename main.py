import streamlit as st
import numpy as np
import pandas as pd
from src.utils import *
from src.data_setup import *
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
        st.success('Initial Analysis...')
    else:
        st.error('URL is not valid')
        st.stop()


# Get podcast transcript
#here I should download audio and transcripe using WhisperAI from podcast URL

# Convert VTT to CSV
TRANSCRIPT_PATH = "./data/transcripts/"
VTT_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.vtt"
CSV_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.csv"

convert_vtt_to_csv(TRANSCRIPT_PATH, VTT_FILE_NAME, CSV_FILE_NAME)

# Read CSV
def read_csv():
    df = pd.read_csv(f"{TRANSCRIPT_PATH}/{CSV_FILE_NAME}", sep=";", header=None)
    df.columns = ["timestamp", "text"]
    return df

inital_transcript_df = read_csv()

# Reorganize transcript for analysis
analysis_transcript_df = reorganize_transcript(inital_transcript_df)

# Show podcast video
def show_video(url, start_time):
    return st.video(url, start_time=start_time)

#my_video = show_video("https://youtu.be/bUmULlGACEI", start_time=600)# if podcast_url else None

# Show transcript using topic modelling transcript
topic_modeling_transcript = prepare_transcript_for_modelling(analysis_transcript_df)

with st.expander("Show transcript"):
    for idx, row in topic_modeling_transcript.iterrows():
        if st.button(f"{row['timestamp']}"):
            my_video = show_video("https://youtu.be/bUmULlGACEI", 
                                  start_time=timestamp_to_seconds(row['timestamp']))
        st.markdown(f"{row['text']}")
        

