import typing

from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.points_cell import PointsCell
from Events.Game.move.GameObjects.uav import Uav


class Naive_Algo():
    def __init__(self,list_limit,curiosty_ratio):
        self.curiosty_ratio = curiosty_ratio
        self.results_list:typing.List[PointsCell]=[]
        self.list_limit=list_limit
        self.current_attacks={}
        self.current_attacks[0]={"start postion":None,"points":None,"active":False}
        self.current_attacks[1]={"start postion":None,"points":None,"active":False}

    def register_attack(self, start_position:Point,uav_id,points_before_attack):
        if self.current_attacks[uav_id]["active"]==False:
            points_before_attack=points_before_attack
            self.current_attacks[uav_id]={"start postion":start_position,"points before attack":points_before_attack,"active":True}

    def un_register_attack(self, uav_id,current_points):

        self.current_attacks[uav_id]["active"]=False
        points=current_points-self.current_attacks[uav_id]["points before attack"]
        start_location=self.current_attacks[uav_id]["start postion"]
        self.results_list.append(PointsCell(start_location.x,start_location.y,0,points))

