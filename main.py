import streamlit as st
st.set_page_config(page_title="Mario", page_icon=":smiley:", layout="wide", initial_sidebar_state="expanded")
from text import Video_to_Text
import streamlit.components.v1 as components  # Import Streamlit
import ssl
import os
from moviepy.editor import VideoFileClip
from brain import *
import traceback
# import sys

ssl._create_default_https_context = ssl._create_unverified_context

st.title('Transcript')

# upload video
video_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "mov"])
# get length of video with moviepy

url = st.sidebar.text_input('Insert URL')
txt = st.text_area('Transcript', key = 'transcript_')
try:
    if url:
        summary, context = summarizer_from_url(url)

    elif txt:
        summary, context = summarizer(txt)
        st.text_area('Summary', summary, key = 'summary')

    elif video_file is not None:
        '''
        read file missing
        '''
        # clip
        clip = VideoFileClip(video_file)
        duration = clip.duration
        print(duration)
        st.sidebar.video(video_file)
        time_per_second = (13*60) / 280
        # run video to text
        with st.spinner(f'Wait for it... it will take {(duration*time_per_second)//60} minuts'):
            transcript = Video_to_Text('video.mp4').transcript
            st.text_area('Transcript', transcript, height=500,key= 'transcript')
            st.success('Done!')
            summary, context = summarizer(transcript)
    else:
        st.write('No file selected')

    with st.expander('Ask me a question'):
        question = st.text_input('Question')
        if question:
            answer = question_answering(summary, question)
            st.text_area('Answer', answer['answer'], key='answer')  
except:
    st.write('Problem')
    # write which error occured
    st.write(traceback.format_exc())

if '__main__' == __name__:
    # run only once
    if not st._is_running_with_streamlit:
       os.system("streamlit run main.py") # run streamlit


    
