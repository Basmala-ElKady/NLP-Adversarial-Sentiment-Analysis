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


LOCAL_SYNONYMS = {
    "good": "decent", "great": "excellent", "excellent": "great",
    "bad": "poor", "terrible": "awful", "awful": "terrible",
    "beautiful": "gorgeous", "happy": "glad", "sad": "gloomy",
    "love": "like", "hate": "dislike", "like": "appreciate",
    "fast": "quick", "slow": "sluggish", "easy": "simple",
    "simple": "easy", "hard": "difficult", "difficult": "hard",
    "nice": "pleasant", "pleasant": "nice", "fun": "enjoyable",
    "boring": "dull", "dull": "boring", "smart": "clever",
    "dumb": "foolish", "amazing": "wonderful", "wonderful": "amazing"
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
    Replace n words in the sentence with their synonyms.
    First tries local high-speed dictionary, then falls back to WordNet if NLTK is loaded.
    """
    words = sentence.split()
    if not words:
        return sentence

    # Try local synonyms first for speed and absolute reliability
    candidates = []
    for i, word in enumerate(words):
        clean_word = "".join(c for c in word if c.isalnum()).lower()
        if clean_word in LOCAL_SYNONYMS:
            candidates.append((i, clean_word))

    if candidates:
        to_replace = random.sample(candidates, min(len(candidates), n))
        new_words = words.copy()
        for idx, clean in to_replace:
            orig = words[idx]
            syn = LOCAL_SYNONYMS[clean]
            if orig.isupper():
                syn = syn.upper()
            elif orig[0].isupper():
                syn = syn.capitalize()
            # Keep punctuation
            prefix = "".join(c for c in orig if not c.isalnum() and orig.index(c) < len(orig)/2)
            suffix = "".join(c for c in orig if not c.isalnum() and orig.index(c) >= len(orig)/2)
            new_words[idx] = f"{prefix}{syn}{suffix}"
        return " ".join(new_words)

    # WordNet fallback
    try:
        import nltk
        from nltk.corpus import wordnet
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet', quiet=True)

        new_words = words.copy()
        random_word_list = list(set([w for w in words if w.isalnum()]))
        random.shuffle(random_word_list)
        num_replaced = 0
        for random_word in random_word_list:
            synonyms = []
            for syn in wordnet.synsets(random_word):
                for l in syn.lemmas():
                    synonyms.append(l.name().replace('_', ' '))
            if len(synonyms) > 1:
                synonym = random.choice(list(set(synonyms)))
                if random_word.isupper():
                    synonym = synonym.upper()
                elif random_word[0].isupper():
                    synonym = synonym.capitalize()
                new_words = [synonym if w == random_word else w for w in new_words]
                num_replaced += 1
            if num_replaced >= n:
                break
        return ' '.join(new_words)
    except Exception:
        # Graceful fallback to typo attack if everything else fails
        return typo_attack(sentence)
