import random
import nltk
from nltk.corpus import wordnet


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


def synonym_replacement(sentence, n=1):
    """
    Replace n words in the sentence with their synonyms from WordNet.
    """
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

    words = sentence.split()
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word.isalnum()]))
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = []
        for syn in wordnet.synsets(random_word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        if len(synonyms) > 1:
            synonym = random.choice(list(set(synonyms)))
            new_words = [synonym if word == random_word else word for word in new_words]
            num_replaced += 1
        if num_replaced >= n:
            break

    return ' '.join(new_words)
