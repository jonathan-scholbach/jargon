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
        self.blocked_vocables = []
        self.resubmission_interval = resubmission_interval

    def run(self):
        vocable = self.progress.next_vocable(self.blocked_vocables)

        self.blocked_vocables.append(vocable)

        if len(self.blocked_vocables) >= self.resubmission_interval:
            self.blocked_vocables.pop(0)

        try:
            self.progress.enter_result(
                vocable,
                self.__ask_question(vocable=vocable),
            )
            self.run()

        except TerminateError:
            self.__quit()

    def __ask_question(self, vocable: "Vocable") -> bool:
        clear()

        cprint(" | ".join(vocable.source) + "\n\n", "yellow")
        
        valid_answers = vocable.target

        while valid_answers:
            answer = input()

            if answer == "x":
                raise TerminateError

            print("\n")
            
            valid_answers, answer_correct = self.__evaluate_answer(
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
                for valid_answer in valid_answers:
                    cprint("\t" + valid_answer, "blue")
                answer_correct = False
                break

        input()

        return answer_correct

    def __typo_process(self, answer: str, valid_answers: tp.List[str]) -> str:
        """Check if answer is a typo variant of a valid answer and transform
        it to valid answer if so."""
        if answer in valid_answers:
            return answer

        if self.allow_typos:
            for valid_answer in valid_answers:
                if damerau_levenshtein(answer, valid_answer, 3):
                    cprint("Beware of typos! The correct answer is:", "cyan")
                    cprint(f"\n\t{valid_answer}\n", "blue")
                    answer = valid_answer
                    break

        return answer

    def __evaluate_answer(
        self,
        answer: str,
        valid_answers: tp.List[str],
    ) -> tp.Tuple[tp.List[str], bool]:
        """Evaluate answer agains possible valid answers."""
        answer = self.__typo_process(answer, valid_answers)

        if answer in valid_answers:
            if self.treat_synonyms_as_alternatives:
                return [], True
            else:
                valid_answers.remove(answer)
                return valid_answers, True
        else:
            return valid_answers, False

    def __quit(self):
        cprint(
            f"You spent {int((dt.datetime.now() - self.start).total_seconds() / 60)} "
            " minutes in a useful manner. Bye Bye!\n",
            "cyan",
        )
