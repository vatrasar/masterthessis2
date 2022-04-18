from random import Random
from tkinter import Tk, Canvas

from Events.Game.move.GameObjects.algos.tools.enum.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.event import Event
from Events.Game.move.GameObjects.algos.tools.gui_tools import create_circle, create_squer, \
    create_line

from PIL import Image
class Visualisation_event(Event):
    def __init__(self, time_of_event, event_owner, tk_master:Tk,canvas:Canvas,game_state:GameState,visualisation_delay):
        super().__init__(time_of_event, event_owner, tk_master,game_state)

        self.canvas=canvas
        self.visualisation_delay=visualisation_delay
        # if time_of_event>1950:
        #     self.visualisation_delay=200


    def save_to_file(self,time):
        self.canvas.postscript(file="./history/temp/image"+str(time)+".ps", colormode='color')
        img = Image.open("./history/temp/image"+str(time)+".ps")
        img.save("./history/history/image"+str(time)+'.png', 'png')


    def handle_event(self, event_list, settings: Settings, rand: Random,iteration_function):
        super().handle_event(event_list, settings, rand,iteration_function)
        self.canvas.delete("all")
        self.game_state.update_postions(self.time_of_event,settings.v_of_uav,settings.velocity_hand,self.event_owner,settings.jump_ratio,settings,event_list)
        event_time=self.time_of_event+settings.visualzation_update_interval
        visualisation_event=Visualisation_event(event_time, self.event_owner, self.tk_master, self.canvas, self.game_state,settings.visualisation_speed)
        event_list.append_event(visualisation_event,UavStatus.VISUALISE)

        self.draw_all_elements(settings.uav_size,settings.map_size_x,settings.hand_size,settings.r_of_LR,settings.intuder_size,settings.minimal_hand_range,settings)
        if self.time_of_event%1==0 and self.time_of_event>3100 and settings.visualisation==2:
            self.save_to_file(self.time_of_event)

        # self.canvas.update()





    def draw_all_elements(self,uav_size,map_size_x,hand_size,hand_range,intruder_size,minimal_hand_range,settings:Settings):

        for point in settings.lif_of_invisible:

            create_circle(point.x,point.y,point.r,self.canvas,"grey")
        if len(self.game_state.hands_list)==2:
            squer_bootm_start=0
            squer_top_end=map_size_x/2.0
            if self.game_state.hands_list[0].side==Sides.RIGHT:
                self.game_state.hands_list.reverse()
            for hand in self.game_state.hands_list:
                create_squer(squer_bootm_start,0,squer_top_end, intruder_size,self.canvas,hand.color)
                squer_bootm_start=map_size_x/2.0
                squer_top_end=map_size_x
        else:
            create_squer(0,0,map_size_x, intruder_size,self.canvas,"blue")#target
        # create_circle(1011,396,hand_size,self.canvas,"black") #marker
        for uav in self.game_state.uav_list:#uavs
            if uav.status!=UavStatus.DEAD and uav.status!=UavStatus.TIER_2:

                # create_circle(uav.position.x, uav.position.y,settings.safe_margin*1.2,self.canvas,"black")
                create_circle(uav.position.x, uav.position.y,uav_size,self.canvas,"green")








        for hand in self.game_state.hands_list:#hands
            if hand.status==HandStatus.JUMP:
                create_circle(hand.position.x, hand.position.y,hand_size,self.canvas,"red")
            else:
                create_circle(hand.position.x, hand.position.y,hand_size,self.canvas,hand.color)


            #ranges boxes
            boxes=[]

            if hand.side==Sides.LEFT:

                up_start = Point(0, hand_range)
                up_end = Point(map_size_x/2.0,hand_range)
                boxes.append((up_start, up_end, hand.color))
                left_start=Point(map_size_x/2.0,hand_range)
                left_end=settings.left_box

                down_start=settings.left_box
                down_end=Point(settings.left_box.x,intruder_size)
                boxes.append((left_start, left_end, hand.color))
                boxes.append((down_start, down_end, hand.color))
            else:
                up_start=Point(map_size_x/2.0,hand_range)
                up_end=Point(map_size_x,hand_range)
                boxes.append((up_start,up_end,hand.color))

                right_start = Point(map_size_x/2.0,hand_range)
                right_end = settings.right_box
                boxes.append(( right_start,right_end,hand.color))
                down_start=settings.right_box
                down_end=Point(settings.right_box.x+1,intruder_size)
                boxes.append((down_start, down_end, hand.color))

            for box in boxes:
                create_line(box[0],box[1],self.canvas,box[2])









