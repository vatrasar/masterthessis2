from random import Random

import typing
from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_list, Result_record
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_algos import Target_choose
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes, Learning_algos
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.algos.annealing_algo import Annealing_Algo
from Events.Game.move.algos.list_algo import list_algo_new_targets
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_random_position_on_tier1


class Naive_Algo():
    def __init__(self,list_limit,curiosty_ratio,iterations_for_learning,settings:Settings,hit_list,uav_list,rand:Random):
        self.curiosty_ratio = curiosty_ratio
        self.results_list=Result_list(settings.zone_width,settings.naive_algo_list_limit,settings)
        self.settings=settings
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
        self.hit_list=hit_list
        self.fake_targets_list=[]
        self.is_fake_attack={0:False,1:False}
        self.uav_list:typing.List[Uav]=uav_list
        if settings.learning_algo_type==Learning_algos.SA:
            self.anneling_algorithm=Annealing_Algo(settings,rand)




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
        if not self.is_fake_attack[uav_id]:
            self.random_move[uav_id]=True


        self.targert_attacks[uav_id]=None
        if self.is_after_attack(uav_list):
            self.un_register_attack(uav_id,points1,points2,settings,uav_list)


    def remove_target(self,uav_index):
        self.targert_attacks[uav_index]=None

    # def update_result_to_exisiting_record(self,points,settings):
    #     for record in self.results_list:
    #         postion1=record[0]
    #         postion2=record[1]
    #         if get_2d_distance(record[0],postion1)<=settings.map_resolution and get_2d_distance(record[1],postion2)<=settings.map_resolution:
    #
    #             record["attaks_number"]=record["attaks_number"]+1
    #             average_points=(points+record["points"])/record["attaks_number"]
    #             record["points"]=average_points
    #
    #             return True
    #
    #     return False
    def adnotate_hit(self,point,position):
        self.iteration_number=self.iteration_number+1
        print("iteration:"+str(self.iteration_number))
        self.hit_list.add_hit(position,point)

    def un_register_attack(self, uav_id,current_points1,current_points2,settings:Settings,uav_list):


        self.current_attacks[uav_id]["active"]=False
        self.after_attack[uav_id]=True

        if not self.is_fake_attack[uav_id]:
            self.random_move[uav_id]=True


        if self.is_after_attack(uav_list):

            points=[]
            points_sum=0
            for uav in uav_list:
                points=uav.points-self.current_attacks[uav.index]["points before attack"]
                points_sum=points_sum+points
                self.adnotate_hit(points,self.current_attacks[uav.index]["start postion"])

            # if self.update_result_to_exisiting_record(points_sum,settings):
            #     return
            if points_sum==0:
                return

            tiers_uav={0:None,1:None}
            for uav in uav_list:
                tiers_uav[uav.index]=uav.attack_started_from_tier2
            self.results_list.add_result_point(self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"],points_sum,tiers_uav[0],tiers_uav[1])
            if settings.learning_algo_type==Learning_algos.SA:
                self.anneling_algorithm.un_register_attack(points_sum,[self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"]],settings)



    def exploitation(self,settings,rand:Random,uav_index,uav_list):
        #waitnig for secound drone
        if self.random_move[uav_index] and self.is_after_attack(uav_list):
            number_of_fake_targets=min(len(self.results_list.result_list)-1,settings.fake_targets_number)

            self.results_list.sort_list()
            self.fake_targets_list.extend(self.results_list.result_list[1:number_of_fake_targets+1])

            self.random_move[0]=False
            self.random_move[1]=False


        if len(self.fake_targets_list)>0 and self.is_after_attack(uav_list):
            self.is_fake_attack[0]=True
            self.is_fake_attack[1]=True
            self.choose_random[0]=True
            self.choose_random[1]=True
            self.after_attack[0]=False
            self.after_attack[1]=False
            self.update_tragets_using_result_record(self.fake_targets_list[0])
            # self.targert_attacks[0]=self.fake_targets_list[0].position1
            # self.targert_attacks[1]=self.fake_targets_list[0].position2
            self.fake_targets_list.remove(self.fake_targets_list[0])
            return


        if (not self.is_after_attack(uav_list) ):

            self.is_fake_attack[uav_index]=True
            self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
            self.choose_random[uav_index]=False

            return



        #chooseing true target
        self.after_attack[0]=False
        self.after_attack[1]=False
        self.choose_random[0]=True
        self.choose_random[1]=True

        self.is_fake_attack[uav_index]=False


        x=rand.random()
        new_target=None
        if len(self.results_list.result_list)==0:
            self.targert_attacks[0]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            self.targert_attacks[1]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            return



        self.type_of_algo_choose[0]=Target_choose.BEST_FROM_LIST
        self.type_of_algo_choose[1]=Target_choose.BEST_FROM_LIST

        best_result=self.results_list.get_best_from_list()
        if best_result==None:
            self.targert_attacks[0]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            self.targert_attacks[1]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
        else:
            self.update_tragets_using_result_record(best_result)
            # self.targert_attacks[0]=best_result.position1
            # self.targert_attacks[1]=best_result.position2

    def learning(self,settings,rand:Random,uav_index,uav_list):




        if (not self.is_after_attack(uav_list) ):

            self.is_fake_attack[uav_index]=True
            self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
            self.choose_random[uav_index]=False

            return



        #chooseing true target
        self.after_attack[0]=False
        self.after_attack[1]=False
        self.choose_random[0]=True
        self.choose_random[1]=True

        self.is_fake_attack[uav_index]=False

        #choosing new target by algo
        if self.settings.learning_algo_type==Learning_algos.RS:
            target1,target2=list_algo_new_targets(settings,rand)
            self.targert_attacks[0]=target1
            self.targert_attacks[1]=target2
            return
        elif self.settings.learning_algo_type==Learning_algos.SA:

            target1,target2=self.anneling_algorithm.get_new_targets(settings,rand)
            self.targert_attacks[0]=target1
            self.targert_attacks[1]=target2
            return
    def choose_new_target(self,settings,rand:Random,uav_index,uav_list):

        #fake move
        if settings.mode=="learning":
            self.learning(settings,rand,uav_index,uav_list)
        if settings.mode=="exploitation":
            self.exploitation(settings,rand,uav_index,uav_list)



        # if self.choose_random[uav_index] and self.is_limit_reached():
        #     self.targert_attacks[uav_index]=get_random_position_on_tier1(rand,settings.map_size_x,settings.tier1_distance_from_intruder)
        #     self.choose_random[uav_index]=False
        #     return
        # else:
        #     self.choose_random[uav_index]=True



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
        return self.hit_list.iteration>self.iterations_for_learning or self.settings.mode==Modes.EXPLOITATION

    def load_memory(self):
        file=open("data/Memory.txt","r")
        lines=file.readlines()
        for line in lines[1:]:

            line_elements=line.split(" ")
            position1=Point(float(line_elements[0]),self.settings.tier1_distance_from_intruder)
            position2=Point(float(line_elements[1]),self.settings.tier1_distance_from_intruder)
            # zone1=int(line_elements[2])
            # zone2=int(line_elements[3])
            points=float(line_elements[4])

            tier1=bool(line_elements[5])
            tier2=bool(line_elements[6])



            self.results_list.add_result_point(position1,position2,points,tier1,tier2)
    def get_uav_with_index(self, index):

        for uav in self.uav_list:
            if uav.index==index:
                return uav
        return None
    def update_tragets_using_result_record(self, record:Result_record):
        if len(self.uav_list)<2:
            self.targert_attacks[0]=record.position1
            self.targert_attacks[1]=record.position2
            return

        current_target1=self.targert_attacks[0]
        current_target2=self.targert_attacks[1]
        if current_target2==None:
            uav=self.get_uav_with_index(1)
            current_target2=uav.position

        if current_target1==None:
            uav=self.get_uav_with_index(0)
            current_target1=uav.position


        distance1=get_2d_distance(current_target1,record.position1)
        distance2=get_2d_distance(current_target2,record.position2)
        distance_sum_nomral_order=distance2+distance1

        distance1=get_2d_distance(current_target2,record.position1)
        distance2=get_2d_distance(current_target1,record.position2)
        distance_sum_reverse_order=distance2+distance1

        if distance_sum_nomral_order<distance_sum_reverse_order:
            self.targert_attacks[0]=record.position1
            self.targert_attacks[1]=record.position2
        else:
            self.targert_attacks[1]=record.position1
            self.targert_attacks[0]=record.position2
