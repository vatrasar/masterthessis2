from Events.Game.move.GameObjects.movableObject import MovableObject


class Intruder(MovableObject):
    def __init__(self, x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position):
        super().__init__(x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position)
