import random
from runner import Runner
from Events.Game.settings import Settings


def main():
    settings:Settings=Settings()
    try:
        settings_file_name_f=open("settingsFiles/settingsFileName.txt")
        settingsFileName_line:str=settings_file_name_f.readline()
        _,settingsFileName=settings.get_property_pair(settingsFileName_line)
        file_with_properties=open("settingsFiles/"+settingsFileName)
        settings.get_properties(file_with_properties)
    except Exception as exp:
        print(str(exp))
        return

    #init state
    rand = random.Random(settings.seed)  # 800

    runner=Runner(settings,rand)
    runner.run()




if __name__ == '__main__':
    main()

