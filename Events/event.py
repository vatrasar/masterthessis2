from random import Random

from Events.Game.GameObjects.movableObject import MovableObject
from Events.Game.settings import Settings


class Event():
    def __init__(self, time_of_event, target_position, event_owner, next_status, last_postion_update_time):
        self.time_of_event=time_of_event
        self.target_position=target_position
        self.event_owner:MovableObject=event_owner
        self.next_status=next_status
        self.last_postion_update_time=last_postion_update_time

    def handle_event(self,event_list,settings:Settings,rand:Random):
        event_list.delete_event(self)
        self.event_owner.next_event=None
        self.event_owner.set_status(self.next_status)
        self.event_owner.set_new_position(self.target_position)


