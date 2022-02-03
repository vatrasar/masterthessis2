import logging
import typing

from Events.Game.move.GameObjects.intruder import Intruder
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.point import Point

from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.get_position import get_point_on_tier1, get_point_base_on_distance
import typing

class GameState():
    def __init__(self, uav_number,v_of_uav,velocity_hand,map_size,hands_number):

        self.visualize_first=True

        #init UAv
        self.uav_list:typing.List[Uav] = []
        self.list_of_dead_uavs=[]

        for i in range(0, uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,v_of_uav,i,0,UavStatus.TIER_2,None))

        #init hands
        self.hands_list:typing.List[Hand] = []
        if(hands_number==1):
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size,0,HandStatus.TIER_0,None))
        else:
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.RIGHT,map_size,map_size,0,HandStatus.TIER_0,None))
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size,map_size,0,HandStatus.TIER_0,None))

        self.intruder=Intruder(0,0,UavStatus.WAIT,20,20,0,UavStatus.WAIT,Point(0,0,))
        logging.info("state initiated")



    def update_postions(self,current_time,uav_velocity,hand_velocity,event_owner):
        for uav in self.uav_list: #uavs to update
            if event_owner!=uav:
                if uav.status!=UavStatus.TIER_2 or uav.status!=UavStatus.DEAD:
                    delta_time=current_time-uav.last_postion_update_time
                    distance=delta_time*uav_velocity #distance which was taken during delta
                    if (uav.next_status == UavStatus.TIER_1 and uav.status == UavStatus.TIER_1) or (uav.next_status == UavStatus.DODGE and uav.status == UavStatus.PLANED_DODGE):  # move on circle
                        uav.set_new_position(get_point_on_tier1(uav.position,distance,uav.target_position),current_time)
                    else:
                        uav.set_new_position(get_point_base_on_distance(uav.position, distance, uav.target_position), current_time)



        for hand in self.hands_list:
            if event_owner!=hand:
                if hand.status!=HandStatus.WAIT and hand.status!=HandStatus.TIER_0:
                    delta_time=current_time-hand.last_postion_update_time
                    distance=delta_time*hand_velocity
                    hand.set_new_position(get_point_base_on_distance(hand.position, distance, hand.target_position), current_time)





