import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Learning_algos, Modes
from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import print_line
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings

def sort_uav1_pos(u):
    return u.position1.x

def sort_uav2_pos(u):
    return u.position2.x

class Result_tr_record():
    def __init__(self,postion1,postion2,tier1,tier2,points1,points2,sum_of_points, current_solution1,current_solution2,accept_prob,x,decision,temperature):

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


class Result_tr_list():
    def __init__(self,settings:Settings):
        self.settings = settings
        self.result_tr_list:typing.List[typing.List[Result_tr_record]]=[]
        self.current_run=[]



    def end_run(self):
        self.result_tr_list.append(self.current_run)
        self.current_run=[]
    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points, current_solution1=None,current_solution2=None,accept_prob=None,x=None,decision=None,temperature=None):
        self.current_run.append(Result_tr_record(postion1,position2,tier1,tier2,points1,points2,sum_of_points,current_solution1,current_solution2,accept_prob,x,decision,temperature))


    def save_to_file(self,settings):

        file=open("./results/res1_tr.csv","w")
        settings.add_settings_to_csv(file)
        for i,run in enumerate(self.result_tr_list):
            run.sort(key=sort_uav1_pos)
            file.write("run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum, #curr sol1, #curr sol2, #acc prob, #x,   #acc/rej, #temp\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
                for i,record in enumerate(run):
                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
                for i,record in enumerate(run):

                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
        file.close()

        file=open("./results/res1_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):

            file.write("#run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                header_list=["#iter", "#att pos dr1", "#tier1", "#att pos dr2", "#tier2", "#pts1", "#pts2", "#pts sum", "#curr sol1", "#curr sol2", "#acc prob", "#x","#acc/rej", "#temp"]
                print_line(file,header_list)
                file.write("#1 2 3 4 5 6 7 8 9 10 11 12 13 14\n")
                for i,record in enumerate(run):
                    str="%d %.2f %d %.2f %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %s %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter #att pos dr1 #tier1 #att pos dr2 #tier2 #pts1 #pts2 #pts sum\n")
                file.write("#1 2 3 4 5 6 7 8\n")
                for i,record in enumerate(run):

                    str="%d %.2f %d %.2f %d %.2f %.2f %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
            file.write("\n")
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
                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter, #att pos dr1, #tier1, #att pos dr2, #tier2, #pts1, #pts2, #pts sum\n")
                file.write("1, 2, 3, 4, 5, 6, 7, 8\n")
                for i,record in enumerate(run):

                    str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
        file.close()

        file=open("./results/res2_tr.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_tr_list):
            file.write("#run %d\n"%(i+1))
            if settings.learning_algo_type==Learning_algos.SA and settings.mode==Modes.LEARNING:
                file.write("#iter #att pos dr1 #tier1 #att pos dr2 #tier2 #pts1 #pts2 #pts sum #curr sol1 #curr sol2 #acc prob #x   #acc/rej #temp\n")
                file.write("#1 2 3 4 5 6 7 8 9 10 11 12 13 14\n")
                for i,record in enumerate(run):
                    str="%d %.2f %d %.2f %d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %s %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                    file.write(str)
            else:
                file.write("#iter #att pos dr1 #tier1 #att pos dr2 #tier2 #pts1 #pts2 #pts sum\n")
                file.write("#1 2 3 4 5 6 7 8\n")
                for i,record in enumerate(run):

                    str="%d %.2f %d %.2f %d %.2f %.2f %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                    file.write(str)
            file.write("\n")
        file.close()
