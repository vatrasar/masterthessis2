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

    def save_to_file(self,hits_list):

        file=open("./data/HITS.csv","w")
        for i,hit_list in enumerate(hits_list):
            file.write("run %d\n"%(i))
            file.write("#hits number, #best attack position, #best attack points,  #mean points\n")
            for hit in hit_list.hit_list\
                    :
                if hit.best_attack_postion==None:
                    file.write("0, -, -, -\n")
                else:
                    file.write("%d, %.2f, %.2f, %.2f\n"%(hit.number_of_hits,hit.best_attack_postion.x,hit.best_points,hit.points_mean))
        file.close()




