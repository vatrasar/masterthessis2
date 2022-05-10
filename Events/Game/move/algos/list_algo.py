from random import Random

from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.get_position import get_random_position_on_tier1


def list_algo_new_targets(settings:Settings,rand:Random):
    target1=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
    target2=get_random_position_on_tier1(rand,settings.map_size_x-2,settings.tier1_distance_from_intruder)
    return (target1,target2)
