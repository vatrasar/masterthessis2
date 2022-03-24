import logging
import typing

from Events.Game.gameState import GameState
from Events.Game.game_state_stac import GameStateStac
from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.tools.other_tools import create_folder
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.distance import get_2d_distance
from matplotlib import pyplot as plt
import csv

class Statistics():

    def __init__(self):
        self.game_states_list:typing.List[GameStateStac]=[]
    def update_stac(self,game_state,settings):

        to_svae=GameStateStac(game_state,settings)
        self.settings=settings

        self.game_states_list.append(to_svae)






    def save(self):
        logger = logging.getLogger('matplotlib')
        logger2 = logging.getLogger('PIL')
        logger.setLevel(level=logging.WARNING)
        save_directory = create_folder("./charts")
        logger2.setLevel(level=logging.WARNING)

        # distance between uav
        x=[]
        y=[]
        for state in self.game_states_list:
            if state.uav_list[0].status!=UavStatus.DEAD and state.uav_list[1].status!=UavStatus.DEAD and state.uav_list[0].status!=UavStatus.TIER_2 and state.uav_list[1].status!=UavStatus.TIER_2 :
                distance=get_2d_distance(state.uav_list[0].position,state.uav_list[1].position)
                x.append(state.t_curr)
                y.append(distance)
        plt.plot(x,y)
        plt.savefig(save_directory+"/"+"distance_between_uav.svg")
        plt.clf()
        import os



        #distance to hands
        x = []
        y = []
        xr1, yr1, xl1, yl1 = [], [], [], []
        xr2, yr2, xl2, yl2 = [], [], [], []
        if self.settings.hands_number > 0:
            for state in self.game_states_list:



                if len(state.uav_list)>0 and state.uav_list[0].status!=UavStatus.TIER_2:#hand1
                    if len(state.uav_list)>0 and state.uav_list[0].status!=UavStatus.TIER_2:#uav1
                       if state.uav_list[0].status!=UavStatus.DEAD:
                            distance1=get_2d_distance(state.hands_list[0].position,state.uav_list[0].position)
                            xr1.append(state.t_curr)
                            yr1.append(distance1)

                    if len(state.uav_list)>1 and state.uav_list[1].status!=UavStatus.TIER_2:
                        if state.uav_list[1].status != UavStatus.DEAD:
                            distance1 = get_2d_distance(state.hands_list[0].position, state.uav_list[1].position)

                            xr2.append(state.t_curr)
                            yr2.append(distance1)

                if len(state.uav_list)>0 and len(state.hands_list)>1 and state.uav_list[0].status!=UavStatus.TIER_2:#hand2
                    if len(state.uav_list) > 0 and state.uav_list[0].status != UavStatus.TIER_2: # uav1
                        if state.uav_list[0].status!=UavStatus.DEAD:
                            distance1 = get_2d_distance(state.hands_list[1].position, state.uav_list[0].position)
                            xl1.append(state.t_curr)
                            yl1.append(distance1)

                    if len(state.uav_list) > 1 and state.uav_list[1].status != UavStatus.TIER_2:
                        if state.uav_list[1].status != UavStatus.DEAD:
                            distance1 = get_2d_distance(state.hands_list[1].position, state.uav_list[1].position)

                            xl2.append(state.t_curr)
                            yl2.append(distance1)
            #plot
            if len(xl1)>0:
                plt.plot(xl1, yl1)
                plt.plot(xl2, yl2)
                plt.legend(["uav1","uav2"])
                plt.savefig(save_directory + "/" + "distanceToL.svg")
                plt.clf()

            if len(xr1) > 0:
                plt.plot(xr1, yr1)
                plt.plot(xr2, yr2)
                plt.legend(["uav1","uav2"])
                plt.savefig(save_directory + "/" + "distanceToR.svg")
                plt.clf()


        #points of uavs
        x1,x2=[],[]
        y1,y2=[],[]
        x_sum,y_sum=[],[]
        for state in self.game_states_list:
            if len(state.uav_list)>0:
                x1.append(state.t_curr)
                y1.append(state.uav_list[0].points)

            if len(state.uav_list)>1:
                x2.append(state.t_curr)
                y2.append(state.uav_list[1].points)
                x_sum.append(state.t_curr)
                y_sum.append(state.uav_list[1].points+state.uav_list[0].points)
        if len(x1) > 0:
            plt.plot(x1, y1)
            plt.plot(x2, y2)

            plt.legend(["uav1", "uav2"])
            plt.savefig(save_directory + "/" + "points.svg")
            plt.clf()

            plt.plot(x_sum, y_sum)
            plt.savefig(save_directory + "/" + "pointsSum.svg")
            plt.clf()

        # plt.plot(x,y)
        # plt.savefig(save_directory+"/"+"distance_between_uav.svg")



        #log file
        header_row=["czas","uav1 pozycja","uav1 status"]
        if self.settings.uav_number==2:
            header_row.append("uav2 pozycja")
            header_row.append("uav2 status")

        if self.settings.hands_number>0:
            header_row.append("ręka pozycja")


        if self.settings.uav_number == 2:
            header_row.append("odległość pomiędzy uav")


        rows=[]
        rows.append(header_row)
        for stac in self.game_states_list:
            uav_distance=get_2d_distance(stac.uav_list[0].position,stac.uav_list[1].position)
            row=[]
            row.append(stac.t_curr)
            row.append("(%.2f,%.2f)"%(stac.uav_list[0].position.x,stac.uav_list[0].position.y))
            row.append("%s"%(stac.uav_list[0].status.to_string()))
            if self.settings.uav_number == 2:
                row.append("(%.2f,%.2f)"%(stac.uav_list[1].position.x,stac.uav_list[1].position.y))
                row.append("%s" % (stac.uav_list[1].status.to_string()))
            if self.settings.hands_number > 0:
                row.append("(%.2f,%.2f)" % (stac.hands_list[0].position.x, stac.hands_list[0].position.y))
            if self.settings.uav_number == 2:
                row.append("%.2f" % (uav_distance))
            rows.append(row)


        f=open(save_directory+"/log.csv",mode='w')
        writer=csv.writer(f)
        for row in rows:
            writer.writerow(row)

        f.close()






