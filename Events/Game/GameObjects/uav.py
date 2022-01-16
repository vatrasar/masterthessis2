from Events.Game.GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index):
        super(Uav, self).__init__(x,y,status,40,velocity)
        self.points=points
        self.last_path=[]
        self.index=index
        self.action = -1
