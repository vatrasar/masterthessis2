import tkinter

master=tkinter.Tk()
master.title("nazwa okna")
canvas=tkinter.Canvas(master,width=400,height=400)
canvas.pack()
canvas.create_rectangle(0, 0, 100, 50, fill="blue")
master.mainloop()
