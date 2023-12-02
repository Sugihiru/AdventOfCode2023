from dataclasses import dataclass


@dataclass
class GameParams:
    """Parameter of a game (= number of required cubes) for part 02"""

    game_id: int
    red: int = 0
    green: int = 0
    blue: int = 0

    def set_max_required_cubes(self, nb_cubes: int, cube_color: str):
        setattr(self, cube_color, max(getattr(self, cube_color), nb_cubes))

    def get_power(self):
        return self.red * self.green * self.blue


class Part01:
    MAX_PER_COLOR = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    @classmethod
    def parse_line(cls, line: str) -> int:
        game_infos, line, *_ = line.split(":")
        game_id = int(game_infos.replace("Game ", ""))

        # We don't need to care about the individual sets
        # so we just convert them for ease
        line = line.replace(";", ",").replace(",", " ")
        cubes = line.split()

        for nb_cubes, cube_color in zip(cubes[::2], cubes[1::2]):
            if int(nb_cubes) > cls.MAX_PER_COLOR[cube_color]:
                return 0

        return game_id

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert (
            cls.parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
            == 1
        )
        assert (
            cls.parse_line(
                "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
            )
            == 2
        )
        assert (
            cls.parse_line(
                "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
            )
            == 0
        )
        assert (
            cls.parse_line(
                "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
            )
            == 0
        )
        assert (
            cls.parse_line("Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green")
            == 5
        )

    @classmethod
    def parse_file(cls) -> int:
        res = 0
        with open("input.txt", "r") as f:
            for line in f:
                res += cls.parse_line(line)
        return res


class Part02:
    @classmethod
    def parse_line(cls, line: str) -> GameParams:
        game_infos, line, *_ = line.split(":")
        game_id = int(game_infos.replace("Game ", ""))
        game_params = GameParams(game_id=game_id)

        # We don't need to care about the individual sets
        # so we just convert them for ease
        line = line.replace(";", ",").replace(",", " ")
        cubes = line.split()

        for nb_cubes, cube_color in zip(cubes[::2], cubes[1::2]):
            game_params.set_max_required_cubes(int(nb_cubes), cube_color)

        return game_params

    @classmethod
    def test_parse_line(cls):
        # Provided examples
        assert cls.parse_line(
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
        ) == GameParams(game_id=1, red=4, green=2, blue=6)
        assert cls.parse_line(
            "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue"
        ) == GameParams(game_id=2, red=1, green=3, blue=4)
        assert cls.parse_line(
            "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red"
        ) == GameParams(game_id=3, red=20, green=13, blue=6)
        assert cls.parse_line(
            "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red"
        ) == GameParams(game_id=4, red=14, green=3, blue=15)
        assert cls.parse_line(
            "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
        ) == GameParams(game_id=5, red=6, green=3, blue=2)

    @classmethod
    def parse_file(cls) -> int:
        res = 0
        with open("input.txt", "r") as f:
            for line in f:
                res += cls.parse_line(line).get_power()
        return res


if __name__ == "__main__":
    Part01.test_parse_line()
    Part02.test_parse_line()

    print(Part01.parse_file())
    print(Part02.parse_file())
