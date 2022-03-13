import typing

from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, HandStatus
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.distance import get_horizontal_distance, get_2d_distance
from Events.Game.move.get_position import get_point_based_on_time
from Events.Game.move.time import get_travel_time_to_point


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

def check_if_uav_is_in_range(uav:Uav,hand:Hand,settings):
    from Events.hand_chase import get_max_hand_range_in_x
    max_y_range=get_max_hand_range_in_x(hand.side,settings.minimal_hand_range,settings.r_of_LR,settings.map_size_x,uav.position.x)
    if max_y_range>uav.position.y:
        return True
    else:
        return False

def check_if_path_save(path, uav:Uav, hand:Hand, settings:Settings):
    jump_velocity=settings.jump_ratio*settings.velocity_hand
    if hand==None:
        return True
    if hand.status!=HandStatus.JUMP:
        return True

    travel_time=0
    last_postion=uav.position
    for cell in path:
        travel_time=travel_time+get_travel_time_to_point(last_postion,cell.position,settings.v_of_uav)
        target_point=get_point_based_on_time(hand.position, travel_time, hand.target_position, jump_velocity)
        if get_2d_distance(hand.position,target_point)<settings.uav_size*2:
            return False

    return False

def check_if_point_safe(arrive_time, hand, cell, settings):
    jump_velocity=settings.jump_ratio*settings.velocity_hand
    target_point=get_point_based_on_time(hand.position, arrive_time, hand.target_position, jump_velocity)
    if get_2d_distance(cell.position,target_point)<settings.uav_size*2:
        return False
    else:
        return True