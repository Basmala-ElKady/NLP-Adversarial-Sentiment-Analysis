import os

from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support
)

from data_loader import load_sst2_dataset
from tokenizer import tokenize_function
from tokenizer import tokenizer
from utils import get_device


MODEL_NAME = "distilbert-base-uncased"

OUTPUT_DIRECTORY = "../models/final_robust_model"


def compute_metrics(eval_prediction):

    predictions, labels = eval_prediction

    predictions = predictions.argmax(axis=1)

    accuracy = accuracy_score(
        labels,
        predictions
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            labels,
            predictions,
            average="binary"
        )
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }


def main():

    print("Loading dataset...")

    dataset = load_sst2_dataset()

    print("Tokenizing dataset...")

    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True
    )

    print("Loading model...")

    model = (
        AutoModelForSequenceClassification
        .from_pretrained(
            MODEL_NAME,
            num_labels=2
        )
    )

    device = get_device()

    model.to(device)

    training_args = TrainingArguments(
        output_dir="../results",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=1,
        weight_decay=0.01,
        logging_steps=50
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["validation"],
        compute_metrics=compute_metrics
    )

    print("Starting training...")

    trainer.train()

    print("Saving model...")

    os.makedirs(
        OUTPUT_DIRECTORY,
        exist_ok=True
    )

    model.save_pretrained(
        OUTPUT_DIRECTORY
    )

    tokenizer.save_pretrained(
        OUTPUT_DIRECTORY
    )

    print("Training completed successfully.")


if __name__ == "__main__":
    main()
