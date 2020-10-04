import os
import typing as tp

from src.lesson import Lesson
from src.exercise import Exercise
from src.io import cprint, clear, Table


class Course:
    def __init__(
        self,
        dir: str,
        user: str = "default_user",
        inverted: bool = False,
        allow_typos: bool = False,
        treat_synonyms_as_alternatives: bool = False,
    ) -> None:
        self.dir = dir
        self.user = user
        self.inverted = inverted
        self.allow_typos = allow_typos
        self.treat_synonyms_as_alternatives = treat_synonyms_as_alternatives

    @property
    def lessons(self) -> tp.List["Lesson"]:
        return sorted(
            [
                Lesson(
                    vocab_file_path=os.path.join(self.dir, path),
                    user=self.user,
                    inverted=self.inverted,
                )
                for path in os.listdir(self.dir)
                if os.path.splitext(path)[1] == ".csv"
            ],
            key=lambda l: l.vocab_file_path,
        )

    def run(self) -> None:
        while True:
            clear()
            cprint("Choose a lesson from the course (by its number):\n", "cyan")

            header = ["No.", "LESSON", "ACCOMPLISHMENT"]

            Table(
                rows=[header]
                + [
                    [index + 1, lesson.name, f"{lesson.accomplishment_rate:.0%}"]
                    for index, lesson in enumerate(self.lessons)
                ]
            ).print()

            inp = input("\n\t")
            if inp == "q":
                break

            lesson_index = int(inp) - 1
            lesson = self.lessons[lesson_index]

            Exercise(
                lesson=lesson,
                allow_typos=self.allow_typos,
                treat_synonyms_as_alternatives=self.treat_synonyms_as_alternatives,
            ).run()
