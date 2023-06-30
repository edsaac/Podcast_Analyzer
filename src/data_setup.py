"""prepare and download data if needed"""
import pandas as pd

def convert_vtt_to_csv(TRANSCRIPT_PATH, TRANSCRIPT_FNAME_VTT, TRANSCRIPT_FNAME_CSV):
    """
    This function converts a VTT transcript file to a CSV format. 

    Parameters:
    TRANSCRIPT_PATH (str): The path to the transcript files.
    TRANSCRIPT_FNAME_VTT (str): The filename of the VTT transcript.
    TRANSCRIPT_FNAME_CSV (str): The desired filename for the output CSV transcript.
    """
    with open(f"{TRANSCRIPT_PATH}/{TRANSCRIPT_FNAME_VTT}") as oldfile, open(f"{TRANSCRIPT_PATH}/{TRANSCRIPT_FNAME_CSV}", 'w') as newfile:
        old_lines = oldfile.read().split('\n')
        clean_lines = [line for line in old_lines if line not in ['', 'WEBVTT']]

        for line_idx in range(0, len(clean_lines)-1, 2):
            timestamp = clean_lines[line_idx].split('-->')[0].strip()
            # Remove milliseconds
            timestamp = timestamp.split('.')[0]
            # Standardize timestamp format
            timestamp = "00:" + timestamp if len(timestamp.split(':')) < 3 else timestamp
            timestamp = "0" + timestamp if len(timestamp.split(':')[0]) < 2 else timestamp
            text = clean_lines[line_idx+1].rstrip()
            new_line = f"{timestamp};{text}\n"
            newfile.write(new_line)



def reorganize_transcript(df):
    """
    This function recreates the transcript dataframe, concatenating partial sentences into full ones.
    
    Parameters:
    df (pandas.DataFrame): A dataframe that contains timestamped text transcripts.
    
    Returns:
    transcript_df (pandas.DataFrame): A dataframe with full sentences for analysis purposes.
    """
    # Recreate the dataframe with full sentences
    transcript_df = pd.DataFrame(columns=df.columns)

    for idx, timestamp, text in df.itertuples():
        while text[-1] != '.':
            idx += 1
            text += df.loc[idx]['text']
        transcript_df = pd.concat([transcript_df, pd.DataFrame({'timestamp': timestamp, 'text': text}, index=[0])], ignore_index=True)

    # Remove any piece of text if it is included in previous text
    not_part_of_previous = [True]
    for i in range(1, len(transcript_df)):
        not_part_of_previous.append(transcript_df['text'][i] not in transcript_df['text'][i-1])
    transcript_df = transcript_df[not_part_of_previous] 

    return transcript_df


def prepare_transcript_for_modelling(transcript_df):
    """
    This function prepares a transcript dataframe for text summarization and topic modelling 
    
    Parameters:
    transcript_df (pandas.DataFrame): A dataframe that contains timestamped text transcripts.

    Returns:
    transcript_df_topic (pandas.DataFrame)
    """
    transcript_df['group'] = transcript_df.index // 8
    transcript_df_topic = transcript_df.groupby('group').agg({
        'timestamp': 'first',
        'text': ' '.join
    })
    
    return transcript_df_topic


def prepare_transcript_for_book_extraction(transcript_df):
    """
    This function prepares a transcript dataframe for book titles extraction 
    
    Parameters:
    transcript_df (pandas.DataFrame): A dataframe that contains timestamped text transcripts.

    Returns:
    grouped_transcript_df (pandas.DataFrame)
    """
    transcript_df['group'] = transcript_df.index // 20
    grouped_transcript_df = transcript_df.groupby('group').agg({
        'timestamp': 'first',
        'text': ' '.join,
        'is_book_related': 'any',
        'book_candidates': 'sum',
        'named_entities': 'sum',
    })
    
    return grouped_transcript_df
