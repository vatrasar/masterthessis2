
from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.tools.point import Point


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion,naive_algo):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)
        self.points=points

        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
        self.points=0
        from Events.Game.move.GameObjects.algos.naive_algo import Naive_Algo
        self.naive_algo:Naive_Algo=naive_algo

    def register_attack(self,start_position:Point):
        self.naive_algo.register_attack(start_position,self.index,self.points)

    def asign_points(self, points):
        self.points=self.points+points
