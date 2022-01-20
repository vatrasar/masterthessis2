from Events.Game.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.GameObjects.movableObject import MovableObject
from Events.Game.GameObjects.tools.point import Point


class Hand(MovableObject):
    def __init__(self,status,velocity_hand,side:Sides,map_x_size,map_y_size,last_postion_update_time,next_status,target_postion,x=0,y=0):
        super(Hand, self).__init__(x,y,status,40,velocity_hand,last_postion_update_time,next_status,target_postion)

        self.chasing_drone=None
        self.tier_0_position=self.get_hand_tier0_position(side,map_x_size,map_y_size)



    def get_hand_tier0_position(self, side,map_x_size,map_y_size):


        if side.LEFT:
            return Point(map_x_size*0.25,map_y_size*0.2)
        else:
            return Point(map_x_size*0.75,map_y_size*0.2)



