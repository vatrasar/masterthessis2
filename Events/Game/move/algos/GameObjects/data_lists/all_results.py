import typing

from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_record
from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Learning_algos, Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.multirun_tools import get_mean, get_std
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings

def sort_uav1_pos(u):
    return u.position1.x

def sort_uav2_pos(u):
    return u.position2.x

def sort_iterations(u):
    return u.iter

class Result_tr_record():
    def __init__(self,postion1,postion2,tier1,tier2,points1,points2,sum_of_points, current_solution1,current_solution2,accept_prob,x,decision,temperature,dr1_points,dr2_points,current_best_result,av_pts=0,number_of_no_progress=0,not_accept_counter=0,diff=0.0,av_pts_new=0.0):


        self.dr1_points = dr1_points
        self.dr2_points = dr2_points
        self.temperature = temperature
        self.decision = decision
        self.x = x

        self.accept_prob = accept_prob
        self.current_solution2 = current_solution2
        self.current_solution1 = current_solution1
        self.sum_points = sum_of_points
        self.position1 =postion1
        self.position2 =postion2
        self.points1=points1
        self.points2=points2
        self.points2=points2
        self.tier1=tier1
        self.tier2=tier2
        self.number_of_hits=1
        self.iter=0
        self.current_best_result=current_best_result
        self.c_best=-1
        self.not_accept_counter=not_accept_counter
        self.av_pts=av_pts
        self.number_of_no_progress=number_of_no_progress
        self.diff=diff
        self.av_pts_new=av_pts_new


    def copy_iteration(self,iteration_to_copy):
        self.dr1_points = iteration_to_copy.dr1_points
        self.dr2_points = iteration_to_copy.dr2_points


        # self.x = iteration_to_copy.x


        # self.current_solution2 = iteration_to_copy.current_solution2
        # self.current_solution1 = iteration_to_copy.current_solution1
        self.sum_points = iteration_to_copy.sum_points
        self.position1 =iteration_to_copy.position1
        self.position2 =iteration_to_copy.position2
        self.points1=iteration_to_copy.points1
        self.points2=iteration_to_copy.points2
        self.points2=iteration_to_copy.points2
        self.tier1=iteration_to_copy.tier1
        self.tier2=iteration_to_copy.tier2


def sort_results(e:Result_record):
    return e.points
