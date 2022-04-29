from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.get_position import get_random_position_on_tier1


class Result_record():
    def __init__(self,postion1,postion2,points,tier1,tier2,zone1,zone2):

        self.points = points
        self.position1 =postion1
        self.position2 =postion2
        self.zone1=zone1
        self.zone2=zone2
        self.tier1=tier1
        self.tier2=tier2




class Result_list():

    def __init__(self,zone_width,list_limit):
        self.list_limit = list_limit
        self.zone_width = zone_width
        self.result_list:typing.List[Result_record]=[]

    def add_result_point(self, postion1,postion2, points,tier1,tier2):
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

        file=open("./data/Memory.txt","w")
        file.write("#position1 #position2 #zone1 #zone2 #reward #tier1 #tier2\n")
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
