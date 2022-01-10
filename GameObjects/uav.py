from GameObjects.movableObject import MovableObject


class Uav(MovableObject):
    def __init__(self,x,y,status, points,velocity,index):
        super(Uav, self).__init__(x,y,40,velocity)
        self.points=points
        self.last_path=[]
        self.status=status
        self.index=index
        self.action = -1
