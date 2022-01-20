from random import Random
from tkinter import Tk, Canvas

from Events.Game.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.GameObjects.tools.point import Point
from Events.Game.gameState import GameState
from Events.Game.settings import Settings
from Events.event import Event
from Events.Game.GameObjects.tools.gui_tools import create_circle, transfer_point_to_gui_format





class Visualisation_event(Event):
    def __init__(self, time_of_event, event_owner, tk_master:Tk,canvas:Canvas,game_state):
        super().__init__(time_of_event, event_owner, tk_master)

        self.canvas=canvas

        self.game_state:GameState=game_state



    def handle_event(self, event_list, settings: Settings, rand: Random,iteration_function):
        super().handle_event(event_list, settings, rand,iteration_function)
        self.canvas.delete("all")
        self.game_state.update_postions(self.time_of_event,settings.v_of_uav,self.event_owner)
        event_time=self.time_of_event+settings.visualzation_update_interval
        visualisation_event=Visualisation_event(event_time, self.event_owner, self.tk_master, self.canvas, self.game_state)
        event_list.append_event(visualisation_event,UavStatus.VISUALISE)

        self.draw_all_elements(settings.uav_size,settings.map_size)


        self.canvas.update()
        print("ok")
        if settings.visualisation==1:
            self.tk_master.after(100,iteration_function)



    def draw_all_elements(self,uav_size,map_size):
        for uav in self.game_state.uav_list:
            if uav.status!=UavStatus.DEAD and uav.status!=UavStatus.TIER_2:
                transfered_position=transfer_point_to_gui_format(uav.position,map_size)
                create_circle(transfered_position.x, transfered_position.y,uav_size,self.canvas)

