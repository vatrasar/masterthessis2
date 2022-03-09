import typing
from random import Random

from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.FluidCel import FluidCell
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, HandStatus
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_uav_is_in_range
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.find import find_target_for_jump
from Events.Game.move.get_position import get_point_based_on_time
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list



def init_jump(path:typing.List[FluidCell], uav_position, uav_velocity, hand, hand_jump_velocity, settings, current_time, tk_master, game_state, event_list):
    target_point=find_target_for_jump(path, uav_position, hand.position, uav_velocity, hand_jump_velocity,settings,hand)
    if target_point==None:
        from Events.hand_chase import plan_chase_event
        plan_chase_event(hand,settings,event_list,current_time,tk_master,game_state)
    else:
        plan_jump_event(target_point, hand,  settings, current_time, tk_master, game_state, event_list)


def plan_jump_event(target_point, hand, settings:Settings, current_time, tk_master, game_state, event_list):


    jump_velocity=settings.velocity_hand*settings.jump_ratio
    old_target=target_point
    if get_2d_distance(hand.position,target_point)<jump_velocity*settings.intruder_time_of_reaction:#check if hand reach tearget in time shorter then reaction intereval

        trevel_time=get_travel_time_to_point(hand.position,target_point,jump_velocity)
        if trevel_time<settings.minimal_travel_time:
            if hand.status==HandStatus.WAIT_AFTER_JUMP:
                hand.delete_current_event(event_list)
                hand.stop_chasing()
                hand.status=HandStatus.WAIT
            else:
                new_event=Jump_event(current_time+settings.time_to_wait_after_jump,hand,tk_master,hand.target_uav,HandStatus.WAIT_AFTER_JUMP,target_point,game_state,old_target)
                event_list.append_event(new_event,HandStatus.WAIT_AFTER_JUMP)

        else:

            time_of_event=trevel_time+current_time
            new_event=Jump_event(time_of_event,hand,tk_master,hand.target_uav,HandStatus.JUMP,target_point,game_state,old_target)
            event_list.append_event(new_event,HandStatus.JUMP)
    else:
        target_point=get_point_based_on_time(hand.position, settings.intruder_time_of_reaction, target_point, jump_velocity)
        time_of_event=settings.intruder_time_of_reaction+current_time
        new_event=Jump_event(time_of_event,hand,tk_master,hand.target_uav,HandStatus.CHASING,target_point,game_state,old_target)
        event_list.append_event(new_event,HandStatus.JUMP)
        hand.last_postion_update_time=current_time



class Jump_event(Event):

    def __init__(self, time_of_event, event_owner:Hand, tk_master,target_uav:Uav,next_status:HandStatus,target_postion:Point,game_state,old_target):
        super().__init__(time_of_event, event_owner, tk_master,game_state)
        self.event_owner:Hand=event_owner
        self.event_owner.target_uav=target_uav
        self.event_owner.next_status=next_status
        self.event_owner.target_position=target_postion
        self.old_target=old_target

    def handle_event(self, event_list:Event_list, settings: Settings, rand: Random, iteration_function):
        super().handle_event(event_list, settings, rand, iteration_function)
        if self.event_owner.target_uav.status==UavStatus.TIER_2 or self.event_owner.target_uav.status==UavStatus.DEAD:
            self.event_owner.set_status(HandStatus.TIER_0)
            self.event_owner.stop_chasing()
            self.event_owner.next_event=None
            return

        else:
            if (self.event_owner.target_uav.status==UavStatus.ON_ATTACK or self.event_owner.target_uav.status==UavStatus.ON_BACK) and check_if_uav_is_in_range(self.event_owner.target_uav,self.event_owner,settings):
                plan_jump_event(self.old_target,self.event_owner,settings,self.time_of_event,self.tk_master,self.game_state,event_list)
            else:
                from Events.hand_chase import plan_chase_event
                plan_chase_event(self.event_owner,settings,event_list,self.time_of_event,self.tk_master,self.game_state)




