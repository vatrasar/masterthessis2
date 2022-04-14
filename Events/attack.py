from random import Random



from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.algos.tools.enum.enumStatus import UavStatus
from Events.Game.move.GameObjects.algos.tools.geometry import get_transform_between_points
from Events.Game.move.GameObjects.algos.tools.point import Point
from Events.Game.move.GameObjects.algos.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_path_save, check_is_horizontal_distance_form_hands_safe
from Events.Game.move.distance import get_2d_distance, get_vector_with_direction_and_length
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.GameObjects.algos.tools.map_ranges_tools import put_point_in_range_of_map
from Events.Game.move.path_planning import search_back_path, search_attack_patch
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list



def plan_attack(current_time, event_owner:Uav,tk_master,path,v_of_uav,game_state,event_list:Event_list,status,safe_margin,settings:Settings):
    if len(path)==2:
        print("plan_attack")
    target_position=path[1].position
    dt_arrive=get_travel_time_to_point(event_owner.position,target_position,v_of_uav)
    event_time=dt_arrive+current_time
    new_event=Attack(event_time,event_owner,tk_master,target_position,status,game_state,path[1:],safe_margin)
    event_list.append_event(new_event,status)
    if settings.mode=="list" and (not event_owner.naive_algo.is_limit_reached()):
        event_owner.register_attack(target_position)

    if settings.mode=="annealing":
        event_owner.annealing_algo.register_attack(target_position,event_owner.index,event_owner.points)




def plan_attck_dodge_move(current_time, event_owner:Uav,tk_master,game_state:GameState,settings:Settings,event_list:Event_list):
    target_position=None
    if len(game_state.hands_list)>1 and get_2d_distance(game_state.hands_list[0].position,game_state.hands_list[1].position)<settings.safe_margin:
        vector1=get_transform_between_points(game_state.hands_list[0].position,event_owner.position)
        vector2=get_transform_between_points(game_state.hands_list[1].position,event_owner.position)
        result_vector=Point(vector2.x+vector1.x,vector2.y+vector1.y)
        result_vector=get_vector_with_direction_and_length(result_vector,settings.safe_margin/2)
        target_position=Point(event_owner.position.x+result_vector.x,event_owner.position.y+result_vector.y)


    else:

        closest_hand=None
        for hand in game_state.hands_list:
            if closest_hand==None:
                closest_hand=hand

            if get_2d_distance(event_owner.position,hand.position)<get_2d_distance(event_owner.position,closest_hand.position):
                closest_hand=hand

        direction=event_owner.position.x-closest_hand.position.x


        if direction<0:
            target_position=Point(event_owner.position.x-settings.safe_margin/2,event_owner.position.y)
            put_point_in_range_of_map(target_position,settings.map_size_x,settings.map_size_y)
            if get_2d_distance(target_position,event_owner.position)<settings.safe_margin/4:
                target_position=Point(event_owner.position.x+settings.safe_margin/2,event_owner.position.y)
        else:
            target_position=Point(event_owner.position.x+settings.safe_margin/2,event_owner.position.y)
            put_point_in_range_of_map(target_position,settings.map_size_x,settings.map_size_y)
            if get_2d_distance(target_position,event_owner.position)<settings.safe_margin/4:
                target_position=Point(event_owner.position.x-settings.safe_margin/2,event_owner.position.y)



    put_point_in_range_of_map(target_position,settings.map_size_x,settings.map_size_y)

    # if target_position.x<0 or target_position.x>settings.map_size_x:
    #     if event_owner.position.x<settings.map_size_x/2:
    #         target_position=Point(event_owner.position.x+settings.safe_margin/2+settings.hand_size,event_owner.position.y)
    #     else:
    #         target_position=Point(event_owner.position.x-settings.safe_margin/2-settings.hand_size,event_owner.position.y)
    #


    is_point_safe=True
    for hand in game_state.hands_list:#checking for safety
        if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*2:
            if get_2d_distance(hand.position,event_owner.position)<(settings.uav_size+settings.hand_size)*2:
                if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*1.1:
                    is_point_safe=False
            else:
                is_point_safe=False


    for secound_uav in game_state.uav_list:#checking for safety
        if secound_uav!=event_owner and get_2d_distance(secound_uav.position,target_position)<settings.uav_size*2:
            is_point_safe=False



    if not is_point_safe:
        is_point_safe=False
        target_position.y=target_position.y-(settings.uav_size+settings.hand_size)
        put_point_in_range_of_map(target_position,settings.map_size_x,settings.map_size_y)
        for hand in game_state.hands_list:#checking for safety
            if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*2:
                is_point_safe=False

        for secound_uav in game_state.uav_list:#checking for safety
            if secound_uav!=event_owner and get_2d_distance(secound_uav.position,target_position)<settings.uav_size*2:
                is_point_safe=False
        if not is_point_safe:
            from Events.wait import plan_wait

            plan_wait(current_time,settings.uav_wait_time,event_owner,tk_master,game_state,event_list,settings.safe_margin)

    else:
        dt_arrive=get_travel_time_to_point(event_owner.position,target_position,settings.v_of_uav)
        event_time=dt_arrive+current_time
        target_cell=game_state.game_map.get_floading_point(target_position)
        new_event=Attack(event_time,event_owner,tk_master,target_position,UavStatus.ATTACK_DODGE_MOVE,game_state,[target_cell],settings.safe_margin)
        event_list.append_event(new_event,UavStatus.ATTACK_DODGE_MOVE)



