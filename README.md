Sure, I can add the application link to your README file. Here's how you can do it:

```markdown
# Podcast Analyzer

Podcast Analyzer is a tool built with Streamlit, Whisper, LangChain to analyze the content of podcasts. 

## Features

The app has the following features:

1. **YouTube Link Input**: Enter a YouTube link and get the content transcribed using the Whisper ASR API (requires OpenAI API key).
2. **Transcription Display**: View the transcription of your podcast audio file, segmented and timestamped.
3. **Named Entity Recognition**: Select the types of named entities you want to identify in the text, and visualize them using word clouds.
4. **Question Answering**: Ask questions about the content of your podcast and get answers using a QA model.
5. **Summarization and Topic Modeling**: Get a summary of your podcast content and extract the main topics discussed.

## Live Demo

You can access a live demo of the app [here](https://podcastmaster.streamlit.app/).

## Setup

To get started, clone this repository and navigate into the directory.

```bash
git clone https://github.com/ahmad-alismail/podcast-analyzer.git
cd podcast-analyzer
```

Install the necessary dependencies with the following command:

```bash
pip install -r requirements.txt
```

Run the app with Streamlit:

```bash
streamlit run main.py
```

In the app, you can input your OpenAI API key in the sidebar. If you don't have an OpenAI API key, the app will use a default video for analysis.

## Contribution

Feel free to fork this repository, create a branch, add commits, and open a pull request.

## License

This project is under the [MIT License](LICENSE).
```

