import io
from collections import defaultdict
from typing import Optional


class Part01:
    NON_SYMBOLS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")

    @classmethod
    def is_adjacent_to_symbol(
        cls, array: list[str], start: int, end: int, row: int
    ) -> bool:
        """Check if the string delimited by [start, end) is delimited by a symbol

        Args:
            array (list[str]): array to check
            start (int): start of the string (inclusive)
            end (int): end of the string (exclusive)
            row (int): row to check

        Returns:
            bool: whether the string is delimited by a symbol
        """
        # We could cache this and reuse it through functions
        # but it's not costly enough for the input of AOC
        # so I'd rather simplify the code
        row_length = len(array[row])

        chars_to_check = []
        # Take the upper row
        if row > 0:
            chars_to_check += array[row - 1][
                max(0, start - 1) : min(row_length, end + 1)
            ]
        # Take the left char
        if start != 0:
            chars_to_check.append(array[row][start - 1])
        # Take the right char
        if end < row_length:
            chars_to_check.append(array[row][end])
        # Take the lower row
        if row + 1 != len(array):
            chars_to_check += array[row + 1][
                max(0, start - 1) : min(row_length, end + 1)
            ]

        return any(x not in cls.NON_SYMBOLS for x in chars_to_check)

    @classmethod
    def parse_array(cls, array: list[str], row: int) -> int:
        """Parse the array to find every number in row surrounded by a symbol

        Args:
            array (list[str]): array to check
            row (int): row to check

        Returns:
            int: sum of numbers surrounded by a symbol
        """
        res = 0
        i = 0

        while i < len(array[row]):
            if array[row][i].isdigit():
                start_idx_of_nb = i
                while i < len(array[row]) and array[row][i].isdigit():
                    i += 1
                end_idx_of_nb = i
                if cls.is_adjacent_to_symbol(
                    array, start_idx_of_nb, end_idx_of_nb, row
                ):
                    res += int(array[row][start_idx_of_nb:end_idx_of_nb])
            else:
                i += 1

        return res

    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> int:
        res = 0
        rows = []

        for idx, line in enumerate(f):
            rows.append(line.strip())
            if idx == 1:
                res += cls.parse_array(rows, 0)
            elif len(rows) == 3:
                res += cls.parse_array(rows, 1)
                rows.pop(0)
        res += cls.parse_array(rows, -1)
        return res

    @classmethod
    def test_is_adjacent_to_symbol(cls):
        assert cls.is_adjacent_to_symbol(
            [
                "...*...",
                "179....",
                ".......",
            ],
            start=0,
            end=3,
            row=1,
        )
        assert cls.is_adjacent_to_symbol(
            [
                "....179",
                "...*...",
                ".......",
            ],
            start=4,
            end=7,
            row=0,
        )
        assert cls.is_adjacent_to_symbol(
            [
                ".......",
                ".*....",
                "..179..",
            ],
            start=2,
            end=5,
            row=2,
        )
        assert not cls.is_adjacent_to_symbol(
            [
                "**...**",
                "**.9.**",
                "**...**",
            ],
            start=3,
            end=4,
            row=1,
        )

    @classmethod
    def test_parse_array(cls):
        assert (
            cls.parse_array(
                [
                    ".........",
                    "......998",
                    ".........",
                ],
                1,
            )
            == 0
        )
        assert (
            cls.parse_array(
                [
                    ".......",
                    "......*",
                    "....17.",
                ],
                2,
            )
            == 17
        )
        assert (
            cls.parse_array(
                [
                    "17.....",
                    "...*...",
                    ".....",
                ],
                0,
            )
            == 0
        )
        assert (
            cls.parse_array(
                [
                    "17.....",
                    "..*....",
                    ".......",
                ],
                0,
            )
            == 17
        )
        assert (
            cls.parse_array(
                [
                    ".......",
                    ".......",
                    "17*3...",
                ],
                2,
            )
            == 20
        )
        assert (
            cls.parse_array(
                [
                    "798...145..629..",
                    "...*.....-......",
                    "59..489.817&880.",
                ],
                2,
            )
            == 489 + 817 + 880
        )
        # Some cases from the provided example
        assert (
            cls.parse_array(
                [
                    "467..114..",
                    "...*......",
                    "..35..633.",
                ],
                0,
            )
            == 467
        )
        assert (
            cls.parse_array(
                [
                    "467..114..",
                    "...*......",
                    "..35..633.",
                ],
                1,
            )
            == 0
        )
        assert (
            cls.parse_array(
                [
                    "...*......",
                    "..35..633.",
                    "..*...#...",
                ],
                1,
            )
            == 35 + 633
        )

    @classmethod
    def test_parse_file(
        cls,
    ):
        # Provided test case
        f = io.StringIO(
            """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
        )
        assert cls._parse_file(f) == 4361

        # Custom testcases
        f = io.StringIO(
            """..........
.......998
.........."""
        )
        assert cls._parse_file(f) == 0

        f = io.StringIO(
            """..8...145..629..
...*.....-..&...
59..489.817.880."""
        )
        assert cls._parse_file(f) == 8 + 145 + 629 + 489 + 817 + 880

        f = io.StringIO(
            """7.8*..145..629.
***************
.....89.817.880"""
        )
        assert cls._parse_file(f) == 7 + 8 + 145 + 629 + 89 + 817 + 880

    @classmethod
    def parse_file(cls) -> int:
        with open("input.txt", "r") as f:
            return cls._parse_file(f)


class Part02:
    @classmethod
    def get_adjacent_gear_pos(
        cls, array: list[str], start: int, end: int, row: int
    ) -> Optional[tuple[int, int]]:
        """Check if the string delimited by [start, end) has a gear around it, and returns its position

        Args:
            array (list[str]): array to check
            start (int): start of the string (inclusive)
            end (int): end of the string (exclusive)
            row (int): row to check

        Returns:
            Optional[tuple[int]]: position of the gear around the string, or None if there's no gear nearby
        """
        # We could cache this and reuse it through functions
        # but it's not costly enough for the input of AOC
        # so I'd rather simplify the code
        row_length = len(array[row])

        # Check the upper row
        if (
            row > 0
            and (
                gear_y_pos := array[row - 1].find(
                    "*", max(0, start - 1), min(row_length, end + 1)
                )
            )
            != -1
        ):
            return (row - 1, gear_y_pos)
        # Check the left char
        if start != 0 and array[row][start - 1] == "*":
            return (row, start - 1)
        # Check the right char
        if end < row_length and array[row][end] == "*":
            return (row, end)
        # Check the lower row
        if (
            row + 1 != len(array)
            and (
                gear_y_pos := array[row + 1].find(
                    "*", max(0, start - 1), min(row_length, end + 1)
                )
            )
            != -1
        ):
            return (row + 1, gear_y_pos)

    @classmethod
    def parse_array(cls, array: list[str], row: int) -> dict:
        """Parse the array to find every number in row surrounded by a symbol

        Args:
            array (list[str]): array to check
            row (int): row to check

        Returns:
            int: sum of numbers surrounded by a symbol
        """
        i = 0

        gear_to_numbers = defaultdict(list)

        while i < len(array[row]):
            if array[row][i].isdigit():
                start_idx_of_nb = i
                while i < len(array[row]) and array[row][i].isdigit():
                    i += 1
                end_idx_of_nb = i
                if gear_pos := cls.get_adjacent_gear_pos(
                    array, start_idx_of_nb, end_idx_of_nb, row
                ):
                    gear_to_numbers[gear_pos].append(
                        int(array[row][start_idx_of_nb:end_idx_of_nb])
                    )
            else:
                i += 1

        return gear_to_numbers

    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> int:
        res = 0
        rows = []
        gear_to_numbers = defaultdict(list)

        idx = 0

        for idx, line in enumerate(f):
            rows.append(line.strip())
            if idx == 1:
                for gear_pos, numbers in cls.parse_array(rows, 0).items():
                    gear_to_numbers[gear_pos] += numbers
            elif len(rows) == 3:
                for gear_pos, numbers in cls.parse_array(rows, 1).items():
                    gear_to_numbers[(gear_pos[0] + idx - 2, gear_pos[1])] += numbers
                rows.pop(0)

        for gear_pos, numbers in cls.parse_array(rows, -1).items():
            gear_to_numbers[(gear_pos[0] + idx - 1, gear_pos[1])] += numbers

        # Compute product of all relevant gears
        res = 0
        for numbers in gear_to_numbers.values():
            if len(numbers) == 2:
                res += numbers[0] * numbers[1]
        return res

    @classmethod
    def test_get_adjacent_gear_pos(cls):
        assert cls.get_adjacent_gear_pos(
            [
                "...*...",
                "179....",
                ".......",
            ],
            start=0,
            end=3,
            row=1,
        ) == (0, 3)

    @classmethod
    def test_parse_file(
        cls,
    ):
        # Provided test case
        f = io.StringIO(
            """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""
        )
        assert cls._parse_file(f) == 467 * 35 + 755 * 598

    @classmethod
    def parse_file(cls) -> int:
        with open("input.txt", "r") as f:
            return cls._parse_file(f)


if __name__ == "__main__":
    Part01.test_is_adjacent_to_symbol()
    Part01.test_parse_array()
    Part01.test_parse_file()
    Part02.test_get_adjacent_gear_pos()
    Part02.test_parse_file()

    print(Part01.parse_file())
    print(Part02.parse_file())
