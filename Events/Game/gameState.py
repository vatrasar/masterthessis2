import logging
from random import Random

from Events.Game.move.Simple_map import Simple_map
from Events.Game.move.algos.GameObjects.data_lists.Hit_list import Hit_list
from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_list
from Events.Game.move.algos.GameObjects.data_lists.all_results import Result_tr_list
from Events.Game.move.algos.GameObjects.data_lists.result import Result_file
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.naive_algo import Naive_Algo
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.intruder import Intruder
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point

from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_point_on_tier1, get_point_base_on_distance
import typing

class GameState():
    def __init__(self, uav_number,v_of_uav,velocity_hand,map_size_x,map_size_y,hands_number,map_resolution,uav_size,hand_size,list_of_cells_with_points,settings,setting:Settings,rand:Random,hit_list,result_tr_list,result_file):

        self.visualize_first=True
        self.t_curr=0
        #init UAv
        self.uav_list:typing.List[Uav] = []
        self.list_of_dead_uavs=[]
        self.hit_list=hit_list
        self.result_tr_list=result_tr_list
        self.result_file=result_file
        from Events.Game.move.Game_Map import GameMap
        simple_map=Simple_map(map_size_x,map_size_y,map_resolution,uav_size,hand_size,list_of_cells_with_points,settings)
        self.game_map=GameMap(map_size_x,map_size_y,map_resolution,uav_size,hand_size,list_of_cells_with_points,settings,simple_map)
        self.rand=rand



        for i in range(0, uav_number):
            self.uav_list.append(Uav(0,0,UavStatus.TIER_2,0,v_of_uav,i,0,UavStatus.TIER_2,None,0,0,0,0))
        self.naive_algo=Naive_Algo(settings.naive_algo_list_limit,settings.naive_algo_curiosity_ratio,settings.iterations_for_learning,settings,self.hit_list,self.uav_list,rand,self.result_tr_list,self.result_file)
        #init hands
        self.hands_list:typing.List[Hand] = []
        if(hands_number==1):
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size_x,map_size_y,0,HandStatus.TIER_0,None))
        elif (hands_number==2):
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.RIGHT,map_size_x,map_size_y,0,HandStatus.TIER_0,None))
            self.hands_list.append(Hand(HandStatus.TIER_0,velocity_hand,Sides.LEFT,map_size_x,map_size_y,0,HandStatus.TIER_0,None))
        if settings.load_memory or settings.mode==Modes.EXPLOITATION:
            self.naive_algo.load_memory()
        self.intruder=Intruder(0,0,UavStatus.WAIT,20,20,0,UavStatus.WAIT,Point(0,0,),0)
        logging.info("state initiated")


    def update_postions(self,current_time,uav_velocity,hand_velocity,event_owner,jump_ratio,settings,event_list):





        self.game_map.update_map(self.uav_list,self.hands_list,None)
        for uav in self.uav_list: #uavs to update
            if event_owner!=uav:
                if uav.status!=UavStatus.TIER_2 and uav.status!=UavStatus.DEAD and uav.status!=UavStatus.WAIT:
                    delta_time=current_time-uav.last_postion_update_time
                    distance=delta_time*uav_velocity #distance which was taken during delta
                    if (uav.next_status == UavStatus.TIER_1 and uav.status == UavStatus.TIER_1) or (uav.next_status == UavStatus.DODGE and uav.status == UavStatus.PLANED_DODGE):  # move on circle
                        uav.set_new_position(get_point_on_tier1(uav.position,distance,uav.target_position),current_time)
                    else:
                        uav.set_new_position(get_point_base_on_distance(uav.position, distance, uav.target_position), current_time)



        for hand in self.hands_list:
            if event_owner!=hand:
                if hand.status not in [HandStatus.WAIT,HandStatus.TIER_0,HandStatus.WAIT_AFTER_JUMP]:
                    delta_time=current_time-hand.last_postion_update_time
                    distance=0
                    if hand.status==HandStatus.JUMP:
                        distance=delta_time*hand_velocity*jump_ratio
                    else:
                        distance=delta_time*hand_velocity
                    hand.set_new_position(get_point_base_on_distance(hand.position, distance, hand.target_position), current_time)
        self.check_collisions(settings,event_list,current_time)
        if settings.drone_energy_destroy_condition:
            self.check_energy(event_list)

    def check_energy(self, event_list):
        # check uav energy
        uav_list_to_delete = []
        for uav in self.uav_list:
            if uav.energy < 0:
                uav_list_to_delete.append(uav)
        for uav_to_delete in uav_list_to_delete:
            self.remove_drone(event_list, uav_to_delete)

    def check_collisions(self,settings,event_list,time):
        uav_list_to_delete=[]
        for uav in self.uav_list:
            if uav.position!=None:
                for hand in self.hands_list:
                    if get_2d_distance(uav.position,hand.position)<settings.hand_size+settings.uav_size:

                        uav_list_to_delete.append(uav)

        for uav_to_delete in uav_list_to_delete:
            print("colision!")

            # self.remove_drone(event_list, uav_to_delete)
            event=uav_to_delete.next_event
            event_list.delete_event(uav_to_delete.next_event)
            event.back_on_tier_after_collision(settings,self.rand,event_list,time)



    def remove_drone(self, event_list, uav_to_delete):
        event_list.delete_event(uav_to_delete.next_event)
        for hand in self.hands_list:
            if hand.target_uav == uav_to_delete:
                hand.set_chasing_drone(None)
        self.list_of_dead_uavs.append(uav_to_delete)
        uav_to_delete.set_status(UavStatus.DEAD)
        self.uav_list.remove(uav_to_delete)





