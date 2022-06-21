from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import math
import typing

class Hit_list_record():
    def __init__(self,index):
        self.zone_index=index
        self.number_of_hits=0
        self.best_attack_postion:Point=None
        self.best_points=None
        self.points_mean=0


class Hit_list():
    def __init__(self,settings:Settings):
        self.hit_list:typing.List[Hit_list_record]=[]
        number_of_zones=math.ceil(settings.map_size_x/float(settings.zone_width))
        self.zones_width=float(settings.zone_width)
        self.iteration=0
        for zone in range(0,number_of_zones):
            self.hit_list.append(Hit_list_record(zone))

    def add_hit(self, postion, points):
        self.iteration=self.iteration+1
        zone_index=int(postion.x / self.zones_width)

        zone_stac=self.hit_list[zone_index]
        zone_stac.number_of_hits=zone_stac.number_of_hits+1
        if zone_stac.best_attack_postion==None:
            zone_stac.best_attack_postion=postion
            zone_stac.best_points=points
        else:
            if zone_stac.best_points<points:
                zone_stac.best_attack_postion=postion
                zone_stac.best_points=points

        zone_stac.points_mean=(zone_stac.points_mean*(zone_stac.number_of_hits-1)+points)/float(zone_stac.number_of_hits)

    def save_to_file(self,hits_list,reasons_to_stop_simulation):

        file=open("./results/HITS.csv","w")
        for i,hit_list in enumerate(hits_list):
            file.write("run, %d, reason to stop, %s\n"%(i,reasons_to_stop_simulation[i].value))
            file.write("#hits number, #best attack position, #best attack points,  #mean points\n")
            for zone in hit_list.hit_list:
                if zone.best_attack_postion==None:
                    file.write("0, -, -, -\n")
                else:
                    file.write("%d, %.2f, %.2f, %.2f\n"%(zone.number_of_hits,zone.best_attack_postion.x,zone.best_points,zone.points_mean))
        file.close()

        file=open("./results/freq_of_hits.txt","w")
        for i,hit_list in enumerate(hits_list):

            #counting number of hits
            number_of_all_hits=0
            for zone in hit_list.hit_list:
                number_of_all_hits=number_of_all_hits+zone.number_of_hits


            file.write("run, %d\n"%(i))

            file.write("#zone_id freq average_rew\n")
            file.write("#1 2 3\n")
            for zone_number,zone in enumerate(hit_list.hit_list):
                if zone.best_attack_postion==None:
                    file.write("%d 0 0\n"%(zone_number))
                else:
                    file.write("%d %.2f %.2f\n"%(zone_number,zone.number_of_hits/float(number_of_all_hits),zone.points_mean))
        file.close()



        file=open("./results/freq_of_hits.csv","w")
        for i,hit_list in enumerate(hits_list):

            #counting number of hits
            number_of_all_hits=0
            for zone in hit_list.hit_list:
                number_of_all_hits=number_of_all_hits+zone.number_of_hits


            file.write("run, %d\n"%(i))

            file.write("zone_id, freq, average_rew\n")

            for zone_number,zone in enumerate(hit_list.hit_list):
                if zone.best_attack_postion==None:
                    file.write("%d, 0, 0\n"%(zone_number))
                else:
                    file.write("%d, %.2f, %.2f\n"%(zone_number,zone.number_of_hits/float(number_of_all_hits),zone.points_mean))
        file.close()




