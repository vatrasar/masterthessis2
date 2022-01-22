from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.check import check_distance_between_uav, check_if_same_move_direction
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus

from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.collisions import check_colisions
from Events.Game.move.decisions import decide_whether_uav_attack, decide_whether_uav_back_on_tier2
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.time import get_d_t_arrive_poison, get_travel_time_on_tier1

from Events.event import Event
from Events.make_dodge import Make_dodge


def plan_enter_from_tier2(event_list,settings,current_time,event_owner,rand,master_tk,state):
    time_of_next_event=get_d_t_arrive_poison(settings.arrive_deterministic,settings.lambda1)+current_time
    target_position=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
    event=Move_along(time_of_next_event, event_owner, master_tk, target_position, UavStatus.TIER_1, state)
    event_list.append_event(event,UavStatus.TIER_2)

class Move_along(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state):
        super().__init__(time_of_event, event_owner,tk_master)
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state



    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)
        self.state.update_postions(self.time_of_event,settings.v_of_uav,self.event_owner)

        if decide_whether_uav_attack(settings.mode,settings.prob_of_attack,rand) and False:
            pass
        else: #no attack
            if decide_whether_uav_back_on_tier2(settings.prob_of_return_to_T2,rand,self.state.uav_list,settings.dodge_radius): #back to tier 2
                plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.state)
            else:#move on tier 1

                counter=0
                target_postion=None
                while(True):
                    counter=counter+1
                    if counter>10:
                        plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.state)
                        return
                    target_postion=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
                    if check_distance_between_uav(self.state.uav_list,settings.save_distance)==False and check_if_same_move_direction(self.event_owner,self.state.uav_list,target_postion):
                        continue
                    else:
                        break


                is_colision,start_dodge_postion,dodge_position=check_colisions(self.event_owner,self.state.uav_list,target_postion,settings.dodge_radius,settings.save_distance)
                if is_colision:
                    event_time=get_travel_time_on_tier1(start_dodge_postion,self.event_owner.position,settings.v_of_uav)+self.time_of_event
                    event=Make_dodge(event_time, self.event_owner, self.tk_master, start_dodge_postion, UavStatus.PLANED_DODGE,target_postion,dodge_position,self.state)
                    event_list.append_event(event,UavStatus.PLANED_DODGE)
                else:
                    event_time=get_travel_time_on_tier1(target_postion,self.event_owner.position,settings.v_of_uav)+self.time_of_event
                    event=Move_along(event_time, self.event_owner, self.tk_master, target_postion, UavStatus.TIER_1,self.state)
                    event_list.append_event(event,UavStatus.TIER_1)





