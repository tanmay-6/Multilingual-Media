import google.generativeai as genai
from Key import API_KEY

def read_srt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    return srt_content

def split_by_linebreak(srt_content):
    segments_of_srt = srt_content.split('\n\n')
    return segments_of_srt

def split_string_to_list(input_string):
    # Split the string by newlines
    lines = input_string.split('\n')
    
    # Initialize a list of size 3 with empty strings
    result = ["", "", ""]
    
    # Assign the first line, second line, and the rest to the list
    if len(lines) > 0:
        result[0] = lines[0]  # First line
    if len(lines) > 1:
        result[1] = lines[1]  # Second line
    if len(lines) > 2:
        result[2] = '\n'.join(lines[2:])  # The rest of the string
    
    return result

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
    #code is required for the audio generation
    return language, code

def translate_text(text, language="hindi"):
    genai.configure(api_key=API_KEY)

    # Use the correct model and function
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    prompt_tuning = """
### Translation Task with Specific Conditions:

- Input text may contain multiple text lines separated by blank lines. Keep the number of text lines in the output identical to the input.
- Ensure every line of text is translated.
- If any inappropriate or offensive word is detected in the input, replace it with the '*' symbol. Do not skip any words or lines.
- If the input contains a single word, still translate it as a complete output.
- if the text is not understandable put a dollar sign in the output.

Input Example:

I think you already know that if you
want to improve your English speaking ability, you

will have to practice, right?

ass vsda cse.

You will have to speak.

damn it!
---

Output should follow the same format with translated text:
- Maintain text lines as in the original text.
- Replace any inappropriate words with '$' (e.g., curse words or sensitive terms).

Output Example:

मुझे लगता है कि आप पहले से ही जानते हैं कि यदि आप
अपनी अंग्रेजी बोलने की क्षमता में सुधार करना चाहते हैं, तो आप

अभ्यास करना होगा, है ना?

$

आपको बोलना होगा।

****!
"""


    response = model.generate_content(f"""
        {prompt_tuning}                              
        Translate the following text into {language} Language.
        The text is:\n{text}""")
    
    try:
        translated_transcribe = response.candidates[0].content.parts[0].text
        return translated_transcribe
        # Write the translated text to a new file
        
    except Exception as e:
        print(f"Translation failed: {e}")
        return ""

def write_srt_file(subtitle_list, file_name="translated_sub.srt"):
    output_file = 'translated_sub.srt'

    # Open the output .srt file for writing
    with open(output_file, 'w', encoding='utf-8') as srt_file:
        for line in subtitle_list:
            for l in line:
                srt_file.write(l + "\n")
            # Write each line to the output .srt file
            srt_file.write("\n")

if __name__ == "__main__":
    srt_file_path = 'subtitle.srt'
    srt_content = read_srt_file(srt_file_path)
    segments = split_by_linebreak(srt_content)

    while(len(segments) > 0 and segments[-1] == ""):
        segments.pop()

    for i in range(len(segments)):
        segments[i] = split_string_to_list(segments[i])

    language, code = choose_language()

    text_to_translate = ""
    for segment in segments:
        text_to_translate += segment[2] + "\n\n"

    translated_text = translate_text(text_to_translate, language)

    translated_segments = split_by_linebreak(translated_text)

    while(len(translated_segments) > 0 and (translated_segments[-1] == None or translated_segments[-1] == "")):
        translated_segments.pop()

    print("lens :",len(segments))
    print("lent :",len(translated_segments))
    # print("type :",type(translated_segments))
    # print("first_t sample :",translated_segments[0])
    # print("first_s sample :",segments[0])
    # print("last_t sample :",translated_segments[-1])
    # print("last_s sample :",segments[-1])
    # print("last_t type :",type(translated_segments[-1]))
    # print("last_s type :",type(segments[-1]))

    for i in range(min(len(segments), len(translated_segments))):
        segments[i][2] = translated_segments[i]
        #print(segments[i], "\n\n")
    
    write_srt_file(segments, "translated_sub.txt")