import math
import typing
from random import Random
import numpy as np
from Events.Game.move.GameObjects.algos.tools.enum.enum_algos import Target_choose
from Events.Game.move.GameObjects.algos.tools.map_ranges_tools import is_in_bondaries
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.algos.tools.points_cell import PointsCell
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_random_position_on_tier1


class Annealing_Algo():
    def __init__(self,settings:Settings,rand:Random):
        self.temperature=settings.temperature
        self.current_attacks={}
        self.temperature_reduction=settings.temperature_reduction
        self.current_attacks[0]={"start postion":None,"points":None,"active":False}
        self.current_attacks[1]={"start postion":None,"points":None,"active":False}

        init_start_x=rand.random()*settings.map_size_x
        self.current_result={"position":Point(init_start_x,settings.tier1_distance_from_intruder), "points":0}
        self.targert_attacks={0:None,1:None}
        self.randm_np=np.random.RandomState()
        self.randm_np.seed(rand.randint(0,200000))
        self.step=math.sqrt(settings.temperature)
        self.choose_random=False
        self.iteration=0
        self.annealing_number_of_iterations=settings.annealing_number_of_iterations
        self.can_terget_be_changed=True



    def register_attack(self, start_position:Point,uav_id,points_before_attack):

        if self.current_attacks[uav_id]["active"]==False:
            self.targert_attacks[uav_id]=None
            self.current_attacks[uav_id]["active"]=True

            points_before_attack=points_before_attack
            self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points_before_attack,"active":True}

    def get_target_postion(self,index,rand,settings):
        if self.targert_attacks[index]==None:
            self.choose_new_target(settings,rand,index)
        return self.targert_attacks[index]

    def un_register_attack(self, uav_id,current_points,settings:Settings,rand:Random):
        self.iteration=self.iteration+1
        self.current_attacks[uav_id]["active"]=False
        candidate_points=current_points-self.current_attacks[uav_id]["points before attack"]
        candidate:Point=self.current_attacks[uav_id]["start postion"]

        value_delta=candidate_points-self.current_result["points"]
        if np.log(rand.random())*settings.temperature<value_delta:#if true than accept
            self.current_result={"position":candidate,"points":candidate_points}

        self.remove_target(uav_id,settings)

    def cancel_attack(self,uav_index,rand:Random,settings:Settings):
        self.iteration=self.iteration+1
        if np.log(rand.random())*settings.temperature<0:#if true than accept
            self.current_result={"position":self.targert_attacks[uav_index],"points":0}
        self.remove_target(uav_index,settings)

    def remove_target(self,uav_index,settings:Settings):


        self.temperature=settings.temperature_reduction*self.temperature #reduction of temperature
        self.targert_attacks[uav_index]=None
        self.can_terget_be_changed=True


    def choose_new_target(self,settings,rand:Random,uav_index):
        if self.iteration>self.annealing_number_of_iterations:
            if self.choose_random:
                self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
                self.choose_random=False
                return
            else:
                self.choose_random=True
                self.targert_attacks[uav_index]=self.current_result["position"]
                return
        # if self.can_terget_be_changed==False:
        #     print("test")

        # if self.choose_random:
        #     self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
        #     self.choose_random=False
        #     return
        # else:
        #     self.choose_random=True

        candidate=self.current_result["position"].x+self.randm_np.normal()*self.step
        while not is_in_bondaries(1,settings.map_size_x-10,candidate):
            candidate=self.current_result["position"].x+self.randm_np.normal()*self.step

        self.targert_attacks[uav_index]=Point(candidate,settings.tier1_distance_from_intruder)
        self.can_terget_be_changed=False

