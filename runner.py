from Events.Game.Statistics import Statistics
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.settings import Settings
import tkinter

from Events.hand_control_event import plan_hand_control_event
from Events.move_along import plan_enter_from_tier2
from Events.events_list import Event_list
from Events.visualisation_event import Visualisation_event
from Events.event import Event

class Runner():
    def __init__(self,settings:Settings,rand,statistics:Statistics):
        self.settings=settings
        self.rand=rand
        self.current_time=0
        self.master=None
        self.statistics=statistics



    def run(self):
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size_x,self.settings.map_size_y,self.settings.hands_number,self.settings.map_resolution,self.settings.uav_size,self.settings.hand_size,self.settings.list_of_cell_points)
            self.game_state.game_map.update_map(self.game_state,None)
            self.events_list=Event_list()
            #init uavs events


            if self.settings.visualisation==1:#visualisation

                self.master=tkinter.Tk()
                self.master.title("nazwa okna")
                canvas=tkinter.Canvas(self.master,width=self.settings.map_size_x,height=self.settings.map_size_y)
                canvas.pack()
                event_time=self.current_time+self.settings.visualzation_update_interval
                self.game_state.visualisation_owner=MovableObject(0,0,UavStatus.VISUALISE,0,0,0,None,None)
                visualisation_event=Visualisation_event(event_time,self.game_state.visualisation_owner,self.master,canvas,self.game_state)

                self.events_list.append_event(visualisation_event,UavStatus.VISUALISE)
                self.master.after(1,self.single_iteration)


            for uav in self.game_state.uav_list:
                plan_enter_from_tier2(self.events_list,self.settings,self.current_time,uav,self.rand,self.master,self.game_state,self.settings.safe_margin)

            plan_hand_control_event(self.current_time,self.settings,self.game_state.intruder,self.master,self.game_state,self.events_list)
            if self.settings.visualisation==1:#visualisation
                self.master.mainloop()




    def single_iteration(self):

        closest_event:Event=self.events_list.get_closest_event()
        update_stac_step=1
        self.current_time=closest_event.time_of_event
        self.game_state.t_curr=self.current_time
        if self.current_time>58.5:
             print("ok")
        closest_event.handle_event(self.events_list,self.settings,self.rand,self.single_iteration)
        if self.current_time-update_stac_step>0:
            update_stac_step=update_stac_step+1
            self.statistics.update_stac(self.game_state,self.settings)
        print(self.current_time)

        if self.current_time==1000:
            self.master.quit()
            self.statistics.save()





