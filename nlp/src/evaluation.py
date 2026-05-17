import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
from nlp.src.config import JSON_DIR, CSV_DIR
import pandas as pd

def compute_metrics(results):
    """Computes precision, recall, F1, ASR from attack results."""
    total = len(results)
    success = sum(1 for r in results if r['success'])
    failed = total - success
    asr = success / total if total > 0 else 0
    
    metrics = {
        "total_samples": total,
        "successful_attacks": success,
        "failed_attacks": failed,
        "attack_success_rate": round(asr, 4)
    }
    return metrics

def save_evaluation_results(results, attack_name):
    """Saves metrics to JSON and detailed results to CSV."""
    metrics = compute_metrics(results)
    
    # Save JSON
    with open(JSON_DIR / f"{attack_name}_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    # Save CSV
    df = pd.DataFrame(results)
    df.to_csv(CSV_DIR / f"{attack_name}_details.csv", index=False)
    
    return metrics
