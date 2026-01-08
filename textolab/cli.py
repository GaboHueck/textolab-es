import argparse
from pathlib import Path

from textolab.markov_babbler import MarkovBabbler
from textolab.phraser import load_corpus, tokenize_text
from textolab.sample import sample_phrase
from textolab.structure import text_to_structure
from textolab.describe import describe_text

def main():
    parser = argparse.ArgumentParser(
            prog = "textolab-es",
            description = "textolab is a modular collection of tools that makes corpus exploration easier."
            )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- subcommands ---
    # sample
    sample_parser = subparsers.add_parser(
            "sample",
            help="Take a random sample or chose one from a corpus",
            )
    sample_parser.add_argument(
            "path",
            type=Path,
            help="Path to text",
            )
    sample_parser.add_argument(
            "-n",
            "--number",
            type=int,
            default=None,
            help="Numbre of phrase to print. If omitted, a random phrase is chosen.",
            )
    sample_parser.add_argument(
        "--language",
        default=None,
        help="Language code passed to Phraser object (default: español)",
    )
            
    # babbler
    babble_parser = subparsers.add_parser(
            "babbler",
            help="Generate text using a n-order Markov chain trained from a text file.",
            )
    babble_parser.add_argument(
            "path",
            type=Path,
            help="Path to text.",
            )
    babble_parser.add_argument(
            "-n",
            "--ngram",
            type=int,
            default=2,
            help="N-gram size or order of the Markov chain for training (default: 2)",
            )
    babble_parser.add_argument(
            "-N",
            "--length",
            type=int,
            default=50,
            help="Number of tokens to be generated (default: 50)",
            )
    babble_parser.add_argument(
            "--tokenizer",
            default="nltk",
            choices=["nltk","spacy"],
            help="Tokenizador to be used.",
            )

    # structure
    structure_parser = subparsers.add_parser(
            "structure",
            help="Generate a table of the structure of sentences in the corpus.",
            )
    structure_parser.add_argument(
            "path",
            type=Path,
            help="Path to text.",
            )
    structure_parser.add_argument(
            "--language",
            type=str,
            default=None,
            help="Language the text is in.",
            )
    structure_parser.add_argument(
            "--to_csv",
            type=str,
            help="Name of the output file (comma-separated).",
            )
    structure_parser.add_argument(
            "--to_tsv",
            type=str,
            help="Name of the output file (tab-separated).",
            )

    # describe
    describe_parser = subparsers.add_parser(
            "describe",
            help="Generate a descriptive profile of the corpus.",
    )
    describe_parser.add_argument(
            "path",
            type=Path,
            help="Path to the text corpus",
    )
    describe_parser.add_argument(
            "--tokenizer",
            default="nltk",
            choices=["nltk", "spacy"],
            help="Tokenizer to be used",
            )
    describe_parser.add_argument(
            "--language",
            type=str,
            default=None,
            help="Language the text is in",
            )
    describe_parser.add_argument(
            "--top-n",
            type=int,
            default=10,
            help="Max. number of most common tokens to be shown",
            )

    # other subcommands will go here

    args = parser.parse_args()


    # --- dispatch ---
    if args.command == "sample":
        output = sample_phrase(
                str(args.path),
                n = args.number,
                language = args.language
                )
        print(output)

    elif args.command == "babbler":
        print(f"Loading text...")
        text = load_corpus(str(args.path))
        tokens = tokenize_text(
                text = text,
                tokenizer = args.tokenizer
                )
        
        print(f"Building Markov babbler order {args.ngram}...")
        babbler = MarkovBabbler(args.ngram)
        print("Training...")
        babbler.train(tokens)
        print(f"Markov babbler trained. Generating text {args.length} words long...")
        output = babbler.generate(args.length)
        
        print(output)
    
    elif args.command == "structure":
        output = text_to_structure(
                str(args.path),
                language = args.language,
                to_csv = args.to_csv,
                to_tsv = args.to_tsv,
                )
        print(output)

    elif args.command == "describe":
        stats, summary = describe_text(
        path=args.path,
        tokenizer=args.tokenizer,
        language=args.language,
        top_n=args.top_n,
        )
        print(summary)


if __name__ == "__main__":
    main()
