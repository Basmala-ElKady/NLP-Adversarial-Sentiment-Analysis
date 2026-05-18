import sys
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from nlp.src.config import MODEL_DIR

class ModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.tokenizer = None
            cls._instance.device = None
        return cls._instance

    def get_model_and_tokenizer(self):
        """Loads and returns model, tokenizer, and device lazily on demand."""
        if self.model is None:
            if not os.path.exists(MODEL_DIR):
                raise FileNotFoundError(f"Model directory {MODEL_DIR} not found. Ensure model is placed there.")
            
            print("[🚀] Lazily loading robust model and tokenizer from local path on demand...")
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
            self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
            self.model.to(self.device)
            self.model.eval()
            print("[✨] Robust model loaded successfully!")
            
        return self.model, self.tokenizer, self.device

# Create a singleton wrapper
loader = ModelLoader()

def get_model():
    return loader.get_model_and_tokenizer()[0]

def get_tokenizer():
    return loader.get_model_and_tokenizer()[1]

def get_device():
    return loader.get_model_and_tokenizer()[2]
