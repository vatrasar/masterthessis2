from Events.Game.Statistics import Statistics
from Events.Game.move.GameObjects.algos.naive_algo import Naive_Algo
from Events.Game.move.GameObjects.algos.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.algos.tools.settings import Settings
import tkinter

from Events.Game.move.get_position import get_random_position_between_tier1_and_0, get_random_position_on_tier1
from Events.Game.move.map_ranges_tools import get_max_hand_range_in_x
from Events.Game.move.time import get_d_t_arrive_poison
from Events.hand_chase import plan_chase_event
from Events.hand_control_event import plan_hand_control_event
from Events.move_along import plan_enter_from_tier2
from Events.events_list import Event_list
from Events.visualisation_event import Visualisation_event
from Events.event import Event
from Events.wait import plan_wait


class Runner():
    def __init__(self,settings:Settings,rand,statistics:Statistics):
        self.settings=settings
        self.rand=rand
        self.current_time=0
        self.master=None
        self.statistics=statistics




    def run_normal(self):
            naive_alog=Naive_Algo(self.settings.naive_algo_list_limit,self.settings.naive_algo_curiosity_ratio)
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size_x,self.settings.map_size_y,self.settings.hands_number,self.settings.map_resolution,self.settings.uav_size,self.settings.hand_size,self.settings.list_of_cell_points,self.settings,naive_alog)
            self.game_state.game_map.update_map(self.game_state,None)
            self.events_list=Event_list()
            #init uavs events


            if self.settings.visualisation==1:#visualisation

                self.setup_visualisation()



            for uav in self.game_state.uav_list:
                plan_enter_from_tier2(self.events_list,self.settings,self.current_time,uav,self.rand,self.master,self.game_state,self.settings.safe_margin)

            if self.settings.mode_debug==2:
                self.setup_debug2(self.events_list)

            if self.settings.mode_debug!=3:
                plan_hand_control_event(self.current_time+get_d_t_arrive_poison(self.settings.arrive_deterministic,self.settings.lambda1,self.rand),self.settings,self.game_state.intruder,self.master,self.game_state,self.events_list)

            if self.settings.visualisation==1:#visualisation
                self.master.after(1, self.single_iteration)
                self.master.mainloop()
            else:
                while self.current_time<=self.settings.T:
                    self.single_iteration()

    def setup_visualisation(self):
        self.master = tkinter.Tk()
        self.master.title("nazwa okna")
        canvas = tkinter.Canvas(self.master, width=self.settings.map_size_x, height=self.settings.map_size_y)
        canvas.pack()
        event_time = self.current_time + self.settings.visualzation_update_interval
        self.game_state.visualisation_owner = MovableObject(0, 0, UavStatus.VISUALISE, 0, 0, 0, None, None)
        visualisation_event = Visualisation_event(event_time, self.game_state.visualisation_owner, self.master, canvas,
                                                  self.game_state,self.settings.visualisation_speed)
        self.events_list.append_event(visualisation_event, UavStatus.VISUALISE)

    def single_iteration(self):

        closest_event:Event=self.events_list.get_closest_event()

        update_stac_step=1
        self.current_time=closest_event.time_of_event
        self.game_state.t_curr=self.current_time
        if self.current_time>=138.22:
             print("ok")
        # if len(self.events_list.event_list)>5:
        #      print("ok")
        closest_event.handle_event(self.events_list,self.settings,self.rand,self.single_iteration)
        if self.current_time-update_stac_step>0:
            update_stac_step=update_stac_step+1
            self.statistics.update_stac(self.game_state,self.settings)
        print(self.current_time)

        if self.current_time>self.settings.T:
            if self.settings.visualisation==1:
                self.master.quit()
            self.statistics.save()

    def setup_debug2(self,event_list):
        for uav in self.game_state.uav_list:

            uav.delete_current_event(self.events_list)
            for hand in self.game_state.hands_list:
                if hand.target_uav==None:
                    hand.start_chasing(uav)
                    break


            # x=(self.settings.map_size_x)*self.rand.random()
            # y=(get_max_hand_range_in_x(uav.chasing_hand.side,self.settings.minimal_hand_range,self.settings.r_of_LR,self.settings.map_size_x,x)-self.settings.intuder_size)*self.rand.random()+self.settings.intuder_size
            # uav.position=Point(x,y)
            rand_pos=get_random_position_on_tier1(self.rand,self.settings.map_size_x,self.settings.tier1_distance_from_intruder)
            uav.position=get_random_position_between_tier1_and_0(self.settings.map_size_x,get_max_hand_range_in_x(uav.chasing_hand.side,self.settings.minimal_hand_range,self.settings.r_of_LR,self.settings.map_size_x,rand_pos.x,self.settings),self.settings.intuder_size,self.rand,rand_pos.x)
            plan_wait(0,20000,uav, self.master,self.game_state,event_list,self.settings.safe_margin)
            plan_chase_event(uav.chasing_hand,self.settings,event_list,0,self.master,self.game_state)




