from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import Sides
from Events.Game.move.algos.GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)


        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
        self.points=0
        self.points=points
        self.attack_started_from_tier2=True

    def asign_points(self, points):
        self.points=self.points+points
