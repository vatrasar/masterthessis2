from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import typing

class Sos_record():
    def __init__(self,position1,position2, time):
        self.time = time
        self.position2 = position2
        self.position1 = position1

class Sos_list():

    def __init__(self,settings:Settings):
        self.settings = settings
        self.sos_list:typing.List[typing.List[Sos_record]]=[]
        self.current_sos_list:typing.List[Sos_record]=[]

    def add_record(self,time,position1,postion2):
        sos_record=Sos_record(position1,postion2,time)
        self.current_sos_list.append(sos_record)

    def end_run(self):
        self.sos_list.append(self.current_sos_list)
        self.current_sos_list=[]

    def save(self):
        file=open("./results/sos.txt","w")
        self.settings.add_settings_to_csv(file)
        for i,run in enumerate(self.sos_list):
            # run.sort(key=sort_uav1_pos)
            file.write("#run %d\n"%(i+1))

            file.write(f'{"#time":<9s} {"position1":<12s} {"position2":<12s}\n')
            file.write(f'{"#1":<9s} {"2":<12s} {"3":<12s}\n')
            for i,record in enumerate(run):
                str=f'{record.time:<9.2f} {record.position1.x:<12.2f} {record.position2.x:<12.2f}\n'
                file.write(str)
            file.write('\n')
        file.close()

