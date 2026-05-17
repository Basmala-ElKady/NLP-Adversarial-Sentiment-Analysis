from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Robust Sentiment Analysis API"
)

app.include_router(router)
