from random import Random

from Events.Game.Statistics import Statistics
from Events.Game.gnuplot import export_to_gnuplot
from Events.Game.move.algos.GameObjects.data_lists.Debug import Debug_file
from Events.Game.move.algos.GameObjects.data_lists.Hit_list import Hit_list
from Events.Game.move.algos.GameObjects.data_lists.all_results import Result_tr_list
from Events.Game.move.algos.GameObjects.data_lists.result import Result_file
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import UavStatus, Sides
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_stop_reasons import Reason_to_stop
from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
from Events.Game.move.algos.GameObjects.movableObject import MovableObject
from Events.Game.gameState import GameState
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import tkinter

from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.get_position import get_random_position_between_tier1_and_0, get_random_position_on_tier1, \
    get_random_postion_x_in_hand_range
from Events.Game.move.algos.GameObjects.data_lists.tools.map_ranges_tools import get_max_hand_range_in_x
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
        self.rand:Random=rand
        self.current_time=0
        self.master=None
        self.statistics=statistics
        self.run_stac_list=[]
        self.run_hits=[]
        self.memory_list=[]
        self.reason_to_stop_simulation=[]
        self.debug_file=Debug_file(settings)



    def run_multirun(self):
        self.hit_list=Hit_list(self.settings)
        self.result_tr_list=Result_tr_list(self.settings)
        self.result_file=Result_file(self.settings)
        for i in range(0,self.settings.number_of_runs):

            seed_for_run=self.rand.randint(0,100000000)
            rand_for_run=Random(seed_for_run)
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size_x,self.settings.map_size_y,self.settings.hands_number,self.settings.map_resolution,self.settings.uav_size,self.settings.hand_size,self.settings.list_of_cell_points,self.settings,self.settings,rand_for_run,self.hit_list,self.result_tr_list,self.result_file)

            self.game_state.game_map.update_map(self.game_state.uav_list,self.game_state.hands_list,None)
            self.events_list=Event_list()
            for uav in self.game_state.uav_list:
                plan_enter_from_tier2(self.events_list,self.settings,self.current_time,uav,rand_for_run,self.master,self.game_state,self.settings.safe_margin)


            event_time=self.settings.visualzation_update_interval
            self.game_state.visualisation_owner = MovableObject(0, 0, UavStatus.VISUALISE, 0, 0, 0, None, None)
            visualisation_event = Visualisation_event(event_time, self.game_state.visualisation_owner, self.master, None,
                                              self.game_state,self.settings.visualisation_speed)
            self.events_list.append_event(visualisation_event, UavStatus.VISUALISE)
            while self.perform_singel_iteration(rand_for_run):

                continue
            self.result_tr_list.end_run()
            self.result_file.end_run()
            self.memory_list.append(self.game_state.naive_algo.results_list)
            self.hit_list=Hit_list(self.settings)
            self.current_time=0

        # export_to_gnuplot(self.run_stac_list,self.run_hits,self.settings)

        self.statistics.save()
        clear_folder("./results")
        self.hit_list.save_to_file(self.run_hits,self.reason_to_stop_simulation)
        self.game_state.naive_algo.results_list.save_to_file(self.memory_list)
        if self.settings.mode==Modes.LEARNING:
            self.result_tr_list.save_to_file(self.settings)
            self.result_tr_list.save_to_file_uav1(self.settings)
        else:
            self.result_file.save_to_file2(self.settings)
            self.result_file.save_to_file1(self.settings)

        self.debug_file.save_to_file(self.settings)





    def run_normal(self):
            self.hit_list=Hit_list(self.settings)
            self.result_tr_list=Result_tr_list(self.settings)
            self.result_file=Result_file(self.settings)
            self.game_state=GameState(self.settings.uav_number,self.settings.v_of_uav,self.settings.velocity_hand,self.settings.map_size_x,self.settings.map_size_y,self.settings.hands_number,self.settings.map_resolution,self.settings.uav_size,self.settings.hand_size,self.settings.list_of_cell_points,self.settings,self.settings,self.rand,self.hit_list,self.result_tr_list,self.result_file)


            self.game_state.game_map.update_map(self.game_state.uav_list,self.game_state.hands_list,None)
            self.events_list=Event_list()



            if self.settings.visualisation in [1,2]:#visualisation

                self.setup_visualisation()
            else:
                event_time=self.settings.visualzation_update_interval
                self.game_state.visualisation_owner = MovableObject(0, 0, UavStatus.VISUALISE, 0, 0, 0, None, None)
                visualisation_event = Visualisation_event(event_time, self.game_state.visualisation_owner, self.master, None,
                                                  self.game_state,self.settings.visualisation_speed)
                self.events_list.append_event(visualisation_event, UavStatus.VISUALISE)

            #init uavs events
            for uav in self.game_state.uav_list:
                plan_enter_from_tier2(self.events_list,self.settings,self.current_time,uav,self.rand,self.master,self.game_state,self.settings.safe_margin)

            if self.settings.mode_debug=="12":
                self.setup_debug2(self.events_list)

            if self.settings.mode_debug!="13":
                plan_hand_control_event(self.current_time+get_d_t_arrive_poison(self.rand),self.settings,self.game_state.intruder,self.master,self.game_state,self.events_list)

            if self.settings.visualisation in [1,2]:#visualisation
                self.master.after(1, self.single_iteration)
                self.master.mainloop()
            else:
                while self.perform_singel_iteration(self.rand):
                    continue
            self.result_tr_list.end_run()
            self.result_file.end_run()
            self.memory_list.append(self.game_state.naive_algo.results_list)
            self.hit_list=Hit_list(self.settings)
            export_to_gnuplot(self.run_stac_list,self.run_hits,self.settings)
            self.statistics.save()
            clear_folder("./results")
            self.hit_list.save_to_file(self.run_hits,self.reason_to_stop_simulation)
            self.game_state.naive_algo.results_list.save_to_file(self.memory_list)
            if self.settings.mode==Modes.LEARNING:
                self.result_tr_list.save_to_file(self.settings)
                self.result_tr_list.save_to_file_uav1(self.settings)
            else:
                self.result_file.save_to_file2(self.settings)
                self.result_file.save_to_file1(self.settings)

            self.debug_file.save_to_file(self.settings)






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

        return self.perform_singel_iteration(self.rand)

    def perform_singel_iteration(self, rand):

        closest_event: Event = self.events_list.get_closest_event()
        update_stac_step = 1
        self.current_time = closest_event.time_of_event
        # if self.current_time>2000:
        #     print("test")
        self.game_state.t_curr = self.current_time
        # if self.current_time>550.5:
        #      print("ok")
        # # if len(self.events_list.event_list)>5:
        # #      print("ok")
        # if len(self.events_list.event_list)<6:
        #     print("test")
        closest_event.handle_event(self.events_list, self.settings, rand, self.single_iteration)
        if self.current_time%1==0:

            self.statistics.update_stac(self.game_state, self.settings)
        print(self.current_time)



        if self.is_simulation_finished():
            self.run_stac_list.append(self.statistics)
            self.run_hits.append(self.game_state.hit_list)
            if self.settings.is_multirun:

                self.statistics = Statistics(self.settings)
                return False
            if self.settings.visualisation in [1, 2]:

                self.master.quit()


            return False

        return True


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
            x=get_random_postion_x_in_hand_range(uav,self.settings,self.rand)

            uav.position=get_random_position_between_tier1_and_0(self.settings.map_size_x,get_max_hand_range_in_x(uav.chasing_hand.side,self.settings.minimal_hand_range,self.settings.r_of_LR,self.settings.map_size_x,x,self.settings),self.settings.intuder_size,self.rand,x)
            plan_wait(0,20000,uav, self.master,self.game_state,event_list,self.settings.safe_margin)
            plan_chase_event(uav.chasing_hand,self.settings,event_list,0,self.master,self.game_state)

    def is_simulation_finished(self):
        if len(self.game_state.uav_list)<2:
            self.reason_to_stop_simulation.append(Reason_to_stop.ONE_UAV_KILLED)
            return True

        if self.current_time>self.settings.T:
            self.reason_to_stop_simulation.append(Reason_to_stop.TIME)
            return True
        sum_of_points = 0
        for uav in self.game_state.uav_list:

            sum_of_points=uav.points+sum_of_points

        if self.settings.number_of_points_to_win<sum_of_points:
            self.reason_to_stop_simulation.append(Reason_to_stop.POINTS_LIMIT)
            return True

        # if self.game_state.naive_algo.iteration_number>self.game_state.naive_algo.iterations_for_learning:
        #     self.game_state.naive_algo.reason_why_learning_stoped=Reason_to_stop.ITERATIONS
        #     self.reason_to_stop_simulation.append(self.game_state.naive_algo.reason_why_learning_stoped)
        #     return True
        if self.settings.mode==Modes.EXPLOITATION:
            if self.settings.energy_simulation_end_condition==True:
                for uav in self.game_state.uav_list:
                    if uav.energy>self.settings.uav_energy:
                        self.reason_to_stop_simulation.append(Reason_to_stop.ENERGY)
                        return True
                if self.game_state.intruder.energy>self.settings.intruder_max_energy:
                        self.reason_to_stop_simulation.append(Reason_to_stop.ENERGY)
                        return True
        if self.settings.mode==Modes.LEARNING:

            if self.game_state.naive_algo.is_learning_finished():
                self.reason_to_stop_simulation.append(self.game_state.naive_algo.reason_why_learning_stoped)
                return True
        return False
        # if (self.game_state.intruder.energy<0 and self.settings.energy_simulation_end_condition):



