from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enumStatus import HandStatus
from Events.Game.move.algos.GameObjects.data_lists.tools.point import Point
from Events.Game.move.distance import get_2d_distance
from Events.Game.move.get_position import get_point_based_on_time
from Events.Game.move.time import get_travel_time_to_point


def evaluation_check_if_point_safe_time(game_state,target_position,settings,event_owner_pos,safe_distance):




    is_point_safe=True

    if get_2d_distance(event_owner_pos,Point(0,settings.intuder_size))<safe_distance or get_2d_distance(event_owner_pos,Point(settings.map_size_x,settings.intuder_size))<safe_distance:
        return

    for hand in game_state.hands_list:#checking for safety


        uav_time=get_travel_time_to_point(event_owner_pos,target_position,settings.v_of_uav)
        hand_time=get_travel_time_to_point(hand.position,target_position,settings.velocity_hand*settings.jump_ratio)
        safe_space=safe_distance/settings.v_of_uav

        safe_distance_for_jump=(settings.hand_size+settings.uav_size)*2
        if get_2d_distance(event_owner_pos,hand.position)<safe_distance and get_2d_distance(event_owner_pos,target_position)<get_2d_distance(target_position,hand.position) and get_2d_distance(hand.position,target_position)>get_2d_distance(hand.position,event_owner_pos):
           my_safe_distance=((settings.hand_size+settings.uav_size)*1.1)
           safe_space= my_safe_distance/settings.v_of_uav

        if hand.status==HandStatus.JUMP and get_2d_distance(event_owner_pos,hand.position)<safe_distance_for_jump and get_2d_distance(event_owner_pos,target_position)<get_2d_distance(target_position,hand.position) and get_2d_distance(hand.position,target_position)>get_2d_distance(hand.position,event_owner_pos):
           safe_distance_for_jump=((settings.hand_size+settings.uav_size)*1.1)

        # if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*2:
        #     if get_2d_distance(hand.position,event_owner.position)<(settings.uav_size+settings.hand_size)*2:
        #         if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*1.1:
        #             is_point_safe=False
        #     else:
        #         is_point_safe=False
        if hand.status==HandStatus.JUMP:#dynamic targets
            uav_time=get_travel_time_to_point(event_owner_pos,target_position,settings.v_of_uav)
            hand_future_position=get_point_based_on_time(hand.position, uav_time, hand.target_position, settings.velocity_hand*settings.jump_ratio)
            if get_2d_distance(target_position,hand_future_position)<safe_distance_for_jump:
                return False

        elif get_2d_distance(event_owner_pos,Point(0,settings.intuder_size))<safe_distance*2 or get_2d_distance(event_owner_pos,Point(settings.map_size_x,settings.intuder_size))<safe_distance*2:

            my_safe_distance=safe_distance
            if get_2d_distance(hand.position,event_owner_pos)<safe_distance*2:
                my_safe_distance=(settings.hand_size+settings.uav_size)*2

            if get_2d_distance(hand.position,target_position)<my_safe_distance:
                is_point_safe=False
        elif safe_space+uav_time>hand_time:
            is_point_safe=False

    # for secound_uav in game_state.uav_list:#checking for safety
    #     if secound_uav!=event_owner and get_2d_distance(secound_uav.position,target_position)<settings.uav_size*2:
    #         is_point_safe=False
    return is_point_safe



def evaluation_check_if_point_safe_distance(game_state,target_position,settings,event_owner_pos,safe_distance):




    is_point_safe=True



    for hand in game_state.hands_list:#checking for safety


        uav_time=get_travel_time_to_point(event_owner_pos,target_position,settings.v_of_uav)
        hand_time=get_travel_time_to_point(hand.position,target_position,settings.velocity_hand*settings.jump_ratio)
        safe_space=safe_distance/settings.v_of_uav
        my_safe_distance=safe_distance
        safe_distance_for_jump=(settings.hand_size+settings.uav_size)*2
        if get_2d_distance(event_owner_pos,hand.position)<safe_distance and get_2d_distance(event_owner_pos,target_position)<get_2d_distance(target_position,hand.position) and get_2d_distance(hand.position,target_position)>get_2d_distance(hand.position,event_owner_pos):
           my_safe_distance=((settings.hand_size+settings.uav_size)*1.1)
           safe_space= my_safe_distance/settings.v_of_uav

        if hand.status==HandStatus.JUMP and get_2d_distance(event_owner_pos,hand.position)<safe_distance_for_jump and get_2d_distance(event_owner_pos,target_position)<get_2d_distance(target_position,hand.position) and get_2d_distance(hand.position,target_position)>get_2d_distance(hand.position,event_owner_pos):
           safe_distance_for_jump=((settings.hand_size+settings.uav_size)*1.1)

        # if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*2:
        #     if get_2d_distance(hand.position,event_owner.position)<(settings.uav_size+settings.hand_size)*2:
        #         if get_2d_distance(hand.position,target_position)<(settings.uav_size+settings.hand_size)*1.1:
        #             is_point_safe=False
        #     else:
        #         is_point_safe=False
        if hand.status==HandStatus.JUMP:#dynamic targets
            uav_time=get_travel_time_to_point(event_owner_pos,target_position,settings.v_of_uav)
            hand_future_position=get_point_based_on_time(hand.position, uav_time, hand.target_position, settings.velocity_hand*settings.jump_ratio)
            if get_2d_distance(target_position,hand_future_position)<safe_distance_for_jump:
                return False

        elif get_2d_distance(hand.position,target_position)<safe_distance:
            is_point_safe=False

    # for secound_uav in game_state.uav_list:#checking for safety
    #     if secound_uav!=event_owner and get_2d_distance(secound_uav.position,target_position)<settings.uav_size*2:
    #         is_point_safe=False
    return is_point_safe

