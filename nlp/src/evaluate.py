import numpy as np
import torch

from attacks import leetspeak_attack


def evaluate_stability(
    model,
    tokenizer,
    dataset,
    device
):
    """
    Evaluate model robustness
    against adversarial attacks.

    Args:
        model
        tokenizer
        dataset
        device

    Returns:
        float: Stability score.
    """

    results = []

    model.eval()

    for sample in dataset:

        original_text = sample["sentence"]

        perturbed_text = leetspeak_attack(
            original_text
        )

        original_inputs = tokenizer(
            original_text,
            return_tensors="pt",
            truncation=True,
            padding=True
        ).to(device)

        perturbed_inputs = tokenizer(
            perturbed_text,
            return_tensors="pt",
            truncation=True,
            padding=True
        ).to(device)

        with torch.no_grad():

            original_logits = model(
                **original_inputs
            ).logits

            perturbed_logits = model(
                **perturbed_inputs
            ).logits

        original_prediction = torch.argmax(
            original_logits,
            dim=1
        ).item()

        perturbed_prediction = torch.argmax(
            perturbed_logits,
            dim=1
        ).item()

        results.append(
            original_prediction
            == perturbed_prediction
        )

    return np.mean(results)
