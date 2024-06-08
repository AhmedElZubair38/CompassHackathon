import subprocess
import whisper
import os

def extract_audio(video_file, audio_file):
    command = ['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', audio_file]
    subprocess.run(command)

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
    subprocess.run(command)

def add_live_captions_to_video(video_file, output_file):
    audio_file = 'audio.wav'
    srt_file = 'captions.srt'

    extract_audio(video_file, audio_file)
    transcription = transcribe_audio(audio_file)
    create_srt(transcription, srt_file)
    add_captions_to_video(video_file, srt_file, output_file)

# video_file = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4'

video_file = 'https://storage.cloud.google.com/compasshackathon/german.mp4'
# second news channel video 
# https://storage.googleapis.com/aai-web-samples/news.mp4

# home_directory = os.path.expanduser('~')
# output_file = os.path.join(home_directory, 'output_video.mp4')

output_file = 'output_video.mp4'

add_live_captions_to_video(video_file, output_file)