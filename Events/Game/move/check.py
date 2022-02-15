import typing

from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.distance import get_horizontal_distance


def check_distance_between_uav(uav_list:typing.List[Uav],save_distance):
    if len(uav_list)<2:
        return True
    if get_horizontal_distance(uav_list[0].position, uav_list[1].position)<save_distance:
        return False
    else:
        return True

def check_if_same_move_direction(event_owner:MovableObject,uav_list:typing.List[Uav],target_postion):
    if len(uav_list)<2:
        return False
    secound_uav=None
    for uav in uav_list:
        if uav!=event_owner:
            secound_uav=uav

    if event_owner.status==UavStatus.TIER_2 or  secound_uav.status==UavStatus.TIER_2:
        return False

    vector1=target_postion.x-event_owner.position.x
    vector2=secound_uav.target_position.x-secound_uav.position.x
    if vector1*vector2>0:
        return True
    else:
        return False



def chekc_if_uav_goes_to_trash(event_owner, potential_crash_point, target_postion,save_distance):
    distance_to_trash=get_horizontal_distance(event_owner.position, potential_crash_point)
    distance_to_target=get_horizontal_distance(event_owner.position, target_postion)
    if distance_to_trash>distance_to_target+save_distance:
        return False
    vector_to_crash_point = potential_crash_point.x - event_owner.position.x
    vecotr_to_target = target_postion.x - event_owner.position.x
    if vecotr_to_target*vector_to_crash_point>0:
        return True
    else:
        return False


def check_if_in_safe_distance(uav,hands_list,safe_margin):
    for hand in hands_list:
        if get_horizontal_distance(uav.position,hand.position)<safe_margin:
            return False
    return True

def check_if_cell_is_on_map(cell:Point,max_index_x,max_index_y):
    if cell.x<max_index_x and cell.x>=0 and cell.y<max_index_y and cell.y>=0:
        return True
    else:
        return False