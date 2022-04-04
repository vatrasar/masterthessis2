from random import random, Random

from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, HandStatus, Sides
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_uav_is_in_range
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_point_based_on_time, get_point_base_on_distance
from Events.Game.move.map_ranges_tools import get_max_hand_range_in_x, get_max_x_in_range
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list
from Events.hand_back import plan_hand_back_event
from Events.jump_event import plan_jump_event, init_jump
from Events.wait import plan_wait


def plan_chase_event(event_owner:Hand,settings,event_list:Event_list,current_time,tk_master,game_state):

    target_uav_pos=event_owner.target_uav.position
    x=get_max_x_in_range(event_owner.side,settings,target_uav_pos.x)
    max_y_hand=get_max_hand_range_in_x(event_owner.side,settings.minimal_hand_range,settings.r_of_LR,settings.map_size_x,x,settings)
    target_y_for_hand=min(max_y_hand,target_uav_pos.y)
    last_point_on_path=Point(x,target_y_for_hand)

    if get_2d_distance(event_owner.position,last_point_on_path)<settings.velocity_hand*settings.intruder_time_of_reaction:#check if hand reach tearget in time shorter then reaction intereval
        target_point=last_point_on_path
        trevel_time=get_travel_time_to_point(event_owner.position,target_point,settings.velocity_hand)
        if trevel_time<settings.minimal_travel_time:
            new_event=Hand_chase(current_time+settings.intruder_time_of_reaction,event_owner,tk_master,event_owner.target_uav,HandStatus.CHASING,target_point,game_state)
            event_list.append_event(new_event,HandStatus.WAIT)

        else:

            time_of_event=trevel_time+current_time
            new_event=Hand_chase(time_of_event,event_owner,tk_master,event_owner.target_uav,HandStatus.CHASING,target_point,game_state)
            event_list.append_event(new_event,HandStatus.CHASING)
    else:
        target_point=get_point_based_on_time(event_owner.position,settings.intruder_time_of_reaction,last_point_on_path,settings.velocity_hand)
        time_of_event=settings.intruder_time_of_reaction+current_time
        new_event=Hand_chase(time_of_event,event_owner,tk_master,event_owner.target_uav,HandStatus.CHASING,target_point,game_state)
        event_list.append_event(new_event,HandStatus.CHASING)
        event_owner.last_postion_update_time=current_time





class Hand_chase(Event):

    def __init__(self, time_of_event, event_owner:Hand, tk_master,target_uav:Uav,next_status:HandStatus,target_postion:Point,game_state):
        super().__init__(time_of_event, event_owner, tk_master,game_state)
        self.event_owner:Hand=event_owner
        self.event_owner.target_uav=target_uav
        self.event_owner.next_status=next_status
        self.event_owner.target_position=target_postion

    def handle_event(self, event_list:Event_list, settings: Settings, rand: Random, iteration_function):
        super().handle_event(event_list, settings, rand, iteration_function)
        if self.event_owner.target_uav.status==UavStatus.TIER_2 or self.event_owner.target_uav.status==UavStatus.DEAD:
            self.event_owner.set_status(HandStatus.TIER_0)
            self.event_owner.stop_chasing()
            self.event_owner.next_event=None
            return

        else:
            if (self.event_owner.target_uav.status in [UavStatus.WAIT,UavStatus.ON_BACK,UavStatus.ON_ATTACK,UavStatus.ATTACK_DODGE_MOVE]) and check_if_uav_is_in_range(self.event_owner.target_uav,self.event_owner,settings):
                if self.event_owner.target_uav.status!=UavStatus.WAIT:
                    init_jump(self.event_owner.target_uav.next_event.old_path,self.event_owner.target_uav.position,settings.v_of_uav,self.event_owner,settings.velocity_hand*settings.jump_ratio,settings,self.time_of_event,self.tk_master,self.game_state,event_list,rand)
                else:
                    init_jump([],self.event_owner.target_uav.position,settings.v_of_uav,self.event_owner,settings.velocity_hand*settings.jump_ratio,settings,self.time_of_event,self.tk_master,self.game_state,event_list,rand)
            else:
                if self.event_owner.target_uav.status in [UavStatus.DEAD, UavStatus.TIER_2]:
                    plan_hand_back_event(event_list,settings,self.event_owner,self.game_state,self.time_of_event,self.tk_master)
                else:
                    plan_chase_event(self.event_owner,settings,event_list,self.time_of_event,self.tk_master,self.game_state)
        # if self.event_owner.target_uav.status==UavStatus.TIER_2 or self.event_owner.target_uav.status==UavStatus.DEAD:
        #     self.event_owner.set_status(HandStatus.BACK)
        # target_uav_pos=self.event_owner.target_uav.position
        # max_y_hand=get_max_hand_range_in_x(settings.minimal_hand_range,settings.minimal_hand_range,settings.map_size,target_uav_pos.x)
        # target_y_for_hand=min(max_y_hand,target_uav_pos.y)
        # last_point_on_path=Point(self.event_owner.target_uav.position.x,target_y_for_hand)
        #
        # if get_2d_distance(self.event_owner.position,last_point_on_path)<settings.velocity_hand*settings.intruder_time_of_reaction:#check if hand reach tearget in time shorter then reaction intereval
        #     target_point=last_point_on_path
        #     trevel_time=get_travel_time_to_point(self.event_owner.position,target_point,settings.velocity_hand)
        #     if trevel_time<settings.minimal_travel_time:
        #         new_event=Hand_chase(self.time_of_event+settings.intruder_time_of_reaction,self.event_owner,self.tk_master,self.event_owner.target_uav,HandStatus.CHASING,target_point)
        #         event_list.append_event(new_event,HandStatus.WAIT)
        #
        #     time_of_event=trevel_time+self.time_of_event
        #     new_event=Hand_chase(time_of_event,self.event_owner,self.tk_master,self.event_owner.target_uav,HandStatus.CHASING,target_point)
        #     event_list.append_event(new_event,HandStatus.CHASING)
        # else:
        #     target_point=get_point_based_on_time(self.event_owner.position,settings.intruder_time_of_reaction,last_point_on_path,settings.velocity_hand)
        #     time_of_event=settings.intruder_time_of_reaction+self.time_of_event
        #     new_event=Hand_chase(time_of_event,self.event_owner,self.tk_master,self.event_owner.target_uav,HandStatus.CHASING,target_point)
        #     event_list.append_event(new_event,HandStatus.CHASING)






