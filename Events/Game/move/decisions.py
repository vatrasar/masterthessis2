from random import Random
import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.algos.naive_algo import Naive_Algo
from Events.Game.move.check import check_if_algo_target_reached


def decide_whether_uav_attack(mode,prob_of_attack,rand:Random,uav:Uav,settings:Settings,naive_alog:Naive_Algo,uav_list):
    """

    :param mode:
    :param prob_of_attack:
    :param rand:
    :return true if attack false if not
    """
    if(settings.exploitation_type=="random" and settings.mode==Modes.EXPLOITATION):
        x=rand.random()
        if x<prob_of_attack:
            return True
        else:
            return False
    else:

        if naive_alog.get_target_postion(uav.index,rand,settings,uav_list)==None:
            naive_alog.choose_new_target(settings,rand,uav.index,uav_list)


        if check_if_algo_target_reached(uav.position,naive_alog.get_target_postion(uav.index,rand,settings,uav_list),settings):
            if naive_alog.choose_random[uav.index]==False:
                naive_alog.choose_new_target(settings,rand,uav.index,uav_list)
                return False
            # check_if_algo_target_reached(uav.position,uav.naive_algo.get_target_postion(uav.index,rand,settings),settings)
            return True
        else:
            return False


def decide_whether_uav_back_on_tier2(prob_of_return_to_T2,rand:Random,uav_list:typing.List[Uav],dodge_radius,settings:Settings,uav:Uav):
    # if len(uav_list)==2:
    #     if uav_list[0].status==UavStatus.TIER_1 and uav_list[1].status==UavStatus.TIER_1:
    #         if get_distance_on_tier1(uav_list[0].position,uav_list[1].position)<dodge_radius*4 :
    #             return True
    # if settings.mode=="list" and uav.naive_algo.is_limit_reached():
    #     return True
    if settings.tier2_mode==True:
         return True

    x=rand.random()
    if x<prob_of_return_to_T2:
        return True
    else:
        return False


