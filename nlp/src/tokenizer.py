from transformers import AutoTokenizer


MODEL_NAME = "distilbert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def tokenize_function(examples):
    """
    Tokenize input sentences.

    Args:
        examples (dict): Batch of text samples.

    Returns:
        dict: Tokenized output.
    """

    return tokenizer(
        examples["sentence"],
        padding="max_length",
        truncation=True
    )
