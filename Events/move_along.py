from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.check import check_distance_between_uav, check_if_same_move_direction, check_if_in_safe_distance
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus

from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.collisions import check_colisions
from Events.Game.move.decisions import decide_whether_uav_attack, decide_whether_uav_back_on_tier2
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.path_planning import search_attack_patch
from Events.Game.move.time import get_d_t_arrive_poison, get_travel_time_on_tier1
from Events.attack import plan_attack

from Events.event import Event
from Events.make_dodge import Make_dodge


def plan_enter_from_tier2(event_list,settings,current_time,event_owner,rand,master_tk,state,safe_margin):
    time_of_next_event=get_d_t_arrive_poison(settings.arrive_deterministic,settings.lambda1,rand)+current_time
    target_position=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
    event=Move_along(time_of_next_event, event_owner, master_tk, target_position, UavStatus.TIER_1, state,safe_margin)
    event_list.append_event(event,UavStatus.TIER_2)



def plan_move_along(event_list, event_owner, target_postion, current_time, game_state, settings, tk_master,safe_margin):
    is_colision,start_dodge_postion,dodge_position=check_colisions(event_owner,game_state.uav_list,target_postion,settings.dodge_radius,settings.save_distance)
    if is_colision:
        event_time= get_travel_time_on_tier1(start_dodge_postion,event_owner.position,settings.v_of_uav) + current_time
        event=Make_dodge(event_time, event_owner, tk_master, start_dodge_postion, UavStatus.PLANED_DODGE,target_postion,dodge_position,game_state,safe_margin)
        event_list.append_event(event,UavStatus.PLANED_DODGE)
    else:
        event_time= get_travel_time_on_tier1(target_postion,event_owner.position,settings.v_of_uav) + current_time
        event=Move_along(event_time, event_owner, tk_master, target_postion, UavStatus.TIER_1,game_state,safe_margin)
        event_list.append_event(event,UavStatus.TIER_1)

class Move_along(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state,safe_margin):
        super().__init__(time_of_event, event_owner,tk_master,state)
        self.safe_margin = safe_margin

        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state



    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)

        self.state.update_postions(self.time_of_event,settings.v_of_uav,settings.velocity_hand,self.event_owner,settings.jump_ratio,settings,event_list)

        if decide_whether_uav_attack(settings.mode,settings.prob_of_attack,rand) and check_if_in_safe_distance(self.event_owner,self.state.hands_list,self.safe_margin):#if true then attack
            path=search_attack_patch(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings,self.game_state.hands_list)
            if path!=None:
                plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_ATTACK,settings.safe_margin)
                return



        #no attack
        if decide_whether_uav_back_on_tier2(settings.prob_of_return_to_T2,rand,self.state.uav_list,settings.dodge_radius): #back to tier 2
            plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.state,self.safe_margin)
        else:#move on tier 1

            counter=0
            target_postion=None
            while(True):
                counter=counter+1
                if counter>10:
                    plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.state,self.safe_margin)
                    return
                target_postion=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
                if check_distance_between_uav(self.state.uav_list,settings.save_distance)==False and check_if_same_move_direction(self.event_owner,self.state.uav_list,target_postion):
                    continue
                else:
                    break

            plan_move_along(event_list,self.event_owner,target_postion,self.time_of_event,self.game_state,settings,self.tk_master,self.safe_margin)
