import itertools


class MahjongEfficiency(object):
    """
    Class to generate the shanten of a given Japanese Mahjong hand.

    Methods:
        error_handling():
            Checks that the input contains 14 tiles and a maximum of 4 of each tile.
        map_input_hand():
            Returns the hand in the mapped format ready for further computation.
        create_tile_combinations():
            Returns lists containing all the melds, couples and eyes that can be formed from each suit.
    """

    def __init__(self, hand):
        """

        :param hand:
        """
        # hand = input("Please input a hand: ")
        self.shuntsu = []
        self.ankou = []
        self.kanchan = []
        self.pair = []
        self.penchan = []
        self.ryanmen = []
        self.hand_array = []
        self.melds = []
        self.eyes = []
        self.couples = []
        self.mapping_array = [["m", 0], ["p", 9], ["s", 18], ["z", 27]]
        self.floor = [1, 10, 19, 28]
        self.ceiling = [9, 18, 27, 34]

        # ----------------------------
        self.hand = hand.replace(" ", "")  # Need to remove whitespace to avoid errors.
        self.error_handling()  # This call checks that the number of tiles is 14.
        self.map_input_hand()
        self.error_handling()  # This second call checks that the maximum number of each tile is 4.
        print("Hand: {}".format(self.hand))

        combinations = []
        for i in range(0, len(self.floor)):
            combinations.append(self.tile_combinations(self.floor[i], self.ceiling[i]))

        kokushi_shanten = self.kokushi_musou(self.floor, self.ceiling)
        chiitoitsu_shanten = self.chiitoitsu()
        shanten = self.get_shanten()
        self.shanten = min(chiitoitsu_shanten, shanten, kokushi_shanten)

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

    def tile_combinations(self, floor: int, ceiling: int):
        """
        Takes the floor and ceiling of a suit and generates tile combinations of melds, couples and eyes, where melds
        are groups of three, couples are groups of two, and eyes are single tiles.\n
        It then groups these combinations into types, where n is in range(1, 34):\n
        Melds: \n
        shuntsu: (n, n+1, n+2) and ankou: (n, n, n), \n
        Couples:\n
        kanchan: (n, n+2), penchan: (1, 2) or (8, 9), ryanmen: (n, n+1) (excluding penchan waits), pair (n, n)
        """
        suit = [i for i in self.hand_array if ceiling >= i >= floor]
        self.melds = list(set([i for i in itertools.combinations(suit, 3)]))
        self.couples = list(set([i for i in itertools.combinations(suit, 2)]))
        self.eyes = list(set([i for i in itertools.combinations(suit, 1)]))
        for i in range(0, len(self.melds)):
            self.meld_type(self.melds[i])
        for i in range(0, len(self.couples)):
            if min(self.couples[i]) >= self.floor[3]:
                self.couple_type(self.couples[i], self.floor[3], self.ceiling[3])
            elif self.floor[3] >= min(self.couples[i]) >= self.floor[2]:
                self.couple_type(self.couples[i], self.floor[2], self.ceiling[2])
            elif self.floor[2] >= min(self.couples[i]) >= self.floor[1]:
                self.couple_type(self.couples[i], self.floor[1], self.ceiling[1])
            else:
                self.couple_type(self.couples[i], self.floor[0], self.ceiling[0])

    def meld_type(self, combination: tuple):
        if min(combination) >= self.floor[3]:
            if combination[0] == sum(combination) / len(combination):
                self.ankou.append(combination)
        else:
            if combination[1] == sum(combination) / len(combination) and combination[1] == combination[0] + 1:
                self.shuntsu.append(combination)
            if combination[0] == sum(combination) / len(combination):
                self.ankou.append(combination)

    def couple_type(self, combination: tuple, floor: int, ceiling: int):
        if floor < self.floor[3]:
            if (combination[1] == combination[0] + 1) and (combination != (floor, ceiling)):
                self.ryanmen.append(combination)
            if (combination[1] == combination[0] + 1) and (combination[0] == floor or combination[1] == ceiling):
                self.penchan.append(combination)
            if combination[1] == combination[0] + 2:
                self.kanchan.append(combination)
            if combination[0] == combination[1]:
                self.pair.append(combination)
        else:
            if combination[0] == combination[1]:
                self.pair.append(combination)

    def chiitoitsu(self) -> int:
        chiitoitsu_shanten = 6 - len(self.pair)
        return chiitoitsu_shanten

    def kokushi_musou(self, floor: int, ceiling: int) -> int:
        terminals = [i for i in self.eyes if i in (floor or ceiling)]
        kokushi_shanten = 13 - len(terminals)
        return kokushi_shanten

    def get_shanten(self):
        shanten = 6
        return shanten

    def output(self):
        if self.shanten > -1:
            print("Shanten: {}".format(self.shanten))
        elif self.shanten == -1:
            print("This hand is complete.")
        else:  # This should be impossible
            raise Exception("Shanten not within bounds: {}".format(self.shanten))
