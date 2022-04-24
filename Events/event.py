from random import Random

from Events.Game.gameState import GameState
from Events.Game.move.algos.GameObjects.movableObject import MovableObject
from Events.Game.move.algos.GameObjects.tools.settings import Settings


class Event():
    def __init__(self, time_of_event, event_owner,tk_master,game_state):
        self.time_of_event=time_of_event

        self.event_owner:MovableObject=event_owner
        self.visualisation_delay=1
        self.game_state:GameState=game_state
        self.tk_master=tk_master

    def handle_event(self,event_list,settings:Settings,rand:Random,iteration_function):
        self.event_owner.delete_current_event(event_list)

        self.event_owner.set_status(self.event_owner.next_status)
        self.event_owner.set_new_position(self.event_owner.target_position,self.time_of_event)
        if settings.visualisation in [1,2] and not settings.is_multirun:
            self.tk_master.after(self.visualisation_delay,iteration_function)





