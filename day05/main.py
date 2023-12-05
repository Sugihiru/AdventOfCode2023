import io
from dataclasses import dataclass


@dataclass
class SeedRange:
    start: int
    steps: int

    @property
    def end(self) -> int:
        """End of range, inclusive"""
        return self.start + self.steps - 1


@dataclass
class SectionMapping:
    """Represents one line of a section, eg '50 98 2'"""

    source_start: int
    destination_start: int
    steps: int

    @property
    def source_end(self) -> int:
        return self.source_start + self.steps - 1

    def get_corresponding_destination(self, nb: int) -> int:
        # We should raise an Exception here, but for the sake of simplicity we don't
        if nb < self.source_start or nb > self.source_start + self.steps - 1:
            return -1
        return nb + self.destination_start - self.source_start

    def get_corresponding_ranges(
        self, seed_range: SeedRange
    ) -> tuple[SeedRange | None, list[SeedRange]]:
        """Get the next range corresponding to seed_range
        Also provides any leftover ranges

        Args:
            seed_range (SeedRange): seed range to process

        Returns:
            tuple[SeedRange | None, list[SeedRange]]:
            - computed seed range, or None if it is not included
            - list of split leftover ranges
        """
        start_range = self.get_corresponding_destination(seed_range.start)
        end_range = self.get_corresponding_destination(seed_range.end)

        # Fully included
        if start_range != -1 and end_range != -1:
            return (SeedRange(start_range, seed_range.steps), [])
        # Only start is included
        if start_range != -1 and end_range == -1:
            steps = self.steps - (seed_range.start - self.source_start)
            return (
                SeedRange(start_range, steps),
                [SeedRange(seed_range.start + steps, seed_range.steps - steps)],
            )
        # Only end is included
        if start_range == -1 and end_range != -1:
            steps = seed_range.steps - (self.source_start - seed_range.start)
            return (
                SeedRange(
                    self.destination_start,
                    steps,
                ),
                [SeedRange(seed_range.start, seed_range.steps - steps)],
            )

        # Outside with part included
        if seed_range.start < self.source_start and seed_range.end > self.source_end:
            return (
                SeedRange(self.destination_start, self.steps),
                [
                    SeedRange(seed_range.start, self.source_start - seed_range.start),
                    SeedRange(
                        seed_range.end - (seed_range.end - self.source_end) + 1,
                        seed_range.end - self.source_end,
                    ),
                ],
            )

        # Completely outside
        return None, []

    @classmethod
    def test_get_corresponding_destination(cls):
        # Provided test cases
        section_mapping = cls(source_start=50, destination_start=52, steps=48)
        assert section_mapping.get_corresponding_destination(79) == 81
        assert section_mapping.get_corresponding_destination(50) == 52
        assert section_mapping.get_corresponding_destination(97) == 99
        assert section_mapping.get_corresponding_destination(49) == -1
        assert section_mapping.get_corresponding_destination(98) == -1

    @classmethod
    def test_get_corresponding_ranges(cls):
        section_mapping = cls(source_start=50, destination_start=10, steps=20)
        # Fully included
        assert section_mapping.get_corresponding_ranges(SeedRange(50, 10)) == (
            SeedRange(10, 10),
            [],
        )
        assert section_mapping.get_corresponding_ranges(SeedRange(50, 1)) == (
            SeedRange(10, 1),
            [],
        )
        # Only start is included
        assert section_mapping.get_corresponding_ranges(SeedRange(50, 30)) == (
            SeedRange(10, 20),
            [SeedRange(70, 10)],
        )
        assert section_mapping.get_corresponding_ranges(SeedRange(55, 22)) == (
            SeedRange(15, 15),
            [SeedRange(70, 7)],
        )
        # Only end is included
        assert section_mapping.get_corresponding_ranges(SeedRange(40, 30)) == (
            SeedRange(10, 20),
            [SeedRange(40, 10)],
        )
        assert section_mapping.get_corresponding_ranges(SeedRange(45, 11)) == (
            SeedRange(10, 6),
            [SeedRange(45, 5)],
        )
        # Outside with part included
        assert section_mapping.get_corresponding_ranges(SeedRange(40, 40)) == (
            SeedRange(10, 20),
            [SeedRange(40, 10), SeedRange(70, 10)],
        )
        assert section_mapping.get_corresponding_ranges(SeedRange(37, 41)) == (
            SeedRange(10, 20),
            [SeedRange(37, 13), SeedRange(70, 8)],
        )
        # Totally outside
        assert section_mapping.get_corresponding_ranges(SeedRange(1, 3)) == (
            None,
            [],
        )
        assert section_mapping.get_corresponding_ranges(SeedRange(100, 309831)) == (
            None,
            [],
        )


