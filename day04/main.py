import io
from collections import defaultdict
from io import TextIOWrapper


class Part01:
    @classmethod
    def get_nb_matching_numbers(cls, line: str):
        # Discard the CardID part
        _, line, *_ = line.split(":")
        winning_nbs_row, player_nbs_row, *_ = line.split("|")
        winning_nbs = [int(x) for x in winning_nbs_row.split()]
        player_nbs = [int(x) for x in player_nbs_row.split()]

        matches = 0
        for player_nb in player_nbs:
            matches += int(player_nb in winning_nbs)
        return matches

    @classmethod
    def parse_line(cls, line: str):
        matches = cls.get_nb_matching_numbers(line.strip())
        if matches <= 1:
            return matches
        return 2 ** (matches - 1)

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == 8
        assert cls.parse_line("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1") == 2
        assert cls.parse_line("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83") == 1
        assert cls.parse_line("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11") == 0

    @classmethod
    def parse_file(cls) -> int:
        res = 0
        with open("input.txt", "r") as f:
            for line in f:
                res += cls.parse_line(line)
        return res


class Part02(Part01):
    @classmethod
    def parse_line(cls, line: str):
        return cls.get_nb_matching_numbers(line)

    @classmethod
    def _parse_file(cls, f: TextIOWrapper):
        possessed_cards = defaultdict(int)
        for idx, line in enumerate(f):
            possessed_cards[idx] += 1
            matches = cls.parse_line(line)
            for i in range(matches):
                possessed_cards[idx + i + 1] += possessed_cards[idx]
        return sum(possessed_cards.values())

    @classmethod
    def test_parse_file(cls):
        # Provided test case
        f = io.StringIO(
            """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""
        )
        assert cls._parse_file(f) == 30

    @classmethod
    def parse_file(cls) -> int:
        with open("input.txt", "r") as f:
            return cls._parse_file(f)


if __name__ == "__main__":
    Part01.test_parse_line()
    Part02.test_parse_file()

    print(Part01.parse_file())
    print(Part02.parse_file())
