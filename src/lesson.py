from collections import namedtuple
from os.path import basename, exists, getmtime, join as pathjoin, splitext
from os import makedirs
import sys
import typing as tp

from src.vocable import Vocable
from src.io import cprint


class Lesson:
    DIR = ".progress"
    SEP = ";"
    SEQ_LENGTH = 3  # relevant progress sequence length

    def __init__(
        self,
        vocab_file_path: str,
        user: str = "default_user",
        inverted: bool = False,
    ):
        self.vocab_file_path = vocab_file_path
        self.user = user
        self._inverted = inverted
        self.__load()

    def __getitem__(self, key: tp.Union[int, slice]) -> tp.Optional["Vocable"]:
        self.__sort()

        return self.data[key]

    @property
    def name(self):
        return self.__vocab_file_name.split("__")[-1]

    @property
    def __vocab_file_name(self):
        return basename(splitext(self.vocab_file_path)[0])

    @property
    def __dir(self):
        return pathjoin(*[Lesson.DIR, self.user, self.__vocab_file_name])

    @property
    def __path(self):
        """Path where to take lesson data from and where to store to.

        This depends on the vocable file, its last modification date and the
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
            self.data = []

            for index, line in enumerate(file):
                try:
                    self.data.append(
                        Vocable(
                            *[cell.strip() for cell in line.split(self.SEP)]
                        )
                    )
                except:
                    cprint(
                        f"Lesson file '{self.vocab_file_path}' malformatted at "
                        f"line {index + 1}.",
                        "red",
                    )
                    sys.exit(0)

    def __sort(self):
        """Push entries with weak performance to the top.

        If performance of two entries equals over recent exercises, prioritize
        the vocable with lesser practice.
        """
        self.data.sort(
            key=lambda vocable: vocable.progress_rank(
                self.SEQ_LENGTH, default=(self.SEQ_LENGTH - 1) / self.SEQ_LENGTH
            )
        )

    def __store(self) -> None:
        if not exists(self.__path):
            makedirs(self.__dir, exist_ok=True)
        with open(self.__path, "w+") as file:
            for vocable in self.data:
                file.write(
                    self.SEP.join(
                        [
                            vocable.raw_target,
                            vocable.raw_source,
                            vocable.hint,
                            vocable.progress,
                        ]
                    )
                    + "\n"
                )

    def __find(self, vocable: str) -> tp.Optional[int]:
        return self.data.index(vocable)

    def enter_result(self, vocable: "Vocable", result: bool):
        index = self.__find(vocable)
        vocable = self.data[index]
        self.data[index] = Vocable(
            source=vocable.raw_source,
            target=vocable.raw_target,
            progress=vocable.progress + str(int(result)),
        )
        self.__store()

    def next_vocable(self, blocked_vocables=tp.List["Vocable"]) -> "Vocable":
        self.__sort()

        vocable = next(
            vocab
            for vocab in self[: max(len(blocked_vocables) + 1, len(self.data))]
            if vocab not in blocked_vocables
        )
        vocable = vocable.invert() if self._inverted else vocable

        return vocable
