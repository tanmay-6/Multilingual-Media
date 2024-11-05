import whisper

def generate_srt(audio_file_path, output_srt_path):
    # Load the Whisper model
    model = whisper.load_model("base")  # You can use "tiny", "small", "medium", or "large" based on your setup

    # Transcribe the audio and get segments with timestamps
    result = model.transcribe(audio_file_path, task="transcribe")

    # Initialize an SRT file content
    srt_content = ""
    for i, segment in enumerate(result["segments"]):
        # Format SRT index, start time, end time, and text
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"].strip()

        # Create an SRT entry
        srt_content += f"{i + 1}\n{start_time} --> {end_time}\n{text}\n\n"

    # Write the SRT content to a file
    with open(output_srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)

    print(f"SRT file generated and saved to {output_srt_path}")

def format_timestamp(seconds):
    """Helper function to format timestamp in SRT format (HH:MM:SS,MS)"""
    hrs, secs = divmod(int(seconds), 3600)
    mins, secs = divmod(secs, 60)
    msecs = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{msecs:03}"

# Example usage
audio_file = "aud1.wav"  # Replace with the path to your audio file
output_srt = "sub_whisper.srt"          # Desired output file path
generate_srt(audio_file, output_srt)
