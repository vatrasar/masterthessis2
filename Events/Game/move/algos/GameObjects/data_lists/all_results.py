import typing

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
    def __init__(self,postion1,postion2,tier1,tier2,points1,points2,sum_of_points, current_solution1,current_solution2,accept_prob,x,decision,temperature,dr1_points,dr2_points,current_best_result):

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


class Result_tr_list():
    def __init__(self,settings:Settings):
        self.settings = settings
        self.result_tr_list:typing.List[typing.List[Result_tr_record]]=[]
        self.current_run=[]
        self.current_best_result=0



    def end_run(self):
        self.result_tr_list.append(self.current_run)
        self.current_run=[]
    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points,dr1_points,dr2_points, current_solution1=None,current_solution2=None,accept_prob=None,x=None,decision=None,temperature=None):

        current_mean_result=(points1+points2)/2.0
        if current_mean_result>self.current_best_result:
            self.current_best_result=current_mean_result
        self.current_run.append(Result_tr_record(postion1,position2,tier1,tier2,points1,points2,sum_of_points,current_solution1,current_solution2,accept_prob,x,decision,temperature,dr1_points,dr2_points,self.current_best_result))


    def save_to_file(self,settings):





        for i,run in enumerate(self.result_tr_list):

            for i,record in enumerate(run):
                record.iter=i+1

        file=open("./results/res1_tr.csv","w")
        settings.add_settings_to_csv(file)
        for i,run in enumerate(self.result_tr_list):
            run.sort(key=sort_uav1_pos)
            file.write("run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum, #curr sol1, #curr sol2, #acc prob, #x,   #acc/rej, #temp\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
                for i,record in enumerate(run):
                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
                for i,record in enumerate(run):

                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
        file.close()

        file=open("./results/res1_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):

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

        file_name="results"
        if settings.is_multirun:
            file_name="m_results"
        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)

        for i,run in enumerate(self.result_tr_list):
            run.sort(key=sort_iterations)
            file.write("#run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:

                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum iteration":<20s} {"#pts sum":<9s} {"#curr sol1":<10s} {"#curr sol2":<10s} {"#acc prob":<10s} {"#x":<6s} {"#acc/rej":<9s} {"#temp":<9s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<20s} {"9":<9s} {"10":<10s} {"11":<10s} {"12":<10s} {"13":<6s} {"14":<9s} {"15":<9s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<20.2f} {record.dr1_points+record.dr2_points:<9.2f} {record.current_solution1.x:<10.2f} {record.current_solution2.x:<10.2f} {record.accept_prob:<10.2f} {record.x:<6.2f} {record.decision:<9d} {record.temperature:<9.2f}\n'
                    file.write(str)
            else:
                file.write(f'{"#iter":<9s} {"#att pos dr1":<13s} {"#tier1":<6s} {"#att pos dr2":<13s} {"#tier2":<6s} {"#pts1":<9s} {"#pts2":<9s} {"#pts sum":<9s} {"best result":<12s}\n')
                file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<9s} {"8":<9s} {"9":<12s}\n')
                for i,record in enumerate(run):

                    str=f'{record.iter:<9d} {record.position1.x:<13.2f} {record.tier1:<6d} {record.position2.x:<13.2f} {record.tier2:<6.2f} {record.points1:<9.2f} {record.points2:<9.2f} {record.sum_points:<9.2f} {record.current_best_result:<12.2f}\n'
                    file.write(str)
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

        file=open("./results/res2_tr.csv","w")
        settings.add_settings_to_csv(file)


        for i,run in enumerate(self.result_tr_list):
            file.write("run %d\n"%(i+1))
            run.sort(key=sort_uav2_pos)
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:

                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum, #curr sol1, #curr sol2, #acc prob, #x,   #acc/rej, #temp\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
                for i,record in enumerate(run):
                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
                for i,record in enumerate(run):

                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(record.iter,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
        file.close()

        file=open("./results/res2_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):
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
