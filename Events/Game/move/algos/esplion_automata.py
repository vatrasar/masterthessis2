import typing
from random import Random

from Events.Game.move.algos.GameObjects.data_lists.Result_list import Result_record
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings


class Epslion_automata():

    def __init__(self,settings:Settings):
        self.lr_memory:typing.List[typing.List[Result_record]]=[[],[]]

        self.is_trainning=True
        self.is_reset=False
        self.settings=settings
        self.candidates_for_lr:typing.List[typing.List[int]]=[[],[]]
        self.last_action=None
        self.all_goals_list=None
        self.leader=0
        self.action_counter=[]
        self.is_active_epslion_attack=False
        self.epslion_automata_old=[]
        self.was_last_epsilion=False

        for i in range(0,10):
            self.action_counter.append(0)



    def reset(self):
        self.lr_memory:typing.List[typing.List[Result_record]]=[]
        self.is_trainning=True
        self.is_reset=False
    def save_old_memory(self):
       memmory_to_save=[[],[]]
       for record in self.lr_memory[0]:
            memmory_to_save[0].append(record)
       for record in self.lr_memory[1]:
            memmory_to_save[1].append(record)
       self.epslion_automata_old.append(memmory_to_save)
    def get_random_action_for_training(self,random:Random):

        self.switch_leader()
        action=self.candidates_for_lr[self.leader][random.randint(0,len(self.candidates_for_lr[self.leader])-1)]

        self.last_action=action
        return action

    def switch_leader(self):
        if self.leader == 0:
            self.leader = 1
        else:
            self.leader = 0
    def un_register_attack(self, points):
        new_record:Result_record=self.last_action.copy()
        self.lr_memory[self.leader].remove(self.lr_memory[self.leader][0])
        new_record.points=points
        self.lr_memory[self.leader].append(new_record)
        self.is_active_epslion_attack=False
        self.save_old_memory()

    def append_new_record(self,points_sum):
        if self.last_action!=None:
            if points_sum==0:
                return
            new_record:Result_record=self.last_action.copy()
            new_record.points=points_sum
            if self.settings.l_lr>len(self.lr_memory[self.leader]):
                self.lr_memory[self.leader].append(new_record)
            self.last_action=None

            if self.settings.l_lr<=len(self.lr_memory[0]) and self.settings.l_lr<=len(self.lr_memory[1]):
                self.is_reset=True

    def load_data_from_files(self):
        file1=open("settingsFiles/goals_uav1.txt", "r")
        file2=open("settingsFiles/goals_uav2.txt")

        temp_candidates=[[],[]]
        lines=file1.readlines()
        lines=lines[1:]
        for line in lines:

            action_number=int(line)
            temp_candidates[0].append(action_number)
        file1.close()

        lines=file2.readlines()
        lines=lines[1:]
        for line in lines:

            action_number=int(line)
            temp_candidates[1].append(action_number)



        file2.close()



        #translation for real records
        for i,uv_lr_list in enumerate(temp_candidates):
            for index_of_action in uv_lr_list:

                for record in self.all_goals_list:
                    if record.action_number == index_of_action:
                        self.candidates_for_lr[i].append(record)

    def set_source_for_lr(self, result_list):
        self.all_goals_list=result_list

    def choose_best(self):
        self.switch_leader()
        self.is_active_epslion_attack=True
        best=None
        for i in self.lr_memory[self.leader]:
            if best==None:
                best=i
            elif best.points<i.points:
                best=i
        self.last_action=best

        self.action_counter[self.last_action.action_number]=self.action_counter[self.last_action.action_number]+1
        return best

    def update_action_counter(self, action_number,action):
        self.action_counter[action_number]=self.action_counter[action_number]+1
        self.last_action=action


    def save_old_lr_memory(self):
        file1=open("./results/automata_memory1.txt","w")
        file2=open("./results/automata_memory2.txt", "w")
        iteration_counter=0
        for memory in self.epslion_automata_old:

            if iteration_counter==0:
                file1.write("start\n")
            else:
                file1.write("iteration %d\n"%(iteration_counter))

            file1.write(f'{"#action id":<10s} {"av pts":<10s}\n')
            for record in memory[0]:
                file1.write(f'{record.action_number:<10d} {record.points/2.0:<10.2f}\n')

            if iteration_counter==0:
                file2.write("start\n")
            else:
                file2.write("iteration %d\n"%(iteration_counter))
            file2.write(f'{"#action id":<10s} {"av pts":<10s}\n')
            for record in memory[1]:
                file2.write(f'{record.action_number:<10d} {record.points/2.0:<10.2f}\n')

            iteration_counter=iteration_counter+1
        file1.close()
        file2.close()
