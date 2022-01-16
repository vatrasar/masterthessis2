import math
from random import Random

from Events.Game.GameObjects.point import Point
from Events.Game.settings import Settings


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
    return Point(map_width*rand.random(),tier1_distance)
