from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import typing

class Result_file_record():
    def __init__(self,time,postion1,postion2,tier1,tier2,points1,points2,sum_of_points, energy_spending1, energy1_spending_sum,energy_spending2,energy2_spending_sum,intruder_energy_spending,sum_intruder_energy_spending):

        self.sum_intruder_energy_spending = sum_intruder_energy_spending
        self.intruder_energy_spending = intruder_energy_spending
        self.energy2_spending_sum = energy2_spending_sum
        self.energy_spending2 = energy_spending2
        self.energy1_spending_sum = energy1_spending_sum
        self.energy_spending1 = energy_spending1
        self.time = time

        self.sum_points = sum_of_points
        self.position1 =postion1
        self.position2 =postion2
        self.points1=points1
        self.points2=points2

        self.tier1=tier1
        self.tier2=tier2
        self.number_of_hits=1


class Result_file():
    def __init__(self,settings:Settings):
        self.settings = settings
        self.result_lists:typing.List[typing.List[Result_file_record]]=[]
        self.current_run=[]

    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points, time,energy_spending2,energy2_spending_sum,energy_spending1,energy1_spending_sum,intruder_energy_spending,sum_intruder_energy_spending):
        self.current_run.append(Result_file_record(time,postion1.x,position2.x,tier1,tier2,points1,points2,sum_of_points,energy_spending1,energy1_spending_sum,energy_spending2,energy2_spending_sum,intruder_energy_spending,sum_intruder_energy_spending))

    def end_run(self):
        self.result_lists.append(self.current_run)
        self.current_run=[]

    def save_to_file(self,settings:Settings):

        file=open("./data/results.csv","w")
        settings.add_settings_to_csv(file)
        for i,run in enumerate(self.result_lists):
            file.write("#time, #attack postion drone 1 ,#tier, #attack position drone 2, #tier, #points1,#energy spending dr1, #sum energy spending dr1, #points dr2,#energy spending dr2, #sum energy spending dr2, #sum of points, #intruder energy spending, #sum of intruder energy spending\n")
            for i,record in enumerate(run):

                str="%.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
                file.write(str)
        file.close()

        file=open("./data/results.txt","w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_lists):
            file.write("#time #attack postion drone 1 #tier #attack position drone 2 #tier #points1 #energy spending dr1 #sum energy spending dr1 #points dr2 #energy spending dr2 #sum energy spending dr2 #sum of points #intruder energy spending #sum of intruder energy spending\n")
            for i,record in enumerate(run):

                str="%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
                file.write(str)
        file.close()
