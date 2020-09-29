"""The application's entry point from command line."""

from src import Exercise, Progress, argument_parser


if __name__ == "__main__":
    args = argument_parser.parse_args()

    Exercise(
        progress=Progress(
            vocab_file_path=args.file_path, user=args.user, inverted=args.invert
        ),
        allow_typos=args.typos,
        treat_synonyms_as_alternatives=args.alternatives,
    ).run()
