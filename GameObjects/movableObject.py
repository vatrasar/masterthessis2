from GameObjects.point import Point


class MovableObject():
    def __init__(self,x,y,object_size,velocity):
        self.position=Point(x,y)
        self.next_event=None
        self.object_size=object_size
        self.velocity=float(velocity)
