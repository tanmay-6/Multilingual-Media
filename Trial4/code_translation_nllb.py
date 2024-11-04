from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def translate_text_nllb(text, source_language, target_language):
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

# Example usage
text_to_translate = "Hello, how are you?"
source_language = "eng_Latn"  # English
target_language = "hin_Deva"  # Hindi

translated_text = translate_text_nllb(text_to_translate, source_language, target_language)
print(f"Translated Text: {translated_text}")
