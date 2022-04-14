from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.algos.naive_algo import Naive_Algo
from Events.Game.move.GameObjects.hand import Hand
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav


class GameStateStac():
    def __init__(self,game_state:GameState,settings:Settings):


        #hands
        self.hands_list=[]
        naive_algo=Naive_Algo(0,9)
        for hand in game_state.hands_list:
            hand_copy=Hand(hand.status,hand.velocity,hand.side,settings.map_size_x,settings.map_size_y,hand.next_status,hand.target_position,hand.position.x,hand.position.y)
            hand_copy.position.x=hand.position.x
            hand_copy.position.y=hand.position.y
            self.hands_list.append(hand_copy)


        #drones
        self.uav_list=[]
        for uav in game_state.uav_list:


            uav_copy=Uav(uav.position.x,uav.position.y,uav.status,uav.points,uav.velocity,uav.index,uav.last_postion_update_time,uav.next_status,uav.target_position,naive_algo,None)
            uav_copy.points=uav.points
            self.uav_list.append(uav_copy)
        if len(game_state.list_of_dead_uavs) > 0:
            for uav in game_state.list_of_dead_uavs:
                uav_copy = Uav(uav.position.x, uav.position.y, uav.status, uav.points, uav.velocity, uav.index,uav.last_postion_update_time,uav.next_status,uav.target_position,naive_algo,None)
                self.uav_list.append(uav_copy)
        if self.uav_list[0].index>self.uav_list[1].index:
            self.uav_list.reverse()


        self.t_curr=game_state.t_curr


