import math
from random import Random

from Events.Game.move.algos.GameObjects.tools.point import Point
from Events.Game.move.distance import get_horizontal_distance, get_2d_distance


def get_travel_time_on_tier1(target_postion:Point,current_position:Point,drone_velocity):


    distance=get_horizontal_distance(current_position, target_postion)
    time=distance/drone_velocity


    distance=0
    # if direction==Sides.RIGHT:
    #     if target_postion.x<current_position.x:
    #         distance=map_size-current_position.x+target_postion.x
    #     else:
    #         distance=target_postion.x-current_position.x
    #
    #
    # else:
    #     if target_postion.x>current_position.x:
    #         distance=map_size-target_postion.x+current_position.x
    #     else:
    #         distance=current_position.x-target_postion.x
    #
    # time=distance/float(drone_velocity)
    return time


def get_d_t_arrive_poison(is_arrive_deterministic,lambda1,rand:Random):
    d_ta_arrive=0
    if is_arrive_deterministic:
        d_ta_arrive = 1.0 / lambda1
    else:
        d_ta_arrive = -(1.0 / lambda1)* math.log(rand.random(), math.e)
    return d_ta_arrive


def get_travel_time_to_point(source:Point,target:Point,velocity):
    distance=get_2d_distance(source,target)
    time=distance/velocity
    return time
