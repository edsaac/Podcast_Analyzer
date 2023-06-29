import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Podcast Analyzer", page_icon=":robot:")

st.image(image='imgs\podcast_analyzer.png')

def get_input_type():
    input_type = st.radio("Set your input type", label_visibility='collapsed', key="Podcast URL", 
                          options=["Podcast Video", "Transcript File"], horizontal = True)
    return input_type

input_type = get_input_type()

def get_text():
    input_text = st.text_input(label="Podcast label", label_visibility='collapsed', placeholder=f"Your {input_type} URL...", key="podcast_input")
    return input_text

podcast_input = get_text()

