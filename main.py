import random

from Events.Game.Statistics import Statistics
from runner import Runner
from Events.Game.move.GameObjects.tools.settings import Settings


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
        settings.get_properties(file_with_properties,file_with_rewards)
    except Exception as exp:
        print(str(exp))
        return

    #init state
    rand = random.Random(975)  # 800

    runner=Runner(settings,rand, statistics)
    runner.run()




if __name__ == '__main__':
    main()

