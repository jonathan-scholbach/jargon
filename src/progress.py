from collections import namedtuple
from os.path import basename, exists, getmtime, join as pathjoin, splitext
from os import makedirs

import typing as tp


ProgressEntry = namedtuple(
    "ProgressEntry", "solution question progress", defaults=["", "", "0"]
)


class Progress:
    DIR = ".progress"
    SEP = ";"
    SEQ_LENGTH = 3  # relevant progress sequence length

    def __init__(self, vocab_file_path: str, user: str = "default_user"):
        self.vocab_file_path = vocab_file_path
        self.user = user
        self.__load()

    def __getitem__(
        self, key: tp.Union[int, slice, str]
    ) -> tp.Optional["ProgressEntry"]:
        self.__sort()

        return self.data[key]

    @property
    def __vocab_file_name(self):
        return basename(splitext(self.vocab_file_path)[0])

    @property
    def __dir(self):
        return pathjoin(*[Progress.DIR, self.user, self.__vocab_file_name])

    @property
    def __path(self):
        """Path where to take progress data from and where to store to.

        This depends on the vocabulary file, its last modification date and the
        user.
        """
        return pathjoin(
            *[self.__dir, str(getmtime(self.vocab_file_path)) + ".csv"]
        )

    def __load(self):
        if exists(self.__path):
            path = self.__path
        else:
            path = self.vocab_file_path

        with open(path, "r") as file:
            self.data = [
                ProgressEntry(*[cell.strip() for cell in line.split(";")])
                for line in file
            ]

    def __sort(self):
        """Push entries with weak performance to the top.

        If performance of two entries equals over recent exercises, prioritize
        the entry with lesser practice.
        """
        self.data.sort(
            key=lambda entry: (
                sum(
                    [  # average performance on recent practices
                        int(char)
                        for char in entry.progress[
                            -min(self.SEQ_LENGTH, len(entry.progress))
                        ]
                    ]
                )
                / len(entry.progress),
                len(entry.progress),
            ),
        )

    def __store(self) -> None:
        if not exists(self.__path):
            makedirs(self.__dir, exist_ok=True)
        with open(self.__path, "w+") as file:
            for entry in self.data:
                file.write("; ".join([*entry]) + "\n")

    def __find(self, question: str) -> tp.Optional[int]:
        for index, entry in enumerate(self.data):
            if entry.question == question:
                return index

    def enter_result(self, question: str, result: bool):
        index = self.__find(question)
        entry = self.data[index]
        self.data[index] = ProgressEntry(
            question=entry.question,
            solution=entry.solution,
            progress=entry.progress + str(int(result)),
        )
        self.__store()

    def next_entry(self, blocked_questions=tp.List[str]) -> "ProgressEntry":
        candidates = self[: len(blocked_questions) + 1]
        for candidate in candidates:
            if candidate.question not in blocked_questions:
                return candidate
