import streamlit as st

st.title('CAPTIONIZE AI')

st.sidebar.title('Navigation')
pages = ['Home', 'myPlay', 'myLive', 'Blogs', '☁️ Upload Video']
page = st.sidebar.radio('', pages)

if page == 'Home':
    st.title('🏠Home')
    st.write('Welcome to the Home page.')
elif page == 'myPlay':
    st.title('myPlay')
    st.write('Welcome to the myPlay page.')
elif page == 'myLive':
    st.title('myLive')
    st.write('Welcome to the myLive page.')
elif page == 'Blogs':
    st.title('Blogs')
    st.write('Welcome to the Blogs page.')
elif page == '☁️ Upload Video':
    st.title('Upload Video')

    col1, col2 = st.columns([2, 1])

    tab1, tab2, tab3, tab4 = st.tabs(["Enter Video URL", "Details", "Audience & Visibility", "Category & Language"])

    with tab1:
            
            st.title("Proceed with Regular Video")
            meow = st.text_input("Video URL")

            st.title("OR")


            import streamlit as st
            import subprocess
            import whisper
            import os
            import tempfile
            from urllib import request
            from pathlib import Path


            def extract_audio(video_file, audio_file):
                command = ['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file]
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def transcribe_audio(audio_file):
                model = whisper.load_model("base")
                result = model.transcribe(audio_file)
                return result

            def create_srt(transcription, srt_file):
                with open(srt_file, 'w') as f:
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
                command = ['ffmpeg', '-i', video_file, '-vf', f"subtitles={srt_file}", output_file]
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def add_live_captions_to_video(video_file, output_file):
                audio_file = 'audio.wav'
                srt_file = 'captions.srt'

                extract_audio(video_file, audio_file)
                transcription = transcribe_audio(audio_file)
                create_srt(transcription, srt_file)
                add_captions_to_video(video_file, srt_file, output_file)

            st.title("Video Captioning With Live Language Translation")
            st.markdown("Provide an MP4 video URL to generate a captioned video.")

            video_url = st.text_input("To Be AI Captionized Video URL")

            if video_url:

                st.write("Downloading and displaying the original video...")
                
                with st.spinner('Processing video...'):

                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
                        original_video_file = tmp.name
                        request.urlretrieve(video_url, original_video_file)

                    st.video(original_video_file)

                    output_file = 'output_video.mp4'
                    
                    add_live_captions_to_video(video_url, output_file)
                    st.write("Video processing complete!")
                    
                    st.write("Displaying the captioned video:")
                    if Path(output_file).is_file():
                        st.video(output_file)
                    else:
                        st.error("Failed to process video. Please try again.")
            
            st.title("OR")

            st.title("Generate video using your own text prompt! (Yet To Be Implemented In Stage 2!)")
            meow = st.text_input("To Be Generated Test Prompt")

            
    with tab2:

        st.header("Video Details")

        title = st.text_input("Enter a video title")
        description = st.text_area("Enter a description")

        st.subheader("Thumbnail")
        thumbnail = st.file_uploader("Upload Thumbnail", type=["jpg", "png"])

    with tab3:

        st.header("Audience & Visibility")

    with tab4:

        st.header("Category & Language")