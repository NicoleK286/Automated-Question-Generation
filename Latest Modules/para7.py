import language_tool_python
import torch
import re
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

# Create a LanguageTool instance
lang_tool = language_tool_python.LanguageTool('en-US')


model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)

# Create a LanguageTool instance
lang_tool = language_tool_python.LanguageTool('en-US')

def preprocess_input_text(input_text):
    # Correct grammar using LanguageTool
    matches = lang_tool.check(input_text)
    corrected_text = lang_tool.correct(input_text)

    # Capitalize the first word of the first sentence
    corrected_tokens = corrected_text.split()
    corrected_tokens[0] = corrected_tokens[0].capitalize()

    # Remove periods in the middle of the sentence
    corrected_tokens = [token if token != '.' else '' for token in corrected_tokens]

    # Remove consecutive repeated words within a sentence
    corrected_tokens = [re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', token, flags=re.IGNORECASE) for token in corrected_tokens]

    # Correct consecutive articles
    tokens = []
    for i, token in enumerate(corrected_tokens):
        if i > 0 and token.lower() in ['the', 'this'] and corrected_tokens[i - 1].lower() in ['which', 'what']:
            # Skip appending "the" after "which" or "what"
            continue
        else:
            tokens.append(token)

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
#input_text = "Which The American Community Survey table from which the data is compiled has Assigned three - digit code that represents summary level of a geographic level that is not equal to 140 ?"
#response = get_response(input_text, num_return_sequences=1)
#print(response)