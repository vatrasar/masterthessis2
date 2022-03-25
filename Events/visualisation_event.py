import logging
from random import Random
from tkinter import Tk, Canvas

from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus, Sides, HandStatus
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.event import Event
from Events.Game.move.GameObjects.tools.gui_tools import create_circle, transfer_point_to_gui_format, create_squer, \
    create_line


class Visualisation_event(Event):
    def __init__(self, time_of_event, event_owner, tk_master:Tk,canvas:Canvas,game_state:GameState):
        super().__init__(time_of_event, event_owner, tk_master,game_state)

        self.canvas=canvas
        self.visualisation_delay=40
        # if time_of_event>100:
        #     self.visualisation_delay=200




    def handle_event(self, event_list, settings: Settings, rand: Random,iteration_function):
        super().handle_event(event_list, settings, rand,iteration_function)
        self.canvas.delete("all")
        self.game_state.update_postions(self.time_of_event,settings.v_of_uav,settings.velocity_hand,self.event_owner,settings.jump_ratio,settings,event_list)
        event_time=self.time_of_event+settings.visualzation_update_interval
        visualisation_event=Visualisation_event(event_time, self.event_owner, self.tk_master, self.canvas, self.game_state)
        event_list.append_event(visualisation_event,UavStatus.VISUALISE)

        self.draw_all_elements(settings.uav_size,settings.map_size_x,settings.hand_size,settings.r_of_LR,settings.intuder_size,settings.minimal_hand_range,settings)


        # self.canvas.update()





    def draw_all_elements(self,uav_size,map_size_x,hand_size,hand_range,intruder_size,minimal_hand_range,settings:Settings):

        create_squer(0,0,map_size_x, intruder_size,self.canvas)#target
        # create_circle(122,267,hand_size,self.canvas,"black") #marker
        for uav in self.game_state.uav_list:#uavs
            if uav.status!=UavStatus.DEAD and uav.status!=UavStatus.TIER_2:

                # create_circle(uav.position.x, uav.position.y,settings.safe_margin,self.canvas,"black")
                create_circle(uav.position.x, uav.position.y,uav_size,self.canvas,"green")







        for hand in self.game_state.hands_list:#hands
            if hand.status==HandStatus.JUMP:
                create_circle(hand.position.x, hand.position.y,hand_size,self.canvas,"red")
            else:
                create_circle(hand.position.x, hand.position.y,hand_size,self.canvas,hand.color)


            #ranges boxes
            boxes=[]

            if hand.side==Sides.LEFT:

                up_start=Point(0,hand_range)
                up_end=Point(map_size_x/2.0,hand_range)
                boxes.append((up_start,up_end,hand.color))
                right_start=Point(map_size_x/2.0,hand_range)
                right_end=Point(map_size_x,minimal_hand_range)
                boxes.append((right_start,right_end,hand.color))
            else:
                up_start=Point(map_size_x/2.0,hand_range)
                up_end=Point(map_size_x,hand_range)
                boxes.append((up_start,up_end,hand.color))
                left_start=Point(map_size_x/2.0,hand_range)
                left_end=Point(0,minimal_hand_range)
                boxes.append((left_start,left_end,hand.color))

            for box in boxes:
                create_line(box[0],box[1],self.canvas,box[2])









