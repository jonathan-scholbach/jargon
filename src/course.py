import os
import typing as tp

from src.lesson import Lesson
from src.exercise import Exercise
from src.io import cprint, clear, Table, date_diff, title_from_path


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
    def name(self):
        return title_from_path(self.dir)

    @property
    def description(self):
        try:
            path = next(
                filter(
                    lambda f: os.path.splitext(f)[1] == ".txt",
                    os.listdir(self.dir),
                )
            )
            with open(os.path.join(self.dir, path)) as file:
                return file.read()

        except StopIteration:
            return ""

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
            cprint(f"COURSE: {self.name}", "white")
            cprint(self.description, "green")
            print()
            cprint(
                "Choose a lesson from the course (by its number). "
                "You can also combine multiple lessons, by separating the "
                "lesson numbers by comma:\n",
                "cyan",
            )

            header = ["No.", "LESSON", "ACCOMPLISHMENT", "LAST EXERCISE"]

            Table(
                rows=[header]
                + [
                    [
                        index + 1,
                        lesson.name,
                        f"{lesson.accomplishment_rate:.0%}",
                        date_diff(lesson.last_exercise_date),
                    ]
                    for index, lesson in enumerate(self.lessons)
                ]
            ).print()

            inp = input("\n\t")
            if inp == "q":
                break

            lesson_indices = map(lambda s: int(s.strip()) - 1, inp.split(","))
            lessons = map(lambda index: self.lessons[index], lesson_indices)

            Exercise(
                lessons=lessons,
                allow_typos=self.allow_typos,
                treat_synonyms_as_alternatives=self.treat_synonyms_as_alternatives,
            ).run()
