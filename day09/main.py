import io


class Part01:
    @classmethod
    def parse_line(cls, line: str) -> list[int]:
        return [int(x) for x in line.strip().split()]

    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> list[list[int]]:
        res: list[list[int]] = []
        for line in f:
            res.append(cls.parse_line(line))
        return res

    @classmethod
    def compute_all_sequences(cls, seq: list[int]) -> list[list[int]]:
        all_sequences = []
        current_sequence = seq
        all_sequences.append(current_sequence)
        while not all(x == 0 for x in current_sequence):
            next_seq = []
            for nb, next_nb in zip(current_sequence, current_sequence[1:]):
                next_seq.append(next_nb - nb)
            current_sequence = next_seq
            all_sequences.append(current_sequence)
        return all_sequences

    @classmethod
    def extrapolate_sequence_value(cls, all_seq: list[list[int]]) -> int:
        extrapolated_nb = 0
        for seq in reversed(all_seq):
            extrapolated_nb = extrapolated_nb + seq[-1]
        return extrapolated_nb

    @classmethod
    def test_compute_all_sequences(cls):
        assert cls.compute_all_sequences([0, 3, 6, 9, 12, 15]) == [
            [0, 3, 6, 9, 12, 15],
            [3, 3, 3, 3, 3],
            [0, 0, 0, 0],
        ]

    @classmethod
    def test_extrapolate_sequence_value(cls):
        assert (
            cls.extrapolate_sequence_value(
                [
                    [0, 3, 6, 9, 12, 15],
                    [3, 3, 3, 3, 3],
                    [0, 0, 0, 0],
                ]
            )
            == 18
        )

    @classmethod
    def test_parse_line(cls):
        assert cls.parse_line("-7 -12 -7 25 100 241 508 1055") == [
            -7,
            -12,
            -7,
            25,
            100,
            241,
            508,
            1055,
        ]

    @classmethod
    def parse_file(cls) -> list[list[int]]:
        with open("input.txt", "r") as f:
            return cls._parse_file(f)

    @classmethod
    def solve(cls) -> int:
        res = 0
        sequences = cls.parse_file()
        for seq in sequences:
            all_seq = cls.compute_all_sequences(seq)
            res += cls.extrapolate_sequence_value(all_seq)
        return res


class Part02(Part01):
    @classmethod
    def extrapolate_sequence_value(cls, all_seq: list[list[int]]) -> int:
        extrapolated_nb = 0
        for seq in reversed(all_seq):
            extrapolated_nb = seq[0] - extrapolated_nb
        return extrapolated_nb

    @classmethod
    def test_extrapolate_sequence_value(cls):
        assert (
            cls.extrapolate_sequence_value(
                [
                    [0, 3, 6, 9, 12, 15],
                    [3, 3, 3, 3, 3],
                    [0, 0, 0, 0],
                ]
            )
            == -3
        )


if __name__ == "__main__":
    Part01.test_parse_line()
    Part01.test_compute_all_sequences()
    Part01.test_extrapolate_sequence_value()
    Part02.test_extrapolate_sequence_value()

    print(Part01.solve())
    print(Part02.solve())
