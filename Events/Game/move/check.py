import typing


from Events.Game.move.Game_Map import GameMap
from Events.Game.move.algos.GameObjects.hand import Hand
from Events.Game.move.algos.GameObjects.movableObject import MovableObject
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import UavStatus, HandStatus, Sides
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
from Events.Game.move.algos.GameObjects.uav import Uav
from Events.Game.move.distance import get_horizontal_distance, get_2d_distance
from Events.Game.move.get_position import get_point_based_on_time
from Events.Game.move.algos.GameObjects.data_lists.tools.map_ranges_tools import get_max_x_in_range
from Events.Game.move.time import get_travel_time_to_point


def check_distance_between_uav(uav_list:typing.List[Uav],save_distance):
    if len(uav_list)<2:
        return True
    if get_horizontal_distance(uav_list[0].position, uav_list[1].position)<save_distance:
        return False
    else:
        return True

def check_if_same_move_direction(event_owner:MovableObject,uav_list:typing.List[Uav],target_postion):
    if len(uav_list)<2:
        return False
    secound_uav=None
    for uav in uav_list:
        if uav!=event_owner:
            secound_uav=uav

    if event_owner.status==UavStatus.TIER_2 or  secound_uav.status==UavStatus.TIER_2:
        return False

    vector1=target_postion.x-event_owner.position.x
    vector2=secound_uav.target_position.x-secound_uav.position.x
    if vector1*vector2>0:
        return True
    else:
        return False



def chekc_if_uav_goes_to_trash(event_owner, potential_crash_point, target_postion,save_distance):
    distance_to_trash=get_horizontal_distance(event_owner.position, potential_crash_point)
    distance_to_target=get_horizontal_distance(event_owner.position, target_postion)
    if distance_to_trash>distance_to_target+save_distance:
        return False
    vector_to_crash_point = potential_crash_point.x - event_owner.position.x
    vecotr_to_target = target_postion.x - event_owner.position.x
    if vecotr_to_target*vector_to_crash_point>0:
        return True
    else:
        return False


def check_if_in_safe_distance(uav,hands_list,safe_margin):
    for hand in hands_list:
        if get_horizontal_distance(uav.position,hand.position)<safe_margin:
            return False
    return True

def check_if_cell_is_on_map(cell:Point,max_index_x,max_index_y):
    if cell.x<max_index_x-2 and cell.x>=1 and cell.y<max_index_y-2 and cell.y>=1:
        return True
    else:
        return False

def check_if_uav_is_visible(uav:Uav,game_map:GameMap):
    index=game_map.get_point_on_map_index(uav.position.x,uav.position.y)
    if game_map.memory_invisible[index.y][index.x]==1:
        return False
    else:
        return True



def check_if_uav_is_in_range(uav:Uav,hand:Hand,settings):
    from Events.hand_chase import get_max_hand_range_in_x
    x=get_max_x_in_range(hand.side,settings,uav.position.x)
    if hand.side==Sides.LEFT and x<uav.position.x:
        return False
    elif hand.side==Sides.RIGHT and x>uav.position.x:
        return False

    max_y_range=get_max_hand_range_in_x(hand.side,settings.minimal_hand_range,settings.r_of_LR,settings.map_size_x,x,settings)
    if max_y_range>uav.position.y:
        return True
    else:
        return False


def check_if_point_is_in_range(point:Point,hand:Hand,settings):
    from Events.hand_chase import get_max_hand_range_in_x
    x=get_max_x_in_range(hand.side,settings,point.x)
    if hand.side==Sides.LEFT and x<point.x:
        return False
    elif hand.side==Sides.RIGHT and x>point.x:
        return False

    max_y_range=get_max_hand_range_in_x(hand.side,settings.minimal_hand_range,settings.r_of_LR,settings.map_size_x,x,settings)
    if max_y_range>point.y:
        return True
    else:
        return False

def check_if_algo_target_reached(uav_postion,target_position,settings):
    return get_2d_distance(uav_postion,target_position)<settings.map_resolution*2

def check_is_horizontal_distance_form_hands_safe(hands_list:typing.List[Hand], uav, safe_margin,jump_velocity,settings:Settings):

    # actual_margin=jump_velocity*4*1.5
    # for hand in hands_list:
    #     if hand.status==HandStatus.JUMP:
    #         actual_margin=safe_margin*2
    #     # elif hand.status==HandStatus.CHASING and hand.target_uav==uav:
    #     #     actual_margin=safe_margin*1.5
    #     elif hand.status==HandStatus.WAIT_AFTER_JUMP and uav.status!=UavStatus.ON_ATTACK:
    #         actual_margin=0
    #     else:
    #         actual_margin=jump_velocity*4*1.5
    #
    #     if abs(uav.position.x-hand.position.x)<actual_margin:
    #
    #         return False

    safe_distance_to_take=(settings.uav_size+settings.hand_size)*settings.safe_distance_ratio
    time_of_uav_to_take_distance=safe_distance_to_take/settings.v_of_uav
    save_distance=jump_velocity*time_of_uav_to_take_distance
    for hand in hands_list:

        actual_margin=jump_velocity*4*1.5
        actual_margin=save_distance
        if hand.status==HandStatus.WAIT_AFTER_JUMP and uav.status!=UavStatus.ON_ATTACK:
            actual_margin=settings.uav_size+settings.hand_size
        if get_2d_distance(uav.position,hand.position)<actual_margin:
            return False

    return True

