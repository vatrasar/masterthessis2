from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.path_planning import search_back_path
from Events.Game.move.time import get_travel_time_to_point

from Events.event import Event
from Events.events_list import Event_list


def plan_wait(current_time,uav_wait_time, event_owner,tk_master,game_state,event_list:Event_list,safe_margin):

    target_position=event_owner.position

    event_time=current_time+uav_wait_time
    new_event=Wait(event_time,event_owner,tk_master,target_position,UavStatus.WAIT,game_state,safe_margin,uav_wait_time)
    event_list.append_event(new_event,UavStatus.ON_BACK)

class Wait(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state,safe_margin,uav_wait_time):
        super().__init__(time_of_event, event_owner,tk_master,state)
        self.uav_wait_time = uav_wait_time

        self.safe_margin = safe_margin

        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state


    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)

        #plan to back
        path=search_back_path(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings.tier1_distance_from_intruder)
        if path!=None:
            from Events.attack import plan_attack
            plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_BACK,settings.safe_margin)
            return
        else:
            plan_wait(self.time_of_event,self.uav_wait_time,self.event_owner,self.tk_master,self.game_state,event_list,self.safe_margin)
