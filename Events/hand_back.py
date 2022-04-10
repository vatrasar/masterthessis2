from random import Random

from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.algos.tools.enum.enumStatus import HandStatus
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.check import check_if_point_is_reached
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_point_based_on_time
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list

def plan_hand_back_event(event_list, settings,hand,game_state,time_of_event,tk_master):
        tier0_pos=hand.get_hand_tier0_position(hand.side,settings.map_size_x,settings.map_size_y/2.0)
        hand.last_postion_update_time=time_of_event
        if check_if_point_is_reached(settings.velocity_hand, settings.minimal_travel_time, hand.position,
                                     tier0_pos):
            hand.set_status(HandStatus.TIER_0)
            hand.next_status = HandStatus.TIER_0
        elif get_2d_distance(hand.position,
                             tier0_pos) < settings.velocity_hand * settings.intruder_time_of_reaction:  # chack if target in close range
            trevel_time = get_travel_time_to_point(hand.position, tier0_pos, settings.velocity_hand)
            time_of_event = trevel_time + time_of_event
            new_event = Hand_back(time_of_event, hand, tk_master, HandStatus.TIER_0, tier0_pos,
                                  game_state)
            event_list.append_event(new_event, HandStatus.BACK)

        else:
            new_target_point = get_point_based_on_time(hand.position, settings.intruder_time_of_reaction,
                                                       tier0_pos, settings.velocity_hand)
            trevel_time = get_travel_time_to_point(hand.position, new_target_point, settings.velocity_hand)
            time_of_event = trevel_time + time_of_event
            new_event = Hand_back(time_of_event, hand, tk_master, HandStatus.BACK, new_target_point,
                                  game_state)
            event_list.append_event(new_event, HandStatus.BACK)

        # hand.last_postion_update_time=time_of_event


class Hand_back(Event):

    def __init__(self, time_of_event, event_owner:Hand, tk_master,next_status:HandStatus,target_postion:Point,game_state):
        super().__init__(time_of_event, event_owner, tk_master,game_state)

        self.event_owner:Hand=event_owner

        self.event_owner.next_status=next_status
        self.event_owner.target_position=target_postion

    def handle_event(self, event_list:Event_list, settings: Settings, rand: Random, iteration_function):
        super().handle_event(event_list, settings, rand, iteration_function)

        plan_hand_back_event(event_list,settings,self.event_owner,self.game_state,self.time_of_event,self.tk_master)





