from fastapi import APIRouter

from app.schemas.sentiment_schema import (
    SentimentRequest
)

from app.services.predictor import (
    predict_sentiment
)

router = APIRouter()


@router.get("/")
def home():

    return {
        "message": (
            "Robust Sentiment Analysis API"
        )
    }


@router.post("/predict")
def predict(
    request: SentimentRequest
):

    prediction = predict_sentiment(
        request.text
    )

    return {
        "prediction": prediction
    }
