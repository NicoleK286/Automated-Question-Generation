import warnings
warnings.filterwarnings("ignore", message="`prepare_seq2seq_batch` is deprecated")
import re
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def preprocess_input_text(input_text):
    # Tokenize the input_text
    tokens = tokenizer.tokenize(input_text)

    # Capitalize the first worda
    
    if len(tokens) > 0:
        tokens[0] = tokens[0].capitalize()

    # Remove periods in the middle of the sentence
    for i in range(1, len(tokens) - 1):
        if tokens[i] == '.':
            tokens[i] = ''

    # Remove consecutive repeated words within a sentence
    tokens = [re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', token, flags=re.IGNORECASE) for token in tokens]

    # Ensure appropriate spacings between words
    processed_text = ' '.join(tokens)

    return processed_text

def get_response(input_text, num_return_sequences):
    # Preprocess input_text
    input_text = preprocess_input_text(input_text)

    # Generate response
    batch = tokenizer(input_text, truncation=True, padding='longest', max_length=60, return_tensors="pt").to(torch_device)
    translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)
    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    return tgt_text

# Example usage:
input_text = "this is a sample sentence. it has multiple periods. let's process it."
response = get_response(input_text, num_return_sequences=1)
#print(response)
