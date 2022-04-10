from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.algos.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import chekc_if_uav_goes_to_trash
from Events.Game.move.distance import get_horizontal_distance
from Events.Game.move.get_position import get_point_on_tier1


def check_colisions(event_owner:MovableObject,uavs_list,target_postion:Point,dodge_radius,save_distance):
    if len(uavs_list)<2:
        return (False,None,None)
    secound_uav:Uav=None

    for uav in uavs_list:#find another uav
        if uav!=event_owner:
            secound_uav=uav

    if is_cross_on_tier1(event_owner, secound_uav, target_postion,save_distance):
        distance= get_horizontal_distance(event_owner.position, secound_uav.position) / 2.0
        start_dodge_postion=get_point_on_tier1(event_owner.position,distance-dodge_radius,secound_uav.position)

        if distance<dodge_radius:
            start_dodge_postion=event_owner.position
        colision_point=get_point_on_tier1(event_owner.position,distance,secound_uav.position)
        dodge_position=Point(colision_point.x,colision_point.y+dodge_radius)
        return (True,start_dodge_postion,dodge_position)
    else:
        return (False,None,None)


def is_cross_on_tier1(event_owner, secound_uav, target_postion,save_distance):
    if event_owner.status==UavStatus.TIER_2 or  secound_uav.status==UavStatus.TIER_2 or secound_uav.status==UavStatus.DODGE or secound_uav.status==UavStatus.BACK_FROM_DODGE or secound_uav.status==UavStatus.PLANED_DODGE:
        return False
    #are on collision course
    distance_to_potentioal_crash= get_horizontal_distance(event_owner.position, secound_uav.position) / 2.0
    potential_crash_point=get_point_on_tier1(event_owner.position,distance_to_potentioal_crash,secound_uav.position)
    if chekc_if_uav_goes_to_trash(event_owner, potential_crash_point, target_postion,save_distance) and chekc_if_uav_goes_to_trash(secound_uav, potential_crash_point, secound_uav.target_position,save_distance):
        return True
    else:
        return False








