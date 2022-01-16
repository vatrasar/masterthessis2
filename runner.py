from Events.Game.gameState import GameState
from Events.Game.settings import Settings


class Runner():
    def __init__(self,settings:Settings,rand):
        self.settings=settings
        self.rand=rand

    def run(self):
            game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size,self.settings.hands_number)
            if self.settings.visualisation==0:



