import torch


def get_device():
    """
    Detect available device.

    Returns:
        torch.device
    """

    return torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )
