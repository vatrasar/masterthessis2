from random import Random
import typing

from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_algo_target_reached
from Events.Game.move.distance import get_2d_distance




def decide_whether_uav_attack(mode,prob_of_attack,rand:Random,uav:Uav,settings:Settings):
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
    if (mode=="list"):

        if uav.naive_algo.get_target_postion(uav.index,rand,settings)==None:
            uav.naive_algo.choose_new_target(settings,rand,uav.index)


        if check_if_algo_target_reached(uav.position,uav.naive_algo.get_target_postion(uav.index,rand,settings),settings):

            return True
        else:
            return False
    if (mode=="annealing"):
        # if uav.annealing_algo.choose_random==False:
        #     uav.annealing_algo.choose_new_target(settings,rand,uav.index)
        #     return False
        if uav.annealing_algo.get_target_postion(uav.index,rand,settings)==None:
                uav.annealing_algo.choose_new_target(settings,rand,uav.index)


        if check_if_algo_target_reached(uav.position,uav.annealing_algo.get_target_postion(uav.index,rand,settings),settings):
            print("ITER:"+str(uav.annealing_algo.iteration))
            if uav.annealing_algo.annealing_number_of_iterations<uav.annealing_algo.iteration and uav.annealing_algo.choose_random==False:
                uav.annealing_algo.choose_new_target(settings,rand,uav.index)

                return False
            else:
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


