class MahjongEfficiency(object):
    """
    Class to generate the shanten of a given Japanese Mahjong hand.

    Methods:
        error_handling():
            Checks that the input contains 14 tiles and a maximum of 4 of each tile.
        map_input_hand():
            Generates the hand in the mapped format ready for further computation.
        count_meld():
            Counts the number of melds (shuntsu and ankou), couples (penchan, ryanmen and kanchan), and pairs
        get_shanten():
            Generates the normal shanten, kokushi shanten, and chiitoitsu shanten.
        output():
            Prints the final shanten.
    """

    def __init__(self, hand):
        # hand = input("Please input a hand: ")
        self.hand_array = []

        self.mapping_array = [["m", 0], ["p", 9], ["s", 18], ["z", 27]]
        self.floor = [1, 10, 19, 28]
        self.ceiling = [9, 18, 27, 34]

        # ----------------------------
        self.hand = hand.replace(" ", "")  # Need to remove whitespace to avoid errors.
        self.error_handling()  # This call checks that the number of tiles is 14.
        self.map_input_hand()
        self.error_handling()  # This second call checks that the maximum number of each tile is 4.
        print("Hand: {}".format(self.hand))

        self.shanten = self.get_shanten(self.floor, self.ceiling)
        self.output()

    def error_handling(self):
        """Checks whether the input has 14 tiles, no more than 4 of any tile, and the correct characters."""
        stripped_hand = "".join([char for char in self.hand if char.isdigit()])
        if len(stripped_hand) != 14:
            raise Exception("Please input a valid starting hand of 14 tiles.")

        unwanted_char = [char for char in self.hand if char not in "123456789mpsz"]
        if len(unwanted_char) > 0:
            raise Exception("Please input a valid hand. This cannot contain: {}.".format(unwanted_char))

        # ----------------------------
        count = [self.hand_array.count(i) for i in self.hand_array]
        more_than_four = [i for i in count if i > 4]
        if len(more_than_four) > 0:
            raise Exception("Please input a valid hand. You can not have more than 4 of any tile")

    def map_input_hand(self):
        """
        Takes the input hand and maps it to: 1-9 manzu, 10-18 pinzu, 19-27 souzu, 28-34 jihai.
        Red fives and flower tiles are excluded.
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
                    tiles = mutable_hand[last_index:index]
                    # Maps the tiles to the new numbers
                    tiles = [int(k) + self.mapping_array[ma_index][1] for k in tiles]
                    self.hand_array.extend(tiles)
        self.hand_array.sort()

    def count_melds(self, suit):
        jihai = [1 for _ in suit if self.floor[3] <= suit[0] and len(suit) > 0]
        complete_melds = 0
        incomplete_melds = 0
        pairs = 0
        complete_melds_true = 1
        while len(suit) > 1:
            if len(suit) > 2 and complete_melds_true:  # Loop for complete melds. They are always of length 3.
                if suit[0] == (suit[1] == suit[2] or suit[0] == suit[1] - 1 == suit[2] - 2) and not jihai:
                    complete_melds += 1
                    del suit[0:3]  # Need to delete the meld from the suit so that numbers are not counted twice.
                elif suit[0] == suit[1] == suit[2]:  # Jihai can only have ankou.
                    complete_melds += 1
                    del suit[0:3]
                else:  # If there are no more complete melds, we need to stop the loop.
                    complete_melds_true = 0
            else:
                if (suit[0] == suit[1] - 1 or suit[0] == suit[1] - 2) and not jihai:
                    incomplete_melds += 1
                    del suit[0:2]
                elif suit[0] == suit[1]:
                    pairs += 1
                    del suit[0:2]
                else:
                    del suit[0]
                    # If there are no incomplete melds, we need to remove the first value and continue.
                    # Because two incomplete melds can be more than 4 tiles away from one another, if we break it will
                    # not count the second couple.
        return complete_melds, incomplete_melds, pairs

    def get_shanten(self, floor: list, ceiling: list) -> (int, int, int):
        complete_meld = 0
        incomplete_meld = 0
        pair = 0
        for i in range(0, 4):
            suit = [tile for tile in self.hand_array if floor[i] <= tile <= ceiling[i]]
            meld, couple, pairs = self.count_melds(suit)
            complete_meld += meld
            incomplete_meld += couple
            pair += pairs

        terminals_full = [i for i in self.hand_array if i in floor or i in ceiling or i > 27]
        terminals = set(terminals_full)
        if len(terminals) != len(terminals_full):  # If there is a pair
            kokushi_shanten = 13 - len(terminals) - 1
        else:
            kokushi_shanten = 13 - len(terminals)
        chiitoitsu_shanten = 6 - pair

        shanten = 8 - 2 * complete_meld - incomplete_meld - pair
        return chiitoitsu_shanten, shanten, kokushi_shanten

    def output(self):
        shanten = min(self.shanten)
        if 6 >= shanten > -1:
            print("Normal shanten: {}, chiitoitsu shanten: {}, kokushi shanten: {}"
                  .format(self.shanten[1], self.shanten[0], self.shanten[2]))
        elif shanten == -1:
            print("This hand is complete.")
        else:  # This should be impossible
            raise Exception("Shanten not within bounds: {}".format(shanten))
