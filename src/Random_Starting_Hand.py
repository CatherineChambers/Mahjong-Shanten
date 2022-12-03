import numpy as np


def random_starting_hand(input_number: int) -> list:
    """ Generates a number of random Mahjong hands specified by the input integer. """
    k = 0
    final_output = []
    while k < int(input_number):
        k += 1

        # Creates tiles_by_code, which lists the number of tiles 1-9 of each suit (1-7 for jihai)
        suits = np.linspace(1, 9, 9, dtype=int)
        tiles_by_code = np.concatenate([suits, suits, suits, np.linspace(1, 7, 7, dtype=int)])
        # Creates a tiles_array, which lists the number of non-duplicated tiles in each suit 1-34
        tiles = np.linspace(1, 34, 34, dtype=int)
        tiles_array = np.concatenate([tiles, tiles, tiles, tiles])

        chosen_tiles = np.random.choice(tiles_array, 14, replace=False)

        # Attributes the tiles to the correct suit and creates the hand using standard tile notation
        manzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if i < 10])
        pinzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 9 < i < 19])
        souzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 18 < i < 28])
        jihai = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 27 < i < 35])
        hand_as_list = manzu + list("m") + pinzu + list("p") + souzu + list("s") + jihai + list("z")
        hand_output = "".join(str(i) for i in hand_as_list)

        final_output.append(hand_output)
    return final_output
