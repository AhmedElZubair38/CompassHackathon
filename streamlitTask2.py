# import streamlit as st
# import subprocess
# import whisper
# import os
# import requests

# # Utility functions

# def download_video(url, output_path):
#     response = requests.get(url, stream=True)
#     with open(output_path, 'wb') as out_file:
#         for chunk in response.iter_content(chunk_size=1024):
#             out_file.write(chunk)
#     return output_path

# def extract_audio(video_file, audio_file):
#     command = ['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file]
#     subprocess.run(command, check=True)

# def transcribe_audio(audio_file):
#     model = whisper.load_model("base")
#     result = model.transcribe(audio_file)
#     return result

# def create_srt(transcription, srt_file):
#     with open(srt_file, 'w', encoding='utf-8') as f:
#         for i, segment in enumerate(transcription['segments']):
#             start = segment['start']
#             end = segment['end']
#             text = segment['text']
            
#             start_time = format_timestamp(start)
#             end_time = format_timestamp(end)
            
#             f.write(f"{i+1}\n")
#             f.write(f"{start_time} --> {end_time}\n")
#             f.write(f"{text}\n\n")

# def format_timestamp(seconds):
#     milliseconds = int((seconds % 1) * 1000)
#     seconds = int(seconds)
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# def add_captions_to_video(video_file, srt_file, output_file):
#     command = ['ffmpeg', '-i', video_file, '-vf', f"subtitles={srt_file}", '-c:a', 'copy', output_file]
#     subprocess.run(command, check=True)

# # Streamlit Interface
# st.title("Live Captioning for Videos")

# # Choose input method
# option = st.radio("Select input method:", ('Upload Video', 'Video URL'))

# if option == 'Upload Video':
#     uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
#     if uploaded_file is not None:
#         video_file_path = os.path.join("temp_video.mp4")
#         with open(video_file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
#         st.success("Video file uploaded successfully.")
# else:
#     video_url = st.text_input("Enter the video URL (MP4 format)")
#     if video_url:
#         video_file_path = os.path.join("temp_video.mp4")
#         download_video(video_url, video_file_path)
#         st.success("Video file downloaded successfully.")

# # Process the video if a file path is available
# if 'video_file_path' in locals() and st.button("Generate Captions"):
#     home_directory = os.path.expanduser('~')
#     audio_file = os.path.join(home_directory, 'audio.wav')
#     srt_file = os.path.join(home_directory, 'captions.srt')
#     output_file = os.path.join(home_directory, 'output_video.mp4')

#     with st.spinner("Processing... This may take a few minutes."):
#         # Extract audio, transcribe, and create captions
#         extract_audio(video_file_path, audio_file)
#         transcription = transcribe_audio(audio_file)
#         create_srt(transcription, srt_file)
#         add_captions_to_video(video_file_path, srt_file, output_file)
    
#     st.success("Captions generated and added to the video successfully.")

#     # Display the output video with captions
#     st.video(output_file)

#     # Provide a download link
#     with open(output_file, "rb") as f:
#         st.download_button("Download Video with Captions", f, file_name="output_video.mp4")



import streamlit as st
import subprocess
import whisper
import os
import requests

# Utility functions
def download_video(url, output_path):
    response = requests.get(url, stream=True)
    with open(output_path, 'wb') as out_file:
        for chunk in response.iter_content(chunk_size=1024):
            out_file.write(chunk)
    return output_path

def extract_audio(video_file, audio_file):
    command = ['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file]
    subprocess.run(command, check=True)

def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result

def create_srt(transcription, srt_file):
    with open(srt_file, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(transcription['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            start_time = format_timestamp(start)
            end_time = format_timestamp(end)
            
            f.write(f"{i+1}\n")
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

def format_timestamp(seconds):
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def add_captions_to_video(video_file, srt_file, output_file):
    # Properly format the path for Windows
    srt_file_path = srt_file.replace("\\", "/")
    command = ['ffmpeg', '-i', video_file, '-vf', f"subtitles='{srt_file_path}'", '-c:a', 'copy', output_file]
    subprocess.run(command, check=True)

# Streamlit Interface
st.title("Live Captioning for Videos")

# Choose input method
option = st.radio("Select input method:", ('Upload Video', 'Video URL'))

if option == 'Upload Video':
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
    if uploaded_file is not None:
        video_file_path = "temp_video.mp4"
        with open(video_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Video file uploaded successfully.")
else:
    video_url = st.text_input("Enter the video URL (MP4 format)")
    if video_url:
        video_file_path = "temp_video.mp4"
        download_video(video_url, video_file_path)
        st.success("Video file downloaded successfully.")

# Process the video if a file path is available
if 'video_file_path' in locals() and st.button("Generate Captions"):
    home_directory = os.path.expanduser('~')
    audio_file = os.path.join(home_directory, 'audio.wav')
    srt_file = os.path.join(home_directory, 'captions.srt')
    output_file = os.path.join(home_directory, 'output_video.mp4')

    with st.spinner("Processing... This may take a few minutes."):
        try:
            # Extract audio, transcribe, and create captions
            extract_audio(video_file_path, audio_file)
            transcription = transcribe_audio(audio_file)
            create_srt(transcription, srt_file)
            add_captions_to_video(video_file_path, srt_file, output_file)
        
            st.success("Captions generated and added to the video successfully.")

            # Display the output video with captions
            st.video(output_file)

            # Provide a download link
            with open(output_file, "rb") as f:
                st.download_button("Download Video with Captions", f, file_name="output_video.mp4")
        except subprocess.CalledProcessError as e:
            st.error(f"An error occurred: {e}")

