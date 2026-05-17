import random


LEETSPEAK_MAPPING = {
    "a": "@",
    "e": "3",
    "i": "!",
    "o": "0",
    "s": "$"
}


def leetspeak_attack(sentence):
    """
    Apply leetspeak perturbation.

    Args:
        sentence (str): Original sentence.

    Returns:
        str: Perturbed sentence.
    """

    return "".join(
        LEETSPEAK_MAPPING.get(char.lower(), char)
        for char in sentence
    )


def typo_attack(sentence):
    """
    Remove the last character
    from a random word.

    Args:
        sentence (str): Original sentence.

    Returns:
        str: Modified sentence.
    """

    words = sentence.split()

    if not words:
        return sentence

    random_index = random.randint(0, len(words) - 1)

    if len(words[random_index]) > 1:
        words[random_index] = words[random_index][:-1]

    return " ".join(words)


def repeated_character_attack(sentence):
    """
    Repeat random character
    inside a random word.

    Args:
        sentence (str): Original sentence.

    Returns:
        str: Modified sentence.
    """

    words = sentence.split()

    if not words:
        return sentence

    random_index = random.randint(0, len(words) - 1)

    word = words[random_index]

    if len(word) > 1:

        char_index = random.randint(0, len(word) - 1)

        word = (
            word[:char_index]
            + word[char_index] * 2
            + word[char_index:]
        )

    words[random_index] = word

    return " ".join(words)
