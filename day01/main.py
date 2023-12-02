class Part01:
    @classmethod
    def parse_line(cls, line: str) -> int:
        first_digit = next(x for x in line if x.isdigit())
        last_digit = next(x for x in line[::-1] if x.isdigit())

        return int(f"{first_digit}{last_digit}")

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line("1abc2") == 12
        assert cls.parse_line("pqr3stu8vwx") == 38
        assert cls.parse_line("a1b2c3d4e5f") == 15
        assert cls.parse_line("treb7uchet") == 77

    @classmethod
    def parse_file(cls) -> int:
        res = 0
        with open("input.txt", "r") as f:
            for line in f:
                res += cls.parse_line(line)
        return res


class Part02:
    SPELLED_NBS = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    @classmethod
    def parse_line(cls, line: str) -> int:
        first_digit: str = ""
        last_digit: str = ""
        for idx, c in enumerate(line):
            nb = None
            if c.isdigit():
                nb = c
            else:
                # From the current pos, check if we have a spelled number
                for spelled_nb_value, spelled_nb in enumerate(cls.SPELLED_NBS):
                    if line.startswith(spelled_nb, idx):
                        nb = str(spelled_nb_value + 1)

            if nb and not first_digit:
                first_digit = nb
            elif nb:
                last_digit = nb

        return int(f"{first_digit}{last_digit or first_digit}")

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line("two1nine") == 29
        assert cls.parse_line("eightwothree") == 83
        assert cls.parse_line("abcone2threexyz") == 13
        assert cls.parse_line("xtwone3four") == 24
        assert cls.parse_line("4nineeightseven2") == 42
        assert cls.parse_line("zoneight234") == 14
        assert cls.parse_line("7pqrstsixteen") == 76
        # My test cases
        assert cls.parse_line("twoone") == 21
        assert cls.parse_line("smdqspmlv3twokthree") == 33
        assert cls.parse_line("six1jgpvqtwo378") == 68

    @classmethod
    def parse_file(cls) -> int:
        res = 0
        with open("input.txt", "r") as f:
            for line in f:
                res += cls.parse_line(line)
        return res


if __name__ == "__main__":
    Part01.test_parse_line()
    Part02.test_parse_line()

    print(Part01.parse_file())
    print(Part02.parse_file())
