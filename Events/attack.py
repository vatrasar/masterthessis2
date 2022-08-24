from random import Random



from Events.Game.gameState import GameState
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import UavStatus
from Events.Game.move.algos.GameObjects.data_lists.tools.geometry import get_transform_between_points
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.check import check_if_path_save, check_is_horizontal_distance_form_hands_safe
from Events.Game.move.distance import get_2d_distance, get_vector_with_direction_and_length
from Events.Game.move.evaluation import evaluate
from Events.Game.move.get_position import get_random_position_on_tier1
from Events.Game.move.algos.GameObjects.data_lists.tools.map_ranges_tools import put_point_in_range_of_map
from Events.Game.move.path_planning import search_back_path, search_attack_patch
from Events.Game.move.time import get_travel_time_to_point
from Events.event import Event
from Events.events_list import Event_list



def plan_attack(current_time, event_owner:Uav,tk_master,path,v_of_uav,game_state:GameState,event_list:Event_list,status,safe_margin,settings:Settings):
    if status==UavStatus.ON_ATTACK:

        event_owner.target_with_points=path[-1]


    if len(path)==2:
        print("plan_attack")
    target_position=path[1].position
    dt_arrive=get_travel_time_to_point(event_owner.position,target_position,v_of_uav)
    event_time=dt_arrive+current_time
    new_event=Attack(event_time,event_owner,tk_master,target_position,status,game_state,path[1:],safe_margin)
    event_list.append_event(new_event,status)



def get_target_point_according_to_direction(direction,event_owner,settings,distnace_to_move):
    if direction<0:
        target_position=Point(event_owner.position.x-distnace_to_move,event_owner.position.y)
        put_point_in_range_of_map(target_position,settings.map_size_x,settings.tier1_distance_from_intruder-10,settings.intuder_size)
        # if get_2d_distance(target_position,event_owner.position)<settings.safe_margin/4:
        #     distance=abs(direction)*1.1
        #     target_position=Point(event_owner.position.x+distance,event_owner.position.y)
    else:
        target_position=Point(event_owner.position.x+distnace_to_move,event_owner.position.y)
        put_point_in_range_of_map(target_position,settings.map_size_x,settings.tier1_distance_from_intruder-10,settings.intuder_size)
        # if get_2d_distance(target_position,event_owner.position)<settings.safe_margin/4:
        #     # target_position=Point(event_owner.position.x-settings.safe_margin/2,event_owner.position.y)
        #     distance=abs(direction)*1.1
        #
        #     target_position=Point(event_owner.position.x-distance,event_owner.position.y)
    return target_position


def get_direction_according_to_wall(uav_pos:Point,settings:Settings,current_dir):
    safe_distance_to_take=(settings.uav_size+settings.hand_size)*settings.safe_distance_ratio
    time_of_uav_to_take_distance=safe_distance_to_take/settings.v_of_uav
    my_save_distance=settings.velocity_hand*settings.jump_ratio*time_of_uav_to_take_distance

    if abs(uav_pos.x-settings.map_size_x)<my_save_distance:
        return -1
    if uav_pos.x<my_save_distance:
        return 1
    else:
        return current_dir


def plan_attck_dodge_move(current_time, event_owner:Uav,tk_master,game_state:GameState,settings:Settings,event_list:Event_list):
    target_position=None



    move_distance_in_dodge=10

    dodge_move_planning2(current_time, event_list, event_owner, game_state, move_distance_in_dodge, settings, tk_master)
    # if not dodge_move_planning(current_time, event_list, event_owner, game_state, move_distance_in_dodge, settings, tk_master,check_if_point_safe_attack_dodge_space_wide):
    #     move_distance_in_dodge=settings.v_of_uav*3
    #     if not dodge_move_planning(current_time, event_list, event_owner, game_state, move_distance_in_dodge, settings, tk_master,check_if_point_safe_attack_dodge_time):
    #         move_distance_in_dodge=settings.v_of_uav*3
    #         if not dodge_move_planning(current_time, event_list, event_owner, game_state, move_distance_in_dodge, settings, tk_master,check_if_point_safe_attack_dodge_short_sapce):
    #             from Events.wait import plan_wait
    #             plan_wait(current_time, settings.uav_wait_time, event_owner, tk_master, game_state, event_list,
    #                       settings.safe_margin)

