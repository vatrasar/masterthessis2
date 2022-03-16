from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_path_save, check_is_horizontal_distance_form_hands_safe
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.path_planning import search_back_path, search_attack_patch
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list
from Events.wait import plan_wait


def plan_attack(current_time, event_owner,tk_master,path,v_of_uav,game_state,event_list:Event_list,status,safe_margin):
    if len(path)==2:
        print("plan_attack")
    target_position=path[1].position
    dt_arrive=get_travel_time_to_point(event_owner.position,target_position,v_of_uav)
    event_time=dt_arrive+current_time
    new_event=Attack(event_time,event_owner,tk_master,target_position,status,game_state,path[1:],safe_margin)
    event_list.append_event(new_event,status)





class Attack(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state,path,safe_margin):
        super().__init__(time_of_event, event_owner,tk_master,state)
        self.safe_margin = safe_margin
        self.old_path=path
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state


    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)
        if len(self.old_path)>=2:
            if check_if_path_save(self.old_path,self.event_owner,self.event_owner.chasing_hand,settings,self.game_state.hands_list):
                plan_attack(self.time_of_event,self.event_owner,self.tk_master,self.old_path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin)
            else:

                attack_path_found=False
                if self.event_owner.status==UavStatus.ON_ATTACK and check_is_horizontal_distance_form_hands_safe(self.state.hands_list, self.event_owner, settings.safe_margin):
                    path=search_attack_patch(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings,self.game_state.hands_list)
                    if path!=None:
                        attack_path_found=True
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin)
                    else:
                        attack_path_found=False

                if attack_path_found==False or self.event_owner.status==UavStatus.ON_BACK:
                    path=search_back_path(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings.tier1_distance_from_intruder,settings,self.game_state.hands_list)
                    if path!=None:
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_BACK,settings.safe_margin)
                        return
                    else:
                        plan_wait(self.time_of_event,settings.uav_wait_time,self.event_owner,self.tk_master,self.game_state,event_list,self.safe_margin)



        else:#target reached
            if self.event_owner.status==UavStatus.ON_ATTACK:
                #asign points
                uav:Uav=self.event_owner

                uav.asign_points(self.old_path[0].points)

                #plan to back
                path=search_back_path(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings.tier1_distance_from_intruder,settings,self.game_state.hands_list)
                if path!=None:
                    plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_BACK,settings.safe_margin)
                    return
                else:
                    plan_wait(self.time_of_event,settings.uav_wait_time,self.event_owner,self.tk_master,self.game_state,event_list,self.safe_margin)

            elif self.event_owner.status==UavStatus.ON_BACK:
                target_postion=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
                from Events.move_along import plan_move_along
                plan_move_along(event_list,self.event_owner,target_postion,self.time_of_event,self.game_state,settings,self.tk_master,self.safe_margin)




