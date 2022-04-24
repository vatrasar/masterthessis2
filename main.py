import random

from Events.Game.Statistics import Statistics
from Events.Game.move.algos.GameObjects.tools.other_tools import clear_folder
from runner import Runner
from Events.Game.move.algos.GameObjects.tools.settings import Settings


def main():
    settings:Settings=Settings()
    statistics=Statistics()

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
        return

    #init state
    rand = random.Random(settings.seed)  # 800

    runner=Runner(settings,rand, statistics)
    if settings.is_multirun:
        runner.run_multirun()
    else:
        runner.run_normal()




if __name__ == '__main__':
    main()

