"""The application's entry point from command line."""

import datetime as dt
import os
import sys

from src import Course, Exercise, Lesson
from src.io import argument_parser, clear, cprint


if __name__ == "__main__":
    start_time = dt.datetime.now()

    args = argument_parser.parse_args()

    path = args.path or input(
        "Please enter the path to the directory of the course.\t"
    )

    if not os.path.isdir(path):
        cprint(
            "\nThis is not a directory. (You must name the directory "
            "containing your lessons' csv files.)\n", 
            "red"
        )

        sys.exit()

    Course(
        dir=path,
        user=args.user,
        inverted=args.invert,
        allow_typos=args.typos,
        treat_synonyms_as_alternatives=args.alternatives,
    ).run()

    n_minutes = int((dt.datetime.now() - start_time).total_seconds() / 60)

    clear()
    cprint(
        f"You spent {n_minutes} minute{'s' if n_minutes != 1 else ''} in "
        f"a useful manner. Bye Bye!\n",
        "cyan",
    )
    