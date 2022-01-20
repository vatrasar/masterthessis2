import math
from random import Random

from Events.Game.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.GameObjects.tools.move_tools import get_distance_on_tier1
from Events.Game.GameObjects.tools.point import Point


def decide_whether_uav_attack(mode,prob_of_attack,rand:Random):
    """

    :param mode:
    :param prob_of_attack:
    :param rand:
    :return true if attack false if not
    """
    if(mode=="RW-RA"):
        x=rand.random()
        if x<prob_of_attack:
            return True
        else:
            False

def decide_whether_uav_back_on_tier2(prob_of_return_to_T2,rand:Random):
    x=rand.random()
    if x<prob_of_return_to_T2:
        return True
    else:
        False


def get_d_t_arrive_poison(is_arrive_deterministic,lambda1):
    d_ta_arrive=0
    if is_arrive_deterministic:
        d_ta_arrive = 1.0 / lambda1
    else:
        d_ta_arrive = 1.0 / lambda1* math.log(2, math.e)
    return d_ta_arrive


def get_random_position_on_tier1(rand:Random,map_width,tier1_distance):
    x=(map_width/2.0)*rand.random()
    if rand.randint(0,1)==1:
        x=-x
    return Point(x,tier1_distance)


def choose_travel_direction():
    return Sides.RIGHT



def get_travel_time_on_tier1(target_postion:Point,current_position:Point,drone_velocity):


    distance=get_distance_on_tier1(current_position,target_postion)
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


