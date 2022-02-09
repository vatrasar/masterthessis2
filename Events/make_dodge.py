from random import Random

from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus

from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.time import get_travel_time_to_point, get_travel_time_on_tier1
from Events.event import Event
from Events.events_list import Event_list



class Make_dodge(Event):
    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,old_target,new_target,game_state):
        super().__init__(time_of_event, event_owner,tk_master,game_state)
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status


        self.old_target=old_target
        self.new_target=new_target

    def handle_event(self, event_list:Event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)

        if self.event_owner.status==UavStatus.DODGE:
            new_target=Point(self.event_owner.position.x-settings.dodge_radius,settings.tier1_distance_from_intruder)
            if self.event_owner.position.x>self.old_target.x:# in old target i save init postion where uav start dodge
                new_target=Point(self.event_owner.position.x+settings.dodge_radius,settings.tier1_distance_from_intruder)

            if new_target.x> settings.map_size_x:
                new_target.x=settings.map_size_x

            if new_target.x<0:
                new_target.x=0
            event_time=get_travel_time_to_point(self.event_owner.position,new_target,settings.v_of_uav)+self.time_of_event

            event=Make_dodge(event_time,self.event_owner,self.tk_master,new_target,UavStatus.BACK_FROM_DODGE,self.old_target,None,self.game_state)
            event_list.append_event(event,UavStatus.BACK_FROM_DODGE)

        elif self.event_owner.status==UavStatus.PLANED_DODGE:
            event_time=get_travel_time_to_point(self.event_owner.position,self.new_target,settings.v_of_uav)+self.time_of_event

            event=Make_dodge(event_time,self.event_owner,self.tk_master,self.new_target,UavStatus.DODGE,self.event_owner.position,self.old_target,self.game_state)
            event_list.append_event(event,UavStatus.DODGE)
        else:#backed form DODGE,bakcing to normal status

                target_postion=self.old_target

                event_time=get_travel_time_on_tier1(target_postion,self.event_owner.position,settings.v_of_uav)+self.time_of_event
                from Events.move_along import plan_move_along
                plan_move_along(event_list,self.event_owner,target_postion,self.time_of_event,self.game_state,settings,self.tk_master)

