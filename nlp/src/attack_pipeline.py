import sys
import os
# Inject project root directory into sys.path to allow nlp.src imports when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import textattack

# Dynamically mock UniversalSentenceEncoder if tensorflow_hub is not installed
try:
    import tensorflow_hub
except ImportError:
    print("TensorFlow Hub not found. Mocking UniversalSentenceEncoder to run attacks without TensorFlow...")
    import textattack.constraints.semantics.sentence_encoders
    
    class DummyUniversalSentenceEncoder(textattack.constraints.Constraint):
        def __init__(self, *args, **kwargs):
            super().__init__(compare_against_original=True)
        def _check_constraint(self, transformed_text, reference_text):
            return True
            
    textattack.constraints.semantics.sentence_encoders.UniversalSentenceEncoder = DummyUniversalSentenceEncoder
    try:
        import textattack.constraints.semantics.sentence_encoders.universal_sentence_encoder.universal_sentence_encoder as use_mod
        use_mod.UniversalSentenceEncoder = DummyUniversalSentenceEncoder
    except ImportError:
        pass

from textattack.models.wrappers import HuggingFaceModelWrapper
from textattack.attack_recipes import (
    TextFoolerJin2019,
    BAEGarg2019,
    DeepWordBugGao2018,
    PWWSRen2019
)
# Safe multi-version import chain for StopwordModification to prevent crashes across TextAttack versions
try:
    from textattack.constraints.pre_rejection import StopwordModification
except ImportError:
    try:
        from textattack.constraints.pre_rejection.stopword_modification import StopwordModification
    except ImportError:
        try:
            from textattack.constraints.pre_rejection_constraints import StopwordModification
        except ImportError:
            try:
                from textattack.constraints.overlap.stopword_modification import StopwordModification
            except ImportError:
                import textattack
                # Self-healing fallback definition if TextAttack structure differs
                class StopwordModification(textattack.constraints.Constraint):
                    def __init__(self, stopwords=None):
                        super().__init__(compare_against_original=True)
                        from nltk.corpus import stopwords as nltk_stopwords
                        try:
                            self.stopwords = set(nltk_stopwords.words('english'))
                        except Exception:
                            self.stopwords = {"this", "is", "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "with", "by", "of"}
                    def _check_constraint(self, transformed_text, reference_text):
                        ref_words = reference_text.words
                        trans_words = transformed_text.words
                        for i in range(min(len(ref_words), len(trans_words))):
                            if ref_words[i].lower() != trans_words[i].lower():
                                if ref_words[i].lower() in self.stopwords:
                                    return False
                        return True
from textattack.datasets import HuggingFaceDataset
from textattack import Attacker, AttackArgs
from nlp.src.model_loader import get_model, get_tokenizer
from nlp.src.config import SUPPORTED_ATTACKS

class AdversarialAttackPipeline:
    def __init__(self):
        self._model_wrapper = None
        self.recipes = {
            "textfooler": TextFoolerJin2019,
            "bae": BAEGarg2019,
            "deepwordbug": DeepWordBugGao2018,
            "pwws": PWWSRen2019
        }

    @property
    def model_wrapper(self):
        if self._model_wrapper is None:
            self._model_wrapper = HuggingFaceModelWrapper(get_model(), get_tokenizer())
        return self._model_wrapper

    def _ensure_nltk_loaded(self):
        import nltk
        import socket
        # Set a 3-second timeout to prevent the server from hanging on NLTK downloads
        original_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(3.0)
        
        # Quietly download required NLTK resources
        for res in ["punkt", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng", "wordnet", "omw-1.4"]:
            try:
                if res in ["wordnet", "omw-1.4"]:
                    nltk.data.find(f"corpora/{res}")
                elif res == "punkt":
                    nltk.data.find(f"tokenizers/{res}")
                else:
                    nltk.data.find(f"taggers/{res}")
            except LookupError:
                print(f"[NLTK] Downloading missing resource: {res}...")
                try:
                    nltk.download(res, quiet=True)
                except Exception as e:
                    print(f"[NLTK WARNING] Failed to download {res}: {e}.")
            except Exception as e:
                pass
        socket.setdefaulttimeout(original_timeout)

    def _get_recipe(self, attack_name):
        self._ensure_nltk_loaded()
        attack_name = attack_name.lower()
        if attack_name not in self.recipes:
            raise ValueError(f"Attack {attack_name} not supported. Choose from {SUPPORTED_ATTACKS}")
        recipe = self.recipes[attack_name].build(self.model_wrapper)
        # Prevent TextAttack from altering common grammar/syntactic stop-words
        recipe.constraints.append(StopwordModification())
        return recipe

    def attack_text(self, text: str, attack_name: str):
        """Perform attack on a single text."""
        recipe = self._get_recipe(attack_name)
        # Using the wrapper to get initial label for single text without label
        initial_pred = int(self.model_wrapper([text])[0].argmax())
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
