import math
from random import Random
import numpy as np

from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_list
from Events.Game.move.algos.GameObjects.data_lists.tools.map_ranges_tools import is_in_bondaries
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.check import check_if_cell_is_on_map
from Events.Game.move.get_position import get_random_position_on_tier1
import typing

from Events.Game.move.zones import get_zone_index


class Annealing_Algo():
    def __init__(self,settings:Settings,rand:Random):


        self.temperature=settings.temperature
        self.temperature_reduction=settings.temperature_reduction

        self.iterations_form_last_temperature_update=-1
        self.last_metropolis=0
        self.last_x=0
        self.last_decison=1
        self.randm_np=None
        init_start1_x=None
        self.settings=settings
        init_start2_x=None
        self.not_accepted_counter=0
        self.rand=None
        self.av_pts_new=0
        self.diff=0
        self.is_rand_choose=False
        self.all_accepted_results=[]
        if rand!=None:
            self.randm_np=np.random.RandomState()
            self.randm_np.seed(rand.randint(0,200000))
            self.rand=rand
            init_start1_x=rand.random()*settings.map_size_x
            init_start2_x=rand.random()*settings.map_size_x
        self.current_result={"position":[Point(init_start1_x,settings.tier1_distance_from_intruder),Point(init_start2_x,settings.tier1_distance_from_intruder)], "points":0}
        self.step=self.settings.annealing_step


        self.annealing_number_of_iterations=settings.annealing_number_of_iterations
        self.can_terget_be_changed=True


    def un_register_attack(self, candidate_points,candidate_positions:typing.List[Point],settings:Settings,result_list:Result_list):

        current_points=result_list.get_current_points_from_full_map(self.current_result["position"][0],self.current_result["position"][1])
        self.current_result["points"]=current_points
        self.iterations_form_last_temperature_update=self.iterations_form_last_temperature_update+1
        if self.iterations_form_last_temperature_update>=self.annealing_number_of_iterations:
            self.iterations_form_last_temperature_update=0
            self.temperature=self.temperature*self.temperature_reduction
            # self.step=self.step*self.temperature_reduction
            self.not_accepted_counter=0



        self.av_pts_new=candidate_points

        value_delta=candidate_points-self.current_result["points"]
        self.diff=candidate_points-self.current_result["points"]
        metropolis=math.exp(-abs(value_delta) / self.temperature)
        x=self.rand.random()
        self.last_decison=0
        self.last_x=x
        self.last_metropolis=metropolis
        if value_delta>0:
            self.last_metropolis=1
        if (value_delta>0 or (x<metropolis and not self.is_rand_choose)):#if true than accept
            self.last_decison=1

            self.current_result={"position":candidate_positions,"points":candidate_points}
            z1=get_zone_index(settings,candidate_positions[0].x)
            z2=get_zone_index(settings,candidate_positions[1].x)
            if z1<z2:
                temp=z1
                z1=z2
                z2=temp
            self.all_accepted_results.append((z1,z2,self.temperature))
        else:
            self.not_accepted_counter=self.not_accepted_counter+1









    def get_new_targets(self,settings,rand:Random):

            

        # if self.can_terget_be_changed==False:
        #     print("test")
        candidate1=0
        candidate2=0
        # if self.choose_random:
        #     self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
        #     self.choose_random=False
        #     return
        # else:
        #     self.choose_random=True
        if settings.is_sa_b:
            if self.is_rand_choose:
                candidate1=self.current_result["position"][0].x+self.get_candidate(rand)
                while(not check_if_cell_is_on_map(Point(candidate1,settings.tier1_distance_from_intruder),settings.map_size_x,settings.map_size_y)):
                    candidate1=self.current_result["position"][0].x+self.get_candidate(rand)

                candidate2=self.current_result["position"][1].x+self.get_candidate(rand)
                while(not check_if_cell_is_on_map(Point(candidate2,settings.tier1_distance_from_intruder),settings.map_size_x,settings.map_size_y)):
                    candidate2=self.current_result["position"][1].x+self.get_candidate(rand)

                self.is_rand_choose=False
            else:
                candidate1=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder).x
                candidate2=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder).x
                self.is_rand_choose=True

        else:
            candidate1=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder).x
            candidate2=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder).x


        return (Point(candidate1,settings.tier1_distance_from_intruder),Point(candidate2,settings.tier1_distance_from_intruder))


    def get_candidate(self, rand):
        sign=1
        if rand.randint(0,1)==0:
            sign=-1

        candidate=self.step*rand.random()*sign


        return candidate




