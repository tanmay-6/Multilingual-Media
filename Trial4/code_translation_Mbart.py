from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

def translate_text_mbart(text, source_language, target_language):
    # Load the mBART model and tokenizer
    model_name = "facebook/mbart-large-50-many-to-many-mmt"
    model = MBartForConditionalGeneration.from_pretrained(model_name)
    tokenizer = MBart50TokenizerFast.from_pretrained(model_name)

    # Set the tokenizer's source and target language
    tokenizer.src_lang = source_language
    encoded_text = tokenizer(text, return_tensors="pt")

    # Translate and decode the result
    generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.lang_code_to_id[target_language])
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    return translated_text

# Example usage
text_to_translate = "Hello, how are you today?"
source_language = "en_XX"  # English
target_language = "hi_IN"  # Hindi

translated_text = translate_text_mbart(text_to_translate, source_language, target_language)
print(f"Translated Text: {translated_text}")
