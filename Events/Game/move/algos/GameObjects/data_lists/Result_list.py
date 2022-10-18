from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.zones import get_zone_index

import math
class Result_record():
    def __init__(self,postion1,postion2,points,tier1,tier2,zone1,zone2,reward1,reward2,previous_number_of_hits,best_points,action_number=0):

        self.points = points
        self.best_points=best_points
        self.reward1=reward1
        self.reward2=reward2
        self.position1 =postion1
        self.position2 =postion2
        self.zone1=zone1
        self.zone2=zone2
        self.tier1=tier1
        self.tier2=tier2
        self.number_of_hits=1
        self.number_of_hits2=previous_number_of_hits+1
        self.action_number=action_number
        self.number_of_hits3=0
        self.number_hits_iter1=0
        self.number_hits_iter2=0
        self.avg_iter2=0
        self.avg_iter1=0


    def copy(self):
        new_record=Result_record(self.position1,self.position2,self.points,self.tier1,self.tier2,self.zone1,self.zone2,self.reward1,self.reward2,self.number_of_hits2-1,self.best_points,self.action_number)
        return new_record

def sort_results(e:Result_record):
    return e.points
class Avg_zone_info():
    def __init__(self):
        self.points=0
        self.number_of_hit=0
class Result_list():

    def __init__(self,zone_width,list_limit,settings:Settings):
        self.settings = settings
        self.list_limit = list_limit
        self.zone_width = zone_width

        self.result_list:typing.List[Result_record]=[]
        self.lr_memory1:typing.List[Result_record]=[]
        self.lr_memory2:typing.List[Result_record]=[]
        self.result_map={}
        zones_number=self.settings.naive_algo_list_limit
        self.explatation=settings.mode
        self.avg_rewards_zones={}
        self.full_map_of_goals:typing.List[typing.List[Result_record]]=[]

        for i in range(zones_number):
            new_row=[]
            for p in range(zones_number):

                new_cell=Result_record(Point(self.zone_width*(0.5+i),0),Point(self.zone_width*(0.5+p),0),0,1,1,"-1","-1",0,0,-1,0,0)
                new_row.append(new_cell)
            self.full_map_of_goals.append(new_row)
        for i in range(0,zones_number):
            self.result_map[i]=None
            self.avg_rewards_zones[i]=Avg_zone_info()

    def load_point(self, postion1,postion2, points_best,tier1,tier2,points1,points2,points_av,counter=0):
        old_points=0
        zone_index=get_zone_index(self.settings,postion1.x)
        old_number_of_hits=0
        # if self.result_map[zone_index]!=None:
        #     old_points=self.result_map[zone_index].points
        #     old_number_of_hits=self.result_map[zone_index].number_of_hits2
        #     self.result_list.remove(self.result_map[zone_index])

        zone1="-"
        zone2="-"
        if postion1!=None:
            zone1=str(int(postion1.x / self.zone_width))
        if postion2!=None:
            zone2=str(int(postion2.x / self.zone_width))


        new_record=Result_record(postion1,postion2,points_av,tier1,tier2,zone1,zone2,points1,points2,old_number_of_hits,points_best,counter)
        self.result_list.append(new_record)
        self.result_map[zone_index]=new_record

    def update_avg_of_zone(self,zone_index1,points):
        old_points=self.avg_rewards_zones[zone_index1].points
        old_counter=self.avg_rewards_zones[zone_index1].number_of_hit
        new_points=(old_points*old_counter+points)/float(old_counter+1)
        self.avg_rewards_zones[zone_index1].number_of_hit=old_counter+1
        self.avg_rewards_zones[zone_index1].points=new_points
    def update_tier_avg(self,cell:Result_record,av_pts,tier1,tier2):
       if tier1==1 or tier2==1:
            old_points=cell.avg_iter1
            old_counter=cell.number_hits_iter1
            new_points=(old_points*old_counter+av_pts)/float(old_counter+1)
            cell.number_hits_iter1=cell.number_hits_iter1+1
            cell.avg_iter1=new_points
       else:
            old_points=cell.avg_iter2
            old_counter=cell.number_hits_iter2
            new_points=(old_points*old_counter+av_pts)/float(old_counter+1)
            cell.number_hits_iter2=cell.number_hits_iter2+1
            cell.avg_iter2=new_points

    def update_full_map(self,zone1,zone2, points1,points2,postion1,postion2,tier1,tier2):
        if zone1<zone2:
            zone_temp=zone1
            zone1=zone2
            zone2=zone_temp
        old_points=self.full_map_of_goals[zone1][zone2].points
        old_counter=self.full_map_of_goals[zone1][zone2].number_of_hits3
        av_pts=(points1+points2)/2.0
        new_points=(old_points*old_counter+av_pts)/float(old_counter+1)
        self.full_map_of_goals[zone1][zone2].number_of_hits3=old_counter+1
        self.full_map_of_goals[zone1][zone2].points=new_points
        self.update_tier_avg(self.full_map_of_goals[zone1][zone2],av_pts,tier1,tier2)




        if self.full_map_of_goals[zone1][zone2].best_points<av_pts or self.full_map_of_goals[zone1][zone2].number_of_hits3==1:
            self.full_map_of_goals[zone1][zone2].position1=postion1
            self.full_map_of_goals[zone1][zone2].position2=postion2
            self.full_map_of_goals[zone1][zone2].tier1=tier1
            self.full_map_of_goals[zone1][zone2].tier2=tier2
            self.full_map_of_goals[zone1][zone2].best_points=av_pts
            self.full_map_of_goals[zone1][zone2].zone1=str(zone1)
            self.full_map_of_goals[zone1][zone2].zone2=str(zone2)
            self.full_map_of_goals[zone1][zone2].reward1=points1
            self.full_map_of_goals[zone1][zone2].reward2=points2
    def add_result_point(self, postion1,postion2, points,tier1,tier2,points1,points2,load,counter=0):
        if self.explatation==Modes.EXPLOITATION and not load:
            return
        zone_index=get_zone_index(self.settings,postion1.x)
        zone_index1=get_zone_index(self.settings,postion1.x)
        zone_index2=get_zone_index(self.settings,postion2.x)
        self.update_avg_of_zone(zone_index1,points1)
        self.update_avg_of_zone(zone_index2,points2)
        self.update_full_map(zone_index1,zone_index2,points1,points2,postion1,postion2,tier1,tier2)
        # record_to_update=self.get_record_with_postions(postion1,postion2)
        #
        # if record_to_update!=None:
        #     # record_to_update.number_of_hits=record_to_update.number_of_hits+1
        #     # record_to_update.points=(record_to_update.points+points)/float(record_to_update.number_of_hits)
        #     return




        if self.result_map[zone_index]==None or self.result_map[zone_index].best_points<points:
            old_points=0
            old_number_of_hits=0
            if self.result_map[zone_index]!=None:
                old_points=self.result_map[zone_index].points
                old_number_of_hits=self.result_map[zone_index].number_of_hits2
                self.result_list.remove(self.result_map[zone_index])

            zone1="-"
            zone2="-"
            if postion1!=None:
                zone1=str(int(postion1.x / self.zone_width))
            if postion2!=None:
                zone2=str(int(postion2.x / self.zone_width))
            points_av=(old_points*old_number_of_hits+points)/float(old_number_of_hits+1)

            new_record=Result_record(postion1,postion2,points_av,tier1,tier2,zone1,zone2,points1,points2,old_number_of_hits,points,counter)
            self.result_list.append(new_record)
            self.result_map[zone_index]=new_record
        else:
            old_points=0
            old_number_of_hits=0
            if self.result_map[zone_index]!=None:
                old_points=self.result_map[zone_index].points
                old_number_of_hits=self.result_map[zone_index].number_of_hits2

            self.result_map[zone_index].points=self.avg_rewards_zones[zone_index1].points+self.avg_rewards_zones[zone_index2].points
            self.result_map[zone_index].number_of_hits2=old_number_of_hits+1




    def get_list_of_best(self):
        list_of_best=[]
        for row in self.full_map_of_goals:

            for cell in row:
                to_delete=None
                to_add=None
                # if len(list_of_best)!=10:
                if cell.number_of_hits3!=0:
                    list_of_best.append(cell)
                # else:
                #     for cell_best in list_of_best:
                #         if cell.points>cell_best.points:
                #             to_delete=cell_best
                #             to_add=cell
                #             break
                #     if to_delete!=None:
                #
                #         list_of_best.remove(to_delete)
                #         list_of_best.append(to_add)
        for cell in list_of_best:
            cell.best_points=cell.best_points*2
        return list_of_best
    def save_to_file(self,memory_list):



        # file=open("./results/goals_of_attack.csv","w")
        #
        if self.settings.learning:
            self.result_list=self.get_list_of_best()
        self.sort_list()
        # for i,run in enumerate(memory_list):
        #     file.write("run:%d\n"%(i))
        #     file.write("#position1, #position2, #zone1, #zone2,reward1,reward2, #reward sum, #tier uav1, #tier uav2\n")
        #
        #
        #         file.write("%s, %s, %s, %s,%.2f,%.2f, %.2f, %s, %s\n"%(result.position1,result.position2,result.zone1,result.zone2,result.reward1,result.reward2,result.points,result.tier1,result.tier2))
        # file.close()

        if self.settings.learning:
            file=open("./results/zones_attacks.txt","w")
            file.write(f'{"#zone index":<14s} {"av_pts":<14s} {"number of hits":<14s} \n')
            file.write(f'{"#1":<14s} {"2":<14s} {"3":<14s}\n')
            for key in self.avg_rewards_zones.keys():
                file.write(f'{key+1:<14d} {self.avg_rewards_zones[key].points:<14.2f} {self.avg_rewards_zones[key].number_of_hit:<14.2f}\n')
            file.close()

        file=open("./results/goals_of_attack.txt","w")

        for i,run in enumerate(memory_list):
            for result in run.result_list:

                if result.position1!=None:
                    result.position1="%.2f"%(result.position1.x)
                else:
                    result.position1="-"
                    result.tier1="-"
                    result.zone1="-"


                if result.position2!=None:
                    result.position2="%.2f"%(result.position2.x)
                else:
                    result.position2="-"
                    result.tier2="-"
                    result.zone2="-"
        file.write(f'{"#pos1":<9s} {"pos2":<9s} {"z1":<5s} {"z2":<5s} {"rew1":<9s} {"rew2":<9s} {"rew sum":<11s} {"tier uav1":<11s} {"tier uav2":<11s} {"rew avg multiple hits":<11s}\n')
        file.write(f'{"#1":<9s} {"2":<9s} {"3":<5s} {"4":<5s} {"5":<9s} {"6":<9s} {"7":<11s} {"8":<11s} {"9":<11s} {"10":<11s}\n')
        counter=0
        for result in self.result_list:
            if counter>=10:
                break
            file.write(f'{result.position1:<9s} {result.position2:<9s} {int(result.zone1)+1:<5d} {int(result.zone2)+1:<5d} {result.reward1:<9.2f} {result.reward2:<9.2f} {result.best_points:<11.2f} {int(result.tier1):<11d} {int(result.tier2) :<11d} {result.points:<11.2f}\n')
            counter=counter+1
        file.close()


        if self.settings.learning:
            file2=open("./results/goals_of_attack_all_results.txt","w")
            file2.write(f'{"#pos1":<9s} {"pos2":<9s} {"z1":<5s} {"z2":<5s} {"rew1":<9s} {"rew2":<9s} {"rew sum":<11s} {"tier uav1":<11s} {"tier uav2":<11s} {"rew avg multiple hits":<11s}\n')
            file2.write(f'{"#1":<9s} {"2":<9s} {"3":<5s} {"4":<5s} {"5":<9s} {"6":<9s} {"7":<11s} {"8":<11s} {"9":<11s} {"10":<11s}\n')
            for result in self.result_list:

                file2.write(f'{result.position1:<9s} {result.position2:<9s} {int(result.zone1)+1:<5d} {int(result.zone2)+1:<5d} {result.reward1:<9.2f} {result.reward2:<9.2f} {result.best_points:<11.2f} {int(result.tier1):<11d} {int(result.tier2) :<11d} {result.points:<11.2f}\n')
            file2.close()


            file3=open("./results/max_av_reward.txt","w")
            file3.write(f'{"#zone id":<9s}')
            for i in range(len(self.full_map_of_goals)):
                file3.write(f'{i+1:<9d}')
            file3.write("\n")
            for i in range(len(self.full_map_of_goals)):
                file3.write(f'{i+1:<9d}')
                for p in range(len(self.full_map_of_goals)):
                    if p<=i:
                        file3.write(f'{self.full_map_of_goals[i][p].points:<9.2f}')
                    else:
                        file3.write(f'{self.full_map_of_goals[p][i].points:<9.2f}')
                file3.write("\n")

            file3.close()

            file4=open("./results/best_tier_id.txt","w")
            file4.write(f'{"#zone id":<9s}')
            for i in range(len(self.full_map_of_goals)):
                file4.write(f'{i+1:<9d}')
            file4.write("\n")
            for i in range(len(self.full_map_of_goals)):
                file4.write(f'{i+1:<9d}')
                for p in range(len(self.full_map_of_goals)):
                    if (self.full_map_of_goals[i][p].number_of_hits3==0 and self.full_map_of_goals[p][i].number_of_hits3==0):
                        file4.write(f'{"-":<9s}')
                    else:
                        if not p>i:
                            if self.full_map_of_goals[i][p].avg_iter1>self.full_map_of_goals[i][p].avg_iter2:
                                file4.write(f'{"1":<9s}')
                            else:
                                file4.write(f'{"2":<9s}')
                        else:
                            if self.full_map_of_goals[p][i].avg_iter1>self.full_map_of_goals[p][i].avg_iter2:
                                file4.write(f'{"1":<9s}')
                            else:
                                file4.write(f'{"2":<9s}')
                file4.write("\n")

            file4.close()

            file3=open("./results/zones_hits.txt","w")
            file3.write(f'{"#zone id":<9s}')
            for i in range(len(self.full_map_of_goals)):
                file3.write(f'{i+1:<9d}')
            file3.write("\n")
            for i in range(len(self.full_map_of_goals)):
                file3.write(f'{i+1:<9d}')
                for p in range(len(self.full_map_of_goals)):
                    if p<=i:
                        file3.write(f'{self.full_map_of_goals[i][p].number_of_hits3:<9d}')
                    else:
                        file3.write(f'{self.full_map_of_goals[p][i].number_of_hits3:<9d}')

                file3.write("\n")

            file3.close()

            file4=open("./results/zones_hits3D.txt","w")
            file4.write(f'{"#z1":<9s} {"z2":<9s} {"hits":<9s}')
            for i in range(len(self.full_map_of_goals)):
                file4.write(f'{i+1:<9d}')
            for i in range(len(self.full_map_of_goals)):

                for p in range(len(self.full_map_of_goals)):
                    # file4.write(f'{i:<9d} {i:<9d} {self.full_map_of_goals[i][p].number_of_hits3:<9d}\n')
                    if p<=i:
                        file4.write(f'{self.full_map_of_goals[i][p].number_of_hits3:<9d}\n')
                    else:
                        file4.write(f'{self.full_map_of_goals[p][i].number_of_hits3:<9d}\n')
                file4.write('\n')


            file4.close()

    def save_to_file_with_action(self):


        self.sort_list()

        file=open("./results/LA_goals.txt","w")


        file.write(f'{"#action id":<12s} {"pos1":<9s} {"pos2":<9s} {"z1":<5s} {"z2":<5s} {"rew1":<9s} {"rew2":<9s} {"rew sum":<11s} {"tier uav1":<11s} {"tier uav2":<11s} {"rew avg multiple hits":<11s} \n')
        file.write(f'{"#1":<12s} {"2":<9s} {"3":<9s} {"4":<5s} {"5":<5s} {"6":<9s} {"7":<9s} {"8":<11s} {"9":<11s} {"10":<11s} {"11":<11s}\n')
        counter=1
        for result in self.result_list:
            if counter>=11:
                break
            result.action_number=counter
            file.write(f'{result.action_number:<12d} {result.position1:<9s} {result.position2:<9s} {int(result.zone1)+1:<5d} {int(result.zone2)+1:<5d} {result.reward1:<9.2f} {result.reward2:<9.2f} {result.best_points:<11.2f} {int(result.tier1):<11d} {int(result.tier2):<11d} {result.points:<11.2f}\n')
            counter=counter+1
        file.close()

    def flirt_none_values(self,value):
        if value==None:
            return "-"
        else:
            return value


    def is_limit_reached(self):
        return len(self.result_list)>=self.list_limit

    def get_worse_on_list(self)->Result_record:
        min_record=self.result_list[0]
        for record in self.result_list:
            if record.points<min_record.points:
                min_record=record
        return min_record

    def get_best_from_list(self):

        best_target=self.result_list[0]
        for target in self.result_list:
            if target.points>best_target.points:
                best_target=target
        return best_target

    def sort_list(self):
        self.result_list.sort(key=sort_results)
        self.result_list.reverse()

    def get_record_with_postions(self, postion1, postion2):
        positions_to_check=[]



        for record in self.result_list:

            record_pozitions=[]
            current_postions=[]
            self.add_to_list_if_not_none(record_pozitions,record.position1)
            self.add_to_list_if_not_none(record_pozitions,record.position2)
            self.add_to_list_if_not_none(current_postions,postion1)
            self.add_to_list_if_not_none(current_postions,postion2)
            if len(current_postions)==2:
                if get_2d_distance(record.position1,postion1)<self.settings.map_resolution*2 and get_2d_distance(record.position2,postion2)<self.settings.map_resolution*2:
                    return record
            elif len(current_postions)==1 and len(record_pozitions)>0:
                if get_2d_distance(current_postions[0],record_pozitions[0])<self.settings.map_resolution*2:
                    return record
            else:
                return None
        return None

    def add_to_list_if_not_none(self, list, postion1):
        if postion1!=None:
            list.append(postion1)
