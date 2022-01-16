from Events.Game.GameObjects.point import Point


class MovableObject():
    def __init__(self,x,y,status,object_size,velocity):
        self.position=Point(x,y)
        self.next_event=None
        self.status=status
        self.object_size=object_size
        self.velocity=float(velocity)



    def set_status(self,new_status):
        self.status=new_status

    def set_next_event(self,next_event):
        self.next_event=next_event

    def set_new_position(self, target_position):
        self.position=target_position



