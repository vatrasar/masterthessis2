import typing
from random import Random

from Events.Game.move.GameObjects.algos.tools.enum.enum_algos import Target_choose
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.algos.tools.points_cell import PointsCell
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_random_position_on_tier1


class Naive_Algo():
    def __init__(self,list_limit,curiosty_ratio):
        self.curiosty_ratio = curiosty_ratio
        self.results_list:typing.List[PointsCell]=[]
        self.list_limit=list_limit
        self.current_attacks={}
        self.current_attacks[0]={"start postion":None,"points":None,"active":False}
        self.current_attacks[1]={"start postion":None,"points":None,"active":False}
        self.targert_attacks={0:None,1:None}
        self.type_of_algo_choose=Target_choose.RANDOM_ATTACK

    def register_attack(self, start_position:Point,uav_id,points_before_attack):
        if self.current_attacks[uav_id]["active"]==False:

            points_before_attack=points_before_attack
            self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points_before_attack,"active":True}

    def update_result_to_exisiting_record(self,result,position,settings):
        for record in self.results_list:
            if get_2d_distance(Point(record.x,record.y),position)<=2*settings.map_resolution:

                record.r=record.r+1
                average_points=(result+record.points)/record.r
                record.points=average_points
                return True
        return False

    def un_register_attack(self, uav_id,current_points,settings:Settings):

        self.current_attacks[uav_id]["active"]=False
        points=current_points-self.current_attacks[uav_id]["points before attack"]
        start_location=self.current_attacks[uav_id]["start postion"]
        if self.update_result_to_exisiting_record(points,start_location,settings):
            return

        if points==0:
            return
        if self.is_limit_reached():
            worse_record=self.get_worse_on_list()
            if worse_record.points<points:
                self.results_list.remove(worse_record)
                self.results_list.append(PointsCell(start_location.x,start_location.y,1,points))

        else:
            self.results_list.append(PointsCell(start_location.x,start_location.y,1,points))

    def choose_new_target(self,settings,rand:Random,uav_index):
        x=rand.random()
        new_target=None
        if x<self.curiosty_ratio:
            new_target=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
            self.type_of_algo_choose=Target_choose.RANDOM_ATTACK
        else:
            x=rand.random()
            if x<self.curiosty_ratio:# choose random from list
                i=rand.randint(0,len(self.results_list)-1)
                new_target=self.results_list[i]
                self.type_of_algo_choose=Target_choose.RANDOM_FROM_LIST
            else:#choose best form list
                self.type_of_algo_choose=Target_choose.BEST_FROM_LIST
                new_target=self.get_best_from_list()

        self.targert_attacks[uav_index]=new_target

    def get_best_from_list(self):
        best_target=self.results_list[0]
        for target in self.results_list:
            if target.points>best_target.points:
                best_target=target
        return best_target

    def get_target_postion(self,index,rand,settings):
        if self.targert_attacks[index]==None:
            self.choose_new_target(settings,rand,index)
        return self.targert_attacks[index]

    def is_limit_reached(self):
        return len(self.results_list)>=self.list_limit

    def get_worse_on_list(self):
        min_record=self.results_list[0]
        for record in self.results_list:
            if record.points<min_record.points:
                min_record=record
        return min_record

