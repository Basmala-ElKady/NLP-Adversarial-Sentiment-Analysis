from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from nlp.src.model_loader import loader

# Eagerly load model on startup for zero-latency first request
try:
    print("[🚀] Pre-loading robust model on startup for zero-latency first request...")
    loader.get_model_and_tokenizer()
    print("[✨] Model loaded and ready!")
except Exception as e:
    print(f"[⚠️] Failed to pre-load model on startup: {e}. It will be loaded on first request.")

app = FastAPI(
    title="Robust Sentiment Analysis API",
    description="API for performing inference and adversarial attacks using a trained robust model."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