class Attack(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state,path,safe_margin):
        super().__init__(time_of_event, event_owner,tk_master,state)
        self.safe_margin = safe_margin
        self.old_path=path
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state


    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)
        jump_velocity=settings.jump_ratio*settings.velocity_hand
        if len(self.old_path)>=2:
            if check_if_path_save(self.old_path,self.event_owner,self.event_owner.chasing_hand,settings,self.game_state.hands_list):
                plan_attack(self.time_of_event,self.event_owner,self.tk_master,self.old_path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin,settings)
            else:

                attack_path_found=False
                if self.event_owner.status==UavStatus.ON_ATTACK and check_is_horizontal_distance_form_hands_safe(self.state.hands_list, self.event_owner, settings.safe_margin,jump_velocity):
                    path=None

                    path=search_attack_patch(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings,self.game_state.hands_list)
                    if path!=None:
                        attack_path_found=True
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin,settings)
                    else:
                        attack_path_found=False

                if attack_path_found==False or self.event_owner.status==UavStatus.ON_BACK:

                    path=search_back_path(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings.tier1_distance_from_intruder,settings,self.game_state.hands_list)
                    if path!=None:
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_BACK,settings.safe_margin,settings)
                        return
                    else:
                        plan_attck_dodge_move(self.time_of_event,self.event_owner,self.tk_master,self.game_state,settings,event_list)
                        #plan_wait(self.time_of_event,settings.uav_wait_time,self.event_owner,self.tk_master,self.game_state,event_list,self.safe_margin)



        else:#target reached
            if self.event_owner.status==UavStatus.ON_ATTACK:
                #asign points
                uav:Uav=self.event_owner
                uav.asign_points(self.old_path[0].points)

                self.start_backing(event_list, settings,rand)
            elif self.event_owner.status==UavStatus.ATTACK_DODGE_MOVE:
                self.start_backing(event_list, settings,rand)
            elif self.event_owner.status==UavStatus.ON_BACK:
                if settings.mode=="list":
                    self.event_owner.naive_algo.un_register_attack(self.event_owner.index,self.event_owner.points,settings)
                if settings.mode=="annealing":
                    self.event_owner.annealing_algo.un_register_attack(self.event_owner.index,self.event_owner.points,settings,rand)
                if settings.tier2_mode:
                    from Events.move_along import plan_enter_from_tier2
                    plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.game_state,settings.safe_margin)
                else:
                    self.start_to_move_on_tier1(event_list, rand, settings)

    def start_to_move_on_tier1(self, event_list, rand, settings):

        target_postion = get_random_position_on_tier1(rand, settings.map_size_x, settings.tier1_distance_from_intruder)
        if settings.mode=="list":
            if self.event_owner.naive_algo.is_limit_reached():
                target_postion=self.event_owner.naive_algo.get_target_postion(self.event_owner.index,rand,settings)
        if settings.mode=="annealing":
            target_postion=self.event_owner.annealing_algo.get_target_postion(self.event_owner.index,rand,settings)
        from Events.move_along import plan_move_along
        plan_move_along(event_list, self.event_owner, target_postion, self.time_of_event, self.game_state, settings,
                        self.tk_master, self.safe_margin)

    def start_backing(self, event_list, settings,rand):
        # plan to back
        path = search_back_path(self.event_owner, self.game_state.game_map, settings.v_of_uav,
                                settings.tier1_distance_from_intruder, settings, self.game_state.hands_list)

        if abs(settings.tier1_distance_from_intruder-self.event_owner.position.y)<settings.uav_size:
            self.start_to_move_on_tier1(event_list, rand, settings)
        elif path != None:
            plan_attack(self.time_of_event, self.event_owner, self.tk_master, path, settings.v_of_uav, self.state,
                        event_list, UavStatus.ON_BACK, settings.safe_margin,settings)
        else:
            # plan_wait(self.time_of_event, settings.uav_wait_time, self.event_owner, self.tk_master, self.game_state,
            #           event_list, self.safe_margin)
            plan_attck_dodge_move(self.time_of_event,self.event_owner,self.tk_master,self.game_state,settings,event_list)