# def check_is_distance_form_hands_safe(hands_list:typing.List[Hand], uav, safe_margin):
#     for hand in hands_list:
#
#         if get_2d_distance(uav.position,hand.position)<safe_margin:
#             return False
#
#     return True

def check_if_path_save(path, uav:Uav, chasing_hand:Hand, settings:Settings, hands_list:typing.List[Hand]):

    if settings.mode_debug=="11":
        return True

    jump_velocity=settings.jump_ratio*settings.velocity_hand
    cells_to_check=settings.v_of_uav*5.0/settings.map_resolution
    if (not check_is_horizontal_distance_form_hands_safe(hands_list, uav, settings.safe_margin,jump_velocity,settings)) and uav.status!=UavStatus.ON_BACK:
         return False

    # if chasing_hand==None:
    #     return True
    # if chasing_hand.status!=HandStatus.JUMP:
    #     return True

    travel_time=0
    last_postion=uav.position
    cells_counter=0
    for cell in path:

        travel_time=travel_time+get_travel_time_to_point(last_postion,cell.position,settings.v_of_uav)

        if not check_if_point_safe(travel_time,chasing_hand,cell,settings,hands_list,jump_velocity):
            return False
        # if chasing_hand!=None and chasing_hand.status==HandStatus.JUMP:# checking future targets
        #
        #     target_point=get_point_based_on_time(chasing_hand.position, travel_time, chasing_hand.target_position, jump_velocity)
        #
        #     if get_2d_distance(cell.position,target_point)<settings.uav_size*2:
        #         return False
        #
        # for hand in hands_list:# chacking for static targets
        #     if get_2d_distance(cell.position,hand.position)<settings.uav_size*4:
        #         return False


        cells_counter=1+cells_counter
        if cells_counter>cells_to_check:
            break

    return True

def check_if_point_safe(arrive_time, chasing_hand, cell, settings:Settings,hands_list:typing.List[Hand],jump_velocity):

    safe_distance_to_take=(settings.uav_size+settings.hand_size)*settings.safe_distance_ratio
    time_of_uav_to_take_distance=safe_distance_to_take/settings.v_of_uav
    my_save_distance=jump_velocity*time_of_uav_to_take_distance

    jump_velocity=settings.jump_ratio*settings.velocity_hand
    save_space_outside_LF=(settings.hand_size+settings.uav_size)*1.5
    # if arrive_time<520:
    #     save_space_outside_LF=(settings.hand_size+settings.uav_size)
    if cell.position.y>settings.r_of_LR+save_space_outside_LF:
        return True
    if chasing_hand!=None and chasing_hand.status==HandStatus.JUMP:# checking future targets

        target_point=get_point_based_on_time(chasing_hand.position, arrive_time, chasing_hand.target_position, jump_velocity)

        if get_2d_distance(cell.position,target_point)<(settings.uav_size+settings.hand_size)*2:
            return False

    for hand in hands_list:# chacking for static targets
        save_distance=my_save_distance

        if hand.status==HandStatus.JUMP:
            save_distance=(settings.uav_size+settings.hand_size)*2
        if hand.status==HandStatus.WAIT_AFTER_JUMP or hand.status==HandStatus.WAIT:
            save_distance=min((settings.uav_size+settings.hand_size)*3,my_save_distance)
        if get_2d_distance(cell.position,hand.position)<save_distance:
            return False


    # safe_distance=(settings.uav_size*2/settings.v_of_uav)*jump_velocity*2
    # target_point=get_point_based_on_time(chasing_hand.position, arrive_time, chasing_hand.target_position, jump_velocity)
    # if get_2d_distance(cell.position,target_point)<safe_distance:
    #     return False
    # for hand_ in hands_list:
    #     if get_2d_distance(cell.position,hand_.position)<safe_distance:
    #         return False

    return True

def check_if_point_safe_attack_dodge(game_state,target_position,settings,event_owner):
    is_point_safe=True
    if get_2d_distance(target_position,event_owner.position)<settings.safe_margin/4:
        return False
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
    return is_point_safe


def check_if_point_is_reached(object_velocity,minimal_time_of_travel,object_position,target_position):
    trevel_time=get_travel_time_to_point(object_position,target_position,object_velocity)
    if minimal_time_of_travel>=trevel_time:
        return True
    else:
        return False


def check_if_point_is_reached(object_velocity,minimal_time_of_travel,object_position,target_position):
    trevel_time=get_travel_time_to_point(object_position,target_position,object_velocity)
    if minimal_time_of_travel>=trevel_time:
        return True
    else:
        return False
