import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import torch
import torch.nn.functional as F
from nlp.src.model_loader import model, tokenizer, device

def predict_sentiment(text: str):
    """Predicts sentiment for a given text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128, padding=True).to(device)
    
    with torch.no_grad():
        outputs = model(**inputs)
        
    logits = outputs.logits
    probs = F.softmax(logits, dim=-1)
    confidence, predicted_class = torch.max(probs, dim=-1)
    
    # Assuming label 1 is Positive and 0 is Negative (update based on your dataset)
    label = "Positive" if predicted_class.item() == 1 else "Negative"
    
    return {
        "text": text,
        "prediction": label,
        "confidence": round(confidence.item(), 4)
    }
