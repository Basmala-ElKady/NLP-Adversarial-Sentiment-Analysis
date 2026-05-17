from datasets import load_dataset


def load_sst2_dataset():
    """
    Load the SST-2 dataset from the GLUE benchmark.

    Returns:
        DatasetDict:
            train
            validation
            test
    """

    dataset = load_dataset("glue", "sst2")

    return dataset
