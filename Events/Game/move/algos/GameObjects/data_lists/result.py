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

def sort_list1(x):
    return x.position1

def sort_list2(x):
    return x.position2
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

    def save_to_file2(self, settings:Settings):
        file_name="res2"

        if settings.is_multirun:
            file_name="m_res2"
        file=open("./results/%s.csv"%(file_name),"w")
        settings.add_settings_to_csv(file)
        for i,run in enumerate(self.result_lists):
            run.sort(key=sort_list2)
            file.write("#time, #att pos dr1, #tier, #att pos dr2, #tier, #ps1, #ener spend dr1, #ener sum spen dr1, #pts dr2, #ener spend dr2, #ener sum spen dr2, #pts sum, #intr ener spend, #intr ener sum spend\n")
            file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
            for i,record in enumerate(run):

                str="%.2f, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
                file.write(str)
        file.close()

        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_lists):
            file.write(f'{"#time":<9s} {"#att pos dr1":<13s} {"#tier":<6s} {"#att pos dr2":<13s} {"#tier":<6s} {"#ps1":<9s} {"#ener spend dr1":<16s} {"#ener sum spen dr1":<18s} {"#pts dr2":<9s} {"#ener spend dr2":<15s} {"#ener sum spen dr2":<18s} {"#pts sum":<9s} {"#intr ener spend":<17s} {"#intr ener sum spend":<17s}\n')
            file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<16s} {"8":<18s} {"9":<9s} {"10":<15s} {"11":<18s} {"12":<9s} {"13":<17s} {"14":<17s}\n')
            for i,record in enumerate(run):

                str=f'{record.time:<9.2f} {record.position1:<13.2f} {record.tier1:<6d} {record.position2:<13.2f} {record.tier2:<6d} {record.points1:<9.2f} {record.energy_spending1:<16.2f} {record.energy1_spending_sum:<18.2f} {record.points2:<9.2f} {record.energy_spending2:<15.2f} {record.energy2_spending_sum:<18.2f} {record.sum_points:<9.2f} {record.intruder_energy_spending:<18.2f}{record.sum_intruder_energy_spending:<17.2f}\n'
                file.write(str)
            file.write("\n")
        file.close()

    def save_to_file1(self,settings:Settings):

        file_name="res1"
        if settings.is_multirun:
            file_name="m_res1"
        file=open("./results/%s.csv"%(file_name),"w")
        settings.add_settings_to_csv(file)
        for i,run in enumerate(self.result_lists):
            run.sort(key=sort_list1)

            file.write('#time, #att pos dr1, #tier, #att pos dr2, #tier, #ps1, #ener spend dr1, #ener sum spen dr1, #pts dr2, #ener spend dr2, #ener sum spen dr2, #pts sum, #intr ener spend, #intr ener sum spend\n')
            file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
            for i,record in enumerate(run):

                str="%.2f, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
                file.write(str)
        file.close()

        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_lists):
            file.write(f'{"#time":<9s} {"#att pos dr1":<13s} {"#tier":<6s} {"#att pos dr2":<13s} {"#tier":<6s} {"#ps1":<9s} {"#ener spend dr1":<16s} {"#ener sum spen dr1":<18s} {"#pts dr2":<9s} {"#ener spend dr2":<15s} {"#ener sum spen dr2":<18s} {"#pts sum":<9s} {"#intr ener spend":<17s} {"#intr ener sum spend":<17s}\n')
            file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<16s} {"8":<18s} {"9":<9s} {"10":<15s} {"11":<18s} {"12":<9s} {"13":<17s} {"14":<17s}\n')

            for i,record in enumerate(run):

                str=f'{record.time:<9.2f} {record.position1:<13.2f} {record.tier1:<6d} {record.position2:<13.2f} {record.tier2:<6d} {record.points1:<9.2f} {record.energy_spending1:<16.2f} {record.energy1_spending_sum:<18.2f} {record.points2:<9.2f} {record.energy_spending2:<15.2f} {record.energy2_spending_sum:<18.2f} {record.sum_points:<9.2f} {record.intruder_energy_spending:<18.2f}{record.sum_intruder_energy_spending:<17.2f}\n'
                file.write(str)
            file.write("\n")
        file.close()

