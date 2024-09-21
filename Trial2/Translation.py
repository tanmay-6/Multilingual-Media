import google.generativeai as genai
import os
from Key import API_KEY # type: ignore
# Set up your API key (ensure it's kept safe and not exposed)

genai.configure(api_key=API_KEY)

# Use the correct model and function
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Read the text from the file
with open("transcription.txt", "r") as file:
    text = file.read()

# Make the API call using the correct function 'model.generate'
response = model.generate_content(f"Translate the following text into Hindi Language:\n{text}")

translated_transcribe = response.candidates[0].content.parts[0].text
print(type(translated_transcribe))
# Write the translated text to a new file
with open('translated_text.txt', 'w', encoding='utf-8') as file:
    file.write(translated_transcribe)