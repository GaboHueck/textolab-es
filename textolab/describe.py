from collections import Counter
from pathlib import Path
from typing import Dict, Tuple

from nltk.corpus import stopwords

import pandas as pd

from textolab.phraser import load_corpus, tokenize_text
from textolab.structure import text_to_structure


def describe_text(
    path: str,
    tokenizer: str = "nltk",
    language: str = "spanish",
    include_linebreaks: bool = False,
    top_n: int = 10,
) -> Tuple[Dict, str]:
    """
    Generate a descriptive profile of a text corpus.

    Parameters
    ----------
    path : str
        Path to the text corpus.
    tokenizer : str, optional
        Tokenizer backend to use ("nltk" or "spacy").
    language : str = "spanish"
        Language from which to remove stopwords
    include_linebreaks : bool, optional
        Whether to preserve line breaks during tokenization.
    top_n : int, optional
        Number of most frequent words to include.

    Returns
    -------
    dict
        Dictionary containing corpus statistics.
    str
        Human-readable summary of the corpus profile.
    """
    # --- Load raw text ---
    text = load_corpus(path)

    # --- Token-level statistics ---
    tokens = tokenize_text(
        text=text,
        tokenizer=tokenizer,
        include_linebreaks=include_linebreaks,
    )

    total_tokens = len(tokens)
    token_counts = Counter(tokens)
    unique_tokens = len(token_counts)
    ttr = unique_tokens / total_tokens if total_tokens else 0.0

    # crude stopword / particle filter
    stop_words = set(stopwords.words(language))
    common_particles = stop_words | {
        ".", ",", ";", ":", "!", "?", "(", ")", "[", "]",
        }

    most_common = [
        (tok, cnt)
        for tok, cnt in token_counts.most_common(top_n * 2)
        if tok.lower() not in common_particles
    ][:top_n]

    # --- Structural statistics ---
    structure_df = text_to_structure(path)

    num_phrases = len(structure_df)
    avg_len = structure_df["len"].mean()
    min_len = structure_df["len"].min()
    max_len = structure_df["len"].max()

    # --- POS proportions ---
    pos_series = structure_df["pos"].dropna().astype(str)
    pos_counts = Counter("".join(pos_series))
    total_pos = sum(pos_counts.values())

    pos_proportions = {
        pos: count / total_pos
        for pos, count in pos_counts.items()
    }

    # --- Assemble results ---
    stats = {
        "total_tokens": total_tokens,
        "unique_tokens": unique_tokens,
        "type_token_ratio": round(ttr, 4),
        "most_common_tokens": most_common,
        "num_phrases": num_phrases,
        "avg_phrase_length": round(avg_len, 2),
        "min_phrase_length": int(min_len),
        "max_phrase_length": int(max_len),
        "pos_proportions": pos_proportions,
    }

    summary = (
        f"Corpus description\n"
        f"------------------\n"
        f"Total tokens: {total_tokens}\n"
        f"Unique tokens: {unique_tokens}\n"
        f"Type–token ratio: {stats['type_token_ratio']}\n"
        f"Number of phrases: {num_phrases}\n"
        f"Average phrase length: {stats['avg_phrase_length']}\n"
        f"Min / Max phrase length: {min_len} / {max_len}\n"
        f"Most common tokens (filtered): {most_common}\n"
        f"POS proportions: {pos_proportions}\n"
    )

    return stats, summary

