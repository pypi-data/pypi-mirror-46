import tkinter as tk

class theme():
    def __init__(self):
        # self = tk.Tk()
        self.btn = {}
        self.btn['width'] = 10
        self.btn['height'] = 10
        pass

    def addColor(self):
        self = tk.Tk()
        self.clr = {}
        self.clr['txtFg']    = "green2"
        self.clr['txtBg']    = "black" 
        self.clr['appFg']    = 'white'
        self.clr['appBg']    = "grey30"
        self.config(bg=self.clr['appBg'])
        return self

if __name__ == '__main__':
    app = theme().addColor()
    app.mainloop()
