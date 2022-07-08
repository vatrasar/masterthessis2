import typing

from Events.Game.gameState import GameState
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.check import check_is_point_on_map
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.evaluation_check import evaluation_check_if_point_safe_time


def evaluate(uav_pos:Point,new_pos:Point,settings:Settings,safe_ratio,game_state:GameState):
    safe_distance_to_take=(settings.uav_size+settings.hand_size)*(settings.safe_distance_ratio)
    time_of_uav_to_take_distance=safe_distance_to_take/settings.v_of_uav
    save_distance=settings.velocity_hand*settings.jump_ratio*time_of_uav_to_take_distance+settings.hand_size
    orginal_save_distance=save_distance
    save_distance=max((settings.uav_size+settings.hand_size),save_distance*safe_ratio)
    move_vector=Point(new_pos.x-uav_pos.x,new_pos.y-uav_pos.y)
    result=0
    actual_pos=Point(new_pos.x,new_pos.y)
    is_minimal_safe=False
    reward=0.5

    while get_2d_distance(actual_pos,uav_pos)<orginal_save_distance*2:
        if not check_is_point_on_map(actual_pos,settings.map_size_x,settings.tier1_distance_from_intruder,settings.intuder_size):
            break

        if  evaluation_check_if_point_safe_time(game_state,actual_pos,settings,uav_pos,save_distance):
            result=result+reward
        else:
            if get_2d_distance(actual_pos,uav_pos)<orginal_save_distance:
                if not is_minimal_safe:
                    reward=0.01
                    is_minimal_safe=True
                    save_distance=max((settings.uav_size+settings.hand_size)*1.1,save_distance*(safe_ratio-0.3))
                else:
                    break

        actual_pos=Point(actual_pos.x+move_vector.x,actual_pos.y+move_vector.y)

    return result

