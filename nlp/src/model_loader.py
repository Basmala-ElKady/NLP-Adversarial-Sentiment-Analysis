import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from nlp.src.config import MODEL_DIR
import os

class ModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        """Loads the robust model and tokenizer once."""
        if not os.path.exists(MODEL_DIR):
            raise FileNotFoundError(f"Model directory {MODEL_DIR} not found. Ensure model is placed there.")
            
        print("Loading robust model and tokenizer from local path...")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        self.model.to(self.device)
        self.model.eval()
        print("Model loaded successfully.")

# Singleton instance
loader = ModelLoader()
tokenizer = loader.tokenizer
model = loader.model
device = loader.device
