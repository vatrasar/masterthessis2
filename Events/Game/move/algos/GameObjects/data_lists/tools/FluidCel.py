from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point


class FluidCell():
    def __init__(self,arrive_time,position,i_x,i_y):
        self.parrent:FluidCell=None
        self.uav_arrive_time=arrive_time
        self.points=0
        self.is_safe=False
        self.position:Point=position
        self.is_visited=False
        self.index=Point(i_x,i_y)
        self.is_queue=False


    def set_parrent(self, cell):
        self.parrent=cell

    def set_uav_arrive_time(self, uav_arrive_time):
        self.uav_arrive_time=uav_arrive_time

    def set_points(self, value):
        self.points=value

    def set_visited(self, new_value):
        self.is_visited=new_value

    def set_is_safe(self, new_value):
        self.is_safe=new_value
