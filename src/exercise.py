import datetime as dt
import typing as tp

from src.errors import TerminateError
from src.io import clear, cprint
from src.utils import damerau_levenshtein


class Exercise:
    def __init__(
        self,
        progress: "Progress",
        treat_synonyms_as_alternatives: bool = False,
        allow_typos: bool = False,
        resubmission_interval: int = 5,
    ) -> None:
        self.progress = progress
        self.treat_synonyms_as_alternatives = treat_synonyms_as_alternatives
        self.allow_typos = allow_typos

        self.start = dt.datetime.now()
        self.blocked_questions = []
        self.resubmission_interval = resubmission_interval

    def run(self):
        entry = self.progress.next_entry(self.blocked_questions)
        question, solution = entry.question, entry.solution

        self.blocked_questions.append(question)

        if len(self.blocked_questions) >= self.resubmission_interval:
            self.blocked_questions.pop(0)

        try:
            self.progress.enter_result(
                question,
                self.ask_question(
                    question=question,
                    solution=solution,
                ),
            )
            self.run()

        except TerminateError:
            self.quit()

    def ask_question(self, question: str, solution: str) -> bool:
        clear()
        valid_answers = [s.strip() for s in solution.split(",")]

        cprint(question + "\n\n", "yellow")

        while valid_answers:
            answer = input()

            if answer == "x":
                raise TerminateError

            print("\n")

            valid_answers, answer_correct = self.evaluate_answer(
                answer=answer,
                valid_answers=valid_answers,
            )

            if answer_correct:
                cprint("WELL DONE!", "green")
                if valid_answers:
                    cprint("Keep on naming synonyms!\n", "cyan")

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

    def evaluate_answer(
        self,
        answer: str,
        valid_answers: tp.List[str],
    ) -> tp.Tuple[tp.List[str], bool]:
        """Evaluate answer agains possible valid answers."""
        if self.allow_typos:
            for valid_answer in valid_answers:
                if answer == valid_answer:
                    break

                if damerau_levenshtein(answer, valid_answer, 3):
                    cprint("Beware of typos! The correct answer is:", "cyan")
                    cprint(f"\n\t{valid_answer}\n", "blue")
                    answer = valid_answer
                    break

        if answer in valid_answers:
            if self.treat_synonyms_as_alternatives:
                return [], True
            else:
                valid_answers.remove(answer)
                return valid_answers, True
        else:
            return valid_answers, False

    def quit(self):
        self.end = dt.datetime.now()
        
        cprint(
            f"You spent {int((self.end - self.start).total_seconds() / 60)} "
            " minutes in a useful manner. Bye Bye!\n",
            "cyan",
        )
