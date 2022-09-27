from Events.Game.move.algos.GameObjects.data_lists.tools.enum.enum_settings import Exploitation_types
from Events.Game.move.algos.GameObjects.data_lists.tools.multirun_tools import get_mean, get_std
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import typing

class Result_file_record():
    def __init__(self,time,postion1,postion2,tier1,tier2,points1,points2,sum_of_points, energy_spending1, energy1_spending_sum,energy_spending2,energy2_spending_sum,intruder_energy_spending,sum_intruder_energy_spending,points_sum1,points_sum2,old_points1,old_points2,old_points1_sum,old_points2_sum,actions_counter,is_true_fake_attack,leader,epslion):

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
        self.points_sum2=points_sum2
        self.points_sum1=points_sum1
        self.tier1=tier1
        self.tier2=tier2
        self.number_of_hits=1
        self.old_points1=old_points1
        self.old_points2=old_points2
        self.old_points1_sum=old_points1_sum
        self.old_points2_sum=old_points2_sum
        self.actions_counter=actions_counter
        self.is_true_fake_attack=is_true_fake_attack
        self.leader=leader
        self.is_epslion_attack=epslion


def sort_list1(x):
    return x.position1

def sort_list2(x):
    return x.position2
def sort_list_time(x):
    return x.time
class Result_file():
    def __init__(self,settings:Settings):
        self.settings = settings
        self.result_lists:typing.List[typing.List[Result_file_record]]=[]
        self.current_run=[]

    def add_record(self, postion1,position2,tier1,tier2, points1,points2,sum_of_points, time,energy_spending2,energy2_spending_sum,energy_spending1,energy1_spending_sum,intruder_energy_spending,sum_intruder_energy_spending,points_sum1,points_sum2,old_points1,old_points2,old_points1_sum,old_points2_sum,action_counter,is_true_fake_attack,is_epslion_attack,leader):
        self.current_run.append(Result_file_record(time,postion1.x,position2.x,tier1,tier2,points1,points2,sum_of_points,energy_spending1,energy1_spending_sum,energy_spending2,energy2_spending_sum,intruder_energy_spending,sum_intruder_energy_spending,points_sum1,points_sum2,old_points1,old_points2,old_points1_sum,old_points2_sum,action_counter,is_true_fake_attack,leader,is_epslion_attack))

    def end_run(self):
        self.result_lists.append(self.current_run)
        self.current_run=[]

    def reset_run(self):
        self.current_run=[]
    def save_to_file2(self, settings:Settings):
        file_name="res2"

        if settings.is_multirun:
            file_name="m_res2"
        # file=open("./results/%s.csv"%(file_name),"w")
        # settings.add_settings_to_csv(file)
        # for i,run in enumerate(self.result_lists):
        #     run.sort(key=sort_list2)
        #     file.write("#time, #att pos dr1, #tier, #att pos dr2, #tier, #pts dr1, #ener spend dr1, #ener sum spen dr1, #pts dr2, #ener spend dr2, #ener sum spen dr2, #pts sum, #intr ener spend, #intr ener sum spend\n")
        #     file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
        #     for i,record in enumerate(run):
        #
        #         str="%.2f, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
        #         file.write(str)
        # file.close()

        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_lists):
            run.sort(key=sort_list2)
            file.write(f'{"#time":<9s} {"#att pos dr1":<13s} {"#tier":<6s} {"#att pos dr2":<13s} {"#tier":<6s} {"#pts dr1":<9s} {"#ener spend dr1":<16s} {"#ener sum spen dr1":<18s} {"#pts dr2":<9s} {"#ener spend dr2":<15s} {"#ener sum spen dr2":<18s} {"#pts sum":<9s} {"#intr ener spend":<17s} {"#intr ener sum spend":<21s} {"#max intruder energy":<20s} {"#max uav energy":<16s}\n')
            file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<16s} {"8":<18s} {"9":<9s} {"10":<15s} {"11":<18s} {"12":<9s} {"13":<17s} {"14":<21s} {"15":<20s} {"16":<16s} \n')
            for i,record in enumerate(run):

                str=f'{record.time:<9.2f} {record.position1:<13.2f} {record.tier1:<6d} {record.position2:<13.2f} {record.tier2:<6d} {record.points1:<9.2f} {record.energy_spending1:<16.2f} {record.energy1_spending_sum:<18.2f} {record.points2:<9.2f} {record.energy_spending2:<15.2f} {record.energy2_spending_sum:<18.2f} {record.sum_points:<9.2f} {record.intruder_energy_spending:<18.2f}{record.sum_intruder_energy_spending:<21.2f} {settings.intruder_max_energy:<20.2f} {settings.uav_energy:<16.2f}\n'
                file.write(str)
            file.write("\n")
        file.close()





    def save_to_file1(self,settings:Settings,reasons_to_stop_simulation):

        file_name="res1"
        if settings.is_multirun:
            file_name="m_res1"
        # file=open("./results/%s.csv"%(file_name),"w")
        # settings.add_settings_to_csv(file)
        # for i,run in enumerate(self.result_lists):
        #     run.sort(key=sort_list1)
        #
        #     file.write('#time, #att pos dr1, #tier, #att pos dr2, #tier, #pts dr1, #ener spend dr1, #ener sum spen dr1, #pts dr2, #ener spend dr2, #ener sum spen dr2, #pts sum, #intr ener spend, #intr ener sum spend\n')
        #     file.write("1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14\n")
        #     for i,record in enumerate(run):
        #
        #         my_str="%.2f, %.2f, %d, %.2f, %d, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n"%(record.time,record.position1,record.tier1,record.position2,record.tier2,record.points1,record.energy_spending1,record.energy1_spending_sum,record.points2,record.energy_spending2,record.energy2_spending_sum,record.sum_points,record.intruder_energy_spending,record.sum_intruder_energy_spending)
        #         file.write(my_str)
        # file.close()

        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)
        for i,run in enumerate(self.result_lists):
            run.sort(key=sort_list1)
            file.write(f'{"#time":<9s} {"#att pos dr1":<13s} {"#tier":<6s} {"#att pos dr2":<13s} {"#tier":<6s} {"#pts dr1":<9s} {"#ener spend dr1":<16s} {"#ener sum spen dr1":<18s} {"#pts dr2":<9s} {"#ener spend dr2":<15s} {"#ener sum spen dr2":<18s} {"#pts sum":<9s} {"#intr ener spend":<17s} {"#intr ener sum spend":<21s} {"#max intruder energy":<20s} {"#max uav energy":<16s}\n')
            file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<16s} {"8":<18s} {"9":<9s} {"10":<15s} {"11":<18s} {"12":<9s} {"13":<17s} {"14":<21s} {"15":<20s} {"16":<16s}\n')

            for i,record in enumerate(run):

                my_str=f'{record.time:<9.2f} {record.position1:<13.2f} {record.tier1:<6d} {record.position2:<13.2f} {record.tier2:<6d} {record.points1:<9.2f} {record.energy_spending1:<16.2f} {record.energy1_spending_sum:<18.2f} {record.points2:<9.2f} {record.energy_spending2:<15.2f} {record.energy2_spending_sum:<18.2f} {record.sum_points:<9.2f} {record.intruder_energy_spending:<18.2f}{record.sum_intruder_energy_spending:<21.2f} {settings.intruder_max_energy:<20.2f} {settings.uav_energy:<16.2f}\n'
                file.write(my_str)
            file.write("\n")
        file.close()

        file_name="results"
        if settings.learning==False and settings.exploitation_type==Exploitation_types.EPSLION:
            file_name="results_LA"
        if settings.is_multirun:
            file_name="m_"+file_name


        file=open("./results/%s.txt"%(file_name),"w")
        settings.add_settings_to_data_file(file)
        for run_i,run in enumerate(self.result_lists):
            run.sort(key=sort_list_time)

            file.write(f'{"#time":<9s} {"#att pos dr1":<13s} {"#tier":<6s} {"#att pos dr2":<13s} {"#tier":<6s} {"#ps1":<9s} {"#pts sum dr1":<13s} {"#ener spend dr1":<16s} {"#ener sum spen dr1":<18s} {"#ps2":<9s} {"#pts sum dr2":<13s} {"#ener spend dr2":<15s} {"#ener sum spen dr2":<18s} {"#pts sum in iteration":<23s} {"#pts sum":<9s} {"#intr ener spend":<17s} {"#intr ener sum spend":<21s} {"#max intruder energy":<20s} {"#max uav energy":<16s} {"rew_thr_dr1":<16s} {"rew_thr_dr2":<16s} {"rew_sum_thr_dr1_dr2":<20s} {"reward_sum_total":<18s} ')
            if self.settings.learning==False and self.settings.exploitation_type==Exploitation_types.EPSLION:

                for i in range(0,10):
                    value_str=str(i+1)
                    file.write(f'{value_str+"a":<4s} ')
                file.write(f'{"fake":<10s} {"leader":<10s} {"eps_attack":<10s}')
            file.write("\n")

            file.write(f'{"#1":<9s} {"2":<13s} {"3":<6s} {"4":<13s} {"5":<6s} {"6":<9s} {"7":<13s} {"8":<16s} {"9":<18s} {"10":<9s} {"11":<13s} {"12":<15s} {"13":<18s} {"14":<23s} {"15":<9s} {"16":<17s} {"17":<21s} {"18":<20s} {"19":<16s} {"20":<16s} {"21":<16s} {"22":<20s} {"23":<18s} ')
            if self.settings.learning==False and self.settings.exploitation_type==Exploitation_types.EPSLION:

                for i in range(0,10):
                    file.write(f'{i+24:<4d} ')
                file.write(f'{35:<10d} {36:<10d} {37:<10d}')
            file.write("\n")
            for i,record in enumerate(run):
                sum_to_print_new=record.points1+record.points2
                sum_to_print_old=record.old_points1+record.old_points2
                if record.is_true_fake_attack:
                    # record.points1=-1
                    # record.points2=-1
                    record.old_points1=-1
                    record.old_points2=-1
                    # sum_to_print_new=-1
                    # sum_to_print_old=-1

                my_str=f'{record.time:<9.2f} {record.position1:<13.2f} {record.tier1:<6d} {record.position2:<13.2f} {record.tier2:<6d} {record.old_points1:<9.2f} {record.old_points1_sum:<13.2f} {record.energy_spending1:<16.2f} {record.energy1_spending_sum:<18.2f} {record.old_points2:<9.2f} {record.old_points2_sum:<13.2f} {record.energy_spending2:<15.2f} {record.energy2_spending_sum:<18.2f} {sum_to_print_old:<23.2f} {record.old_points1_sum+record.old_points2_sum:<9.2f} {record.intruder_energy_spending:<18.2f}{record.sum_intruder_energy_spending:<21.2f} {settings.intruder_max_energy:<20.2f} {settings.uav_energy:<16.2f} {record.points1:<16.2f} {record.points2:<16.2f} {sum_to_print_new:<20.2f} {record.points_sum1+record.points_sum2:<18.2f} '
                file.write(my_str)
                if self.settings.learning==False and self.settings.exploitation_type==Exploitation_types.EPSLION:
                    for i in range(0,10):
                        if len(record.actions_counter)>i:
                            file.write(f'{record.actions_counter[i]:<4d} ')
                        else:
                            file.write(f'{"-":<4s} ')
                    if record.is_true_fake_attack:
                        file.write(f'{record.is_true_fake_attack:<10d} {"-":<10s} {"-":<10s}')
                    else:
                        file.write(f'{record.is_true_fake_attack:<10d} {record.leader:<10d} {record.is_epslion_attack:<10d}')
                file.write("\n")


            file.write("reason to stop: %s\n"%(reasons_to_stop_simulation[run_i].value))
            file.write("\n")
        file.close()


        if settings.is_multirun:
            file=open("./results/std_results.txt","w")

            settings.add_settings_to_data_file(file)
            file.write(f'{"#iter":<9s} {"best_avg":<9s} {"best_std":<9s}\n')
            file.write(f'{"#1":<9s} {"2":<9s} {"3":<9s} \n')
            for i,record in enumerate(self.result_lists[0]):
                values=[]
                for _,run in enumerate(self.result_lists):
                    try:
                        values.append(run[i].points1+run[i].points2)
                    except IndexError:
                        pass
                mean_value=get_mean(values)
                std_value=get_std(values)
                my_str=f'{i+1:<9d} {mean_value:<9.2f} {std_value:<9.2f}\n'
                file.write(my_str)



                # file.write("\n")
            file.close()

