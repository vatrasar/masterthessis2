import typing

from Events.Game.move.GameObjects.tools.enum.enumStatus import UavStatus
from Events.Game.move.Game_Map import GameMap
from Events.Game.move.GameObjects.tools.FluidCel import FluidCell
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_cell_is_on_map
from Events.Game.move.distance import get_2d_distance


def get_fluid_neighbours(cell:FluidCell, game_map:GameMap,direction):
    """

    :param cell:
    :param game_map:
    :param direction: 1 up 0 down
    """

    neigbours_list=[]
    result_list=[]
    if direction==UavStatus.ON_ATTACK:#attack
        neighbour_candidate=Point(cell.index.x-1,cell.index.y-1)
        if check_if_cell_is_on_map(neighbour_candidate,len(game_map.fluid_map[0]),len(game_map.fluid_map)):
            neigbours_list.append(neighbour_candidate)

        neighbour_candidate=Point(cell.index.x+1,cell.index.y-1)
        if check_if_cell_is_on_map(neighbour_candidate,len(game_map.fluid_map[0]),len(game_map.fluid_map)):
            neigbours_list.append(neighbour_candidate)

    elif direction==UavStatus.ON_BACK:#back
        neighbour_candidate=Point(cell.index.x-1,cell.index.y+1)
        if check_if_cell_is_on_map(neighbour_candidate,len(game_map.fluid_map[0]),len(game_map.fluid_map)):
            neigbours_list.append(neighbour_candidate)

        neighbour_candidate=Point(cell.index.x+1,cell.index.y+1)
        if check_if_cell_is_on_map(neighbour_candidate,len(game_map.fluid_map[0]),len(game_map.fluid_map)):
            neigbours_list.append(neighbour_candidate)


    for neighbour in neigbours_list:
        result_list.append(game_map.fluid_map[neighbour.y][neighbour.x])
    return result_list



def floading_algo(game_map, uav, v_of_uav, uav_status):
    """
    returns cells with points which are on path
    :param
    :param game_map:
    :param uav:
    :param v_of_uav:
    """
    cells_with_points=[]
    game_map.reset_fluid_map()
    floadin_queue = []
    old_cell = game_map.get_floading_point(uav.position)
    old_cell.uav_arrive_time = 0
    floadin_queue.append(old_cell)

    # fluid marks
    while (len(floadin_queue) > 0):


        old_cell = floadin_queue[0]
        floadin_queue.remove(old_cell)
        old_cell.is_queue=False

        neighbours_list: typing.List[FluidCell] = get_fluid_neighbours(old_cell,game_map,uav_status)

        parents_list=[]
        # check naighbours. set parent and arrive time
        for neighbour in neighbours_list:
            is_parrent=True
            neighbour.set_visited(True)
            game_map.points_to_reset.append(neighbour)



            new_parrent = None
            if neighbour.parrent == None or neighbour.parrent.uav_arrive_time >= old_cell.uav_arrive_time or neighbour.parrent.uav_arrive_time == -1:
                new_parrent = old_cell

            else:
                is_parrent=False
                new_parrent = neighbour.parrent
            distance = get_2d_distance(neighbour.position, new_parrent.position)
            arrive_time = new_parrent.uav_arrive_time + distance / v_of_uav
            is_point_avaiable = True
            # check hand arrive_time
            # is_point_avaiable = game_state.is_point_save(arrive_time, game_state,  neighbour, settings)

            if is_point_avaiable and is_parrent and neighbour.is_queue==False:
                if neighbour.points==0:
                    parents_list.append(neighbour)
                else:
                    cells_with_points.append(neighbour)
                neighbour.set_uav_arrive_time(arrive_time)
                neighbour.set_parrent(new_parrent)
                neighbour.is_queue=True



        floadin_queue.extend(parents_list)

    return cells_with_points


def create_path(best_cell:FluidCell):
    path=[best_cell]
    current_cell=best_cell.parrent
    while current_cell!=None:
        path.append(current_cell)
        current_cell=current_cell.parrent


    path.reverse()

    return path


def search_attack_patch(uav, game_map:GameMap,uav_velocity):

    cells_with_points=floading_algo(game_map, uav, uav_velocity,UavStatus.ON_ATTACK)
    if(len(cells_with_points)>0):
        best_cell=cells_with_points[0]

        for cell in cells_with_points:
            if cell.points>best_cell.points:
                best_cell=cell
    else:
        return None




    path=create_path(best_cell)
    # game_map.show_path(path)
    return path

def search_back_path(uav, game_map:GameMap,uav_velocity, tier1_distance_from_intruder):
    floading_algo(game_map, uav, uav_velocity,UavStatus.ON_BACK)
    target_point=game_map.get_floading_point(Point(uav.position.x,tier1_distance_from_intruder-1))
    path=create_path(target_point)
    return path


