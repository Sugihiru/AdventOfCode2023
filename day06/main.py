import math
from collections import namedtuple

Race = namedtuple("Race", ["time", "distance"])


class Part01:
    @classmethod
    def parse_line(cls, line: str) -> list[int]:
        _, line, *_ = line.split(":")
        return [int(x) for x in line.split()]

    @classmethod
    def get_nb_ways_to_win(cls, race: Race) -> int:
        # Guess I'm lazy today
        # This could be solved by resolving the equation (race.time - x) * x > race.distance
        # Then we could easily get min and max value that solves the equation
        nb_wins = 0
        for speed in range(1, race.time):
            if (race.time - speed) * speed > race.distance:
                nb_wins += 1
        return nb_wins

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line("Time:      7  15   30") == [7, 15, 30]

    @classmethod
    def test_get_nb_ways_to_win(cls):
        # Provided examples
        assert cls.get_nb_ways_to_win(Race(time=7, distance=9)) == 4

    @classmethod
    def parse_file(cls) -> int:
        lines = []
        with open("input.txt", "r") as f:
            lines = f.readlines()
        times = cls.parse_line(lines[0])
        distances = cls.parse_line(lines[1])
        races = [Race(x, y) for x, y in zip(times, distances)]

        return math.prod(cls.get_nb_ways_to_win(race) for race in races)


class Part02(Part01):
    @classmethod
    def parse_line(cls, line: str) -> int:
        _, line, *_ = line.split(":")
        return int("".join(line.split()))

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line("Time:      7  15   30") == 71530

    @classmethod
    def parse_file(cls) -> int:
        lines = []
        with open("input.txt", "r") as f:
            lines = f.readlines()
        race = Race(cls.parse_line(lines[0]), cls.parse_line(lines[1]))
        return cls.get_nb_ways_to_win(race)


if __name__ == "__main__":
    Part01.test_parse_line()
    Part01.test_get_nb_ways_to_win()
    Part02.test_parse_line()

    print(Part01.parse_file())
    print(Part02.parse_file())
