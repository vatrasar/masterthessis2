import typing

import numpy as np








# def check_is_in_dron_search_range(cell_postion, drone_position, intruder_position,search_angle):
#     transform_vecrot_to_intruder=get_transform_between_points(drone_position,intruder_position)
#     temp_point=move_point_with_vector(cell_postion,transform_vecrot_to_intruder)
#     intruder_tmep_point=move_point_with_vector(intruder_position,transform_vecrot_to_intruder)
#     angle=math.degrees(convert_to_360(get_vector_angle(intruder_tmep_point)))
#     anlge_max=angle_positive((angle+search_angle/2.0)%360)
#     anlge_min=angle_positive((angle-search_angle/2.0)%360)
#     orginal_angle=convert_to_360(get_vector_angle(temp_point))
#
#     point_angle=math.degrees(convert_to_360(get_vector_angle(temp_point)))
#
#     # print(("current %.2f radians %.2f point %.2f %.2f")%(point_angle,orginal_angle,temp_point.x,temp_point.y))
#     return is_angle_in_range(point_angle,anlge_min,anlge_max)


#
# def check_is_in_dron_search_range_back(cell_postion, drone_position, intruder_position,search_angle):
#     transform_vecrot_to_intruder=get_transform_between_points(drone_position,intruder_position)
#     temp_point=move_point_with_vector(cell_postion,transform_vecrot_to_intruder)
#     intruder_tmep_point=move_point_with_vector(intruder_position,transform_vecrot_to_intruder)
#
#     point_for_center_angle=Point(-intruder_tmep_point.x,-intruder_tmep_point.y)
#     angle=math.degrees(convert_to_360(get_vector_angle(point_for_center_angle)))
#     anlge_max=angle_positive((angle+search_angle/2.0)%360)
#     anlge_min=angle_positive((angle-search_angle/2.0)%360)
#     orginal_angle=convert_to_360(get_vector_angle(temp_point))
#
#     point_angle=math.degrees(convert_to_360(get_vector_angle(temp_point)))
#
#     # print(("current %.2f radians %.2f point %.2f %.2f")%(point_angle,orginal_angle,temp_point.x,temp_point.y))
#     return is_angle_in_range(point_angle,anlge_min,anlge_max)
from Events.Game.gameState import GameState
from Events.Game.move.GameObjects.movableObject import MovableObject
from Events.Game.move.GameObjects.tools.FluidCel import FluidCell
from Events.Game.move.GameObjects.tools.point import Point
from Events.Game.move.GameObjects.tools.settings import Settings
from Events.Game.move.GameObjects.uav import Uav
from Events.Game.move.check import check_if_cell_is_on_map
from Events.Game.move.distance import get_2d_distance


class GameMap():
    def __init__(self,map_size_x,map_size_y,map_resolution,uav_size,hand_size,list_of_cells_with_points,settings:Settings):
        self.map_size_x=map_size_x
        self.map_size_y=map_size_y
        self.dimension_x = round(map_size_x/map_resolution)
        self.dimension_y = round(map_size_y/map_resolution)
        self.list_of_cells_with_points=list_of_cells_with_points
        self.map_memmory = np.zeros((self.dimension_y,self.dimension_x ), np.int32)
        self.memory_invisible=np.zeros((self.dimension_y,self.dimension_x ), np.int32)
        self.fluid_map:typing.List[typing.List[FluidCell]]=[]
        self.points_to_reset:typing.List[FluidCell]=[]
        self.fluid_memory = np.zeros((self.dimension_y, self.dimension_x), np.int32)
        self.map_resolution=map_resolution
        self.uav_size=uav_size
        self.hand_size=hand_size
        self.settings=settings
        self.build_fluid_map()
        self.build_invisible_map()

    def build_invisible_map(self):
        for invisible in self.settings.lif_of_invisible:
            cells=self.get_all_cells_to_color(Point(invisible.x,invisible.y),invisible.r)
            for cell in cells:
                if check_if_cell_is_on_map(cell,len(self.fluid_map[0]),len(self.fluid_map)):
                    self.memory_invisible[cell.y][cell.x] = 1

    def build_fluid_map(self):
        for i in range(0, self.dimension_y):  # build fluid_map
            self.fluid_map.append([])
            for p in range(0, self.dimension_x):
                point = self.convert_index_to_point(p, i)
                point = Point(point[0], point[1])
                new_cell = FluidCell(0, point, p, i)
                self.fluid_map[i].append(new_cell)

        for cell in self.list_of_cells_with_points:
            point_on_map=self.get_point_on_map_index(cell.x, cell.y)
            self.fluid_map[point_on_map.y][point_on_map.x].points=cell.points

    def reset_fluid_map(self):

        for cell in self.points_to_reset:
            cell.is_queue=False
            cell.is_visited=False
            cell.is_safe=False
            cell.uav_arrive_time=0
            cell.parrent=None

        self.points_to_reset=[]





    def get_point_on_map_index(self,x,y):

        x_i = int(round((x) / self.map_resolution))
        y_i= int(round((y) / self.map_resolution))
        return Point(x_i,y_i)

    def convert_index_to_point(self,x_i,y_i):
        x=x_i*self.map_resolution

        y=y_i*self.map_resolution

        return (x,y)


    def set_object_on_map(self,object:MovableObject,object_size,object_id):
        try:


            # x_i, y_i = self.get_point_on_map_index(object.position.x, object.position.y)
            # drones_candidates.append(Point(x_i, y_i))
            cells_to_color=self.get_all_cells_to_color(object.position,object_size)
            for cell in cells_to_color:
                if check_if_cell_is_on_map(cell,len(self.fluid_map[0]),len(self.fluid_map)):
                    self.map_memmory[cell.y][cell.x] = object_id
                    self.fluid_memory[cell.y][cell.x] = object_id
        except Exception:
            print("error in Game map, method set object on map")


