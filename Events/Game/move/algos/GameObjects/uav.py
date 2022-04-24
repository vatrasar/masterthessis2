from Events.Game.move.algos.annealing_algo import Annealing_Algo
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.algos.GameObjects.movableObject import MovableObject
from Events.Game.move.algos.GameObjects.tools.point import Point


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)


        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
        self.points=0
        self.points=points
        from Events.Game.move.algos.naive_algo import Naive_Algo



    def asign_points(self, points):
        self.points=self.points+points
