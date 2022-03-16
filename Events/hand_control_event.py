from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, HandStatus
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.event import Event
from Events.events_list import Event_list
from Events.hand_chase import plan_chase_event
from Events.jump_event import init_jump


class Hand_control_event(Event):

    def __init__(self, time_of_event, event_owner, tk_master,game_state:GameState):
        super().__init__(time_of_event, event_owner, tk_master,game_state)

    def handle_event(self, event_list, settings: Settings, rand: Random, iteration_function):
        super().handle_event(event_list, settings, rand, iteration_function)


        for uav in self.game_state.uav_list:
            if not(uav.status in [UavStatus.TIER_2 or UavStatus.DEAD]):
                if uav.chasing_hand==None:

                    for hand in self.game_state.hands_list:
                        if hand.target_uav==None:
                            hand.start_chasing(uav)
                            if uav.status in [UavStatus.ON_ATTACK,UavStatus.ON_BACK]:
                                init_jump(uav.next_event.old_path,uav.position,settings.v_of_uav,hand,settings.velocity_hand*settings.jump_ratio,settings,self.time_of_event,self.tk_master,self.game_state,event_list)
                            else:
                                plan_chase_event(hand,settings,event_list,self.time_of_event,self.tk_master,self.game_state)
                            break

                    if uav.chasing_hand==None and (uav.status in [UavStatus.ON_ATTACK,UavStatus.ON_BACK] ):#there was no free hand but this uav is attacking
                        for hand in self.game_state.hands_list:
                            if hand.target_uav.status not in [UavStatus.ON_ATTACK,UavStatus.ON_BACK,UavStatus.WAIT] and hand.status!=HandStatus.WAIT_AFTER_JUMP:
                                hand.delete_current_event(event_list)
                                hand.stop_chasing()
                                hand.start_chasing(uav)

                                init_jump(uav.next_event.old_path,uav.position,settings.v_of_uav,hand,settings.velocity_hand*settings.jump_ratio,settings,self.time_of_event,self.tk_master,self.game_state,event_list)
                                break




        plan_hand_control_event(self.time_of_event,settings,self.event_owner,self.tk_master,self.game_state,event_list)



def plan_hand_control_event(current_time,settings,event_owner,tk_master,game_state,event_list:Event_list):
    event=Hand_control_event(current_time+settings.intruder_time_of_reaction,event_owner,tk_master,game_state)
    event_list.append_event(event,UavStatus.WAIT)
