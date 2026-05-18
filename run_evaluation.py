import os
import sys
import argparse
import matplotlib.pyplot as plt
import pandas as pd

# Inject root directory into sys.path to allow nlp imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp.src.inference import predict_sentiment
from nlp.src.attack_pipeline import pipeline
from nlp.src.config import PLOTS_DIR, REPORTS_DIR, CSV_DIR, JSON_DIR
from nlp.src.evaluation import save_evaluation_results

def run_benchmarking(attack_name="deepwordbug"):
    print("=" * 60)
    print(f"🤖 STARTING ROBUST SENTIMENT ANALYSIS BENCHMARK ({attack_name.upper()}) 🤖")
    print("=" * 60)
    
    # 1. High-quality diverse evaluation dataset (Positive = 1, Negative = 0)
    test_suite = [
        {"text": "This movie is an absolute masterpiece of modern cinema.", "label": 1},
        {"text": "I hated every single second of this dreadfully boring film.", "label": 0},
        {"text": "The acting was superb and the plot was incredibly engaging.", "label": 1},
        {"text": "It was a total waste of money and time, poorly directed.", "label": 0},
        {"text": "An excellent and highly entertaining thriller with great cast.", "label": 1},
        {"text": "Terrible script, awful performance, and extremely slow pacing.", "label": 0},
        {"text": "Highly recommended! One of the best movies of the year.", "label": 1},
        {"text": "The story was predictable and completely lacked any emotion.", "label": 0},
        {"text": "Brilliant cinematography and deeply moving characters.", "label": 1},
        {"text": "Unwatchable trash. I do not recommend this to anyone.", "label": 0}
    ]
    
    results = []
    clean_correct = 0
    adv_correct = 0
    attack_successes = 0
    
    print("\n[+] Running inference and simulating adversarial perturbations...")
    
    for i, item in enumerate(test_suite, 1):
        text = item["text"]
        true_label_id = item["label"]
        true_label = "Positive" if true_label_id == 1 else "Negative"
        
        # Clean prediction
        clean_pred = predict_sentiment(text)
        clean_pred_label = clean_pred["prediction"]
        clean_conf = clean_pred["confidence"]
        is_clean_correct = clean_pred_label == true_label
        
        if is_clean_correct:
            clean_correct += 1
            
        # Adversarial attack
        attack_res = pipeline.attack_text(text, attack_name)
        perturbed_text = attack_res["perturbed_text"]
        
        # Adversarial prediction
        adv_pred = predict_sentiment(perturbed_text)
        adv_pred_label = adv_pred["prediction"]
        adv_conf = adv_pred["confidence"]
        is_adv_correct = adv_pred_label == true_label
        
        if is_adv_correct:
            adv_correct += 1
            
        # Attack success (True if model was correct on clean but got fooled on adversarial)
        attack_success = is_clean_correct and (not is_adv_correct)
        if attack_success:
            attack_successes += 1
            
        print(f"[{i}/{len(test_suite)}] True: {true_label} | Clean Pred: {clean_pred_label} ({clean_conf:.2f}) -> Perturbed Pred: {adv_pred_label} ({adv_conf:.2f})")
        
        results.append({
            "original_text": text,
            "perturbed_text": perturbed_text,
            "true_label": true_label,
            "clean_prediction": clean_pred_label,
            "clean_confidence": clean_conf,
            "perturbed_prediction": adv_pred_label,
            "perturbed_confidence": adv_conf,
            "clean_correct": is_clean_correct,
            "adv_correct": is_adv_correct,
            "attack_success": attack_success
        })
        
    total_samples = len(test_suite)
    clean_accuracy = clean_correct / total_samples
    adv_accuracy = adv_correct / total_samples
    attack_success_rate = attack_successes / clean_correct if clean_correct > 0 else 0
    
    # 2. Save detailed reports
    report_path = REPORTS_DIR / "robustness_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"📊 ADVERSARIAL ROBUSTNESS REPORT ({attack_name.upper()})\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total Test Samples: {total_samples}\n")
        f.write(f"Clean Model Accuracy: {clean_accuracy:.2%}\n")
        f.write(f"Robust Model Accuracy under Attack: {adv_accuracy:.2%}\n")
        f.write(f"Attack Success Rate (ASR): {attack_success_rate:.2%}\n\n")
        f.write("-" * 60 + "\n")
        f.write("Detailed Samples:\n")
        for res in results:
            f.write(f"Original:  \"{res['original_text']}\" (Pred: {res['clean_prediction']})\n")
            f.write(f"Perturbed: \"{res['perturbed_text']}\" (Pred: {res['perturbed_prediction']})\n")
            f.write(f"Success: {res['attack_success']}\n\n")
            
    print(f"\n[+] Detailed evaluation text report saved to: {report_path}")
    
    # Save CSV and JSON using our module
    save_evaluation_results([{
        "success": r["attack_success"],
        "original_text": r["original_text"],
        "perturbed_text": r["perturbed_text"]
    } for r in results], attack_name)
    
    # 3. Generate and save premium visual charts
    print("\n[+] Generating comparative performance visualization...")
    
    # Set a clean plot style using standard matplotlib settings
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = '#f3f4f6'
    plt.rcParams['grid.color'] = '#e5e7eb'
    plt.rcParams['grid.linestyle'] = '--'
    
    # Accuracy Comparison Plot
    plt.figure(figsize=(8, 6))
    modes = ["Clean Text\n(No Attack)", "Adversarial Text\n(Under Attack)"]
    accuracies = [clean_accuracy, adv_accuracy]
    colors = ["#10b981", "#ef4444"] # Premium green & red
    
    bars = plt.bar(modes, accuracies, color=colors, width=0.4, edgecolor='black', linewidth=0.7)
    plt.ylim(0, 1.1)
    plt.grid(True, axis='y', zorder=0)
    
    # Put bars in front of grid
    for bar in bars:
        bar.set_zorder(3)
        
    plt.ylabel("Accuracy Rate (0.0 - 1.0)", fontsize=12, fontweight='bold', labelpad=10)
    plt.title(f"Model Performance Degradation under {attack_name.upper()} Attack", fontsize=14, fontweight='bold', pad=15)
    
    # Annotate bars
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f"{height:.1%}", 
                    xy=(bar.get_x() + bar.get_width() / 2., height),
                    xytext=(0, 5), 
                    textcoords='offset points', ha='center', va='bottom', 
                    fontsize=12, fontweight='bold')
                    
    plot_path = PLOTS_DIR / "robustness_accuracy_comparison.png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    plt.close()
    
    print(f"[+] Comparative accuracy bar plot saved to: {plot_path}")
    
    # Confidence Score distribution plot using histogram
    plt.figure(figsize=(9, 5))
    clean_confs = [r["clean_confidence"] for r in results]
    adv_confs = [r["perturbed_confidence"] for r in results]
    
    plt.hist(clean_confs, bins=10, alpha=0.6, label='Clean Text Confidence', color='#10b981', edgecolor='#059669', zorder=3)
    plt.hist(adv_confs, bins=10, alpha=0.6, label='Adversarial Text Confidence', color='#ef4444', edgecolor='#dc2626', zorder=3)
    plt.grid(True, zorder=0)
    
    plt.title("Distribution of Model Confidence", fontsize=13, fontweight='bold', pad=12)
    plt.xlabel("Confidence Score", fontsize=11, fontweight='bold', labelpad=8)
    plt.ylabel("Frequency", fontsize=11, fontweight='bold', labelpad=8)
    plt.legend(loc="upper left", fontsize=10)
    
    plot_conf_path = PLOTS_DIR / "confidence_score_distribution.png"
    plt.tight_layout()
    plt.savefig(plot_conf_path, dpi=300)
    plt.close()
    
    print(f"[+] Confidence score distribution chart saved to: {plot_conf_path}")
    
    # 4. Print beautiful terminal summary report
    print("\n" + "=" * 60)
    print("📊 ADVERSARIAL COMPARISON SUMMARY")
    print("=" * 60)
    print(f"✔️  Clean Model Accuracy:            {clean_accuracy:.2%}")
    print(f"❌  Adversarial Accuracy:          {adv_accuracy:.2%}")
    print(f"💥  Attack Success Rate (ASR):     {attack_success_rate:.2%}")
    print("-" * 60)
    print("✨ SUCCESS: Comparison completed! Visual charts and reports saved.")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model robustness on clean vs adversarial text.")
    parser.add_argument("--attack", type=str, default="deepwordbug", 
                        choices=["textfooler", "bae", "deepwordbug", "pwws"], 
                        help="TextAttack recipe to run (default: deepwordbug)")
    args = parser.parse_args()
    run_benchmarking(args.attack)
