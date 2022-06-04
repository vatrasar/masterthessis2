from Events.Game.move.algos.GameObjects.data_lists.tools.settings import Settings


class Debug_file():
    def __init__(self,settings:Settings):
        self.settings = settings

        self.current_run=[]


    def save_to_file(self,settings:Settings):
        file_name=""
        if settings.learning:
            file_name="deb_res_tr.csv"
        else:
            file_name="deb_res.csv"
        file=open("./results/"+file_name,"w")

        file.close()
