import copy
import datetime as dt
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
    remaining_solutions = copy.deepcopy(solutions)
    print(clr(question, "yellow") + "\n\n")
    
    answer_correct = True

    while remaining_solutions:
        answer = input()

        if answer == "x":
            raise TerminateError

        print("\n")

        if answer in solutions:
            remaining_solutions.remove(answer)
            print(
                clr("CORRECT!", "green") +
                (clr("\tKeep on naming synonyms!\n", "blue") if remaining_solutions else "")
            )
            
        else:
            print(clr("WRONG! Correct answer would have been: ", "red"))
            for s in remaining_solutions:
                print(clr(s, "blue"))
            answer_correct = False
            break

    input()

    return answer_correct


def evaluate(seq):
    LEN = min(len(seq), RELEVANT_SUCCESS_SEQUENCE_LENGTH)
    return sum([int(char) for char in seq[-LEN:]]) / LEN


if __name__ == "__main__":
    start = dt.datetime.now()
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
            RUN = False

        df.to_csv(FILE_PATH, sep=";", index=False)

    clear()
    end = dt.datetime.now()
    print(
        clr(
            f"You spent {int((end - start).total_seconds() / 60)} minutes in a "
            "useful manner. Bye Bye!", 
            "blue")
    )
