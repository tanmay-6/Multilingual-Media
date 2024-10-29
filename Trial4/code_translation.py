from transformers import MarianMTModel, MarianTokenizer, pipeline

### This is a demo code for translaion using MarianMTModel

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

# Example usage
text_to_translate = "Hello, how are you today?"
source_language = "en"  # "en" for English
target_language = "hi"  # "hi" for Hindi; use "fr" for French, "de" for German, etc.
translated_text = translate_text(text_to_translate, source_language, target_language)
