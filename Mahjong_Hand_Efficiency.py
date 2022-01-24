import numpy as np
import Random_Starting_Hand


class MahjongEfficiency(object):
    def __init__(self, hand):
        self.hand = hand
        self.shanten_count = 0
        tiles = np.linspace(1, 34, 34, dtype=int)
        self.tiles_array = np.concatenate([tiles, tiles, tiles, tiles])
        self.hand_array = []

        # ----------------------------
        self.error_handling()
        self.input_hand_to_tiles_array()
        self.check_tile_combinations()
        self.count_tile_amount()

    def error_handling(self):
        stripped_hand = "".join([char for char in self.hand if char.isdigit()])
        if len(stripped_hand) != 14:  # If the number of digits is not 14
            raise Exception("Please input a valid starting hand of 14 tiles.")

    def input_hand_to_tiles_array(self):
        index = []
        mapping_array = [["m", -1], ["p", 9], ["s", 18], ["z", 27]]
        mutable_hand = self.hand
        stripped_hand_suits = [char for char in self.hand if not char.isdigit()]

        for suit in stripped_hand_suits:
            for suit_list in mapping_array:
                if suit in suit_list:
                    i = mapping_array.index(suit_list)
                    if i == 0:
                        last_index = 0
                    else:
                        last_index = index
                    index = mutable_hand.index(mapping_array[i][0])
                    mutable_hand = mutable_hand.replace(suit, "", 1)
                    tiles = mutable_hand[last_index:index]
                    tiles = [int(k) for k in tiles]
                    self.hand_array.append(self.tiles_array[[k + mapping_array[i][1] for k in tiles]])

    def check_tile_combinations(self):
        pass

    def count_tile_amount(self):
        pass

    def count_fu(self):
        pass

    def count_han(self):
        pass


if __name__ == "__main__":
    random_hand = Random_Starting_Hand.random_starting_hand(1)
    MahjongEfficiency(random_hand)
