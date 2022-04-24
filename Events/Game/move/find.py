import typing

from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.tools.FluidCel import FluidCell
from Events.Game.move.algos.GameObjects.tools.point import Point
from Events.Game.move.algos.GameObjects.tools.settings import Settings
from Events.Game.move.check import check_if_point_is_in_range
from Events.Game.move.time import get_travel_time_to_point



def find_target_for_jump(path:typing.List[FluidCell],uav_postion:Point,hand_position:Point,uav_velocity,hand_jump_velocity,settings:Settings,hand:Hand):
    target_cell=None
    time=0
    last_position=uav_postion
    for cell in path:
        uav_time=time+get_travel_time_to_point(last_position,cell.position,uav_velocity)
        hand_time=get_travel_time_to_point(hand_position,cell.position,hand_jump_velocity)
        if uav_time>hand_time:
            target_cell=cell
            break
        time=uav_time
        last_position=cell.position
    if target_cell==None:
        return target_cell
    from Events.hand_chase import get_max_hand_range_in_x
    if not check_if_point_is_in_range(target_cell.position,hand,settings):
        return None
    max_hand_y=get_max_hand_range_in_x(hand.side,settings.minimal_hand_range,settings.r_of_LR,settings.map_size_x,target_cell.position.x,settings)
    target_position=target_cell.position
    if target_position.y>max_hand_y:
        target_position=Point(target_cell.position.x,max_hand_y)
    return target_position
