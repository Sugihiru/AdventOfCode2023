from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from functools import total_ordering
from typing import Self

CARDS_ORDER = "23456789TJQKA"


class HandValue(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclass
@total_ordering
class Hand:
    cards: str
    bid: int
    cards_counter: Counter
    CARDS_ORDER = "23456789TJQKA"

    def __init__(self, cards: str, bid: int = 0):
        self.cards = cards
        self.bid = bid
        self.cards_counter = Counter(self.cards)

    def __eq__(self, other: Self):
        return self.cards == other.cards

    def __lt__(self, other: Self) -> bool:
        if self.value != other.value:
            return self.value < other.value
        for c1, c2 in zip(self.cards, other.cards):
            if c1 != c2:
                return self.CARDS_ORDER.index(c1) < self.CARDS_ORDER.index(c2)
        return False

    @property
    def value(self) -> int:
        match [x[1] for x in self.cards_counter.most_common()]:
            case [5]:
                return HandValue.FIVE_OF_A_KIND
            case [4, 1]:
                return HandValue.FOUR_OF_A_KIND
            case [3, 2]:
                return HandValue.FULL_HOUSE
            case [3, 1, 1]:
                return HandValue.THREE_OF_A_KIND
            case [2, 2, 1]:
                return HandValue.TWO_PAIR
            case [2, 1, 1, 1]:
                return HandValue.ONE_PAIR
            case _:
                return HandValue.HIGH_CARD

    @classmethod
    def test_value(cls):
        assert cls("AAAAA").value == HandValue.FIVE_OF_A_KIND
        assert cls("AA8AA").value == HandValue.FOUR_OF_A_KIND
        assert cls("23332").value == HandValue.FULL_HOUSE
        assert cls("TTT98").value == HandValue.THREE_OF_A_KIND
        assert cls("23432").value == HandValue.TWO_PAIR
        assert cls("A23A4").value == HandValue.ONE_PAIR
        assert cls("23456").value == HandValue.HIGH_CARD

    @classmethod
    def test_cmp(cls):
        assert cls("AAAAA") > cls("AA8AA") > cls("23332")
        assert cls("KK677") > cls("KTJJT")
        assert cls("T55J5") < cls("QQQJA")
        assert cls("T55J5") == cls("T55J5")


class HandWithJoker(Hand):
    CARDS_ORDER = "J23456789TQKA"

    def __init__(self, cards: str, bid: int = 0):
        super().__init__(cards, bid)
        if self.cards != "JJJJJ" and "J" in self.cards_counter:
            nb_jokers = self.cards_counter.pop("J")
            most_common_key, _ = self.cards_counter.most_common(1)[0]
            self.cards_counter[most_common_key] += nb_jokers

    @classmethod
    def test_value(cls):
        assert cls("JJJJJ").value == HandValue.FIVE_OF_A_KIND
        assert cls("AA8AJ").value == HandValue.FOUR_OF_A_KIND
        assert cls("2J332").value == HandValue.FULL_HOUSE
        assert cls("TTJ98").value == HandValue.THREE_OF_A_KIND
        assert cls("23456").value == HandValue.HIGH_CARD
        assert cls("2J456").value == HandValue.ONE_PAIR
        assert cls("JJ432").value == HandValue.THREE_OF_A_KIND
        assert cls("JJ4J2").value == HandValue.FOUR_OF_A_KIND

    @classmethod
    def test_cmp(cls):
        assert cls("KTJJT") > cls("QQQJA") > cls("T55J5") > cls("KK677") > cls("32T3K")
        assert cls("AAAAA") > cls("JJJJJ")
        assert cls("JJ432") < cls("22243")


class Part01:
    @classmethod
    def parse_line(cls, line: str) -> Hand:
        cards, bid = line.split()
        return Hand(cards, int(bid))

    @classmethod
    def parse_file(cls) -> int:
        hands: list[Hand] = []
        with open("input.txt", "r") as f:
            for line in f:
                hands.append(cls.parse_line(line))

        hands = sorted(hands)
        res = 0
        for idx, hand in enumerate(hands):
            res += (idx + 1) * hand.bid
        return res


class Part02(Part01):
    @classmethod
    def parse_line(cls, line: str) -> HandWithJoker:
        cards, bid = line.split()
        return HandWithJoker(cards, int(bid))


if __name__ == "__main__":
    Hand.test_value()
    Hand.test_cmp()

    HandWithJoker.test_value()
    HandWithJoker.test_cmp()

    print(Part01.parse_file())
    print(Part02.parse_file())
