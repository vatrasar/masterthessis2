from GameObjects.enumStatus import Sides
from GameObjects.movableObject import MovableObject
from GameObjects.point import Point


class Hand(MovableObject):
    def __init__(self,status,velocity_hand,side:Sides,map_x_size,map_y_size,x=0,y=0):
        super(Hand, self).__init__(x,y,40,velocity_hand)
        self.status=status
        self.chasing_drone=None
        self.tier_0_position=self.get_hand_tier0_position(side,map_x_size,map_y_size)



    def get_hand_tier0_position(self, side,map_x_size,map_y_size):


        if side.LEFT:
            return Point(map_x_size*0.25,map_y_size*0.2)
        else:
            return Point(map_x_size*0.75,map_y_size*0.2)
