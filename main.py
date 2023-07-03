import streamlit as st
from src.utils import *
from src.data_setup import *
from src.engine import *
import openai
from dotenv import load_dotenv, find_dotenv
import os
import spacy
import textacy
import numpy as np
from tqdm import tqdm



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
        st.success('URL is valid ✅')
    else:
        st.error('URL is not valid ❌')
        st.stop()


# Get podcast transcript
#here I should download audio and transcripe using WhisperAI from podcast URL

# Convert VTT to CSV
TRANSCRIPT_PATH = "./data/transcripts/"
VTT_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.vtt"
CSV_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.csv"

convert_vtt_to_csv(TRANSCRIPT_PATH, VTT_FILE_NAME, CSV_FILE_NAME)

# Read CSV transcript
def read_csv():
    df = pd.read_csv(f"{TRANSCRIPT_PATH}/{CSV_FILE_NAME}", sep=";", header=None)
    df.columns = ["timestamp", "text"]
    return df

inital_transcript_df = read_csv()

# Reorganize transcript for analysis
analysis_transcript_df = reorganize_transcript(inital_transcript_df)

# Create topic modelling transcript
topic_modeling_transcript = prepare_transcript_for_modelling(analysis_transcript_df)

# Create book titles transcript
#book_titles_transcript = prepare_transcript_for_book_extraction(analysis_transcript_df)


# # Show podcast video and transcript
# def show_video(url, start_time):
#     return st.video(url, start_time=start_time)

# with st.expander("Show transcript"):
#     for idx, row in topic_modeling_transcript.iterrows():
#         if st.button(f"{row['timestamp']}"):
#             my_video = show_video("https://youtu.be/bUmULlGACEI", # change it to podcast_url
#                                   start_time=timestamp_to_seconds(row['timestamp'])) if podcast_url else None
#         st.markdown(f"{row['text']}")
        
def show_word_cloud(df, named_entity):
    return st.pyplot(generate_word_cloud(df, named_entity))

with st.expander("Named Entity Recognition"):
    entity_types = st.multiselect("Select entity types",
                              ['PERSON', 'ORG','WORK_OF_ART', 
                               'LAW', 'GPE', 'LOC', 
                               'PRODUCT', 'EVENT', 'NORP'])      

    if st.button("Extract entities"):
        progress_bar = st.progress(0, text="Operation in progress. Please wait.")
        topic_modeling_transcript = extract_named_entities_in_batches(
            topic_modeling_transcript,
            entity_types=entity_types,
            progress=progress_bar
        )
        topic_modeling_transcript = add_entity_type_columns(topic_modeling_transcript, entity_types)
        # Remove empty lists
        topic_modeling_transcript = topic_modeling_transcript.applymap(lambda x: None if isinstance(x, list) and not x else x)
        progress_bar.empty()  # optional: you may want to remove the progress bar here
        st.success('Done!')
        #st.dataframe(topic_modeling_transcript)
        for entity_type in entity_types:
            show_word_cloud(topic_modeling_transcript, entity_type.lower())



