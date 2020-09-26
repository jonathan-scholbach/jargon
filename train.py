import argparse
import datetime as dt
from os import system, name
import typing as tp

from termcolor import colored as clr

from utils import levenshtein
from progress import Progress


class TerminateError(ValueError):
    pass


def clear():
    if name == "nt":  # for windows
        _ = system("cls")
    else:
        _ = system("clear")


def evaluate_answer(
    answer: str,
    valid_answers: tp.List[str],
    treat_synonyms_as_alternatives: bool = False,
    allow_typos: bool = False,
) -> tp.Tuple[tp.List[str], bool]:
    """Evaluate answer agains possible valid answers."""
    if allow_typos:
        for valid_answer in valid_answers:
            delta = levenshtein(answer, valid_answer)
            if answer == valid_answer:
                break
            elif delta <= 1 or (
                len(answer) == len(valid_answer) and delta == 2
            ):
                print(
                    clr(
                        "Beware of typos! The correct answer is: \n\n\t", "cyan"
                    )
                    + clr(valid_answer + "\n", "blue")
                )
                answer = valid_answer
                break

    if answer in valid_answers:
        if treat_synonyms_as_alternatives:
            return [], True
        else:
            valid_answers.remove(answer)
            return valid_answers, True
    else:
        return valid_answers, False


def exercise(
    question: str,
    solution: str,
    treat_synonyms_as_alternatives: bool = False,
    allow_typos: bool = False,
) -> bool:
    clear()
    valid_answers = [s.strip() for s in solution.split(",")]

    print(clr(question, "yellow") + "\n\n")

    while valid_answers:
        answer = input()

        if answer == "x":
            raise TerminateError

        print("\n")

        valid_answers, answer_correct = evaluate_answer(
            answer=answer,
            valid_answers=valid_answers,
            treat_synonyms_as_alternatives=treat_synonyms_as_alternatives,
            allow_typos=allow_typos,
        )

        if answer_correct:
            print(
                clr("WELL DONE!", "green")
                + (
                    clr(" Keep on naming synonyms!\n", "cyan")
                    if valid_answers
                    else ""
                )
            )

        else:
            print(
                clr(
                    "OH NO! Correct answer"
                    f"{'s ' if len(valid_answers) > 1 else ' '}"
                    "would have been:\n",
                    "red",
                )
            )
            for s in valid_answers:
                print(clr("\t" + s, "blue"))
            answer_correct = False
            break

    input()

    return answer_correct


if __name__ == "__main__":
    start = dt.datetime.now()
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "file_path",
        type=str,
        help=(
            "Location of the vocabulary csv file, as relative file path "
            "(relative to current working directory)"
        ),
        action="store",
    )

    parser.add_argument(
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

    parser.add_argument(
        "-t",
        "--typos",
        help=("If this flag is set, typos are accepted as correct answers."),
        default=False,
        action="store_true",
    )

    parsed = parser.parse_args()

    FILE_PATH = parsed.file_path
    TREAT_SYNONYMS_AS_ALTERNATIVES = parsed.alternatives
    ALLOW_TYPOS = parsed.typos

    progress = Progress(FILE_PATH)

    RUN = True

    blocked_questions = []

    while RUN:
        entry = progress.next_entry(blocked_questions=blocked_questions)
        question, solution = entry.question, entry.solution
        blocked_questions.append(question)
        if len(blocked_questions) >= progress.RESUBMISSION:
            blocked_questions.pop(0)

        try:
            result = exercise(
                question=question,
                solution=solution,
                treat_synonyms_as_alternatives=TREAT_SYNONYMS_AS_ALTERNATIVES,
                allow_typos=ALLOW_TYPOS,
            )

            progress.enter_result(question, result)

        except TerminateError:
            RUN = False

    clear()
    end = dt.datetime.now()
    print(
        clr(
            f"You spent {int((end - start).total_seconds() / 60)} minutes in a "
            "useful manner. Bye Bye!\n",
            "cyan",
        )
    )
