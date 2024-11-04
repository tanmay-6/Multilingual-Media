from transformers import MarianMTModel, MarianTokenizer, pipeline
from language_codes_MB import language_codes


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

def translate_text(text, source_language, target_language):
    # Construct the model name based on source and target languages
    model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"

    # Load the tokenizer and model
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    
    # Initialize the translation pipeline
    translator = pipeline("translation", model=model, tokenizer=tokenizer)

    # Translate the text
    translation = translator(text, max_length=512)
    
    # Extract and print the translated text
    translated_text = translation[0]["translation_text"]
    print(f"Translation ({source_language} -> {target_language}):\n", translated_text)
    
    return translated_text

def write_srt_file(subtitle_list, file_name="translated_sub.srt"):
    output_file = file_name

    # Open the output .srt file for writing
    with open(output_file, 'w', encoding='utf-8') as srt_file:
        for line in subtitle_list:
            for l in line:
                srt_file.write(l + "\n")
            # Write each line to the output .srt file
            srt_file.write("\n")

if __name__ == "__main__":
    srt_file_path = 'subtitle.srt' # Path to the .srt file
    srt_content = read_srt_file(srt_file_path) # get content from srt type string
    segments = split_by_linebreak(srt_content) # split the content by line breaks type list.
    
    for i in range(len(segments)):
        segments[i] = split_string_to_list(segments[i])
    
    if segments[-1][0] == '':
        segments.pop()
    
    print("The language codes are as follows:")
    source = "english"

    while(source not in language_codes):
        source = input("Enter the source language code: ").lower()
    target = "hindi"
    while(target not in language_codes):
        target = input("Enter the target language code: ").lower()

    source_code = language_codes[source]
    target_code = language_codes[target]

    for i in range(len(segments)):
        print(i, end="~")
        segments[i][2] = translate_text(segments[i][2], source_code, target_code)
    
    write_srt_file(segments, "translated_sub.txt")
    #successfully converted all the subtitles
    #could not used be used for a long context.
