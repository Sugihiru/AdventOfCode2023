import io
import itertools
import math
from typing import TypeAlias

Instructions: TypeAlias = list[int]
Nodes: TypeAlias = dict[str, tuple[str, str]]


class Part01:
    @classmethod
    def parse_line_instructions(cls, line: str) -> Instructions:
        line = line.replace("L", "0").replace("R", "1").strip()
        return [int(x) for x in line]

    @classmethod
    def parse_line_node(cls, line: str) -> tuple[str, tuple[str, str]]:
        node_key, node_paths = line.split("=")
        node_key = node_key.strip()
        node_paths = node_paths.replace("(", "").replace(")", "").split(",")
        return node_key, (node_paths[0].strip(), node_paths[1].strip())

    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> tuple[Instructions, Nodes]:
        instructions: Instructions = []
        nodes: Nodes = {}
        for idx, line in enumerate(f):
            if idx == 0:
                instructions = cls.parse_line_instructions(line)
            elif idx >= 2:
                key, paths = cls.parse_line_node(line)
                nodes[key] = paths
        return instructions, nodes

    @classmethod
    def count_steps_to_node(
        cls, instructions: Instructions, nodes: Nodes, start_key: str, end_key: str
    ) -> int:
        nb_steps = 0
        current_key = start_key
        for next_idx in itertools.cycle(instructions):
            current_key = nodes[current_key][next_idx]
            nb_steps += 1
            if current_key == end_key:
                break
        return nb_steps

    @classmethod
    def test_parse_line_instructions(cls):
        assert cls.parse_line_instructions("LLRRLLR") == [0, 0, 1, 1, 0, 0, 1]

    @classmethod
    def test_parse_file(cls):
        f = io.StringIO(
            """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
        )
        res = cls._parse_file(f)
        assert res[0] == [0, 0, 1]
        assert res[1]["AAA"] == ("BBB", "BBB")
        assert res[1]["BBB"] == ("AAA", "ZZZ")
        assert res[1]["ZZZ"] == ("ZZZ", "ZZZ")

    @classmethod
    def test_parse_line_node(cls):
        assert cls.parse_line_node("FCH = (DMS, HVX)") == ("FCH", ("DMS", "HVX"))

    @classmethod
    def test_count_steps_to_node(cls):
        # Provided examples
        assert (
            cls.count_steps_to_node(
                [1, 0],
                {
                    "AAA": ("BBB", "CCC"),
                    "BBB": ("DDD", "EEE"),
                    "CCC": ("ZZZ", "GGG"),
                    "DDD": ("DDD", "DDD"),
                    "EEE": ("EEE", "EEE"),
                    "GGG": ("GGG", "GGG"),
                    "ZZZ": ("ZZZ", "ZZZ"),
                },
                "AAA",
                "ZZZ",
            )
            == 2
        )
        assert (
            cls.count_steps_to_node(
                [0, 0, 1],
                {
                    "AAA": ("BBB", "BBB"),
                    "BBB": ("AAA", "ZZZ"),
                    "ZZZ": ("ZZZ", "ZZZ"),
                },
                "AAA",
                "ZZZ",
            )
            == 6
        )

    @classmethod
    def parse_file(cls) -> tuple[Instructions, Nodes]:
        with open("input.txt", "r") as f:
            return cls._parse_file(f)

    @classmethod
    def solve(cls) -> int:
        instructions, nodes = cls.parse_file()
        current_key = "AAA"
        return cls.count_steps_to_node(instructions, nodes, current_key, "ZZZ")


class Part02(Part01):
    @classmethod
    def solve(cls) -> int:
        instructions, nodes = cls.parse_file()
        current_keys = [key for key in nodes if key.endswith("A")]
        len_keys = len(current_keys)
        nb_steps = 0
        steps_to_end = [0] * len_keys
        for next_idx in itertools.cycle(instructions):
            current_keys = [nodes[key][next_idx] for key in current_keys]
            nb_steps += 1
            # Store the required steps if it reached the end
            for idx in range(len_keys):
                if current_keys[idx].endswith("Z") and steps_to_end[idx] == 0:
                    steps_to_end[idx] = nb_steps
            # If we got all required steps for each key
            if all(required_steps != 0 for required_steps in steps_to_end):
                break

        return math.lcm(*steps_to_end)


if __name__ == "__main__":
    Part01.test_parse_line_instructions()
    Part01.test_parse_line_node()
    Part01.test_parse_file()
    Part01.test_count_steps_to_node()

    print(Part01.solve())
    print(Part02.solve())
