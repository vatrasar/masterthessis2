from random import Random
from tkinter import Tk, Canvas

from Events.Game.GameObjects.enum.enumStatus import UavStatus
from Events.Game.GameObjects.point import Point
from Events.Game.settings import Settings
from Events.event import Event
from gui.gui_tools import create_circle


class Visualisation_event(Event):
    def __init__(self, time_of_event, target_position, event_owner, next_status, last_postion_update_time,tk_master:Tk,iteration_function,canvas:Canvas,x):
        super().__init__(time_of_event, target_position, event_owner, next_status, last_postion_update_time)
        self.tk_master=tk_master
        self.canvas=canvas
        self.iteration_function=iteration_function
        self.x_postion=x


    def handle_event(self, event_list, settings: Settings, rand: Random):
        super().handle_event(event_list, settings, rand)
        self.canvas.delete("all")
        event_time=self.time_of_event+settings.visualzation_update_interval
        visualisation_event=Visualisation_event(event_time,Point(0,0),self.event_owner,UavStatus.VISUALISE,event_time,self.tk_master,self.iteration_function,self.canvas,self.x_postion+10)

        event_list.append_event(visualisation_event,UavStatus.VISUALISE)
        create_circle(self.x_postion,40,10,self.canvas)

        self.tk_master.after(1000,self.iteration_function)
        self.canvas.update()
        print("step")
