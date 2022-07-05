from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import HandStatus
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.movableObject import MovableObject


class Intruder(MovableObject):
    def __init__(self, x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position,energy):
        super().__init__(x, y, status, object_size, velocity, last_postion_update_time, next_status, target_position)
        self.energy=energy
        self.last_updated_energy=0



    def consume_energy(self,settings:Settings,end_time,start_time,energy_consumptiont_type):
        time_delta=end_time-start_time
        ratio=0
        if settings.mode==Modes.LEARNING:
            ratio=0
        elif energy_consumptiont_type==HandStatus.JUMP:
            ratio=settings.jump_ratio
        elif energy_consumptiont_type==HandStatus.CHASING:
            ratio=settings.intruder_energy_cost_chasing
        elif energy_consumptiont_type==HandStatus.WAIT:
            ratio=0


        self.energy=self.energy+time_delta*ratio



    def consume_change_decision(self,settings:Settings):
        if settings.mode==Modes.LEARNING:
            ratio=0
        else:
            self.energy=self.energy+settings.intruder_energy_cost_of_reaction