@dataclass
class Section:
    """Represents a whole 'map' block"""

    mappings: list[SectionMapping]

    def get_corresponding_destination(self, nb: int) -> int:
        for mapping in self.mappings:
            if (res := mapping.get_corresponding_destination(nb)) != -1:
                return res
        return nb

    def get_corresponding_ranges(self, seed_ranges: list[SeedRange]) -> list[SeedRange]:
        """Compute corresponding ranges for all seed_ranges

        Args:
            seed_ranges (list[SeedRange]): seed ranges to process

        Returns:
            list[SeedRange]: processed seed ranges
        """
        res: list[SeedRange] = []
        # Careful: this is not a copy
        left_to_process: list[SeedRange] = seed_ranges

        while left_to_process:
            ranges_to_process: list[SeedRange] = left_to_process[:]
            left_to_process = []
            for range_to_process in ranges_to_process:
                for mapping in self.mappings:
                    new_range, leftover_ranges = mapping.get_corresponding_ranges(
                        range_to_process
                    )
                    if new_range:
                        res.append(new_range)
                        left_to_process += leftover_ranges
                        break
                # No corresponding mappings, keep it as is
                else:
                    res.append(range_to_process)
        # We could probably optimize the output to merge some SeedRange here
        return res

    @classmethod
    def test_get_corresponding_destination(cls):
        section_mapping = cls(
            mappings=[
                SectionMapping(98, 50, 2),
                SectionMapping(50, 52, 48),
            ]
        )
        assert section_mapping.get_corresponding_destination(79) == 81
        assert section_mapping.get_corresponding_destination(50) == 52
        assert section_mapping.get_corresponding_destination(97) == 99
        assert section_mapping.get_corresponding_destination(98) == 50
        assert section_mapping.get_corresponding_destination(49) == 49
        assert section_mapping.get_corresponding_destination(100) == 100
        assert section_mapping.get_corresponding_destination(0) == 0

    @classmethod
    def test_get_corresponding_ranges(cls):
        section_mapping = cls(
            mappings=[
                SectionMapping(98, 50, 2),
                SectionMapping(50, 52, 48),
            ]
        )
        # Converted by first SectionMapping
        assert section_mapping.get_corresponding_ranges([SeedRange(98, 1)]) == [
            SeedRange(50, 1)
        ]
        # Converted by second SectionMapping
        assert section_mapping.get_corresponding_ranges([SeedRange(50, 2)]) == [
            SeedRange(52, 2)
        ]
        # Converted by both SectionMapping
        assert section_mapping.get_corresponding_ranges([SeedRange(96, 4)]) == [
            SeedRange(50, 2),
            SeedRange(98, 2),
        ]
        # Converted by both SectionMapping with leftover before and after
        assert section_mapping.get_corresponding_ranges([SeedRange(0, 150)]) == [
            SeedRange(50, 2),
            SeedRange(52, 48),
            SeedRange(100, 50),
            SeedRange(0, 50),
        ]


