import datetime as dt
import typing as tp

from src.io import parser, cprint, clear
from src.progress import Progress
from src.utils import levenshtein
from src.errors import TerminateError


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
                cprint("Beware of typos! The correct answer is:", "cyan")
                cprint(f"\n\t{valid_answer}\n", "blue")
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

    cprint(question + "\n\n", "yellow")

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
            cprint("WELL DONE!", "green")
            if valid_answers:
                cprint(" Keep on naming synonyms!\n", "cyan")

        else:
            cprint(                
                "OH NO! Correct answer"
                f"{'s ' if len(valid_answers) > 1 else ' '} would have been:\n",
                "red",
            )
            for s in valid_answers:
                cprint("\t" + s, "blue")
            answer_correct = False
            break

    input()

    return answer_correct


if __name__ == "__main__":
    start = dt.datetime.now()
    parsed = parser.parse_args()

    vocab_file_path = parsed.file_path
    treat_synonyms_as_alternatives = parsed.alternatives
    allow_typos = parsed.typos
    user = parsed.user

    progress = Progress(vocab_file_path=vocab_file_path, user=user)

    RUN = True

    blocked_questions = []

    while RUN:
        entry = progress.next_entry(blocked_questions=blocked_questions)
        question, solution = entry.question, entry.solution
        blocked_questions.append(question)
        if len(blocked_questions) >= progress.RESUBMISSION:
            blocked_questions.pop(0)

        try:
            progress.enter_result(
                question,
                exercise(
                    question=question,
                    solution=solution,
                    treat_synonyms_as_alternatives=treat_synonyms_as_alternatives,
                    allow_typos=allow_typos,
                ),
            )

        except TerminateError:
            RUN = False

    clear()
    end = dt.datetime.now()
    cprint(    
        f"You spent {int((end - start).total_seconds() / 60)} minutes in a "
        "useful manner. Bye Bye!\n",
        "cyan"
    )
