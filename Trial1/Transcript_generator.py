#TODO:add a tag for female and male on basis of their voice in transcript.
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_silence
import os

def extract_audio_from_video(video_path, output_audio_path="audio.wav"):
    """Extracts audio from a video file and saves it as a .wav file."""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_audio_path, codec='pcm_s16le')

def split_audio_on_silence(audio_path, silence_threshold=-40, silence_duration=2000):
    """
    Splits audio wherever there is a break (silence) of at least 2 seconds.
    
    Args:
    - audio_path: Path to the audio file.
    - silence_threshold: Volume level considered as silence (in dB). Default is -40 dB.
    - silence_duration: Minimum duration of silence in milliseconds to split. Default is 2000ms (2 seconds).

    Returns:
    - A list of AudioSegment objects split based on silence.
    """
    audio = AudioSegment.from_wav(audio_path)
    
    # Detect silent chunks (returns [(start, end), ...] in milliseconds)
    silent_ranges = detect_silence(audio, min_silence_len=silence_duration, silence_thresh=silence_threshold)
    
    # Convert silent ranges into split points
    split_points = [0] + [end for _, end in silent_ranges] + [len(audio)]
    
    # Split the audio based on the silent ranges
    chunks = [audio[split_points[i]:split_points[i+1]] for i in range(len(split_points)-1)]
    
    return chunks

def transcribe_audio_chunks_with_timestamps(chunks):
    """Transcribes each chunk and adds timestamps."""
    recognizer = sr.Recognizer()
    transcript = []
    current_time = 0  # Track current time in milliseconds
    
    for index, chunk in enumerate(chunks):
        chunk.export("temp.wav", format="wav")
        with sr.AudioFile("temp.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                # Calculate timestamp in seconds
                minutes, seconds = divmod(current_time // 1000, 60)
                timestamp = f"[{int(minutes):02}:{int(seconds):02}]"
                transcript.append(f"{timestamp} {text}")
            except sr.UnknownValueError:
                transcript.append(f"[{int(minutes):02}:{int(seconds):02}] [Unintelligible]")
            except sr.RequestError as e:
                transcript.append(f"[{int(minutes):02}:{int(seconds):02}] [Error: {e}]")
        
        # Update the current time based on the length of the chunk
        current_time += len(chunk)
    
    # Clean up temporary file
    os.remove("temp.wav")
    
    return transcript
def save_transcript(transcript, output_file="transcript.txt"):
    """Saves the transcript to a text file."""
    with open(output_file, "w") as file:
        for line in transcript:
            file.write(line + "\n")

if __name__ == "__main__":
    video_path = "Vid1.mp4"  # Path to your video file
    audio_path = "aud1.wav"

    # Step 1: Extract audio from the video
    extract_audio_from_video(video_path, audio_path)
    chunks = split_audio_on_silence(audio_path, silence_threshold=-40, silence_duration=2000)

    # Step 2: Transcribe the audio with timestamps
    transcript = transcribe_audio_chunks_with_timestamps(chunks)

    # Step 3: Save the transcript to a file
    save_transcript(transcript, "transcript.txt")

    print("Transcript saved to transcript.txt")
