import math
import typing
from typing import List

from Events.Game.Statistics import Statistics
from Events.Game.gameState import GameState
from Events.Game.game_state_stac import GameStateStac
from Events.Game.move.algos.GameObjects.data_lists.Hit_list import Hit_list
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings


def get_std(list_of_valuse):
    mean = get_mean(list_of_valuse)

    sum_of_squares_deviations=0
    for iteration_value in list_of_valuse:
        sum_of_squares_deviations=sum_of_squares_deviations+math.pow(iteration_value-mean,2)

    std=math.sqrt(float(sum_of_squares_deviations)/len(list_of_valuse))


    return std


def get_mean(list_of_valuse):
    sum = 0
    for iteration_value in list_of_valuse:  # calculate sum of points for all iterations
        sum = sum + iteration_value
    mean = float(sum) / len(list_of_valuse)
    return mean


def get_uav_points_sum(state:GameStateStac):
    points_sum=0
    for uav in state.uav_list:
        points_sum=uav.points+points_sum

    for uav in state.dead_uav_list:
        points_sum=uav.points+points_sum
    return points_sum

def get_gnuplot_mean_data(runs_stac_list:List[Statistics]):
    gnuplot_data=[]

    if len(runs_stac_list)>0:
        for i in range(0,len(runs_stac_list[0].game_states_list)-1):
            point_sums_list=[]

            for run_stac in runs_stac_list:
                iteration_i_state=run_stac.game_states_list[i]
                point_sums_list.append(get_uav_points_sum(iteration_i_state))

            std=get_std(point_sums_list)
            mean=get_mean(point_sums_list)
            gnuplot_record=[i,mean,std]
            gnuplot_data.append(gnuplot_record)

    return gnuplot_data


def save_records_to_file(data_to_export:List,file):
    for record in data_to_export:
        file.write("%d %.2f %.2f\n"%(record[0],record[1],record[2]))


def get_uav_with_index(index, state:GameStateStac):
    for uav in state.uav_list:
        if uav.index==index:
            return uav

    for uav in state.dead_uav_list:
        if uav.index==index:
            return uav


def get_uav1_energy_data(runs_stac_list:typing.List[Statistics]):
    gnuplot_data=[]

    if len(runs_stac_list)>0:
        for i in range(0,len(runs_stac_list[0].game_states_list)-1):
            enrgy_sum_list=[]

            for run_stac in runs_stac_list:
                iteration_i_state=run_stac.game_states_list[i]
                uav=get_uav_with_index(0,iteration_i_state)
                enrgy_sum_list.append(uav.energy)

            std=get_std(enrgy_sum_list)
            mean=get_mean(enrgy_sum_list)
            gnuplot_record=[i,mean,std]
            gnuplot_data.append(gnuplot_record)
    return gnuplot_data



def get_uav2_energy_data(runs_stac_list:typing.List[Statistics]):
    gnuplot_data=[]

    if len(runs_stac_list)>0:
        for i in range(0,len(runs_stac_list[0].game_states_list)-1):
            enrgy_sum_list=[]

            for run_stac in runs_stac_list:
                iteration_i_state=run_stac.game_states_list[i]
                uav=get_uav_with_index(1,iteration_i_state)
                enrgy_sum_list.append(uav.energy)

            std=get_std(enrgy_sum_list)
            mean=get_mean(enrgy_sum_list)
            gnuplot_record=[i,mean,std]
            gnuplot_data.append(gnuplot_record)

    return gnuplot_data

def get_gnuplot_energy_data(runs_stac_list:typing.List[Statistics]):
    gnuplot_data=[]

    if len(runs_stac_list)>0:
        for i in range(0,len(runs_stac_list[0].game_states_list)-1):
            enrgy_sum_list=[]

            for run_stac in runs_stac_list:
                iteration_i_state=run_stac.game_states_list[i]
                enrgy_sum_list.append(iteration_i_state.intruder.energy)

            std=get_std(enrgy_sum_list)
            mean=get_mean(enrgy_sum_list)
            gnuplot_record=[i,mean,std]
            gnuplot_data.append(gnuplot_record)

    return gnuplot_data


def get_points_map_data(hits_lists:typing.List[Hit_list],settings:Settings):
    gnuplot_data=[]


    for i in range(0,int(settings.map_size_x)):
        zone_best_value_list=[]
        zone_index=int(i / float(settings.zone_width))

        for hit_list in hits_lists:

            zone_i_best_value=hit_list.hit_list[zone_index].best_points
            if zone_i_best_value==None:
                zone_i_best_value=0
            zone_best_value_list.append(zone_i_best_value)

        std=get_std(zone_best_value_list)
        mean=get_mean(zone_best_value_list)
        gnuplot_record=[i,mean,std]
        gnuplot_data.append(gnuplot_record)

    return gnuplot_data


def get_freqency_of_hits_data(hits_lists:typing.List[Hit_list],settings:Settings):
    gnuplot_data=[]


    for i in range(0,int(settings.map_size_x)):
        zone_best_value_list=[]
        zone_index=int(i / float(settings.zone_width))

        for hit_list in hits_lists:

            zone_i_best_value=hit_list.hit_list[zone_index].number_of_hits
            if zone_i_best_value==None:
                zone_i_best_value=0
            zone_best_value_list.append(zone_i_best_value)

        std=get_std(zone_best_value_list)
        mean=get_mean(zone_best_value_list)
        gnuplot_record=[i,mean,std]
        gnuplot_data.append(gnuplot_record)

    return gnuplot_data


def export_to_gnuplot(runs_stac_list:List[Statistics],hit_lists,settings:Settings):
    data_to_export=get_gnuplot_mean_data(runs_stac_list)
    # clear_folder("./gnuplot")
    file=open("./gnuplot/mean_data.txt","w")
    save_records_to_file(data_to_export,file)
    file.close()

    file=open("./gnuplot/intruder_energy_data.txt","w")
    data_to_export=get_gnuplot_energy_data(runs_stac_list)
    save_records_to_file(data_to_export,file)
    file.close()

    file=open("./gnuplot/uav1_energy_data.txt","w")
    data_to_export=get_uav1_energy_data(runs_stac_list)
    save_records_to_file(data_to_export,file)
    file.close()
    if settings.uav_number>1:
        file=open("./gnuplot/uav2_energy_data.txt","w")
        data_to_export=get_uav2_energy_data(runs_stac_list)
        save_records_to_file(data_to_export,file)
        file.close()


    file=open("./gnuplot/points_map.txt","w")
    data_to_export=get_points_map_data(hit_lists,settings)
    save_records_to_file(data_to_export,file)
    file.close()

    file=open("./gnuplot/freqency_of_hits.txt","w")
    data_to_export=get_freqency_of_hits_data(hit_lists,settings)
    save_records_to_file(data_to_export,file)
    file.close()