#         while (len(drones_candidates) != 0): #set all cells in range
#
#             drone_candidate = drones_candidates[0]
#             drones_candidates.remove(drone_candidate)
#             if get_2d_distance(self.get_cell_with_index(drone_candidate).position, object.position) <= object_size:
#
#                 self.map_memmory[drone_candidate.y][drone_candidate.x] = object_id
#                 self.fluid_memory[drone_candidate.y][drone_candidate.x] = object_id
#
#                 neighbours = self.get_cell_neighbours(drone_candidate.x, drone_candidate.y)
#                 neighbours_to_check = []
#                 for neighbour in neighbours:
#                     if  self.map_memmory[neighbour.y][neighbour.x] == 0:
#                         neighbours_to_check.append(neighbour)
# #neighbour.y<=self.dimension_y and neighbour.y>=0 and neighbour.x>=0 and neighbour.x<=self.dimension_x and
#                 drones_candidates.extend(neighbours_to_check)

    def update_map(self, game_state:GameState,uav:Uav):

        self.map_memmory = np.zeros((self.dimension_y, self.dimension_x), np.int32)
        self.fluid_memory=np.zeros((self.dimension_y, self.dimension_x), np.int32)



        #seting object on map, code works but i turned it of becase of performacnes
        for uav in game_state.uav_list:#set uav positions on map
            self.set_object_on_map(uav,self.uav_size,100)

        for hand in game_state.hands_list:  # set uav positions on map
            self.set_object_on_map(hand,self.hand_size,200)
        #
        #
        # self.set_object_on_map(game_state.intruder,settings.intuder_size,300)







    def get_floading_point(self, position)->FluidCell:
        index=self.get_point_on_map_index(position.x,position.y)
        cell=self.fluid_map[index.y][index.x]
        return cell

    # def get_avaiable_neighbours(self, parrent_cell:FluidCell,uav,game_state:GameState,settings:Settings,first_cell):
    #
    #     x=parrent_cell.index.x
    #     y=parrent_cell.index.y
    #     potential_neighbours_index_list = self.get_cell_neighbours(x, y)
    #
    #     neighbours_cells_list=[]
    #     for cell_index in potential_neighbours_index_list:
    #
    #         if self.check_is_index_proply(cell_index):
    #             cell=self.get_cell_with_index(cell_index)
    #             if cell==first_cell or cell==parrent_cell.parrent:
    #                 continue
    #             if cell.is_visited:
    #                 neighbours_cells_list.append(cell)
    #             #is in search range
    #             elif (check_is_in_dron_search_range(cell.position,uav.position,game_state.intruder.position,20) or get_2d_distance(cell.position,uav.position)<settings.tier1_distance_from_intruder*0.2):
    #
    #                 #assing points
    #                 points=self.get_cell_points(cell, game_state, settings)
    #                 cell.set_points(points)
    #                 neighbours_cells_list.append(cell)
    #                 if self.fluid_memory[cell_index.y][cell_index.x]!=100:
    #                     self.fluid_memory[cell_index.y][cell_index.x]=12
    #
    #     return neighbours_cells_list


        # neighbours_list=[]
        # x_i,y_i=self.get_point_on_map_index(parrent_cell.position.x,parrent_cell.position.y)
        #
        #
        # if(self.dimension>x_i+1 and y_i+1<self.dimension):
        #     cell=self.fluid_map[y_i+1][x_i+1]
        #     if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:
        #
        #         neighbours_list.append(cell)
        #
        #
        # if(0<=x_i-1 and y_i+1<self.dimension):
        #     cell=self.fluid_map[y_i+1][x_i]
        #     if get_2d_distance(cell.position,uav.position)<tier1_distance_from_intruder*1.3 and get_2d_distance(cell.position,uav.position)>tier1_distance_from_intruder:
        #         neighbours_list.append(cell)
        #
        #
        #
        # return neighbours_list

    def get_cell_neighbours(self, x, y)->typing.List[Point]:
        potential_neighbours_index_list = []
        potential_neighbours_index_list.append(Point(x + 1, y))
        potential_neighbours_index_list.append(Point(x - 1, y))
        potential_neighbours_index_list.append(Point(x + 1, y + 1))
        potential_neighbours_index_list.append(Point(x, y + 1))
        potential_neighbours_index_list.append(Point(x - 1, y + 1))
        potential_neighbours_index_list.append(Point(x - 1, y - 1))
        potential_neighbours_index_list.append(Point(x, y - 1))
        potential_neighbours_index_list.append(Point(x + 1, y - 1))
        return potential_neighbours_index_list

    # def get_cell_points(self, cell, game_state, settings):
    #     angle = get_vector_angle(cell.position)
    #     angle = math.degrees(convert_to_360(angle))
    #     for arange in self.poin_ranges:
    #         if arange[0] <= angle and arange[1] > angle and get_2d_distance(cell.position,
    #                                                                         game_state.intruder.position) < settings.back_distance*1.1:
    #             return arange[2]
    #     return 0


    # def check_is_demision_proply(self, demision):
    #     return demision<self.dimension and demision>0




    # def get_best_points_in_range_back(self,game_state:GameState,settings:Settings,uav):
    #     best_cell_in_range=self.fluid_map[0][0]
    #
    #     for row in self.fluid_map:
    #         for cell in row:
    #             if cell.points==1 and game_state.is_correct_drone(cell.position,cell.uav_arrive_time+game_state.t_curr,uav,settings):
    #                 return cell
    #
    #
    #     return None

    def get_cell_with_index(self, cell_index)->FluidCell:
        return self.fluid_map[cell_index.y][cell_index.x]

    # def show_path(self, path:typing.List[FluidCell]):
    #     i=50
    #
    #     for element in path:
    #         self.fluid_memory[element.index.y][element.index.x]=i
    #         i=i+1

    # def get_back_avaiable_neighbours(self, parrent_cell:FluidCell,init_drone_postion,game_state:GameState,settings:Settings,first_cell,temp_ratio):
    #
    #     x=parrent_cell.index.x
    #     y=parrent_cell.index.y
    #     potential_neighbours_index_list = self.get_cell_neighbours(x, y)
    #
    #     neighbours_cells_list=[]
    #     for cell_index in potential_neighbours_index_list:
    #
    #         if self.check_is_index_proply(cell_index):
    #             cell=self.get_cell_with_index(cell_index)
    #             if cell==first_cell or cell==parrent_cell.parrent:
    #                 continue
    #             if cell.is_visited:
    #                 neighbours_cells_list.append(cell)
    #             #is in search range
    #             elif (check_is_in_dron_search_range_back(cell.position,init_drone_postion,game_state.intruder.position,20) or get_2d_distance(cell.position,init_drone_postion)<settings.tier1_distance_from_intruder*0.2):
    #
    #                 #assing points
    #                 points=self.get_cell_points_back(cell, game_state, settings,temp_ratio)
    #                 cell.set_points(points)
    #                 neighbours_cells_list.append(cell)
    #                 if self.fluid_memory[cell_index.y][cell_index.x]!=100:
    #                     self.fluid_memory[cell_index.y][cell_index.x]=12
    #
    #     return neighbours_cells_list

    # def get_cell_points_back(self, cell, game_state, settings,temp_ratio=1):
    #     if(get_2d_distance(game_state.intruder.position,cell.position)>=settings.tier1_distance_from_intruder*temp_ratio):
    #         return 1
    #     else:
    #         return 0

    # def update_simple_map(self, game_state, uav_in_decision):
    #     self.map_memmory = np.zeros((self.settings.simple_dimension, self.settings.simple_dimension), np.int32)
    #
    #
    #
    #
    #     # seting object on map, code works but i turned it of becase of performacnes
    #
    #     for uav in game_state.uav_list:#set uav positions on map
    #         x_i, y_i = self.get_point_on_simple_map_index(uav.position.x, uav.position.y)
    #         if uav==uav_in_decision:
    #             self.map_memmory[y_i][x_i]=1
    #         else:
    #             self.map_memmory[y_i][x_i] = 2
    #
    #     for hand in game_state.hands_list:  # set uav positions on map
    #         x_i, y_i = self.get_point_on_simple_map_index(hand.position.x, hand.position.y)
    #         self.map_memmory[y_i][x_i] = 3

    # def get_point_on_simple_map_index(self, x, y):
    #     x_i = int(round((x - self.simple_y_min) / self.settings.simple_resolution))
    #     y_i = int(round((y - self.simple_y_min) / self.settings.simple_resolution))
    #     return (x_i, y_i)
    def get_all_cells_to_color(self, position, object_size):
        index=self.get_point_on_map_index(position.x,position.y)
        index_distance=round(object_size/self.map_resolution)
        list_of_cells=[]

        for i in range(0,index_distance):
            for p in range(0,index_distance):
                candidates_list=[Point(index.x+i,index.y+p),Point(index.x+i,index.y-p),Point(index.x-i,index.y+p),Point(index.x-i,index.y-p)]
                for candidate in candidates_list:
                    if get_2d_distance(candidate,index)<=index_distance:
                        list_of_cells.append(candidate)


        return list_of_cells

    def show_path(self, path:typing.List[FluidCell]):
        i=50

        for element in path:
            self.fluid_memory[element.index.y][element.index.x]=i
            i=i+1
