class Result_tr_list():
    def __init__(self,settings:Settings):
        self.settings = settings
        self.result_tr_list:typing.List[typing.List[Result_tr_record]]=[]
        self.current_run=[]
        self.current_best_result=0



    def end_run(self):
        self.result_tr_list.append(self.current_run)
        self.current_run=[]
        self.current_best_result=0

    def reset_run(self):
        self.current_run=[]
        self.current_best_result=0
    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points,dr1_points,dr2_points,av_pts=None, current_solution1=None,current_solution2=None,accept_prob=None,x=None,decision=None,temperature=None,number_of_no_progress=None,not_accept_counter=None,av_pts_new=None, diff=None,best_list=None):

        current_mean_result=(points1+points2)/2.0
        if current_mean_result>self.current_best_result:
            self.current_best_result=current_mean_result


        if self.settings.learning_algo_type==Learning_algos.SA:
            self.current_run.append(Result_tr_record(postion1,position2,tier1,tier2,points1,points2,sum_of_points,current_solution1,current_solution2,accept_prob,x,decision,temperature,dr1_points,dr2_points,self.current_best_result,av_pts,number_of_no_progress,not_accept_counter,diff,av_pts_new))
        else:
            self.current_run.append(Result_tr_record(postion1,position2,tier1,tier2,points1,points2,sum_of_points,current_solution1,current_solution2,accept_prob,x,decision,temperature,dr1_points,dr2_points,best_list[0].points))


    def save_to_file(self,settings,reasons_to_stop_simulation):





        for i,run in enumerate(self.result_tr_list):

            for i,record in enumerate(run):
                record.iter=i+1

        # file=open("./results/res1_tr.csv","w")
        # settings.add_settings_to_csv(file)
        # for i,run in enumerate(self.result_tr_list):
        #     run.sort(key=sort_uav1_pos)
        #     file.write("run %d\n"%(i+1))
        #     if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
        #         file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum, #curr sol1, #curr sol2, #acc prob, #x,   #acc/rej, #temp\n")
        #         file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
        #         for i,record in enumerate(run):
        #             str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
        #             file.write(str)
        #     else:
        #         file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
        #         file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
        #         for i,record in enumerate(run):
        #
        #             str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
        #             file.write(str)
        # file.close()

        file=open("./results/res1_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):



            run.sort(key=sort_uav1_pos)
            file.write("#run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:

                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"#curr sol1":<10s} {"#curr sol2":<10s} {"#acc prob":<10s} {"#x":<6s} {"#acc/rej":<9s} {"#temp":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<10s} {"10":<10s} {"11":<10s} {"12":<6s} {"13":<9s} {"14":<9s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f} {record.current_solution1.x:<10.2f} {record.current_solution2.x:<10.2f} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
                    file.write(str)
            else:
                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"#av pts":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<9s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f}\n'
                    file.write(str)
            file.write("\n")
        file.close()

        file_name="results_tr"
        if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
            file_name="sa_results"
        if settings.is_multirun:
            file_name="m_"+file_name
        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)

        for run_i,run in enumerate(self.result_tr_list):

            run.sort(key=sort_iterations)
            file.write("#run %d\n"%(run_i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
            #
            #     file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum iteration":<20s} {"#pts sum":<9s} {"#curr sol1":<10s} {"#curr sol2":<10s} {"#acc prob":<10s} {"#x":<6s} {"#acc/rej":<9s} {"#temp":<9s}\n')
            #     file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<20s} {"9":<9s} {"10":<10s} {"11":<10s} {"12":<10s} {"13":<6s} {"14":<9s} {"15":<9s}\n')
            #     for i,record in enumerate(run):
            #
            #         str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<20.2f} {record.dr1_points+record.dr2_points:<9.2f} {record.current_solution1.x:<10.2f} {record.current_solution2.x:<10.2f} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
            #         file.write(str)


                for counter,iteration in enumerate(run):


                    if counter+1<len(run):
                        iteration.c_best=run[counter+1].av_pts
                        # if (counter+1)%settings.annealing_number_of_iterations==0:
                        #     counter_refues=0
                        # if run[counter+1].decision==0:
                        #     counter_refues=counter_refues+1
                        # iteration.not_accept_counter=counter_refues
                        iteration.not_accept_counter=run[counter+1].not_accept_counter
                        iteration.number_of_no_progress=run[counter+1].number_of_no_progress
                        iteration.diff=run[counter+1].diff
                        iteration.av_pts_new=run[counter+1].av_pts_new
                    else:
                        iteration.c_best="-"
                        iteration.not_accept_counter="-"
                        iteration.number_of_no_progress="-"
                        iteration.diff="-"
                        iteration.av_pts_new="-"

                    if iteration.decision==0:
                        previous_iteration=run[counter-1]
                        iteration.copy_iteration(previous_iteration)

                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"#av_pts":<9s} {"#c_best":<9s} {"av_pts_new":<11s} {"del":<9s} {"#not accept counter":<21s} {"not_improve_counter":<21s} {"#acc prob":<10s} {"#x":<6s} {"#acc/rej":<9s} {"#temp":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<9s} {"10":<9s} {"11":<11s} {"12":<9s} {"13":<21s} {"14":<21s} {"15":<10s} {"16":<6s} {"17":<9s} {"18":<9s}\n')
                for i,record in enumerate(run):
                    if len(run)>i+1:
                        str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.points1+record.points2:<9.2f} {record.av_pts/2.0:<9.2f} {record.c_best/2.0:<9.2f} {record.av_pts_new:<11.2f} {record.diff:<9.2f} {record.not_accept_counter:<21.2f} {record.number_of_no_progress:<21.2f} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
                    else:
                        str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.points1+record.points2:<9.2f} {record.av_pts/2.0:<9.2f} {record.c_best:<9s} {record.av_pts_new:<11.2s} {record.diff:<9.2s} {record.not_accept_counter:<21s} {record.number_of_no_progress:<21s} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
                    file.write(str)
            else:
                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"best result":<12s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<12s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f} {record.current_best_result:<12.2f}\n'
                    file.write(str)
            file.write("reason to stop: %s\n"%(reasons_to_stop_simulation[run_i].value))
            file.write("\n")

        file.close()
        if settings.is_multirun:
            file=open("./results/std_results.txt","w")

            settings.add_settings_to_data_file(file)
            file.write(f'{"#iter":<9s} {"best_avg":<9s} {"best_std":<9s}\n')
            file.write(f'{"#1":<9s} {"2":<9s} {"3":<9s} \n')
            for i,record in enumerate(self.result_tr_list[0]):
                values=[]
                for _,run in enumerate(self.result_tr_list):
                    try:
                        values.append(run[i].points1+run[i].points2)
                    except IndexError:
                        pass
                mean_value=get_mean(values)
                std_value=get_std(values)
                str=f'{record.iter:<9d} {mean_value:<9.2f} {std_value:<9.2f}\n'
                file.write(str)



                # file.write("\n")
            file.close()


    def save_to_file_uav1(self,settings):
        #
        # file=open("./results/res2_tr.csv","w")
        # settings.add_settings_to_csv(file)
        #
        #
        # for i,run in enumerate(self.result_tr_list):
        #     file.write("run %d\n"%(i+1))
        #     run.sort(key=sort_uav2_pos)
        #     if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
        #
        #         file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum, #curr sol1, #curr sol2, #acc prob, #x,   #acc/rej, #temp\n")
        #         file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
        #         for i,record in enumerate(run):
        #             str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
        #             file.write(str)
        #     else:
        #         file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
        #         file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
        #         for i,record in enumerate(run):
        #
        #             str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
        #             file.write(str)
        # file.close()

        file=open("./results/res2_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):
            run.sort(key=sort_uav2_pos)
            file.write("#run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"#curr sol1":<10s} {"#curr sol2":<10s} {"#acc prob":<10s} {"#x":<6s} {"#acc/rej":<9s} {"#temp":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<10s} {"10":<10s} {"11":<10s} {"12":<6s} {"13":<9s} {"14":<9s}\n')
                for i,record in enumerate(run):
                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f} {record.current_solution1.x:<10.2f} {record.current_solution2.x:<10.2f} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
                    file.write(str)
            else:
                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f}\n'
                    file.write(str)
            file.write("\n")
        file.close()
