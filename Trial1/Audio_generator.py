from googletrans import Translator
from gtts import gTTS
import os

# Step 1: Translating the Transcript
def choose_language():
    """Presents language options to the user and returns the selected language code."""
    languages = {
        "1": ("Hindi", "hi"),
        "2": ("Spanish", "es"),
        "3": ("French", "fr"),
        "4": ("Japanese", "ja")
    }

    print("Choose a target language for translation:")
    for key, value in languages.items():
        print(f"{key}: {value[0]}")

    choice = input("Enter the number corresponding to your choice: ")

    if choice in languages:
        return languages[choice][1]
    else:
        print("Invalid choice. Defaulting to Hindi.")
        return "hi"

def translate_transcript(transcript, target_language):
    """Translates the transcript into the target language."""
    translator = Translator()
    translated = translator.translate(transcript, dest=target_language)
    return translated.text

def save_translated_transcript(translated_text, filename="translated_transcript.txt"):
    """Saves the translated transcript to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(translated_text)
    print(f"Translated transcript saved as {filename}")

# Step 2: Transform the Transcript to Audio
def generate_audio_from_transcript(translated_text, language_code, audio_filename="output_audio.mp3"):
    """Generates an audio file from the translated text."""
    tts = gTTS(text=translated_text, lang=language_code)
    tts.save(audio_filename)
    print(f"Audio saved as {audio_filename}")

if __name__ == "__main__":
    # Input Transcript (Example)
    with open("transcript.txt", "r", encoding="utf-8") as f:
        transcript = f.read()

    # Step 1: Choose Language and Translate Transcript
    target_language_code = choose_language()
    translated_transcript = translate_transcript(transcript, target_language_code)
    
    # Save the translated transcript
    save_translated_transcript(translated_transcript, "translated_transcript.txt")

    # Step 2: Convert Translated Transcript to Audio
    generate_audio_from_transcript(translated_transcript, target_language_code, "translated_audio.mp3")
