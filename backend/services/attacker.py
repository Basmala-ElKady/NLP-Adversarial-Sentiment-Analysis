from nlp.src.attack_pipeline import pipeline

def run_attack(text: str, attack_name: str):
    """Wrapper for the attack service using nlp folder."""
    return pipeline.attack_text(text, attack_name)
