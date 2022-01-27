import numpy as np


def random_starting_hand(input_number: int) -> str:
    """ Generates a number of random Mahjong hands specified by the input integer. """
    k = 0
    while True:
        if k == int(input_number):
            break
        k += 1
        suits = np.linspace(1, 9, 9, dtype=int)
        tiles_by_code = np.concatenate([suits, suits, suits, np.linspace(1, 7, 7, dtype=int)])
        tiles = np.linspace(1, 34, 34, dtype=int)
        tiles_array = np.concatenate([tiles, tiles, tiles, tiles])

        chosen_tiles = np.random.choice(tiles_array, 14, replace=False)

        manzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if i < 10])
        pinzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 9 < i < 19])
        souzu = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 18 < i < 28])
        jihai = sorted([tiles_by_code[i - 1] for i in chosen_tiles if 27 < i < 35])
        hand_as_list = manzu + list("m") + pinzu + list("p") + souzu + list("s") + jihai + list("z")
        hand_output = "".join(str(i) for i in hand_as_list)
        return hand_output
