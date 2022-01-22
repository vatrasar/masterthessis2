from random import Random
import typing

from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.distance import get_distance_on_tier1


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
            return False

def decide_whether_uav_back_on_tier2(prob_of_return_to_T2,rand:Random,uav_list:typing.List[Uav],dodge_radius):
    # if len(uav_list)==2:
    #     if uav_list[0].status==UavStatus.TIER_1 and uav_list[1].status==UavStatus.TIER_1:
    #         if get_distance_on_tier1(uav_list[0].position,uav_list[1].position)<dodge_radius*4 :
    #             return True
    x=rand.random()
    if x<prob_of_return_to_T2:
        return True
    else:
        return False


