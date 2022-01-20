from random import Random

from Events.Game.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.settings import Settings
from Events.Game.uav_move import decide_whether_uav_attack, decide_whether_uav_back_on_tier2, get_d_t_arrive_poison, \
    get_random_position_on_tier1, choose_travel_direction, get_travel_time_on_tier1
from Events.event import Event




def plan_enter_from_tier2(event_list,settings,current_time,event_owner,rand,master_tk):
    time_of_next_event=get_d_t_arrive_poison(settings.arrive_deterministic,settings.lambda1)+current_time
    target_position=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
    event=Change_tier_event(time_of_next_event, event_owner, master_tk,target_position,UavStatus.TIER_1,current_time,event_owner.position.x)
    event_list.append_event(event,UavStatus.TIER_2)

class Change_tier_event(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,start_time,start_postion):
        super().__init__(time_of_event, event_owner,tk_master)
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.start_time=start_time
        self.start_postion=start_postion


    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)


        if decide_whether_uav_attack(settings.mode,settings.prob_of_attack,rand) and False:
            pass
        else: #no attack
            if decide_whether_uav_back_on_tier2(settings.prob_of_return_to_T2,rand): #back to tier 2
                plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master)
            else:#move on tier 1


                target_postion=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
                self.event_owner.direction=choose_travel_direction()
                event_time=get_travel_time_on_tier1(target_postion,self.event_owner.position,settings.v_of_uav)+self.time_of_event
                event=Change_tier_event(event_time, self.event_owner,self.tk_master,target_postion,UavStatus.TIER_1,self.time_of_event,self.event_owner.position.x)
                event_list.append_event(event,UavStatus.TIER_1)

        if settings.visualisation==1:
            self.tk_master.after(1,iteration_function)



