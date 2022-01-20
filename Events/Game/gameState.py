import logging
import typing



from Events.Game.GameObjects.tools.enum.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.GameObjects.hand import Hand
from Events.Game.GameObjects.tools.move_tools import get_point_on_tier1
from Events.Game.GameObjects.uav import Uav


class GameState():
    def __init__(self, uav_number,v_of_uav,velocity_hand,map_size,hands_number):

        self.visualize_first=True

        #init UAv
        self.uav_list:typing.List[Uav] = []
        self.list_of_dead_uavs=[]

        for i in range(0, uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,v_of_uav,i,0,UavStatus.TIER_2,None))

        #init hands
        self.hands_list = []
        if(hands_number==1):
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size,0,HandStatus.TIER_0,None))
        else:
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.RIGHT,map_size,map_size,0,HandStatus.TIER_0,None))
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size,0,HandStatus.TIER_0,None))

        logging.info("state initiated")



    def update_postions(self,current_time,uav_velocity,event_owner):
        for uav in self.uav_list: #uavs to update
            if event_owner!=uav:
                if uav.status!=UavStatus.TIER_2 or uav.status!=UavStatus.DEAD:
                    delta_time=current_time-uav.last_postion_update_time
                    distance=delta_time*uav_velocity #distance which was taken during delta
                    if uav.next_status == UavStatus.TIER_1 and uav.status == UavStatus.TIER_1:  # move on circle
                        uav.set_new_position(get_point_on_tier1(uav.position,distance,uav.target_position),current_time)









