from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, HandStatus
from Events.Game.move.GameObjects.tools.geometry import get_angle_between_points
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.check import check_if_uav_is_visible
from Events.event import Event
from Events.events_list import Event_list
from Events.hand_chase import plan_chase_event
from Events.jump_event import init_jump


class Hand_control_event(Event):

    def __init__(self, time_of_event, event_owner, tk_master,game_state:GameState):
        super().__init__(time_of_event, event_owner, tk_master,game_state)

    def handle_event(self, event_list, settings: Settings, rand: Random, iteration_function):
        super().handle_event(event_list, settings, rand, iteration_function)
        list_of_uav=[]
        if len(self.game_state.uav_list)>1 and get_angle_between_points(self.game_state.uav_list[0].position,self.game_state.uav_list[1].position,Point(settings.map_size_x/2,0))>settings.blind_angle:
            uav_to_check=self.game_state.uav_list[rand.randint(0,1)]
            list_of_uav.append(uav_to_check)
        else:
            list_of_uav.extend(self.game_state.uav_list)

        for uav in list_of_uav:
            if not(uav.status in [UavStatus.TIER_2 or UavStatus.DEAD]):
                if uav.chasing_hand==None:

                    for hand in self.game_state.hands_list:
                        if hand.target_uav==None and check_if_uav_is_visible(uav,self.game_state):
                            if hand.next_event!=None:
                                hand.delete_current_event(event_list)
                            hand.start_chasing(uav)

                            plan_chase_event(hand,settings,event_list,self.time_of_event,self.tk_master,self.game_state)
                            break

                    if uav.chasing_hand==None and (uav.status in [UavStatus.ON_BACK,UavStatus.ON_ATTACK,UavStatus.ATTACK_DODGE_MOVE,UavStatus.WAIT] ):#there was no free hand but this uav is attacking
                        for hand in self.game_state.hands_list:
                            if check_if_uav_is_visible(uav,self.game_state) and  (hand.target_uav.status not in [UavStatus.ON_ATTACK,UavStatus.ON_BACK,UavStatus.WAIT,UavStatus.ATTACK_DODGE_MOVE]) and hand.status!=HandStatus.WAIT_AFTER_JUMP:
                                hand.delete_current_event(event_list)
                                hand.stop_chasing()
                                hand.start_chasing(uav)

                                plan_chase_event(hand,settings,event_list,self.time_of_event,self.tk_master,self.game_state)
                                break




        plan_hand_control_event(self.time_of_event,settings,self.event_owner,self.tk_master,self.game_state,event_list)



def plan_hand_control_event(current_time,settings,event_owner,tk_master,game_state,event_list:Event_list):
    event=Hand_control_event(current_time+settings.intruder_time_of_reaction,event_owner,tk_master,game_state)
    event_list.append_event(event,UavStatus.WAIT)
