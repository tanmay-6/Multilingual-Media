import moviepy.editor as mp
from pydub import AudioSegment
import speech_recognition as sr
import os

def extract_audio_from_video(video_file, wav_file="ex_audio.wav"):
    """Extract audio from a video file and save it as a .wav file."""
    video = mp.VideoFileClip(video_file)
    video.audio.write_audiofile(wav_file, codec='pcm_s16le')  # Directly save as WAV
    print(f"Audio extracted and saved as {wav_file}")

def transcribe_audio_to_text(wav_file):
    """Transcribe audio file to text using speech recognition."""
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print(f"Transcription: {text}")
            return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    # Paths to input video, intermediate audio file, and output .wav file
    video_path = "Trial2\Vid1.mp4"
    wav_audio_path = "Trial2\ex_audio.wav"
    
    # Extract audio from the video
    extract_audio_from_video(video_path, wav_audio_path)
    
    # Transcribe the .wav audio to text
    transcribed_text = transcribe_audio_to_text(wav_audio_path)
    
    # Optional: Save the transcription to a text file
    if transcribed_text:
        with open("transcription.txt", "w") as f:
            f.write(transcribed_text)
        print("Transcription saved to transcription.txt")