from random import Random

import typing

from Events.Game.move.algos.GameObjects.data_lists.Hit_list import Hit_list
from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_list, Result_record
from Events.Game.move.algos.GameObjects.data_lists.all_results import Result_tr_list
from Events.Game.move.algos.GameObjects.data_lists.result import Result_file
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_algos import Target_choose
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes, Learning_algos, \
    Exploitation_types
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_stop_reasons import Reason_to_stop
from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import get_uav1_and2
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.algos.annealing_algo import Annealing_Algo
from Events.Game.move.algos.list_algo import list_algo_new_targets
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_random_position_on_tier1


class Naive_Algo():
    def __init__(self,list_limit,curiosty_ratio,iterations_for_learning,settings:Settings,hit_list,uav_list,rand:Random,result_tr:Result_tr_list,result_file:Result_file):
        self.result_file = result_file
        self.result_tr = result_tr
        self.curiosty_ratio = curiosty_ratio
        self.results_list=Result_list(settings.zone_width,settings.naive_algo_list_limit,settings)
        self.settings=settings
        self.list_limit=list_limit
        self.current_attacks={}
        self.current_attacks[0]={"start postion":Point(0,0),"points":0,"active":False,"points before attack":0,"intruder energy before attack":0,"uav_energy":0}
        self.current_attacks[1]={"start postion":Point(0,0),"points":0,"active":False,"points before attack":0,"intruder energy before attack":0,"uav_energy":0}
        self.targert_attacks={0:None,1:None}
        self.after_attack={0:True,1:True}
        self.type_of_algo_choose={0:Target_choose.RANDOM_ATTACK,1:Target_choose.RANDOM_ATTACK}
        self.choose_random={0:True,1:True}
        self.random_move={0:False,1:False}
        self.iteration_number=0
        self.iterations_for_learning=iterations_for_learning
        self.hit_list=hit_list
        self.hit_list2=Hit_list(settings)
        self.fake_targets_list=[]
        self.is_fake_attack={0:False,1:False}
        self.uav_list:typing.List[Uav]=uav_list
        self.last_iterations_points=[]
        self.is_synchronization_needed=False
        self.is_secound_synchorniaztion_needed=False
        self.tiers_uav={0:None,1:None}
        self.number_of_no_progress=0
        self.reason_why_learning_stoped=None
        self.best_points=0



        if settings.learning_algo_type==Learning_algos.SA:
            self.anneling_algorithm=Annealing_Algo(settings,rand)





    def register_attack(self, start_position:Point,uav_id,points_before_attack, intruder_energy,uav_list):
        if self.current_attacks[uav_id]["active"]==False:
            self.current_attacks[uav_id]["active"]=True
            points_before_attack=points_before_attack
            uav_energy=0
            for uav in uav_list:
                if uav.index==uav_id:
                   uav_energy=uav.energy
            self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points_before_attack,"active":True,"intruder energy before attack":intruder_energy,"uav_energy":uav_energy}

    def is_after_attack(self,uav_list):
        is_after_attack=True
        for uav in uav_list:
            if self.after_attack[uav.index]==False:
                is_after_attack=False
        return is_after_attack

    def is_partly_after_attack(self,uav_list):
        is_after_attack=True
        after=False
        not_after=False
        for uav in uav_list:
            if self.after_attack[uav.index]==False:
                not_after=True
            else:
                after=True
        return after and not_after

    def cancel_attack(self,uav_id,start_position,points,rand:Random,settings:Settings,uav_list,intruder,time):
        uav_energy=0
        for uav in uav_list:
            if uav.index==uav_id:
               uav_energy=uav.energy
        uav_list[uav_id].cancel_attack(settings)
        self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points,"active":False,"intruder energy before attack":intruder.energy,"uav_energy":uav_energy}
        self.current_attacks[uav_id]["attack_stop_energy"]=uav_energy

        self.after_attack[uav_id]=True
        points=0
        if not self.is_fake_attack[uav_id]:
            self.random_move[uav_id]=True


        self.targert_attacks[uav_id]=None
        if self.is_after_attack(uav_list):
            self.un_register_attack(uav_id,settings,uav_list,time,intruder)


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

        print("iteration:"+str(self.iteration_number))
        self.hit_list.add_hit(position,point)


    def un_register_attack(self, uav_id,settings:Settings,uav_list:typing.List[Uav],time,intruder):


        self.current_attacks[uav_id]["active"]=False
        self.after_attack[uav_id]=True
        uav_energy=0

        for uav in uav_list:
            if uav.index==uav_id:
                uav_energy=uav.energy
        self.current_attacks[uav_id]["attack_stop_energy"]=uav_energy
        if not self.is_fake_attack[uav_id]:
            self.random_move[uav_id]=True


        if self.is_after_attack(uav_list):



            points=[]
            points_sum=0
            points1=0
            points2=0
            for uav in uav_list:
                points=uav.points-self.current_attacks[uav.index]["points before attack"]
                if uav.index==0:
                    points1=points
                else:
                    points2=points
                points_sum=points_sum+points
                # self.adnotate_hit(points,self.current_attacks[uav.index]["start postion"])


            self.iteration_number=self.iteration_number+1
            self.add_points_to_last_hits_list(points_sum)
            # if self.update_result_to_exisiting_record(points_sum,settings):
            #     return

            is_candidate_accpeted=True
            if points_sum>self.best_points:
                self.best_points=points_sum
                self.number_of_no_progress=0

            else:
                self.number_of_no_progress=self.number_of_no_progress+1


            if points_sum!=0:
                self.results_list.add_result_point(self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"],points_sum,self.tiers_uav[0],self.tiers_uav[1],points1,points2,True)
            if settings.learning_algo_type==Learning_algos.SA:
                self.anneling_algorithm.un_register_attack(points_sum,[self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"]],settings)

            if settings.learning_algo_type!=Learning_algos.SA or settings.mode==Modes.EXPLOITATION or self.anneling_algorithm.last_decison==1:
                for uav in uav_list:
                    if uav.index==0:
                        points=points1
                    else:
                        points=points2
                    self.adnotate_hit(points,self.current_attacks[uav.index]["start postion"])
            #file result_tr
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                self.result_tr.add_record(self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"],self.tiers_uav[0],self.tiers_uav[1],points1,points2,points_sum,uav_list[0].points,uav_list[1].points,self.anneling_algorithm.current_result["points"],self.anneling_algorithm.current_result["position"][0],self.anneling_algorithm.current_result["position"][1],self.anneling_algorithm.last_metropolis,self.anneling_algorithm.last_x,self.anneling_algorithm.last_decison,self.anneling_algorithm.temperature,self.number_of_no_progress,self.anneling_algorithm.not_accepted_counter,self.anneling_algorithm.av_pts_new,self.anneling_algorithm.diff)
            else:
                self.result_tr.add_record(self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"],self.tiers_uav[0],self.tiers_uav[1],points1,points2,points_sum,uav_list[0].points,uav_list[1].points)
            uav1,uav2=get_uav1_and2(uav_list)
            uav1:Uav=uav1
            intruder_start_energy=min(self.current_attacks[0]["intruder energy before attack"],self.current_attacks[1]["intruder energy before attack"])
            intruder_energy_spending=intruder.energy-intruder.last_updated_energy
            intruder.last_updated_energy=intruder.energy
            # uav1_energy_spending=self.current_attacks[0]["attack_stop_energy"]-self.current_attacks[0]["uav_energy"]
            # uav2_energy_spending=self.current_attacks[1]["attack_stop_energy"]-self.current_attacks[1]["uav_energy"]
            uav1_energy_spending=uav1.energy-uav1.last_updated_energy
            uav1.last_updated_energy=uav1.energy
            uav2_energy_spending=uav2.energy-uav2.last_updated_energy
            uav2.last_updated_energy=uav2.energy

            self.result_file.add_record(self.current_attacks[0]["start postion"],self.current_attacks[1]["start postion"],self.tiers_uav[0],self.tiers_uav[1],points1,points2,points_sum,time,uav2_energy_spending,uav2.energy,uav1_energy_spending,uav1.energy,intruder_energy_spending,intruder.energy,uav1.points,uav2.points,uav1.points_without_transhold,uav2.points_without_transhold,uav1.points_without_transhold_sum,uav2.points_without_transhold_sum)


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




        self.choose_true_traget(rand, settings)

    def choose_true_traget(self, rand, settings:Settings):



        if len(self.results_list.result_list)==0 or settings.exploitation_type==Exploitation_types.RANDOM:
            self.targert_attacks[0]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            self.targert_attacks[1]=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
            return
        elif settings.exploitation_type==Exploitation_types.BEST:
            self.choose_best(rand, settings)

        elif settings.exploitation_type==Exploitation_types.WHEEL:
            points_sum=0
            for result in self.results_list.result_list:
                points_sum=points_sum+result.points
            list_resutls_with_probability=[]
            for result in self.results_list.result_list:
                prob=result.points/float(points_sum)
                list_resutls_with_probability.append({"result":result,"prob":prob})
            x=rand.random()
            start=0
            end=0
            current_result=None
            if x==0:
                self.update_tragets_using_result_record(list_resutls_with_probability[0]["result"])
                return

            for result_and_prob in list_resutls_with_probability:
                current_result=result_and_prob["result"]
                start=end
                end=end+result_and_prob["prob"]
                if x>start and x<end:
                    self.update_tragets_using_result_record(result_and_prob["result"])
                    return

            self.update_tragets_using_result_record(current_result)
            return
        elif settings.exploitation_type==Exploitation_types.EPSLION:

            x=rand.random()
            if 1-self.settings.epslion>x:
                self.choose_best(rand, settings)
            else:#choose random from list
                self.lr_memory=self.results_list.result_list[0:min(settings.l_lr,len(self.results_list.result_list))]
                result=self.lr_memory[rand.randint(0,len(self.lr_memory)-1)]
                self.update_tragets_using_result_record(result)
                return




            # self.targert_attacks[0]=best_result.position1
            # self.targert_attacks[1]=best_result.position2

    def choose_best(self, rand, settings):
        self.type_of_algo_choose[0] = Target_choose.BEST_FROM_LIST
        self.type_of_algo_choose[1] = Target_choose.BEST_FROM_LIST
        best_result = self.results_list.get_best_from_list()
        if best_result == None:
            self.targert_attacks[0] = get_random_position_on_tier1(rand, settings.map_size_x - 2,
                                                                   settings.tier1_distance_from_intruder)
            self.targert_attacks[1] = get_random_position_on_tier1(rand, settings.map_size_x - 2,
                                                                   settings.tier1_distance_from_intruder)
        else:
            self.update_tragets_using_result_record(best_result)

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

        self.is_synchronization_needed=True
        if self.settings.learning_algo_type==Learning_algos.RS:
            target1,target2=list_algo_new_targets(settings,rand)
            self.targert_attacks[0]=target1
            self.targert_attacks[1]=target2
            # self.hit_list2.add_hit(self.targert_attacks[0],0)
            # self.hit_list2.add_hit(self.targert_attacks[1],0)

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
        if self.iteration_number>self.iterations_for_learning:
            self.reason_why_learning_stoped=Reason_to_stop.ITERATIONS
            return True
        elif (self.settings.learning_algo_type==Learning_algos.SA and self.anneling_algorithm.temperature<self.settings.temeprature_to_stop):
            self.reason_why_learning_stoped=Reason_to_stop.MINIMUM_TEMPERATURE
            return True
        elif self.is_no_progess():
            self.reason_why_learning_stoped=Reason_to_stop.NO_PROGRESS
            return True
        elif self.settings.mode==Modes.EXPLOITATION:
            self.reason_why_learning_stoped=Reason_to_stop.EXPLOITATION
            return True
        # elif self.settings.learning_algo_type==Learning_algos.SA and self.anneling_algorithm.not_accepted_counter>=self.settings.not_accept_tresh:
        #     self.reason_why_learning_stoped=Reason_to_stop.NOT_ACCEPT_TRESH
        #     return True
        else:
            return False

    def load_memory(self):
        file=open("results/goals_of_attack.txt","r")
        lines=file.readlines()
        for line in lines[2:]:

            line_elements=line.split(" ")
            # if line_elements
            line_elements=list(filter(lambda x:x!="",line_elements))
            position1=Point(float(line_elements[0]),self.settings.tier1_distance_from_intruder)
            position2=Point(float(line_elements[1]),self.settings.tier1_distance_from_intruder)
            # zone1=int(line_elements[2])
            # zone2=int(line_elements[3])
            reward1=float(line_elements[4])
            reward2=float(line_elements[5])
            points=float(line_elements[6])

            tier1=bool(line_elements[7])
            tier2=bool(line_elements[8])



            self.results_list.add_result_point(position1,position2,points,tier1,tier2,reward1,reward2,True)

        self.results_list.sort_list()
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

    def is_no_progess(self):


        if self.number_of_no_progress<self.settings.itertions_without_progress_to_stop:

            return False
        else:
            return True

        # for iter_points in self.last_iterations_points:
        #     if self.last_iterations_points[0]<iter_points:
        #
        #         return False
        #
        # for iter_points in self.last_iterations_points:
        #     if self.last_iterations_points[0]<iter_points:
        #         return False





    def add_points_to_last_hits_list(self, points_sum):
        if len(self.last_iterations_points)<self.settings.itertions_without_progress_to_stop:
            self.last_iterations_points.append(points_sum)
        else:
            self.last_iterations_points.remove(self.last_iterations_points[0])
            self.last_iterations_points.append(points_sum)


