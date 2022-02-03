from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)
        self.points=points
        self.last_path=[]
        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
