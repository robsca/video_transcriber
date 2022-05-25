import streamlit as st
from text import Video_to_Text
import streamlit.components.v1 as components  # Import Streamlit
from graph import *
import ssl
import os
from moviepy.editor import VideoFileClip

ssl._create_default_https_context = ssl._create_unverified_context

st.title('Transcript')

# upload video
video_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "mov"])
# get length of video with moviepy




if video_file is not None:
    # save file
    with open("video.mp4", "wb") as f:
        f.write(video_file.read())
    # clip
    clip = VideoFileClip("video.mp4")
    duration = clip.duration
    print(duration)

    create()
    # open html file
    #with open("gameofthrones.html", "r") as f:

    #    components.html(f.read(),
    #            width=800, height=300)

    # show transcript
    st.sidebar.video(video_file)
    # run video to text
    with st.spinner('Wait for it...'):
        transcript = Video_to_Text('video.mp4').transcript
        st.text_area('Transcript', transcript, height=500)
        st.success('Done!')
        


if '__main__' == __name__:
    # run only once
    if not st._is_running_with_streamlit:
       os.system("streamlit run main.py") # run streamlit


    