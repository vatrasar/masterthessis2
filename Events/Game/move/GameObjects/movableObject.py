from Events.Game.move.GameObjects.tools.point import Point


class MovableObject():
    def __init__(self,x,y,status,object_size,velocity,last_postion_update_time,next_status,target_position):
        self.position=Point(x,y)
        self.status=status
        self.object_size=object_size
        self.velocity=float(velocity)
        self.last_postion_update_time=last_postion_update_time
        self.next_status=next_status
        self.target_position=target_position



    def set_status(self,new_status):
        self.status=new_status

    def set_next_event(self,next_event):
        self.next_event=next_event

    def set_new_position(self, target_position,time):
        self.position=target_position
        self.last_postion_update_time=time

    def delete_current_event(self,event_list):
        if self.next_event!=None:
            event_list.delete_event(self.next_event)
        self.next_event=None