def dodge_move_planning2(current_time, event_list, event_owner, game_state, move_distance_in_dodge, settings, tk_master):
    points_to_check_list=[]
    owner_pos=event_owner.position
    points_to_check_list.append(Point(owner_pos.x+move_distance_in_dodge,owner_pos.y))
    points_to_check_list.append(Point(owner_pos.x-move_distance_in_dodge,owner_pos.y))
    points_to_check_list.append(Point(owner_pos.x,owner_pos.y-move_distance_in_dodge))
    points_to_check_list.append(Point(owner_pos.x,owner_pos.y+move_distance_in_dodge))
    points_to_check_list.append(Point(owner_pos.x+move_distance_in_dodge,owner_pos.y+move_distance_in_dodge))
    points_to_check_list.append(Point(owner_pos.x-move_distance_in_dodge,owner_pos.y+move_distance_in_dodge))
    points_to_check_list.append(Point(owner_pos.x-move_distance_in_dodge,owner_pos.y-move_distance_in_dodge))
    points_to_check_list.append(Point(owner_pos.x+move_distance_in_dodge,owner_pos.y-move_distance_in_dodge))
    safe_ratio=1
    while (True):
        results_list=[]

        for point in points_to_check_list:
            result=evaluate(event_owner.position,point,settings,safe_ratio,game_state)
            results_list.append((point,result))
        max_cell=None

        for point in results_list:
            if max_cell==None:
                max_cell=point
            else:
                if point[1]>max_cell[1]:
                    max_cell=point


        if max_cell[1]==0:
            safe_ratio=safe_ratio-0.1


            safe_distance_to_take=(settings.uav_size+settings.hand_size)*(settings.safe_distance_ratio)
            time_of_uav_to_take_distance=safe_distance_to_take/settings.v_of_uav
            save_distance=settings.velocity_hand*settings.jump_ratio*time_of_uav_to_take_distance+settings.hand_size

            if save_distance*safe_ratio<(settings.uav_size+settings.hand_size):
                from Events.wait import plan_wait
                plan_wait(current_time, settings.uav_wait_time, event_owner, tk_master, game_state, event_list,
                          settings.safe_margin)
                return
        else:
            target_position=max_cell[0]
            dt_arrive = get_travel_time_to_point(event_owner.position, target_position, settings.v_of_uav)
            event_time = dt_arrive + current_time
            target_cell = game_state.game_map.get_floading_point(target_position)
            new_event = Attack(event_time, event_owner, tk_master, target_position, UavStatus.ATTACK_DODGE_MOVE, game_state,
                               [target_cell], settings.safe_margin)
            event_list.append_event(new_event, UavStatus.ATTACK_DODGE_MOVE)
            return





