"""The application's entry point from command line."""

import datetime as dt

from src import Exercise, Progress, argument_parser


if __name__ == "__main__":
    arguments = argument_parser.parse_args()

    vocab_file_path = arguments.file_path
    treat_synonyms_as_alternatives = arguments.alternatives
    allow_typos = arguments.typos
    user = arguments.user

    start = dt.datetime.now()

    progress = Progress(vocab_file_path=vocab_file_path, user=user)
    exercise = Exercise(
        progress,
        allow_typos=allow_typos,
        treat_synonyms_as_alternatives=treat_synonyms_as_alternatives,
    )
    exercise.run()

    end = dt.datetime.now()
