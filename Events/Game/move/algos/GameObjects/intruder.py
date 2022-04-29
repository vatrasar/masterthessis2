from Events.Game.move.algos.GameObjects.movableObject import MovableObject


class Intruder(MovableObject):
    def __init__(self, x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position,energy):
        super().__init__(x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position)
        self.energy=energy
        self.start_jump_time=0
    def consume_energy(self,intruder_energy_consumption,time):
        time_delta=time-self.start_jump_time
        self.energy=self.energy-time_delta*intruder_energy_consumption
