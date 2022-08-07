from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Modes
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import Sides, UavStatus
from Events.Game.move.algos.GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index,last_postion_update_time,next_status,target_postion,energy,last_points,points_without_transhold,points_without_transhold_sum):
        super(Uav, self).__init__(x,y,status,40,velocity,last_postion_update_time,next_status,target_postion)


        self.index=index
        self.action =-1
        self.direction=Sides.RIGHT
        self.chasing_hand:Hand=None
        self.points=0
        self.points=points
        self.attack_started_from_tier2=True
        self.energy=energy
        self.start_energy_time=0
        self.energy_consumptiont_type=UavStatus.TIER_2
        self.target_with_points=None
        self.best_points=last_points
        self.last_updated_energy=0
        self.points_without_transhold=points_without_transhold
        self.points_without_transhold_sum=points_without_transhold_sum


    def beggin_energy_time(self,time,type):
        self.start_energy_time=time
        self.energy_consumptiont_type=type


    def consume_energy(self,settings,time):
        time_delta=time-self.start_energy_time
        ratio=0
        if settings.mode==Modes.LEARNING:
            return
        if self.energy_consumptiont_type==UavStatus.ON_ATTACK:
            ratio=settings.uav_energy_energy_cost_attack
        elif self.energy_consumptiont_type==UavStatus.TIER_1:
            ratio=settings.uav_energy_energy_cost_tier1
        elif self.energy_consumptiont_type==UavStatus.TIER_2:
            ratio=settings.uav_energy_energy_cost_tier2
        energy_consumption=ratio*time_delta

        self.energy=self.energy+energy_consumption

    def cancel_attack(self,settings):
        if settings.mode==Modes.EXPLOITATION:
            self.points_without_transhold=0
            self.points_without_transhold_sum=self.points_without_transhold+self.points_without_transhold_sum
    def asign_points(self, points,settings):
        if settings.mode==Modes.EXPLOITATION:
            self.points_without_transhold=points
            self.points_without_transhold_sum=self.points_without_transhold+self.points_without_transhold_sum
            if points<settings.reward_threshold:
                points=0



            self.points=self.points+points
            if self.best_points<points:
                self.best_points=points

        else:
            self.points=self.points+points

            if self.best_points<points:
                self.best_points=points
