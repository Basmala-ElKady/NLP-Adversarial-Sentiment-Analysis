import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import torch
import torch.nn.functional as F
from nlp.src.model_loader import get_model, get_tokenizer, get_device

def predict_sentiment(text: str, apply_defense: bool = True):
    """Predicts sentiment for a given text using the robust model in a fast, simple manner."""
    model = get_model()
    tokenizer = get_tokenizer()
    device = get_device()
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)
    confidence, predicted_class = torch.max(probs, dim=-1)
    
    label = "Positive" if predicted_class.item() == 1 else "Negative"
    
    return {
        "text": text,
        "prediction": label,
        "confidence": round(confidence.item(), 4)
    }
