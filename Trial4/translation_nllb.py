from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from language_codes_NL import language_codes


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
    # Load the NLLB-200-distilled model and tokenizer
    model_name = "facebook/nllb-200-distilled-600M"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Set the source language and tokenize the input text
    tokenizer.src_lang = source_language
    encoded_text = tokenizer(text, return_tensors="pt")

    # Find the token ID for the target language and set it as the forced_bos_token_id
    target_lang_token_id = tokenizer.convert_tokens_to_ids(target_language)
    generated_tokens = model.generate(**encoded_text, forced_bos_token_id=target_lang_token_id)

    # Decode and return the translated text
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
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
    
    write_srt_file(segments, "translated_sub_nllb.srt")
    print("Successfully converted all the subtitles")
    #successfully converted all the subtitles
    #could not used be used for a long context.
