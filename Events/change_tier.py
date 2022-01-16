from random import Random

from Events.Game.GameObjects.enumStatus import UavStatus
from Events.Game.settings import Settings
from Events.Game.uavMoveTools import decide_whether_uav_attack, decide_whether_uav_back_on_tier2, get_d_t_arrive_poison, \
    get_random_position_on_tier1
from Events.event import Event


class Change_tier(Event):

    def __init__(self, time_of_event, target_position, event_owner, next_status, last_postion_update_time):
        super().__init__(time_of_event, target_position, event_owner, next_status, last_postion_update_time)

    def handle_event(self, event_list,settings:Settings,rand:Random):
        super().handle_event(event_list,settings,rand)


        if self.next_status==UavStatus.TIER_1:#decide what next
            if decide_whether_uav_attack(settings.mode,settings.prob_of_attack,rand):
                pass
            else: #no attack
                if decide_whether_uav_back_on_tier2(settings.prob_of_return_to_T2,rand):#back to tier 2
                    time_of_next_event=get_d_t_arrive_poison(settings.arrive_deterministic,settings.lambda1)+self.time_of_event
                    target_position=get_random_position_on_tier1(rand,settings.map_size,settings.tier1_distance_from_intruder)
                    event=Change_tier(time_of_next_event,target_position,self.event_owner,UavStatus.TIER_1,self.time_of_event)
                    event_list.append_event(event,self.event_owner,UavStatus.TIER_2)
                else:
                    pass

        else


