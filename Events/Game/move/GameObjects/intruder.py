from Events.Game.move.GameObjects.tools.enum.enumStatus import Sides
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.uav import Uav


class Intruder(MovableObject):
    def __init__(self, x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position):
        super().__init__(x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position)
