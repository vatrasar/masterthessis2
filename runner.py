from Events.Game.GameObjects.enum.enumStatus import UavStatus
from Events.Game.GameObjects.movableObject import MovableObject
from Events.Game.GameObjects.point import Point
from Events.Game.gameState import GameState
from Events.Game.settings import Settings
import tkinter

from Events.events_list import Event_list
from Events.visualisation_event import Visualisation_event
from Events.event import Event

class Runner():
    def __init__(self,settings:Settings,rand):
        self.settings=settings
        self.rand=rand
        self.current_time=0

    def run(self):
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size,self.settings.hands_number)
            self.events_list=Event_list()
            if self.settings.visualisation==1:

                master=tkinter.Tk()
                master.title("nazwa okna")
                canvas=tkinter.Canvas(master,width=200,height=200)
                canvas.pack()
                event_time=self.current_time+self.settings.visualzation_update_interval
                self.game_state.visualisation_owner=MovableObject(0,0,UavStatus.VISUALISE,0,0)
                visualisation_event=Visualisation_event(event_time,Point(0,0),self.game_state.visualisation_owner,UavStatus.VISUALISE,self.current_time,master,self.single_iteration,canvas,10)

                self.events_list.append_event(visualisation_event,UavStatus.VISUALISE)
                master.after(1,self.single_iteration)
                master.mainloop()



    def single_iteration(self):

        closest_event:Event=self.events_list.get_closest_event()
        closest_event.handle_event(self.events_list,self.settings,self.rand)