class Attack(Event):

    def __init__(self, time_of_event, event_owner,tk_master,target_postion,next_status,state,path,safe_margin):
        super().__init__(time_of_event, event_owner,tk_master,state)
        self.safe_margin = safe_margin
        self.old_path=path
        self.event_owner.target_position=target_postion
        self.event_owner.next_status=next_status
        self.state:GameState=state
        self.event_owner:Uav=event_owner


    def handle_event(self, event_list,settings:Settings,rand:Random,iteration_function):
        super().handle_event(event_list,settings,rand,iteration_function)
        jump_velocity=settings.jump_ratio*settings.velocity_hand
        if len(self.old_path)>=2:
            if check_if_path_save(self.old_path,self.event_owner,self.event_owner.chasing_hand,settings,self.game_state.hands_list):
                plan_attack(self.time_of_event,self.event_owner,self.tk_master,self.old_path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin,settings)
            else:

                attack_path_found=False
                if self.event_owner.status==UavStatus.ON_ATTACK and check_is_horizontal_distance_form_hands_safe(self.state.hands_list, self.event_owner, settings.safe_margin,jump_velocity,settings):
                    path=None

                    path=search_attack_patch(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings,self.game_state.hands_list)
                    if path!=None:
                        attack_path_found=True
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.game_state,event_list,self.event_owner.status,self.safe_margin,settings)
                    else:

                        attack_path_found=False

                if attack_path_found==False or self.event_owner.status==UavStatus.ON_BACK:
                    if  attack_path_found==False and self.event_owner.status==UavStatus.ON_ATTACK:
                        #give part of points
                        distance_from_tier1=self.event_owner.target_with_points.position.y
                        distance_from_uav=get_2d_distance(self.event_owner.target_with_points.position,self.event_owner.position)
                        if distance_from_tier1-distance_from_uav>0:


                            points=(distance_from_uav/float(distance_from_tier1))*self.event_owner.target_with_points.points
                            self.event_owner.asign_points(points,settings)
                    path=search_back_path(self.event_owner,self.game_state.game_map,settings.v_of_uav,settings.tier1_distance_from_intruder,settings,self.game_state.hands_list)
                    if path!=None:
                        plan_attack(self.time_of_event,self.event_owner,self.tk_master,path,settings.v_of_uav,self.state,event_list,UavStatus.ON_BACK,settings.safe_margin,settings)
                        return
                    elif abs(self.event_owner.position.y-settings.tier1_distance_from_intruder)<30:
                        self.event_owner.consume_energy(settings,self.time_of_event)
                        self.update_algos_results(rand, settings)
                        self.start_to_move_on_tier1(event_list, rand, settings)
                    else:
                        plan_attck_dodge_move(self.time_of_event,self.event_owner,self.tk_master,self.game_state,settings,event_list)
                        #plan_wait(self.time_of_event,settings.uav_wait_time,self.event_owner,self.tk_master,self.game_state,event_list,self.safe_margin)



        else:#target reached
            if self.event_owner.status==UavStatus.ON_ATTACK:
                #asign points
                uav:Uav=self.event_owner
                uav.asign_points(self.old_path[0].points,settings)

                self.start_backing(event_list, settings,rand)
            elif self.event_owner.status==UavStatus.ATTACK_DODGE_MOVE:
                self.start_backing(event_list, settings,rand)
            elif self.event_owner.status==UavStatus.ON_BACK:
                self.event_owner.consume_energy(settings,self.time_of_event)
                self.update_algos_results(rand, settings)
                if settings.tier2_mode:
                    from Events.move_along import plan_enter_from_tier2
                    plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.game_state,settings.safe_margin)
                else:
                    self.start_to_move_on_tier1(event_list, rand, settings)


    def back_on_tier_after_collision(self,settings:Settings,rand:Random,event_list,time):
        self.event_owner.consume_energy(settings,time)
        self.update_algos_results(rand, settings)

        from Events.move_along import plan_enter_from_tier2
        plan_enter_from_tier2(event_list,settings,time,self.event_owner,rand,self.tk_master,self.game_state,settings.safe_margin)
        self.event_owner.set_new_position(Point(0,0),0)
    def update_algos_results(self, rand, settings):

        points1=0
        points2=0
        for uav in self.game_state.uav_list:
            if uav.index==0:
                points1=uav.points
            else:
                points2=uav.points
        self.game_state.naive_algo.un_register_attack(self.event_owner.index, settings,self.game_state.uav_list,self.game_state.t_curr,self.game_state.intruder)


    def start_to_move_on_tier1(self, event_list, rand, settings):


        target_postion=self.game_state.naive_algo.get_target_postion(self.event_owner.index,rand,settings,self.game_state.uav_list)

        from Events.move_along import plan_move_along
        from Events.move_along import plan_enter_from_tier2
        if settings.tier2_mode==True:
            plan_enter_from_tier2(event_list,settings,self.time_of_event,self.event_owner,rand,self.tk_master,self.state,self.safe_margin)
        else:
            plan_move_along(event_list, self.event_owner, target_postion, self.time_of_event, self.game_state, settings,
                        self.tk_master, self.safe_margin,rand)

    def start_backing(self, event_list, settings,rand):
        # plan to back
        path = search_back_path(self.event_owner, self.game_state.game_map, settings.v_of_uav,
                                settings.tier1_distance_from_intruder, settings, self.game_state.hands_list)

        if abs(settings.tier1_distance_from_intruder-self.event_owner.position.y)<settings.uav_size:
            self.event_owner.consume_energy(settings,self.time_of_event)
            self.update_algos_results(rand, settings)
            self.start_to_move_on_tier1(event_list, rand, settings)
        elif path != None:
            plan_attack(self.time_of_event, self.event_owner, self.tk_master, path, settings.v_of_uav, self.state,
                        event_list, UavStatus.ON_BACK, settings.safe_margin,settings)
        else:
            # plan_wait(self.time_of_event, settings.uav_wait_time, self.event_owner, self.tk_master, self.game_state,
            #           event_list, self.safe_margin)
            plan_attck_dodge_move(self.time_of_event,self.event_owner,self.tk_master,self.game_state,settings,event_list)




