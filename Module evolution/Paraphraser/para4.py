import warnings
warnings.filterwarnings("ignore", message="`prepare_seq2seq_batch` is deprecated")

import torch
from transformers import BartForConditionalGeneration, BartTokenizer

model_name = 'facebook/bart-large-cnn'
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name).to(torch_device)

def get_response(input_text, num_return_sequences):
    batch = tokenizer(input_text, truncation=True, padding='longest', max_length=60, return_tensors="pt").to(torch_device)

    translated = model.generate(**batch, max_length=60, num_beams=10, num_return_sequences=num_return_sequences, temperature=1.5)

    tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

    # Remove the period at the end if it exists
    if tgt_text and tgt_text[0].endswith('.'):
        tgt_text[0] = tgt_text[0][:-1]

    return tgt_text







