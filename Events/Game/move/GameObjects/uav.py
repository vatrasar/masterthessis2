from Events.Game.move.GameObjects.algos.naive_algo import Naive_Algo
from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion,naive_algo:Naive_Algo):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)
        self.points=points

        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
        self.points=0
        self.naive_algo=naive_algo


    def asign_points(self, points):
        self.points=self.points+points
