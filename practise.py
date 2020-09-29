"""The application's entry point from command line."""

import datetime as dt

from src import Exercise, Progress, argument_parser


if __name__ == "__main__":
    args = argument_parser.parse_args()

    Exercise(
        progress=Progress(vocab_file_path=args.file_path, user=args.user),
        allow_typos=args.typos,
        treat_synonyms_as_alternatives=args.alternatives,
        invert=args.invert
    ).run()
