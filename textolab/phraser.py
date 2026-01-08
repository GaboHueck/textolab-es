from pathlib import Path
from typing import List
import nltk
import spacy
import os

class Phraser:
    """
    Represents a text corpus segmented into phrases.
    A 'phrase' is defined by the segmentation function below (uses standard nltk sentence tokenizer).

    Expects a txt file of any size.
    """

    def __init__(
        self,
        filehandle: str,
        normalize: bool = True,
        language=None,
    ):
        if language is None:
            language = 'es'

        self.raw_text = self._load_text(filehandle)
        self.raw_text = self._normalize(normalize)

        possible_languages = {'es':'spanish', 'en':'english', 'pt':'portuguese'}
        self.language = possible_languages[language]

        self.phrases: List[str] = self._segment()

    def _load_text(self, filehandle) -> str:
        with open(filehandle,'r', encoding='utf-8') as f:
            text = f.read()
        return text

    def _normalize(self, normalize) -> str:
        if normalize:
            return self.raw_text.replace('\n',' ')
        return self.raw_text

    def _segment(self) -> List[str]:
        return nltk.sent_tokenize(self.raw_text, self.language)

def load_corpus(
    filehandle: str,
    encoding: str = "utf-8"
) -> str:
    """
    Loads text from file.

    Parameters:
        path (str): Path to the text file
        encoding (str): File encoding (default: utf-8)

    Returns:
        str: Raw text loaded from file
    """

    if not os.path.exists(filehandle):
        raise FileNotFoundError(f"File not found: {filehandle}")

    with open(filehandle, encoding=encoding) as f:
        text = f.read()

    return text

def tokenize_text(
    text: str,
    tokenizer: str = "nltk",
    language: str = "spanish",
    include_linebreaks: bool = False,
) -> List[str]:
    """
    Tokenize raw text using NLTK or spaCy.

    Parameters
    ----------
        text : str
        tokenizer : str
        language : str
            For spaCy has to be: "es", "pt", or "en"
            For NLTK has to be: "spanish", "portuguese", or "english"
        include_linebreaks : bool
            (Only works with spaCy)
            Tells function whether to keep linebreaks as tokens

    Returns
    -------
        List[str] of tokens.
    """
    if not include_linebreaks:
        text = text.replace("\n", " ") # Attention: NLTK removes these either way

    if tokenizer == "nltk":
        return nltk.word_tokenize(text, language=language)

    elif tokenizer == "spacy":
        nlp = spacy.load(f"{language}_core_news_lg")
        return [token.text for token in nlp(text)]

    else:
        raise ValueError("tokenizer must be 'nltk' or 'spacy'")

