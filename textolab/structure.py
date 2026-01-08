from typing import List
import pandas as pd
import spacy

from textolab.phraser import Phraser

# Mapping spaCy POS tags to single-letter symbols
POS_MAP = {
    "DET": "A",     # artículo
    "NOUN": "N",    # sustantivo
    "ADJ": "J",     # adjetivo
    "VERB": "V",    # verbo
    "ADV": "D",     # adverbio
    "PRON": "R",    # pronombre
    "ADP": "P",     # preposición
    "CCONJ": "C",   # conjunción coordinada
    "SCONJ": "C",   # conjunción subordinada
    "NUM": "M",     # número
    "PART": "T",    # partícula
    "INTJ": "I",    # interjección
    "PUNCT": "P",   # puntuación (no es utilizado)
    "SYM": "Y",     # símbolo
    "X": "X",
}


def build_structure_table(phraser, language=None) -> pd.DataFrame:
    """
    Construye una representación estructural desde un objeto Phraser.

    Parámetros
    ----------
    phraser : Phraser
        Una instancia del objeto Phraser que contiene las frases del texto.
    language : str
        Código de lenguaje de los modelos de spaCy (e.g. 'es').

    Retorna
    -------
    pandas.DataFrame
        Tabla con las columnas:
        ['full', 'len', 'wordlen', 'minimal', 'pos']
    """
    if language is None:
        language = "es"

    nlp = spacy.load(f"{language}_core_news_lg")

    rows = []

    for phrase in phraser.phrases:
        doc = nlp(phrase)

        wordlen_repr: List[str] = []
        minimal_repr: List[str] = []
        pos_repr: List[str] = []
        sent_size = 0
        
        for token in doc:
            if token.is_punct: # Solamente si es un puntuador entonces se transcribe directamente.
                wordlen_repr.append(token.text)
                minimal_repr.append(token.text)
                pos_repr.append(token.text)
            else:
                sent_size += 1
                wordlen_repr.append(str(len(token.text)))
                minimal_repr.append("w")
                pos_repr.append(POS_MAP.get(token.pos_, "X"))

        rows.append(
            {
                "full": phrase,
                "len": sent_size,
                "wordlen": " ".join(wordlen_repr),
                "minimal": "".join(minimal_repr),
                "pos": "".join(pos_repr),
            }
        )

    return pd.DataFrame(rows)

def text_to_structure(
    filehandle: str,
    language: str = "es",
    to_csv: str = "",
    to_tsv: str = "",
    **phraser_kwargs,
) -> pd.DataFrame:
    """
    Wrapper conveniente para construir la tabla directamente.
    """
    phraser = Phraser(filehandle, **phraser_kwargs)
    structure_table = build_structure_table(phraser, language=language)
    
    if to_csv:
        structure_table.to_csv(to_csv, sep=',')
    if to_tsv:
        structure_table.to_csv(to_tsv, sep='\t')
        
    return structure_table
