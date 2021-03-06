from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import Sides, HandStatus
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.movableObject import MovableObject
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point



class Hand(MovableObject):
    def __init__(self,status,velocity_hand,side:Sides,map_x_size,map_y_size,last_postion_update_time,next_status,target_postion,x=0,y=0):
        super(Hand, self).__init__(x,y,status,40,velocity_hand,last_postion_update_time,next_status,target_postion)


        self.side=side
        self.tier_0_position=self.get_hand_tier0_position(side,map_x_size,map_y_size/2)
        self.position=self.tier_0_position
        self.next_event=None
        if side==Sides.LEFT:
            self.color="blue"
        else:
            self.color="purple"
        from Events.Game.move.algos.GameObjects.uav import Uav
        self.target_uav:Uav=None
        self.energy_consumed=0
        self.start_energy_time=0





    def beggin_energy_time(self,time,type):
        self.start_energy_time=time
        self.energy_consumptiont_type=type

    def get_hand_tier0_position(self, side,map_x_size,map_y_size):


        if Sides.LEFT==side:
            return Point(map_x_size*0.25,map_y_size*0.5)
        else:
            return Point(map_x_size*0.75,map_y_size*0.5)

    def ste_target_uav(self,target_uav):
        self.target_uav=target_uav

    def start_chasing(self, uav):
        self.target_uav=uav
        uav.chasing_hand=self

    def stop_chasing(self):
        self.target_uav.chasing_hand=None
        self.target_uav=None

    def set_chasing_drone(self,drone_to_chase):
        self.chasing_drone=drone_to_chase


