import argparse


argument_parser = argparse.ArgumentParser()

argument_parser.add_argument(
    "file_path",
    type=str,
    help=(
        "Location of the vocabulary csv file, as file path relative to current "
        "working directory)."
    ),
    action="store",
)

argument_parser.add_argument(
    "-a",
    "--alternatives",
    help=(
        "If this flag is set, synonyms are treated as alternatives. That "
        "means, you need to name only one synonym for your answer to be "
        "considered correct."
    ),
    default=False,
    action="store_true",
)

argument_parser.add_argument(
    "-t",
    "--typos",
    help=("If this flag is set, typos are accepted as correct answers."),
    default=False,
    action="store_true",
)

argument_parser.add_argument(
    "-u",
    "--user",
    help=(
        "Name a user. This will keep track of each user's progress "
        "separately."
    ),
    default="default_user",
    action="store",
)
