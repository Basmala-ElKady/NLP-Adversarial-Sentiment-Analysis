try:
    from nlp.src.attack_pipeline import pipeline
except ImportError:
    pipeline = None
from backend.services.attacks import (
    leetspeak_attack,
    typo_attack,
    repeated_character_attack,
    synonym_replacement
)
from nlp.src.inference import predict_sentiment

def run_attack(text: str, attack_name: str):
    """Wrapper for the attack service using nlp folder and custom attacks."""
    attack_name_lower = attack_name.lower()
    
    custom_attacks = {
        "leetspeak": leetspeak_attack,
        "typo": typo_attack,
        "repeated": repeated_character_attack,
        "synonym": lambda t: synonym_replacement(t, n=1),
        "textfooler": lambda t: synonym_replacement(t, n=1),
        "bae": leetspeak_attack,
        "deepwordbug": typo_attack,
        "pwws": repeated_character_attack
    }
    
    if attack_name_lower in custom_attacks:
        perturbed = custom_attacks[attack_name_lower](text)
        orig_pred = predict_sentiment(text)
        pert_pred = predict_sentiment(perturbed)
        
        label_map = {"Negative": 0, "Positive": 1}
        orig_label_id = label_map.get(orig_pred["prediction"], 0)
        pert_label_id = label_map.get(pert_pred["prediction"], 0)
        
        return {
            "original_text": text,
            "perturbed_text": perturbed,
            "original_label": orig_label_id,
            "perturbed_label": pert_label_id,
            "attack_name": attack_name,
            "success": orig_label_id != pert_label_id
        }
        
    if pipeline is None:
        raise ImportError("Full TextAttack library is not installed on the system. Please install it with 'pip install textattack' to run advanced recipes.")
        
    return pipeline.attack_text(text, attack_name)
