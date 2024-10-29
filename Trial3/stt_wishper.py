import whisper

# Very Good for making transcriptions of audio files.

def transcribe_audio_to_text(audio_file_path):
    # Load the Whisper model (use "base" for lightweight processing or "large" for more accurate transcriptions)
    model = whisper.load_model("base")  # You can use "small", "medium", or "large" models for different accuracy levels

    # Transcribe the audio
    result = model.transcribe(audio_file_path)
    
    # Extract and print the text from the result
    transcribed_text = result["text"]
    print("Transcription:\n", transcribed_text)
    
    return transcribed_text

# Example usage
audio_file = "aud1.wav"  # Replace this with the path to your audio file
transcription = transcribe_audio_to_text(audio_file)
