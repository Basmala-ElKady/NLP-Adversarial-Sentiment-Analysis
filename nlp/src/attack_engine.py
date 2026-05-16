import random
import torch
import nltk
from nltk.corpus import wordnet

from textattack.models.wrappers import HuggingFaceModelWrapper

from textattack.attack_recipes import (
    TextFoolerJin2019,
    BAEGarg2020,
    DeepWordBugGao2018,
    PWWSRen2019,
    CLARE2020,
    TextBuggerLi2018,
    HotFlipEbrahimi2017,
    GeneticAlgorithmAlzantot2018
)


class AttackEngine:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.wrapper = HuggingFaceModelWrapper(model, tokenizer)

    def get_attack(self, name):

        attacks = {
            "textfooler": TextFoolerJin2019.build(self.wrapper),
            "bae": BAEGarg2020.build(self.wrapper),
            "deepwordbug": DeepWordBugGao2018.build(self.wrapper),
            "pwws": PWWSRen2019.build(self.wrapper),

            "clare": CLARE2020.build(self.wrapper),
            "textbugger": TextBuggerLi2018.build(self.wrapper),
            "hotflip": HotFlipEbrahimi2017.build(self.wrapper),
            "genetic": GeneticAlgorithmAlzantot2018.build(self.wrapper),
        }

        if name.lower() not in attacks:
            raise ValueError(f"Attack not supported: {name}")

        return attacks[name.lower()]

    def attack_text(self, attack, text):
        return attack.attack(text)

    def batch_attack(self, attack_name, texts, labels=None):

        attack = self.get_attack(attack_name)

        adv_texts = []
        success = 0

        for i, text in enumerate(texts):

            result = attack.attack(text)

            adv_text = str(result.perturbed_text()) if result.perturbed_text() else text

            adv_texts.append(adv_text)

            if labels is not None:
                pred_orig = self.predict(text)
                pred_adv = self.predict(adv_text)

                if pred_orig == labels[i] and pred_adv != labels[i]:
                    success += 1

        return {
            "adversarial_texts": adv_texts,
            "attack_success_rate": success / len(texts) if labels is not None else None
        }

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        with torch.no_grad():
            outputs = self.model(**inputs)

        return torch.argmax(outputs.logits, dim=1).item()


def synonym_replacement(sentence, n=1):
    words = sentence.split()
    new_words = words.copy()

    candidates = list(set([w for w in words if w.isalnum()]))
    random.shuffle(candidates)

    replaced = 0

    for w in candidates:
        synonyms = []

        for syn in wordnet.synsets(w):
            for l in syn.lemmas():
                synonyms.append(l.name())

        if len(synonyms) > 1:
            new = random.choice(list(set(synonyms)))
            new_words = [new if x == w else x for x in new_words]
            replaced += 1

        if replaced >= n:
            break

    return " ".join(new_words)