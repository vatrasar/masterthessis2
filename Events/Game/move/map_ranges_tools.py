from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings


def put_point_in_range_of_map(point:Point,max_range_of_map_x,max_range_of_map_y):

    if point.x<0:
        point.x=0

    if point.x>max_range_of_map_x:
        point.x=max_range_of_map_x

    if point.y<0:
        point.y=0

    if point.y>max_range_of_map_y:
        point.y=max_range_of_map_y
def get_max_x_in_range(hand_side:Sides,settings:Settings,x):
    if hand_side==Sides.LEFT:
        if x>settings.left_box.x:
            return settings.left_box.x
        else:
            return x
    if hand_side==Sides.RIGHT:
        if x<settings.right_box.x:
            return settings.right_box.x
        else:
            return x


def get_max_hand_range_in_x(hand_side:Sides,minimal_hand_range,maximum_hand_range,map_size_x,x,settings:Settings):


    if hand_side==Sides.LEFT:
        if x>map_size_x/2.0:

            a=(maximum_hand_range-settings.left_box.y)/(map_size_x/2.0-settings.left_box.x)
            b=maximum_hand_range-a*map_size_x/2.0



            return x*a+b
        else:
            return  maximum_hand_range

    else:
        if x>map_size_x/2.0:
            return  maximum_hand_range
        else:

            a=(settings.right_box.y-maximum_hand_range)/(settings.right_box.x-map_size_x/2.0)
            b=settings.right_box.y-a*settings.right_box.x
            return x*a+b
