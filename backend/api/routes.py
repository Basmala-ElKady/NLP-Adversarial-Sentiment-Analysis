from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.predictor import get_prediction
from backend.services.attacker import run_attack

router = APIRouter()

class SentimentRequest(BaseModel):
    text: str

class AttackRequest(BaseModel):
    text: str
    attack_name: str = "textfooler"

@router.get("/")
def home():
    return {"message": "Robust Sentiment Analysis API is running."}

@router.post("/predict")
def predict(request: SentimentRequest):
    result = get_prediction(request.text)
    return result

@router.post("/attack")
def attack(request: AttackRequest):
    result = run_attack(request.text, request.attack_name)
    adv_prediction = get_prediction(result["perturbed_text"])
    
    return {
        **result,
        "prediction": adv_prediction["prediction"]
    }
