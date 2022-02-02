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
        self.hand = hand.replace(" ", "")  # Need to remove whitespace to avoid errors.
        self.shanten = 6
        self.hand_array = []
        self.mapping_array = [["m", 0], ["p", 9], ["s", 18], ["z", 27]]

        # ----------------------------
        self.error_handling()  # This call checks that the number of tiles is 14.
        self.map_input_hand()
        self.error_handling()  # This second call checks that the maximum number of each tile is 4.
        print("Hand: {}".format(self.hand))
        print("Hand array: {}".format(self.hand_array))  # For testing only.
        melds_manzu, couples_manzu, eyes_manzu = self.create_tile_combinations(1, 9)
        melds_pinzu, couples_pinzu, eyes_pinzu = self.create_tile_combinations(10, 18)
        melds_souzu, couples_souzu, eyes_souzu = self.create_tile_combinations(19, 27)
        melds_jihai, couples_jihai, eyes_jihai = self.create_tile_combinations(28, 34)

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
                    #  Gets the tiles of each suit, maps them to the new numbers, then appends them to the hand_array.
                    tiles = mutable_hand[last_index:index]
                    tiles = [int(k) + self.mapping_array[ma_index][1] for k in tiles]
                    self.hand_array.extend(tiles)
        self.hand_array.sort()

    def create_tile_combinations(self, floor, ceiling):
        """
        Takes the input hand and creates three lists of tile combinations for each suit.
        These are melds, couples and eyes, where melds are groups of three, couples are groups of two, and eyes are
        single tiles.
        """
        suit = [i for i in self.hand_array if ceiling >= i >= floor]
        melds = [set([i for i in itertools.combinations(suit, 3)])]
        couples = [set([i for i in itertools.combinations(suit, 2)])]
        eyes = [set([i for i in itertools.combinations(suit, 1)])]
        return melds, couples, eyes

    def get_tile_combinations(self, input_combinations):  # Need to change inequalities to match above (y >= s >= x)
        suit_floor = [self.mapping_array[k][1] for k in range(0, len(self.mapping_array))]
        tile_combinations = [i for j in range(0, len(input_combinations)) for i in input_combinations[j]]
        for combination in tile_combinations:
            if len(combination) == 3:
                if combination[0] > suit_floor[3]:
                    self.meld_type(combination)
                elif suit_floor[3] >= combination[0] > suit_floor[2]:
                    self.meld_type(combination)
                elif suit_floor[2] >= combination[0] > suit_floor[1]:
                    self.meld_type(combination)
                elif suit_floor[1] >= combination[0] > suit_floor[0]:
                    self.meld_type(combination)
            if len(combination) == 2:
                if combination[0] > suit_floor[3]:
                    self.couple_type(combination, suit_floor[3], 34)
                elif suit_floor[3] >= combination[0] > suit_floor[2]:
                    self.couple_type(combination, suit_floor[2], suit_floor[3])
                elif suit_floor[2] >= combination[0] > suit_floor[1]:
                    self.couple_type(combination, suit_floor[1], suit_floor[2])
                elif suit_floor[1] >= combination[0] > suit_floor[0]:
                    self.couple_type(combination, suit_floor[0], suit_floor[1])

    def meld_type(self, combination):
        if combination[1] == sum(combination) / len(combination) and combination[1] == combination[0] + 1:
            if combination[0] <= 27:  # Jihai can only be ankou or pairs
                print("shuntsu", combination)
        elif combination[0] == sum(combination) / len(combination):
            print("ankou", combination)

    def couple_type(self, combination, floor, ceiling):  # Need to edit this so that: e.g. floor is 1 ceiling is 9
        if combination[0] <= 27:
            if combination[0] == combination[1] + 1:
                if combination[0] >= floor or combination[1] > ceiling:
                    print("ryanmen", combination)  # ryanmen (n, n+1) 2-sided wait
                else:
                    print("penchan", combination)  # penchan (n, n+1) 1-sided wait (edge-wait)
            elif combination[0] == combination[1] + 2:
                print("kanchan", combination)  # kanchan (n, n+2) 1-sided wait
            elif combination[0] == combination[1]:
                print("pair",
                      combination)  # toitsu, shanpon, or jantou (this depends on the amount of this type present).
        else:  # Jihai can only have pairs, no other couple wait type
            if combination[0] == combination[1]:
                print("pair", combination)

    def chiitoitsu(self, couples):
        pairs = [couple for suit in range(0, len(couples)) for couple in couples[suit] if couple[0] == couple[1]]
        chiitoitsu_shanten = 6 - len(pairs)  # -1 is a winning hand, 0 is a ready hand
        return chiitoitsu_shanten

    def kokushi_musou(self, eyes):  # Need 9 different terminals and honours for 4-shanten
        pass

    def get_shanten(self):
        pass
