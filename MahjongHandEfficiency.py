from itertools import combinations
import numpy as np
import re


# Every hand is at least 6-shanten, though any hand with a pair is at least 5-shanten
# Examples of 6-shanten hands:
# 147m258p369s1234z5z
# 258m258s258p4567z1z

class MahjongEfficiency(object):
    def __init__(self):
        self.tiles_in_hand = {
            "manzu": "m",
            "pinzu": "p",
            "souzu": "s",
            "jihai": "z"
        }
        self.meld_types = {
            # Complete
            "ankou": [],  # Triplet
            "shuntsu": [],  # Sequence
            "tanki": [],  # Pair
            # Incomplete (all need 1 tile to complete)
            "kanchan": [],  # 1-sided wait
            "penchan": [],  # End wait
            "ryanmen": [],  # 2-sided wait
            "toitsu": []  # Pair that needs a third, only applicable if there is a more suitable pair.
        }
        self.hand = input("Please input a starting hand:")
        self.shanten_count = 0

        # ----------------------------
        self.check_input_validity()
        self.separate_hand_suits()
        self.count_wait_types()

    def check_input_validity(self):
        # Need to change this to instead request proper input, rather than editing incorrect input, therefore
        # eliminating the need for re (this was for practice).
        self.hand = re.sub(r"([^\dmpsz])", "", self.hand)  # Remove unwanted characters from input
        if len(re.sub(r"([^\d])", "", self.hand)) != 14:  # If the number of digits is not 14
            raise Exception("Please input a valid starting hand of 14 tiles.")

    def separate_hand_suits(self):
        """
        Takes the input hand string; separates the tiles into each suit then orders them.

        :return: Dictionary of suit names and lists of tiles.

        :rtype: dict[str, list[int, int]]
        """
        for name, item in self.tiles_in_hand.items():
            # Group numerical characters into the dictionary so that each suit is separate.
            self.tiles_in_hand[name] = re.findall(r"(\d+)" + item, self.hand, flags=re.IGNORECASE)
            # Reformat string so that each digit is an element of a list in numerical order.
            self.tiles_in_hand[name] = [list(item) for item in self.tiles_in_hand[name]]
            self.tiles_in_hand[name] = [int(item) for sublist in self.tiles_in_hand[name] for item in sublist]
            self.tiles_in_hand[name] = sorted(self.tiles_in_hand[name])

    def count_wait_types(self):
        for name, item in self.tiles_in_hand.items():
            if len(self.tiles_in_hand[name]) > 0:
                if name != "jihai":
                    tile_combinations = [list(i) for i in list(combinations(self.tiles_in_hand[name], 3))]
                    tile_differences = np.diff(tile_combinations)
                    print("Tile combinations:", tile_combinations)
                    print("Tile differences:", tile_differences)
                else:
                    pass


if __name__ == "__main__":
    MahjongEfficiency()
