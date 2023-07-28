from pathlib import Path
import streamlit as st
from src.utils import *
from src.data_setup import *
from src.engine import *
import openai
from dotenv import load_dotenv, find_dotenv
import os


# Setup credentials in Streamlit
user_openai_api_key = st.sidebar.text_input(
    "OpenAI API Key", type="password", 
    help="Set this to run your own custom videos.",
    key="openai_api_key"
)

if user_openai_api_key:
    openai_api_key = user_openai_api_key
    enable_custom = True
else:
    openai_api_key = "not_supplied"
    enable_custom = False

_ = load_dotenv(find_dotenv())  # add .env to .gitignore
openai.api_key = os.getenv("OPENAI_API_KEY")




# Add image 
# Get the path to the directory containing this script
script_dir = Path(__file__).parent

# Construct a path to the image file
image_path = script_dir / 'imgs' / 'podcast_analyzer.PNG'

# Use the image path in st.image
st.image(image=str(image_path))

"st.session_state object:", st.session_state
# When you press abutton, streamlit reruns your script from top to bottom

# Get podcast URL in video or transcript format
def get_text():
    input_text = st.text_input(label="Podcast label", label_visibility='collapsed', placeholder=f"Type Your Video URL...", key="podcast_input")
    return input_text

podcast_url = get_text()


# Get podcast transcript using Whisper 
if enable_custom:
    if podcast_url:
        if is_valid_url(podcast_url):
            
            st.info("Downloading podcast audio...")
            #audio_file_path = download_audio(podcast_url)
            if 'audio_file_path' not in st.session_state:
                st.session_state['audio_file_path'] = download_audio(podcast_url)
            st.info("Audio downloaded... Transcribing in process...")
            if 'whisper_fname' not in st.session_state:
                st.session_state["whisper_fname"] = transcribe_audio(st.session_state.audio_file_path)
            st.success("Transcription completed!")

        else:
            st.error('URL is not valid ❌')
            st.stop()
else:
    st.info("No API key provided. Using default podcast audio...\n \
            Or enter your OpenAI API key in the sidebar to use your own podcast audio.")


# If OpenAI API key is provided, use the custom transcript
if enable_custom and 'whisper_fname' in st.session_state:
        TRANSCRIPT_PATH = "./data/"
        VTT_FILE_NAME = f"{st.session_state.whisper_fname}.vtt"
        CSV_FILE_NAME = f"{st.session_state.whisper_fname}.csv"
# Otherwise, use the default transcript
else:    
    TRANSCRIPT_PATH = "./data/transcripts/"
    VTT_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.vtt"
    CSV_FILE_NAME = "45_michio_kaku__future_of_humans_aliens_space_travel_and_physics.csv"


# Convert VTT to CSV
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

# Show podcast video and transcript
def show_video(url, start_time):
    return st.video(url, start_time=start_time)

with st.expander("Show Transcript"):
    for idx, row in topic_modeling_transcript.iterrows():
        if st.button(f"{row['timestamp'].split('.')[0]}"):
            my_video = show_video("https://youtu.be/bUmULlGACEI", # change it to podcast_url
                                  start_time=timestamp_to_seconds(row['timestamp'])) if podcast_url else None
        st.markdown(f"{row['text']}")
        
def show_word_cloud(df, named_entity):
    return st.pyplot(generate_word_cloud(df, named_entity))

with st.expander("Named Entity Recognition"):
    entity_types = st.multiselect("Select entity types",
                                    options=['PERSON', 'ORG','WORK_OF_ART', 
                               'LAW', 'GPE', 'LOC', 
                               'PRODUCT', 'EVENT', 'NORP'],
                               default=['PERSON', 'ORG','WORK_OF_ART'])      

    if st.button("Find entities"):
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

## TO-DO Activate chat history and use prompt template
with st.expander("Question Answering"):
    question = st.text_input(
        "Ask something about the video",
        placeholder="What is the sting theory?",
        disabled=not is_valid_url(podcast_url),)
    if question:
        topic_modeling_transcript.to_csv("data/topic_modeling_transcript.csv", index=False)
        
        # Initialize QA chain
        qa_chain = load_qa(file="data/topic_modeling_transcript.csv")
        result = qa_chain({"question": question})
        st.markdown(result["answer"])

## TO-DO correct topics structure
with st.expander("Summarization and Topic Modelling"):
    if st.button("Run Summarization") and is_valid_url(podcast_url):
        topic_modeling_transcript.to_csv("data/topic_modeling_transcript.csv", index=False)

        progress_bar = st.progress(0, text="Summarization in progress. Please wait.")
        summary = run_summarizer(file="data/topic_modeling_transcript.csv")
        progress_bar.empty()  # optional: you may want to remove the progress bar here
        st.markdown("## Summary")
        st.write(summary)
        progress_bar = st.progress(0, text="Extracting topics. Please wait.")
        summary_structured = run_extraction_chain(summary)
        st.markdown("## Topics")
        topics = extract_topics(summary_structured)
        st.dataframe(topics)
        st.success('Done!')


