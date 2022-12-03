from src.Mahjong_Hand_Efficiency import MahjongEfficiency
from src.Random_Starting_Hand import random_starting_hand

if __name__ == "__main__":
    random_hand = random_starting_hand(1)[0]
    MahjongEfficiency(random_hand)
