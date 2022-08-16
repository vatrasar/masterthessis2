import random

from Events.Game.Statistics import Statistics
from Events.Game.move.algos.GameObjects.data_lists.tools.other_tools import clear_folder
from runner import Runner
from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings
import time
import os
import shutil

def main():
    settings:Settings=Settings()
    statistics=Statistics(settings)

    try:
        settings_file_name_f=open("settingsFiles/settingsFileName.txt")
        settingsFileName_line:str=settings_file_name_f.readline()[0:-1]
        rewardsFileName_line:str=settings_file_name_f.readline()

        _,settingsFileName=settings.get_property_pair(settingsFileName_line)
        _,rewardsFileName=settings.get_property_pair(rewardsFileName_line)
        file_with_properties=open("settingsFiles/"+settingsFileName)
        file_with_rewards=open("settingsFiles/"+rewardsFileName)
        file_with_boxes=open("settingsFiles/"+"boxes.txt")
        file_with_invisible=open("settingsFiles/"+"invisible_boxes.txt")
        clear_folder("./history/temp")
        clear_folder("./history/history")
        settings.get_properties(file_with_properties,file_with_rewards,file_with_boxes,file_with_invisible)
    except Exception as exp:
        print(str(exp))
        input(" press close to exit ")
        return


    rand = random.Random(settings.seed)  # 800
    settings.acutal_seed=int(time.time())
    if settings.seed_clock:
        rand =random.Random(settings.acutal_seed) #
    #init state
    if settings.is_directory:
        list_of_files=os.listdir(settings.target_directory)

        for file_name in list_of_files:
            random_for_experyment=random.Random(settings.seed)
            file_with_rewards.close()
            file_with_boxes.close()
            file_with_invisible.close()
            file_with_rewards=open("settingsFiles/"+rewardsFileName)
            file_with_boxes=open("settingsFiles/"+"boxes.txt")
            file_with_invisible=open("settingsFiles/"+"invisible_boxes.txt")


            file_with_properties=open(settings.target_directory+"/"+file_name)
            settings_for_run:Settings=Settings()
            if settings.seed_clock:
                settings_for_run.acutal_seed=rand.randint(0,100000000)
                random_for_experyment=random.Random(rand)
            else:
                settings_for_run.acutal_seed=settings_for_run.seed
            settings_for_run.get_properties(file_with_properties,file_with_rewards,file_with_boxes,file_with_invisible)
            statistics=Statistics(settings_for_run)

            runner=Runner(settings_for_run,random_for_experyment, statistics)

            if settings_for_run.is_multirun:
                runner.run_multirun()
            else:
                runner.run_normal()

            shutil.copytree("./results",settings_for_run.target_directory+"/results")
            shutil.copy(settings.target_directory+"/"+file_name,settings_for_run.target_directory)










    else:

        runner=Runner(settings,rand, statistics)
        if settings.is_multirun:
            runner.run_multirun()
        else:
            runner.run_normal()




if __name__ == '__main__':
    main()

