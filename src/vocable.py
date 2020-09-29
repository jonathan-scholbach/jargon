import typing as tp


class Vocable:
    SYNONYM_SEP = "|"

    def __init__(
        self,
        target: str,
        source: str,
        progress: str = "0",
        inverted: bool = False,
    ) -> None:
        """
        param target: vocable in the target language, synonyms separated by '|'
        param source: vocable in the source language, synonyms separated by '|'
        progress: sequence of '0' or '1' chars indicating failure or success
            on this vocable in previous training rounds.
        param inverted: whether to invert target and source or not.
        """
        self.raw_target = target
        self.raw_source = source
        self.progress = progress or "0"
        self._inverted = inverted
        
    def __repr__(self) -> str:
        return f"{self.source}: {self.target}, {self.progress}"

    def __iter__(self):
        return iter([self.raw_target, self.raw_source, self.progress])

    def __eq__(self, other: "Vocable") -> bool:
        return (
            self.raw_target == other.raw_target 
            and self.raw_source == other.raw_source
        )

    @property
    def source(self) -> tp.List[str]:
        source = self.raw_target if self._inverted else self.raw_source

        return [synonym.strip() for synonym in source.split(self.SYNONYM_SEP)]

    @property
    def target(self) -> tp.List[str]:
        target = self.raw_source if self._inverted else self.raw_target

        return [synonym.strip() for synonym in target.split(self.SYNONYM_SEP)]

    def progress_rank(self, max_seq_length: int) -> tp.Tuple[float, int]:
        """Average performance and number of previous training rounds."""
        res =  (
            sum(
                [  # average performance
                    int(char)
                    for char in self.progress[
                        -min(max_seq_length, len(self.progress))
                    ]
                ]
            )
            / len(self.progress)
        ), len(self.progress)  # number of previous training rounds

        return res

    def invert(self):
        return Vocable(
            target=self.raw_target,
            source=self.raw_source,
            progress=self.progress,
            inverted=not self._inverted
        )
