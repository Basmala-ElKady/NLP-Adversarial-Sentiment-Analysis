from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from nlp.src.model_loader import loader # ensures model is loaded on startup from nlp/src/

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
