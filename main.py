import random
from runner import Runner
from Events.Game.settings import Settings


def main():
    settings:Settings=Settings()
    try:
        settings.get_properties()
    except Exception as exp:
        print(str(exp))
        return

    #init state
    rand = random.Random(settings.seed)  # 800

    runner=Runner(settings,rand)
    runner.run()




if __name__ == '__main__':
    main()