class Part01:
    @classmethod
    def parse_seed_line(cls, line: str) -> list[int]:
        _, line, *_ = line.split(":")
        return [int(x) for x in line.split()]

    @classmethod
    def parse_section_line(cls, line: str) -> SectionMapping:
        dest, src, steps, *_ = line.split()
        return SectionMapping(
            source_start=int(src), destination_start=int(dest), steps=int(steps)
        )

    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> tuple[list[int], list[Section]]:
        seeds: list[int] = []
        sections: list[Section] = []
        current_section = Section([])

        for idx, line in enumerate(f):
            if idx == 0:
                seeds = cls.parse_seed_line(line)
            # Skip empty lines between seeds and first section
            elif idx > 2:
                # Reset on new section
                if line[0].isalpha():
                    sections.append(current_section)
                    current_section = Section([])
                elif line[0].isnumeric():
                    current_section.mappings.append(cls.parse_section_line(line))
        sections.append(current_section)
        return seeds, sections

    @classmethod
    def get_lowest_location(cls, seeds: list[int], sections: list[Section]) -> int:
        lowest_location: int = -1
        for seed in seeds:
            for section in sections:
                seed = section.get_corresponding_destination(seed)
            if lowest_location == -1:
                lowest_location = seed
            else:
                lowest_location = min(seed, lowest_location)
        return lowest_location

    @classmethod
    def _test_helper_get_example_input(cls) -> io.TextIOWrapper:
        """Returns the example input in a TextIOWrapper"""
        return io.StringIO(
            """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
        )

    @classmethod
    def test_parse_seed_line(cls):
        assert cls.parse_seed_line("seeds: 79 14 55 13") == [79, 14, 55, 13]

    @classmethod
    def test_parse_section_line(cls):
        assert cls.parse_section_line("50 98 2") == SectionMapping(98, 50, 2)

    @classmethod
    def test_parse_file(cls):
        f = cls._test_helper_get_example_input()
        seeds, sections = cls._parse_file(f)
        assert seeds == [79, 14, 55, 13]
        assert len(sections) == 7
        assert sections[0] == Section(
            [
                SectionMapping(98, 50, 2),
                SectionMapping(50, 52, 48),
            ]
        )
        assert sections[1] == Section(
            [
                SectionMapping(15, 0, 37),
                SectionMapping(52, 37, 2),
                SectionMapping(0, 39, 15),
            ]
        )
        assert sections[2] == Section(
            [
                SectionMapping(53, 49, 8),
                SectionMapping(11, 0, 42),
                SectionMapping(0, 42, 7),
                SectionMapping(7, 57, 4),
            ]
        )
        assert sections[3] == Section(
            [
                SectionMapping(18, 88, 7),
                SectionMapping(25, 18, 70),
            ]
        )
        assert sections[4] == Section(
            [
                SectionMapping(77, 45, 23),
                SectionMapping(45, 81, 19),
                SectionMapping(64, 68, 13),
            ]
        )
        assert sections[5] == Section(
            [
                SectionMapping(69, 0, 1),
                SectionMapping(0, 1, 69),
            ]
        )
        assert sections[6] == Section(
            [
                SectionMapping(56, 60, 37),
                SectionMapping(93, 56, 4),
            ]
        )

    @classmethod
    def test_get_lowest_location(cls):
        f = cls._test_helper_get_example_input()
        seeds, sections = cls._parse_file(f)
        assert cls.get_lowest_location(seeds, sections) == 35

    @classmethod
    def solve(cls) -> int:
        seeds: list[int] = []
        sections: list[Section] = []
        with open("input.txt", "r") as f:
            seeds, sections = cls._parse_file(f)
        return cls.get_lowest_location(seeds, sections)


class Part02(Part01):
    @classmethod
    def parse_seed_line(cls, line: str) -> list[SeedRange]:
        _, line, *_ = line.split(":")
        seeds_data = [int(x) for x in line.split()]
        res: list[SeedRange] = []
        for seed_start, steps in zip(seeds_data[::2], seeds_data[1::2]):
            res.append(SeedRange(seed_start, steps))
        return res

    # Override the function prototype
    @classmethod
    def _parse_file(cls, f: io.TextIOWrapper) -> tuple[list[SeedRange], list[Section]]:
        return super()._parse_file(f)  # type: ignore

    @classmethod
    def get_lowest_location(
        cls, seed_ranges: list[SeedRange], sections: list[Section]
    ) -> int:
        seed_ranges_to_proceed = seed_ranges
        for section in sections:
            seed_ranges_to_proceed = section.get_corresponding_ranges(
                seed_ranges_to_proceed
            )
        # The min location is the start point of the range with the smallest start
        return min(seed_range.start for seed_range in seed_ranges_to_proceed)

    @classmethod
    def test_parse_seed_line(cls):
        assert cls.parse_seed_line("seeds: 79 14 55 13") == [
            SeedRange(79, 14),
            SeedRange(55, 13),
        ]

    @classmethod
    def test_parse_file(cls):
        f = cls._test_helper_get_example_input()
        seeds, _ = cls._parse_file(f)
        assert seeds == [
            SeedRange(79, 14),
            SeedRange(55, 13),
        ]

    @classmethod
    def test_get_lowest_location(cls):
        f = cls._test_helper_get_example_input()
        seeds, sections = cls._parse_file(f)
        assert cls.get_lowest_location(seeds, sections) == 46


if __name__ == "__main__":
    SectionMapping.test_get_corresponding_destination()
    Section.test_get_corresponding_destination()
    Part01.test_parse_seed_line()
    Part01.test_parse_section_line()
    Part01.test_parse_file()
    Part01.test_get_lowest_location()

    SectionMapping.test_get_corresponding_ranges()
    Section.test_get_corresponding_ranges()
    Part02.test_parse_seed_line()
    Part02.test_parse_file()
    Part02.test_get_lowest_location()

    print(Part01.solve())
    print(Part02.solve())
