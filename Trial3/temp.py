import google.generativeai as genai
from gtts import gTTS
import os
from Key import API_KEY

def choose_language():
    languages = {
        "1": ("Hindi", "hi"),
        "2": ("Spanish", "es"),
        "3": ("French", "fr"),
        "4": ("Japanese", "ja")
    }
    
    print("Choose a language from the below list")
    for key, value in languages.items():
        print(f"{key}: {value[0]}")

    print("Enter the number corresponding to your choice: ")
    choice = input()
    language = languages.get(choice[0], "Hindi")
    if choice in languages:
        code = languages[choice][1]
    else:
        code = "hi"
    return language, code

def generate_audio_from_transcript(translated_text, language_code, audio_filename="output_audio.mp3"):
    """Generates an audio file from the translated text."""
    tts = gTTS(text=translated_text, lang=language_code)
    tts.save(audio_filename)
    print(f"Audio saved as {audio_filename}")

if __name__ == "__main__":
    # Set up your API key (ensure it's kept safe and not exposed)
    genai.configure(api_key=API_KEY)

    # Use the correct model and function
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    # Read the text from the file
    text = """
    I think you already know that if you want
    to improve your English speaking skills, you

    have to practice, right?

    You have to speak.

    Studying grammar will never improve your speaking.

    Listening to English alone will never improve
    your speaking.

    You have to actually speak.

    """

    # Make the API call using the correct function 'model.generate'
    language, code = choose_language()
    response = model.generate_content(f"Translate the following text into {language} Language keep the line breaks intact:\n{text}")
    print(response)
    try:
        translated_transcribe = response.candidates[0].content.parts[0].text
        print(translated_transcribe)
        # Write the translated text to a new file
        # with open('translated_text.txt', 'w', encoding='utf-8') as file:
        #     file.write(translated_transcribe)
    except Exception as e:
        print(f"Translation failed: {e}")
        exit(1)
    
    # generate_audio_from_transcript(translated_transcribe, code, "translated_audio.mp3")
    # print("Audio file generated successfully")
    