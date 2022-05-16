from Events.Game.gameState import GameState
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import UavStatus
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.intruder import Intruder
from Events.Game.move.algos.naive_algo import Naive_Algo
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav


class GameStateStac():
    def __init__(self,game_state:GameState,settings:Settings):

        self.dead_uav_list=[]
        #hands
        self.hands_list=[]
        naive_algo=Naive_Algo(0,9,0,settings,None,None,None,None)
        for hand in game_state.hands_list:
            hand_copy=Hand(hand.status,hand.velocity,hand.side,settings.map_size_x,settings.map_size_y,hand.next_status,hand.target_position,hand.position.x,hand.position.y)
            hand_copy.position.x=hand.position.x
            hand_copy.position.y=hand.position.y
            self.hands_list.append(hand_copy)


        #drones
        self.uav_list=[]
        for uav in game_state.uav_list:


            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity,uav.index,uav.last_postion_update_time,uav.next_status,uav.target_position,uav.energy,uav.last_points)
            uav_copy.points=uav.points
            self.uav_list.append(uav_copy)

        # for uav in game_state.list_of_dead_uavs:
        #     uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity,uav.index,uav.last_postion_update_time,uav.next_status,uav.target_position,naive_algo,None)
        #     uav_copy.points=uav.points
        #     self.dead_uav_list.append(uav_copy)

        if len(game_state.list_of_dead_uavs) > 0:
            for uav in game_state.list_of_dead_uavs:
                uav_copy = Uav(uav.position.x, uav.position.y, uav.status, uav.points, uav.velocity, uav.index,uav.last_postion_update_time,uav.next_status,uav.target_position,settings.uav_energy,uav.last_points)
                self.uav_list.append(uav_copy)
        if len(self.uav_list)>1 and self.uav_list[0].index>self.uav_list[1].index:
            self.uav_list.reverse()


        self.t_curr=game_state.t_curr
        self.intruder=Intruder(0,0,UavStatus.WAIT,20,20,0,UavStatus.WAIT,Point(0,0,),game_state.intruder.energy)


