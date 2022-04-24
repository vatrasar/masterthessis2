import math
from typing import List

from Events.Game.Statistics import Statistics
from Events.Game.game_state_stac import GameStateStac


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

def get_gnuplot_data(runs_stac_list:List[Statistics]):
    gnuplot_data=[]

    if len(runs_stac_list)>0:
        for i in range(0,len(runs_stac_list[0].game_states_list)-1):
            point_sums_list=[]

            for run_stac in runs_stac_list:
                iteration_i_state=run_stac.game_states_list[i]
                point_sums_list.append(get_uav_points_sum(iteration_i_state))

            std=get_std(point_sums_list)
            mean=get_mean(point_sums_list)
            gnuplot_record=[i,std,mean]
            gnuplot_data.append(gnuplot_record)

    return gnuplot_data


def save_records_to_file(data_to_export:List,file):
    for record in data_to_export:
        file.write("%d %.2f %.2f\n"%(record[0],record[1],record[2]))




def export_to_gnuplot(runs_stac_list:List[Statistics]):
    data_to_export=get_gnuplot_data(runs_stac_list)
    # clear_folder("./gnuplot")
    file=open("./gnuplot/data.txt","w")
    save_records_to_file(data_to_export,file)
    file.close()



