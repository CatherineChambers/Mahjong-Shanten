import itertools

import Random_Starting_Hand


class MahjongEfficiency(object):
    """
    Class to generate the shanten of a given Japanese Mahjong hand.

    Attributes:
        hand : str
            The 14 tile input hand.

    Methods:
        error_handling():
            Checks that the input contains 14 tiles and a maximum of 4 of each tile.
        map_input_hand():
            Returns the hand in the mapped format ready for further computation.
    """

    def __init__(self, hand):
        # hand = input("Please input a hand: ")
        self.hand = hand.replace(" ", "")  # Need to remove whitespace to avoid errors.
        self.shanten_count = 0
        self.hand_array = []
        self.mapping_array = [["m", 0], ["p", 9], ["s", 18], ["z", 27]]

        # ----------------------------
        self.error_handling()  # This call checks that the number of tiles is 14.
        self.map_input_hand()
        self.error_handling()  # This second call checks that the maximum number of each tile is 4.
        print("Hand: {}".format(self.hand))
        print("Hand array: {}".format(self.hand_array))  # For testing only.
        melds, pairs, eyes = self.create_tile_combinations()
        self.choose_melds(melds)
        self.choose_melds(pairs)
        self.choose_melds(eyes)

    def error_handling(self):
        stripped_hand = "".join([char for char in self.hand if char.isdigit()])
        if len(stripped_hand) != 14:
            raise Exception("Please input a valid starting hand of 14 tiles.")

        unwanted_char = [char for char in self.hand if char not in "123456789mpsz"]
        if len(unwanted_char) > 0:
            raise Exception("Please input a valid hand. This cannot contain: {}.".format(unwanted_char))

        # ----------------------------
        tiles = [i for sublist in self.hand_array for i in sublist]
        count = [tiles.count(i) for i in tiles]
        more_than_four = [i for i in count if i > 4]
        if len(more_than_four) > 0:
            raise Exception("Please input a valid hand. You can not have more than 4 of any tile")

    def map_input_hand(self):
        """
        Takes the input hand and maps it to: 1-9 manzu, 10-18 pinzu, 19-27 souzu, 28-34 jihai.
        Red fives and flowers tiles are excluded.
        """
        index = 0
        mutable_hand = self.hand
        stripped_hand_suits = [char for char in self.hand if not char.isdigit()]

        for suit in stripped_hand_suits:
            for suit_list in self.mapping_array:
                if suit in suit_list:
                    ma_index = self.mapping_array.index(suit_list)
                    last_index = index
                    # Finds the position of each of "mpsz" in the input hand.
                    index = mutable_hand.index(self.mapping_array[ma_index][0])
                    # Removes the suit character from the hand so that subsequent indexing gives the correct index.
                    # e.g. 123m2p vs 1232p: the index of p should be 4.
                    mutable_hand = mutable_hand.replace(suit, "", 1)
                    #  Gets the tiles of each suit, maps them to the new numbers, then appends them to the hand_array.
                    tiles = mutable_hand[last_index:index]
                    tiles = [int(k) for k in tiles]
                    self.hand_array.append([k + self.mapping_array[ma_index][1] for k in tiles])

    def create_tile_combinations(self):
        melds = []
        pairs = []
        eyes = []
        for suit in self.hand_array:
            melds.append(list(set([i for i in itertools.combinations(suit, 3)])))
            pairs.append(list(set([i for i in itertools.combinations(suit, 2)])))
            eyes.append(list(set([i for i in itertools.combinations(suit, 1)])))
        return melds, pairs, eyes

    def choose_melds(self, tile_combinations):
        for j in range(0, len(tile_combinations)):
            for combination in tile_combinations[j]:
                if combination[0] > self.mapping_array[3][1]:
                    pass
                elif self.mapping_array[3][1] >= combination[0] > self.mapping_array[2][1]:
                    pass
                elif self.mapping_array[2][1] >= combination[0] > self.mapping_array[1][1]:
                    pass
                else:
                    pass

    def count_fu(self):
        pass

    def count_han(self):
        pass


if __name__ == "__main__":
    random_hand = "57899p 4468s 34567z"
    # random_hand = Random_Starting_Hand.random_starting_hand(1)
    MahjongEfficiency(random_hand)
