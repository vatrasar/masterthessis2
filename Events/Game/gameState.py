import logging
import typing



from Events.Game.GameObjects.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.GameObjects.hand import Hand
from Events.Game.GameObjects.uav import Uav


class GameState():
    def __init__(self, uav_number,v_of_uav,velocity_hand,map_size,hands_number):
        self.t_curr=0
        self.visualize_first=True

        #init UAv
        self.uav_list:typing.List[Uav] = []
        self.list_of_dead_uavs=[]

        for i in range(0, uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,v_of_uav,i))

        #init hands
        self.hands_list = []
        if(hands_number==1):
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size))
        else:
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.RIGHT,map_size,map_size))
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size))

        logging.info("state initiated")












