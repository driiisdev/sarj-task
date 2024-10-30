from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import logging
from tqdm import tqdm
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAX_LENGTH = 512
CHUNK_OVERLAP = 50

def initialize_model(model_name: str = "gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token if tokenizer.pad_token is None else tokenizer.pad_token
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    return tokenizer, model, device

def chunk_text(text: str, tokenizer, max_length: int = MAX_LENGTH) -> List[Dict]:
    tokens = tokenizer(text, return_tensors="pt", truncation=False)
    input_ids = tokens['input_ids'][0]
    chunks = []
    position = 0

    while position < len(input_ids):
        end = min(position + max_length, len(input_ids))
        chunk = input_ids[position:end]
        chunks.append({
            'input_ids': chunk,
            'position': position,
            'text': tokenizer.decode(chunk, skip_special_tokens=True)
        })
        position = end - CHUNK_OVERLAP if end < len(input_ids) else end

    return chunks

async def analyze_with_llm(content: str, prompt: str) -> str:

    tokenizer, model, device = initialize_model()

    full_prompt = prompt + "\n" + content
    chunks = chunk_text(full_prompt, tokenizer)
    responses = []

    for chunk in tqdm(chunks, desc="Analyzing text"):
        input_ids = chunk['input_ids'].unsqueeze(0).to(device)
        
        with torch.no_grad():
            output = model.generate(
                input_ids=input_ids,
                max_new_tokens=150,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=tokenizer.pad_token_id
            )
            generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
            responses.append({'text': generated_text, 'position': chunk['position']})
        torch.cuda.empty_cache() 
        
    combined_analysis = " ".join([resp['text'] for resp in sorted(responses, key=lambda x: x['position'])])

    return combined_analysis
