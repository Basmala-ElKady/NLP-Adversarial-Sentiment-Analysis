import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import matplotlib.pyplot as plt
import seaborn as sns
from nlp.src.config import PLOTS_DIR

def plot_attack_success_rate(attack_metrics: dict):
    """Plots attack success rate for different attack recipes."""
    attacks = list(attack_metrics.keys())
    asrs = [metrics['attack_success_rate'] for metrics in attack_metrics.values()]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=attacks, y=asrs, palette="viridis")
    plt.title("Attack Success Rate (ASR) per Recipe")
    plt.ylabel("ASR")
    plt.xlabel("Attack Method")
    plt.ylim(0, 1)
    
    plot_path = PLOTS_DIR / "attack_success_rate.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path

def plot_confidence_comparison(clean_conf, adv_conf):
    """Plots distribution of model confidence before and after attack."""
    plt.figure(figsize=(10, 6))
    sns.kdeplot(clean_conf, label='Clean Confidence', fill=True, color='blue')
    sns.kdeplot(adv_conf, label='Adversarial Confidence', fill=True, color='red')
    plt.title("Confidence Score Comparison")
    plt.xlabel("Confidence")
    plt.ylabel("Density")
    plt.legend()
    
    plot_path = PLOTS_DIR / "confidence_comparison.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path
