from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.distance import get_2d_distance



class Result_record():
    def __init__(self,postion1,postion2,points,tier1,tier2,zone1,zone2):

        self.points = points
        self.position1 =postion1
        self.position2 =postion2
        self.zone1=zone1
        self.zone2=zone2
        self.tier1=tier1
        self.tier2=tier2
        self.number_of_hits=1


def sort_results(e:Result_record):
    return e.points

class Result_list():

    def __init__(self,zone_width,list_limit,settings:Settings):
        self.settings = settings
        self.list_limit = list_limit
        self.zone_width = zone_width
        self.result_list:typing.List[Result_record]=[]


    def add_result_point(self, postion1,postion2, points,tier1,tier2):
        record_to_update=self.get_record_with_postions(postion1,postion2)
        if record_to_update!=None:
            # record_to_update.number_of_hits=record_to_update.number_of_hits+1
            # record_to_update.points=(record_to_update.points+points)/float(record_to_update.number_of_hits)
            return


        if self.is_limit_reached():
            worse_record=self.get_worse_on_list()
            if worse_record.points<points:


                self.result_list.remove(worse_record)
                zone1="-"
                zone2="-"
                if postion1!=None:
                    zone1=str(int(postion1.x / self.zone_width))
                if postion2!=None:
                    zone2=str(int(postion2.x / self.zone_width))

                self.result_list.append(Result_record(postion1,postion2,points,tier1,tier2,zone1,zone2))
        else:
            zone1="-"
            zone2="-"
            if postion1!=None:
                zone1=str(int(postion1.x / self.zone_width))
            if postion2!=None:
                zone2=str(int(postion2.x / self.zone_width))

            self.result_list.append(Result_record(postion1,postion2,points,tier1,tier2,zone1,zone2))

    def save_to_file(self):

        file=open("./data/goals_of_attack.txt","w")
        file.write("#position1 #position2 #zone1 #zone2 #reward #attack from tier2 uav1 #attack from tier2 uav2\n")
        for result in self.result_list:

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

            file.write("%s %s %s %s %.2f %s %s\n"%(result.position1,result.position2,result.zone1,result.zone2,result.points,result.tier1,result.tier2))
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
