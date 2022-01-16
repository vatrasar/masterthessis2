import tkinter

class Visualisation():


    def __init__(self):

        self.master=tkinter.Tk()
        self.master.title("Visualisation")
        self.canvas=tkinter.Canvas(self.master, width=500, height=500)
        self.canvas.pack()
        self.master.mainloop()







