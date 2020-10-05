import datetime as dt
import typing as tp

from src.errors import TerminateError
from src.io import clear, cprint, pluralize, mask
from src.utils import damerau_levenshtein


class Exercise:
    def __init__(
        self,
        lesson: "Lesson",
        treat_synonyms_as_alternatives: bool = False,
        allow_typos: bool = False,
        resubmission_interval: int = 5,
    ) -> None:
        self.lesson = lesson
        self.treat_synonyms_as_alternatives = treat_synonyms_as_alternatives
        self.allow_typos = allow_typos

        self.blocked_vocables = []
        self.resubmission_interval = resubmission_interval

    def run(self):
        vocable = self.lesson.next_vocable(self.blocked_vocables)

        self.blocked_vocables.append(vocable)

        if len(self.blocked_vocables) >= self.resubmission_interval:
            self.blocked_vocables.pop(0)

        try:
            self.lesson.enter_result(
                vocable,
                self.__ask_question(vocable=vocable),
            )
            self.run()

        except TerminateError:
            return

    def __ask_question(self, vocable: "Vocable") -> bool:
        clear()

        cprint(" | ".join(vocable.source) + "\n\n", "yellow")

        valid_answers = vocable.target

        while valid_answers:
            answer = input("\t")

            if answer == "x":
                raise TerminateError

            if answer == "?":
                print()
                cprint(
                    vocable.hint or mask(valid_answers[0]),
                    "magenta",
                )
                print()
                continue

            print("\n")

            valid_answers, answer_correct = self.__evaluate_answer(
                answer=answer,
                valid_answers=valid_answers,
            )

            if answer_correct:
                cprint("WELL DONE!", "green")
                if valid_answers:
                    cprint(
                        f"Name "
                        f"{pluralize(len(valid_answers), 'more synonym')}!\n", 
                        "cyan"
                    )

            else:
                cprint(
                    f"OH NO! The correct answer"
                    f"{'s ' if len(valid_answers) > 1 else ' '} would have "
                    f"been:\n",
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
