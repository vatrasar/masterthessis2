import typing

from Events.Game.move.GameObjects.tools.FluidCel import FluidCell
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.time import get_travel_time_to_point


def find_target_for_jump(path:typing.List[FluidCell],uav_postion:Point,hand_position:Point,uav_velocity,hand_jump_velocity):
    for cell in path:
        uav_time=get_travel_time_to_point(uav_postion,cell.position,uav_velocity)
        hand_time=get_travel_time_to_point(hand_position,cell.position,hand_jump_velocity)
        if uav_time>hand_time:
            return cell

    return path[-1]