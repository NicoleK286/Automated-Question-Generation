import spacy
import torch
import re
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def preprocess_input_text(input_text):
    # Apply spaCy for grammar correction and tokenization
    doc = nlp(input_text)
    
    # Capitalize the first word of the first sentence
    tokens = [doc[0].text.capitalize()] + [token.text for token in doc[1:]]

    # Correct consecutive articles
    corrected_tokens = []
    for i, token in enumerate(tokens):
        if i > 0 and token.lower() in ['the', 'this'] and tokens[i - 1].lower() in ['which', 'what']:
            # Skip appending "the" after "which" or "what"
            continue
        else:
            corrected_tokens.append(token)

    # Remove periods in the middle of the sentence
    for i in range(1, len(corrected_tokens) - 1):
        if corrected_tokens[i] == '.':
            corrected_tokens[i] = ''

    # Remove consecutive repeated words within a sentence
    corrected_tokens = [re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', token, flags=re.IGNORECASE) for token in corrected_tokens]

    # Ensure appropriate spacings between words
    processed_text = ' '.join(corrected_tokens)

    return processed_text

def get_response(input_text, num_return_sequences):
    # Preprocess input_text
    input_text = preprocess_input_text(input_text)

    # Generate response using Pegasus
    batch = tokenizer(input_text, truncation=True, padding='longest', max_length=60, return_tensors="pt").to(torch_device)
    translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return tgt_text

# Example usage:
input_text = "Which The American Community Survey table from which the data is compiled has Assigned three - digit code that represents summary level of a geographic level that is not equal to 140 ?"
response = get_response(input_text, num_return_sequences=1)
print(response)
