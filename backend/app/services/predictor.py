import torch

from app.core.model_loader import (
    tokenizer,
    model,
    device
)


def predict_sentiment(text):
    """
    Predict sentiment label.

    Args:
        text (str)

    Returns:
        str
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    ).to(device)

    with torch.no_grad():

        logits = model(
            **inputs
        ).logits

    prediction = torch.argmax(
        logits,
        dim=1
    ).item()

    return (
        "Positive"
        if prediction == 1
        else "Negative"
    )
