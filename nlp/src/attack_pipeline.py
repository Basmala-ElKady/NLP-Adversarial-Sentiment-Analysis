import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from textattack.models.wrappers import HuggingFaceModelWrapper
from textattack.attack_recipes import (
    TextFoolerJin2019,
    BAEGarg2019,
    DeepWordBugGao2018,
    PWWSRen2019
)
from textattack.datasets import HuggingFaceDataset
from textattack import Attacker, AttackArgs
from nlp.src.model_loader import model, tokenizer
from nlp.src.config import SUPPORTED_ATTACKS

class AdversarialAttackPipeline:
    def __init__(self):
        self.model_wrapper = HuggingFaceModelWrapper(model, tokenizer)
        self.recipes = {
            "textfooler": TextFoolerJin2019,
            "bae": BAEGarg2019,
            "deepwordbug": DeepWordBugGao2018,
            "pwws": PWWSRen2019
        }

    def _get_recipe(self, attack_name):
        attack_name = attack_name.lower()
        if attack_name not in self.recipes:
            raise ValueError(f"Attack {attack_name} not supported. Choose from {SUPPORTED_ATTACKS}")
        return self.recipes[attack_name].build(self.model_wrapper)

    def attack_text(self, text: str, attack_name: str):
        """Perform attack on a single text."""
        recipe = self._get_recipe(attack_name)
        result = recipe.attack(text, 1) # Assumes target label 1 for simplicity, textattack automatically handles this if dataset is provided.
        # Actually for single text without label, textattack is trickier. We can just use the wrapper to get initial label.
        initial_pred = self.model_wrapper([text])[0].argmax()
        result = recipe.attack(text, initial_pred)
        
        return {
            "original_text": text,
            "perturbed_text": str(result.perturbed_text()) if result.perturbed_text() else text,
            "original_label": int(initial_pred),
            "perturbed_label": int(result.perturbed_result.output) if result.perturbed_text() else int(initial_pred),
            "attack_name": attack_name,
            "success": result.perturbed_result.output != initial_pred if result.perturbed_text() else False
        }

    def evaluate_dataset(self, dataset, attack_name: str, num_examples: int = 100):
        """Evaluate attack on a dataset using TextAttack Attacker."""
        recipe = self._get_recipe(attack_name)
        attack_args = AttackArgs(
            num_examples=num_examples,
            log_to_csv=f"results/csv/{attack_name}_results.csv",
            log_to_txt=f"results/reports/{attack_name}_report.txt",
            disable_stdout=True
        )
        
        attacker = Attacker(recipe, dataset, attack_args)
        results = attacker.attack_dataset()
        return results

pipeline = AdversarialAttackPipeline()
