import random

from textolab.phraser import Phraser


def sample_phrase(
    filehandle: str,
    n: int = None,
    **phraser_kwargs,
) -> str:
    """
    Sample a phrase from a text corpus.

    Parameters
    ----------
    filehandle : str
        Input text file.
    n : int, optional
        Index of the phrase to return (1-based). If None, a random
        phrase is selected.
    **phraser_kwargs
        Additional keyword arguments passed to the Phraser constructor.

    Returns
    -------
    str
        Formatted string describing the sampled phrase.
    """
    
    phraser = Phraser(filehandle=filehandle, **phraser_kwargs)
    phrases = phraser.phrases

    if not phrases:
        raise ValueError("No phrases found in text.")

    total = len(phrases)

    if n is None:
        idx = random.randint(1, total)
    else:
        if n < 1 or n > total:
            raise ValueError(f"n must be between 1 and {total}")
        idx = n

    phrase = phrases[idx - 1]

    return f"Frase {idx} de {total}: '{phrase}'"
