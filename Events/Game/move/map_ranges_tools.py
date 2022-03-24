from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.tools.point import Point



def put_point_in_range_of_map(point:Point,max_range_of_map_x,max_range_of_map_y):

    if point.x<0:
        point.x=0

    if point.x>max_range_of_map_x:
        point.x=max_range_of_map_x

    if point.y<0:
        point.y=0

    if point.y>max_range_of_map_y:
        point.y=max_range_of_map_y


def get_max_hand_range_in_x(hand_side:Sides,minimal_hand_range,maximum_hand_range,map_size_x,x):


    if hand_side==Sides.LEFT:
        if x>map_size_x/2.0:

            a=(maximum_hand_range-minimal_hand_range)/(map_size_x/2.0-map_size_x)
            b=maximum_hand_range-a*map_size_x/2.0



            return x*a+b
        else:
            return  maximum_hand_range

    else:
        if x>map_size_x/2.0:
            return  maximum_hand_range
        else:

            a=(minimal_hand_range-maximum_hand_range)/(0-map_size_x/2.0)
            b=minimal_hand_range
            return x*a+b
