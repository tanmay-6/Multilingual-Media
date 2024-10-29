from gtts import gTTS
from moviepy.editor import AudioFileClip, concatenate_audioclips
import re
import os
from datetime import timedelta
import shutil

def parse_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        contents = file.read()

    # Regular expression to match each subtitle block
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\n(.*?)\n\n', re.DOTALL)
    subtitles = []

    for match in pattern.finditer(contents):
        index = match.group(1)
        start_time_str = match.group(2).replace(',', '.')
        end_time_str = match.group(3).replace(',', '.')
        text = match.group(4).replace('\n', ' ')

        # Convert times to timedelta for easier duration calculation
        start_time = timedelta(hours=int(start_time_str[:2]), minutes=int(start_time_str[3:5]), seconds=int(start_time_str[6:8]), milliseconds=int(start_time_str[9:]))
        end_time = timedelta(hours=int(end_time_str[:2]), minutes=int(end_time_str[3:5]), seconds=int(end_time_str[6:8]), milliseconds=int(end_time_str[9:]))
        duration = (end_time - start_time).total_seconds()
        
        subtitles.append({
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "text": text
        })
    return subtitles

def generate_audio_from_subtitles(subtitle_file, output_file, language='hi'):
    # Parse the subtitles manually
    subtitles = parse_srt(subtitle_file)
    audio_clips = []

    # Create a local directory to store audio clips
    audio_clips_dir = "audio_clips"
    os.makedirs(audio_clips_dir, exist_ok=True)

    for i, sub in enumerate(subtitles):
        # Extract the text and duration from each subtitle entry
        text = sub["text"]
        duration = sub["duration"]

        # Generate TTS audio for each subtitle line
        tts = gTTS(text, lang=language)
        temp_audio_path = os.path.join(audio_clips_dir, f"clip_{i}.mp3")
        tts.save(temp_audio_path)
        
        # Load the audio clip and enforce its duration to match the subtitle timing
        audio_clip = AudioFileClip(temp_audio_path).subclip(0, min(duration, AudioFileClip(temp_audio_path).duration))
        audio_clips.append(audio_clip)

    # Concatenate all audio clips to form a continuous audio and write it to the output file
    final_audio = concatenate_audioclips(audio_clips)
    final_audio.write_audiofile(output_file, codec='mp3')

    # Close and release each audio clip to avoid file locking issues
    for clip in audio_clips:
        clip.close()

    # Clean up by removing the audio clips directory and its contents
    shutil.rmtree(audio_clips_dir)
    print(f"Audio generated and saved to {output_file}")

# Example usage
subtitle_file = "translated_sub.srt"  # Replace with the path to your subtitle file
output_audio_file = "output_audio.mp3"  # Desired output file
#language hardcoded to hindi
generate_audio_from_subtitles(subtitle_file, output_audio_file)
