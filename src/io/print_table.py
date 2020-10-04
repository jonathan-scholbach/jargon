import math
import typing as tp

from src.io import cprint


class Table:
    MAX_WIDTH = 200
    PADDING = 10

    def __init__(self, rows: tp.List[tp.List]):
        self.raw_rows = [[str(cell) for cell in row] for row in rows]

    @property
    def __raw_columns(self) -> tp.List[tp.List[str]]:
        return [
            [str(row[col_index]) for row in self.raw_rows]
            for col_index in range(len(self.raw_rows[0]))
        ]

    @property
    def __column_count(self):
        return len(self.__raw_columns)

    @property
    def __raw_col_widths(self) -> tp.List[int]:
        return [max(len(cell) for cell in col) for col in self.__raw_columns]

    @property
    def __col_widths(self) -> tp.List[int]:
        col_widths = self.__raw_col_widths
        table_width = sum(col_widths)

        overlap = (
            table_width + self.__column_count * self.PADDING - self.MAX_WIDTH
        )

        if overlap > 0:  # Shorten each column proportionally to its length
            col_widths = [
                c_width - math.ceil(overlap * (c_width / table_width))
                for c_width in self.__raw_col_widths
            ]

        return col_widths

    @property
    def rows(self) -> tp.List[tp.List[str]]:
        return [
            [
                (cell + " " * self.MAX_WIDTH)[: self.__col_widths[col_index]]
                for col_index, cell in enumerate(row)
            ]
            for row in self.raw_rows
        ]

    def print(
        self,
        header_color: str = "white",
        body_colors: tp.List[str] = ["blue", "green"],
        separate_header: bool = True,
    ):

        for index, row in enumerate(self.rows):
            header = index == 0
            color = body_colors[index % len(body_colors)]

            cprint(
                (" " * self.PADDING).join(row),
                header_color if header else color,
            )

            if header and separate_header:
                print()
