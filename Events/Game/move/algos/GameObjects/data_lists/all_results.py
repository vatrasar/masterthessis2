import typing

from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Learning_algos
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings


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
        self.result_tr_list:typing.List[Result_tr_record]=[]


    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points, current_solution1=None,current_solution2=None,accept_prob=None,x=None,decision=None,temperature=None):
        self.result_tr_list.append(Result_tr_record(postion1,position2,tier1,tier2,points1,points2,sum_of_points,current_solution1,current_solution2,accept_prob,x,decision,temperature))


    def save_to_file(self,settings):

        file=open("./data/results_tr.csv","w")

        if settings.learning_algo_type==Learning_algos.SA:
            file.write("#iteration, #attack postion drone 1 ,#tier1, #attack position drone 2, #tier2, #points1, #points2, #sum of points, #curr solution1, #curr solution2, #accept probablity, #x, #accept/reject, #temperature\n")
            for i,record in enumerate(self.result_tr_list):
                str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %s, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points,record.current_solution1.x,record.current_solution2.x,record.accept_prob,record.x,record.decision,record.temperature)
                file.write(str)
        else:
            file.write("#iteration, #attack postion drone 1 ,#tier1, #attack position drone 2, #tier2, #points1, #points2, #sum of points\n")
            for i,record in enumerate(self.result_tr_list):

                str="%d, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f\n"%(i,record.position1.x,record.tier1,record.position2.x,record.tier2,record.points1,record.points2,record.sum_points)
                file.write(str)
        file.close()