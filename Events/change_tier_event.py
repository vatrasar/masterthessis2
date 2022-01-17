from random import Random

from Events.Game.GameObjects.enum.enumStatus import UavStatus
from Events.Game.settings import Settings
from Events.Game.uav_move import decide_whether_uav_attack, decide_whether_uav_back_on_tier2, get_d_t_arrive_poison, \
    get_random_position_on_tier1, choose_travel_direction, get_travel_time_on_tier1
from Events.event import Event




class Change_tier_event(Event):

    def __init__(self, time_of_event, target_position, event_owner, next_status, last_postion_update_time):
        super().__init__(time_of_event, target_position, event_owner, next_status, last_postion_update_time)

    def handle_event(self, event_list,settings:Settings,rand:Random):
        super().handle_event(event_list,settings,rand)


        if decide_whether_uav_attack(settings.mode,settings.prob_of_attack,rand) and False:
            pass
        else: #no attack
            if decide_whether_uav_back_on_tier2(settings.prob_of_return_to_T2,rand): #back to tier 2
                time_of_next_event=get_d_t_arrive_poison(settings.arrive_deterministic,settings.lambda1)+self.time_of_event
                target_position=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
                event=Change_tier_event(time_of_next_event, target_position, self.event_owner, UavStatus.TIER_1, self.time_of_event)
                event_list.append_event(event,UavStatus.TIER_2)
            else:#move on tier 1


                target_postion=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
                direction=choose_travel_direction()
                event_time=get_travel_time_on_tier1(target_postion,direction,self.event_owner.position,settings.v_of_uav,settings.map_size)+self.time_of_event
                event=Change_tier_event(event_time, target_postion, self.event_owner, UavStatus.TIER_1, self.time_of_event)
                event_list.append_event(event,UavStatus.TIER_1)



