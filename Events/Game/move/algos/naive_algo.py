from random import Random

from Events.Game.move.algos.GameObjects.tools.enum.enum_algos import Target_choose
from Events.Game.move.algos.GameObjects.tools.point import Point
from Events.Game.move.algos.GameObjects.tools.settings import Settings
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_random_position_on_tier1


class Naive_Algo():
    def __init__(self,list_limit,curiosty_ratio,iterations_for_learning):
        self.curiosty_ratio = curiosty_ratio
        self.results_list=[]
        self.list_limit=list_limit
        self.current_attacks={}
        self.current_attacks[0]={"start postion":None,"points":0,"active":False}
        self.current_attacks[1]={"start postion":None,"points":0,"active":False}
        self.targert_attacks={0:None,1:None}
        self.after_attack={0:True,1:True}
        self.type_of_algo_choose={0:Target_choose.RANDOM_ATTACK,1:Target_choose.RANDOM_ATTACK}
        self.choose_random={0:True,1:True}
        self.random_move={0:False,1:False}
        self.iteration_number=0
        self.iterations_for_learning=iterations_for_learning





    def register_attack(self, start_position:Point,uav_id,points_before_attack):
        if self.current_attacks[uav_id]["active"]==False:
            self.current_attacks[uav_id]["active"]=True
            points_before_attack=points_before_attack
            self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points_before_attack,"active":True}

    def is_after_attack(self,uav_list):
        is_after_attack=True
        for uav in uav_list:
            if self.after_attack[uav.index]==False:
                is_after_attack=False
        return is_after_attack

    def cancel_attack(self,uav_id,start_position,points,points1,points2,rand:Random,settings:Settings,uav_list):

        self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points,"active":False}
        self.after_attack[uav_id]=True
        points=0
        self.random_move[uav_id]=True


        self.targert_attacks[uav_id]=None
        if self.is_after_attack(uav_list):
            self.un_register_attack(uav_id,points1,points2,settings,uav_list)


    def remove_target(self,uav_index):
        self.targert_attacks[uav_index]=None

    def update_result_to_exisiting_record(self,points,settings):
        for record in self.results_list:
            postion1=record[0]
            postion2=record[1]
            if get_2d_distance(record[0],postion1)<=settings.map_resolution and get_2d_distance(record[1],postion2)<=settings.map_resolution:

                record["attaks_number"]=record["attaks_number"]+1
                average_points=(points+record["points"])/record["attaks_number"]
                record["points"]=average_points

                return True

        return False


    def un_register_attack(self, uav_id,current_points1,current_points2,settings:Settings,uav_list):

        self.iteration_number=self.iteration_number+1
        self.current_attacks[uav_id]["active"]=False
        self.after_attack[uav_id]=True
        self.random_move[uav_id]=True


        if self.is_after_attack(uav_list):
            self.iteration_number=self.iteration_number+1
            points=[]
            points_sum=0
            for uav in uav_list:
                points=uav.points-self.current_attacks[uav.index]["points before attack"]
                points_sum=points_sum+points

            # if self.update_result_to_exisiting_record(points_sum,settings):
            #     return
            if points_sum==0:
                return
            if not self.is_limit_reached():
                self.results_list.append({"points":points_sum,0:self.current_attacks[0]["start postion"],1:self.current_attacks[1]["start postion"],"attaks_number":1})
            else:
                worse_record=self.get_worse_on_list()
                if worse_record["points"]<points_sum:
                    self.results_list.remove(worse_record)
                    self.results_list.append({"points":points_sum,0:self.current_attacks[0]["start postion"],1:self.current_attacks[1]["start postion"],"attaks_number":1})



    def choose_new_target(self,settings,rand:Random,uav_index,uav_list):

        #fake move




        # if self.choose_random[uav_index] and self.is_limit_reached():
        #     self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
        #     self.choose_random[uav_index]=False
        #     return
        # else:
        #     self.choose_random[uav_index]=True

        #waitnig for secound drone

        if (not self.is_after_attack(uav_list)) or self.random_move[uav_index]:
            self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
            self.choose_random[uav_index]=False
            self.random_move[uav_index]=False
            return



        #chooseing true target
        self.after_attack[0]=False
        self.after_attack[1]=False
        self.choose_random[0]=True
        self.choose_random[1]=True


        x=rand.random()
        new_target=None
        if not self.is_learning_finished():
            self.targert_attacks[0]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            self.targert_attacks[1]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            return



        self.type_of_algo_choose[0]=Target_choose.BEST_FROM_LIST
        self.type_of_algo_choose[1]=Target_choose.BEST_FROM_LIST

        best_result=self.get_best_from_list()
        if best_result==None:
            self.targert_attacks[0]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            self.targert_attacks[1]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
        else:

            self.targert_attacks[0]=best_result[0]
            self.targert_attacks[1]=best_result[1]

    def get_best_from_list(self):

        best_target=self.results_list[0]
        for target in self.results_list:
            if target["points"]>best_target["points"]:
                best_target=target
        return best_target

    def get_target_postion(self,index,rand,settings,uav_list):
        # if self.is_limit_reached():
        #     if index==0:
        #         return Point(10,settings.tier1_distance_from_intruder)
        #     else:
        #         return Point(1000,settings.tier1_distance_from_intruder)

        if self.targert_attacks[index]==None:
            self.choose_new_target(settings,rand,index,uav_list)
        return self.targert_attacks[index]

    def is_learning_finished(self):
        return self.iteration_number>self.iterations_for_learning

    def is_limit_reached(self):
        return len(self.results_list)>=self.list_limit

    def get_worse_on_list(self):
        min_record=self.results_list[0]
        for record in self.results_list:
            if record["points"]<min_record["points"]:
                min_record=record
        return min_record

