from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.settings import Settings
import tkinter

from Events.move_along import plan_enter_from_tier2
from Events.events_list import Event_list
from Events.visualisation_event import Visualisation_event
from Events.event import Event

class Runner():
    def __init__(self,settings:Settings,rand):
        self.settings=settings
        self.rand=rand
        self.current_time=0
        self.master=None

    def run(self):
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size,self.settings.hands_number)
            self.events_list=Event_list()
            #init uavs events


            if self.settings.visualisation==1:#visualisation

                self.master=tkinter.Tk()
                self.master.title("nazwa okna")
                canvas=tkinter.Canvas(self.master,width=self.settings.map_size,height=self.settings.map_size)
                canvas.pack()
                event_time=self.current_time+self.settings.visualzation_update_interval
                self.game_state.visualisation_owner=MovableObject(0,0,UavStatus.VISUALISE,0,0,0,None,None)
                visualisation_event=Visualisation_event(event_time,self.game_state.visualisation_owner,self.master,canvas,self.game_state)

                self.events_list.append_event(visualisation_event,UavStatus.VISUALISE)
                self.master.after(1,self.single_iteration)


            for uav in self.game_state.uav_list:
                plan_enter_from_tier2(self.events_list,self.settings,self.current_time,uav,self.rand,self.master,self.game_state)

            if self.settings.visualisation==1:#visualisation
                self.master.mainloop()




    def single_iteration(self):

        closest_event:Event=self.events_list.get_closest_event()
        self.current_time=closest_event.time_of_event
        if self.current_time>42:
             print("ok")
        closest_event.handle_event(self.events_list,self.settings,self.rand,self.single_iteration)
        print(self.current_time)



