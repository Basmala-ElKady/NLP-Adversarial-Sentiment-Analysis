import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from app.core.config import MODEL_PATH


device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_PATH
)

model = (
    AutoModelForSequenceClassification
    .from_pretrained(MODEL_PATH)
)

model.to(device)

model.eval()
