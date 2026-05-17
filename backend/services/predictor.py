from nlp.src.inference import predict_sentiment

def get_prediction(text: str):
    """Wrapper for the prediction service using nlp folder."""
    return predict_sentiment(text)
