from os import system, name
import sys

import pandas as pd
from termcolor import colored as clr


RELEVANT_SUCCESS_SEQUENCE_LENGTH = 5


class TerminateError(ValueError):
    pass


def clear():
    if name == "nt":  # for windows
        _ = system("cls")
    else:
        _ = system("clear")


def exercise(question: str, solution: str) -> bool:
    clear()
    solutions = [s.strip()  for s in solution.split(",")]
    answer = input(question + "\n\n")
    print("\n")
    if answer == "x":
        raise TerminateError

    if answer in solutions:
        print(clr("CORRECT!", "green"))
    else:
        print(clr(f"WRONG! Correct answer would have been: {solution}", "red"))

    input()

    return answer in solutions


def evaluate(seq):
    LEN = min(len(seq), RELEVANT_SUCCESS_SEQUENCE_LENGTH)
    return sum([int(char) for char in seq[-LEN:]]) / LEN


if __name__ == "__main__":
    try:
        FILE_PATH = sys.argv[1]
    except IndexError:
        FILE_PATH = "vocabulary.csv"

    df = pd.read_csv(FILE_PATH, sep=";", skipinitialspace=True).fillna("0")
    df["success"] = df["success"].astype(int).astype(str)

    RUN = True

    while RUN:
        df.sort_values(
            by=["success"], key=lambda s: s.map(len), inplace=True
        )
        df.sort_values(
            by=["success"], key=lambda s: s.map(evaluate), inplace=True
        )
        row = df.iloc[0]
               
        try:
            row["success"] += str(int(exercise(row[1], row[0])))
        except TerminateError:
            df.to_csv(FILE_PATH, sep=";", index=False)
            RUN = False

    clear()
    print(clr("Bye Bye!", "blue"))
