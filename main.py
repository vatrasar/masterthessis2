import random

from GameObjects.gameState import GameState
from settings import Settings
import logging



def main():
    settings:Settings=Settings()
    try:
        settings.get_properties()
    except Exception as exp:
        print(str(exp))
        return

    #init state
    rand = random.Random(settings.seed)  # 800
    game_state=GameState(settings.uav_number,settings.v_of_uav,settings.velocity_hand,settings.map_size,settings.hands_number)


if __name__ == '__main__':
    main()

